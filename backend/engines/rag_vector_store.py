"""
Semantic Vector Search & RAG Engine (FR-03, FR-05)
==================================================
Implements an in-memory dense + sparse hybrid vector index using NumPy:
- Computes TF-IDF weighted term-document matrix
- Projects into dense latent semantic vectors via Singular Value Decomposition (np.linalg.svd)
- Performs L2-normalized Cosine Similarity + Skill-Ontology Tag Boosting
- Returns grounded citations with similarity confidence scores
"""

from __future__ import annotations
import math
import re
from typing import Any, Dict, List, Optional
import numpy as np


def _tokenize(text: str) -> List[str]:
    cleaned = re.sub(r"[^a-zA-Z0-9\+\-\#]", " ", text.lower())
    stop_words = {
        "the", "and", "for", "with", "into", "from", "that", "this", "are", "over", "using", "across"
    }
    return [tok for tok in cleaned.split() if len(tok) > 1 and tok not in stop_words]


class HybridSemanticVectorRAG:
    def __init__(self, documents: List[Dict[str, Any]]) -> None:
        self.documents: List[Dict[str, Any]] = documents
        self.vocab: Dict[str, int] = {}
        self.idf: Optional[np.ndarray] = None
        self.tfidf_matrix: Optional[np.ndarray] = None
        self.svd_Vt: Optional[np.ndarray] = None
        self.dense_doc_vectors: Optional[np.ndarray] = None
        self._build_index()

    def _build_index(self) -> None:
        tokenized_docs: List[List[str]] = []
        df_counts: Dict[str, int] = {}

        for doc in self.documents:
            full_text = (
                f"{doc.get('title', '')} {doc.get('content', '')} "
                f"{doc.get('provider', '')} {doc.get('certification', '')} "
                f"{' '.join(doc.get('related_skills', []))}"
            )
            tokens = _tokenize(full_text)
            tokenized_docs.append(tokens)
            for tok in set(tokens):
                df_counts[tok] = df_counts.get(tok, 0) + 1

        for idx, tok in enumerate(sorted(df_counts.keys())):
            self.vocab[tok] = idx

        n_docs = len(self.documents)
        n_vocab = len(self.vocab)
        if n_docs == 0 or n_vocab == 0:
            return

        # Compute smoothed IDF
        idf_arr = np.zeros(n_vocab, dtype=np.float64)
        for tok, idx in self.vocab.items():
            idf_arr[idx] = math.log((1.0 + n_docs) / (1.0 + df_counts[tok])) + 1.0
        self.idf = idf_arr

        # Build TF-IDF matrix (n_docs x n_vocab)
        mat = np.zeros((n_docs, n_vocab), dtype=np.float64)
        for d_idx, tokens in enumerate(tokenized_docs):
            if not tokens:
                continue
            for tok in tokens:
                if tok in self.vocab:
                    mat[d_idx, self.vocab[tok]] += 1.0
            mat[d_idx] = (mat[d_idx] / len(tokens)) * self.idf
            norm = np.linalg.norm(mat[d_idx])
            if norm > 1e-9:
                mat[d_idx] /= norm

        self.tfidf_matrix = mat

        # Compute Truncated SVD (Latent Semantic Dense Vectors) for semantic concept matching
        k_dim = min(14, n_docs, n_vocab)
        U, S, Vt = np.linalg.svd(mat, full_matrices=False)
        dense = U[:, :k_dim] * S[:k_dim]
        norms = np.linalg.norm(dense, axis=1, keepdims=True)
        norms[norms < 1e-9] = 1.0
        self.dense_doc_vectors = dense / norms
        self.svd_Vt = Vt[:k_dim, :]

    def search(
        self,
        query: str,
        category: Optional[str] = None,
        skill_ids: Optional[List[str]] = None,
        top_k: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Executes hybrid dense-SVD + sparse TF-IDF + skill-ontology tag retrieval.
        """
        if self.tfidf_matrix is None or self.idf is None:
            return []

        q_tokens = _tokenize(query + (" " + " ".join(skill_ids) if skill_ids else ""))
        q_vec = np.zeros(len(self.vocab), dtype=np.float64)
        for tok in q_tokens:
            if tok in self.vocab:
                q_vec[self.vocab[tok]] += 1.0

        if np.linalg.norm(q_vec) > 1e-9:
            q_vec = (q_vec / max(1, len(q_tokens))) * self.idf
            q_vec /= np.linalg.norm(q_vec)
            sparse_scores = self.tfidf_matrix @ q_vec

            # Project query into SVD dense space
            q_dense = q_vec @ self.svd_Vt.T
            if np.linalg.norm(q_dense) > 1e-9:
                q_dense /= np.linalg.norm(q_dense)
            dense_scores = self.dense_doc_vectors @ q_dense
            combined_scores = 0.60 * sparse_scores + 0.40 * np.clip(dense_scores, 0.0, 1.0)
        else:
            combined_scores = np.full(len(self.documents), 0.35)

        skill_set = set(skill_ids or [])
        results: List[Dict[str, Any]] = []

        for idx, doc in enumerate(self.documents):
            if category and doc.get("category") != category:
                continue

            base_sim = float(combined_scores[idx])
            doc_skills = set(doc.get("related_skills", []))
            overlap = len(skill_set.intersection(doc_skills))
            tag_boost = min(0.45, overlap * 0.22) if skill_set else 0.0
            final_score = round(min(0.99, max(0.18, base_sim + tag_boost)), 3)

            results.append({
                **doc,
                "similarity_score": final_score,
                "matched_skills": sorted(skill_set.intersection(doc_skills)),
            })

        results.sort(key=lambda x: x["similarity_score"], reverse=True)
        return results[:top_k]

/**
 * Zustand Global State Store for SkillPulse AI Workforce Intelligence Portal
 * Manages Forecast Horizon, Knowledge Graph Node Selection, 5-Agent Evolution State,
 * Internal Mobility Matches, and Human-in-the-Loop HR Governance Approvals.
 */

export interface XaiFactor {
  factor: string;
  weight_pct: number;
  evidence?: string;
}

export interface SkillForecast {
  skill_id: string;
  skill_name: string;
  domain: string;
  lifecycle: 'EMERGING' | 'CORE' | 'LEGACY';
  market_growth_yoy_pct: number;
  current_supply: number;
  projected_supply: number;
  projected_demand: number;
  net_shortage_gap: number;
  shortage_risk_score: number;
  shortage_risk_level: 'CRITICAL' | 'HIGH' | 'MODERATE' | 'LOW';
  bus_factor_alert: boolean;
}

export interface WorkforceStoreState {
  activeTab: 'FORECAST' | 'GRAPH' | 'AGENTS' | 'MOBILITY' | 'GOVERNANCE';
  horizonMonths: 6 | 12 | 24;
  selectedEmployeeId: string;
  selectedRoleId: string;
  setActiveTab: (tab: WorkforceStoreState['activeTab']) => void;
  setHorizonMonths: (h: 6 | 12 | 24) => void;
}

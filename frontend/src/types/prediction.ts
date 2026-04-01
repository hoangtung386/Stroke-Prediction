export type RiskLevel = 'Low' | 'Medium' | 'High';

export interface RiskFactor {
    name: string;
    contribution: number;
    description: string;
}

export interface RiskAnalysis {
    riskLevel: RiskLevel;
    probability: number;
    prediction: 0 | 1;
    riskFactors: RiskFactor[];
    recommendations: string[];
    modelUsed?: string;
    modelDescription?: string;
}

export interface PredictionResponse {
    prediction: 0 | 1;
    probability: number;
    risk_level: string;
    confidence: number;
    model_name?: string;
    model_description?: string;
}

export interface ModelInfo {
    id: string;
    name: string;
    description: string;
}

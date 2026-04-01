import { PatientData, RiskAnalysis, PredictionResponse, ModelInfo } from '../types';

const API_BASE_URL = '/api';

interface ModelsResponse {
    models: ModelInfo[];
    count: number;
}

class MLModelService {
    async getAvailableModels(): Promise<ModelInfo[]> {
        const response = await fetch(`${API_BASE_URL}/models`);

        if (!response.ok) {
            throw new Error(`Failed to fetch models: ${response.statusText}`);
        }

        const data: ModelsResponse = await response.json();
        return data.models || [];
    }

    async predict(patientData: PatientData, modelId: string): Promise<PredictionResponse> {
        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ...patientData, model_id: modelId }),
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.error || `Prediction failed: ${response.statusText}`);
        }

        return await response.json();
    }

    formatResult(prediction: PredictionResponse): RiskAnalysis {
        const riskFactors = this.calculateRiskFactors(prediction);
        const recommendations = this.generateRecommendations(prediction.risk_level);

        return {
            riskLevel: prediction.risk_level as RiskAnalysis['riskLevel'],
            probability: prediction.probability,
            prediction: prediction.prediction,
            riskFactors,
            recommendations,
            modelUsed: prediction.model_name,
            modelDescription: prediction.model_description,
        };
    }

    private calculateRiskFactors(prediction: PredictionResponse): RiskAnalysis['riskFactors'] {
        const prob = prediction.probability;
        return [
            {
                name: 'Overall Risk Score',
                contribution: prob,
                description: `${(prob * 100).toFixed(1)}% probability based on ML model analysis`,
            },
        ];
    }

    private generateRecommendations(riskLevel: string): string[] {
        const base = [
            'Maintain regular health check-ups',
            'Follow a balanced diet low in sodium and saturated fats',
            'Engage in regular physical activity (at least 150 minutes/week)',
        ];

        const high = [
            'Consult a healthcare provider immediately for comprehensive evaluation',
            'Monitor blood pressure and glucose levels daily',
            'Consider lifestyle modifications under medical supervision',
            'Discuss preventive medication options with your doctor',
        ];

        const moderate = [
            'Schedule a consultation with your healthcare provider',
            'Monitor blood pressure regularly',
            'Consider stress reduction techniques',
            'Review and optimize current medications if applicable',
        ];

        switch (riskLevel.toLowerCase()) {
            case 'high':
                return [...high, ...base];
            case 'medium':
                return [...moderate, ...base];
            default:
                return base;
        }
    }
}

export const mlModelService = new MLModelService();

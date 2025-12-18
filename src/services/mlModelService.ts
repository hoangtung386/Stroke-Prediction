import { PatientData, RiskAnalysis, PredictionResponse } from '../types';

const API_BASE_URL = '/api';

interface ModelInfo {
    id: string;
    name: string;
    description: string;
}

interface ModelsResponse {
    models: ModelInfo[];
    count: number;
}

class MLModelService {
    /**
     * Get list of available trained models
     */
    async getAvailableModels(): Promise<ModelInfo[]> {
        try {
            const response = await fetch(`${API_BASE_URL}/models`);

            if (!response.ok) {
                throw new Error(`Failed to fetch models: ${response.statusText}`);
            }

            const data: ModelsResponse = await response.json();
            return data.models || [];
        } catch (error) {
            console.error('Error fetching models:', error);
            throw error;
        }
    }

    /**
     * Make a prediction using the specified model
     */
    async predict(patientData: PatientData, modelId: string): Promise<PredictionResponse> {
        try {
            const response = await fetch(`${API_BASE_URL}/predict`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    ...patientData,
                    model_id: modelId
                }),
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.error || `Prediction failed: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error making prediction:', error);
            throw error;
        }
    }

    /**
     * Format API response to RiskAnalysis for UI display
     */
    formatResult(prediction: PredictionResponse): RiskAnalysis {
        // Calculate risk factors based on prediction
        const riskFactors = this.calculateRiskFactors(prediction);

        // Generate recommendations based on risk level
        const recommendations = this.generateRecommendations(prediction.risk_level);

        return {
            riskLevel: prediction.risk_level as RiskAnalysis['riskLevel'],
            probability: prediction.probability,
            prediction: prediction.prediction,
            riskFactors,
            recommendations,
            modelUsed: prediction.model_used
        };
    }

    private calculateRiskFactors(prediction: PredictionResponse): RiskAnalysis['riskFactors'] {
        // Simple risk factor breakdown based on probability
        const prob = prediction.probability;

        return [
            {
                name: 'Overall Risk Score',
                contribution: prob,
                description: `${(prob * 100).toFixed(1)}% probability based on ML model analysis`
            }
        ];
    }

    private generateRecommendations(riskLevel: string): string[] {
        const baseRecommendations = [
            'Maintain regular health check-ups',
            'Follow a balanced diet low in sodium and saturated fats',
            'Engage in regular physical activity (at least 150 minutes/week)'
        ];

        const highRiskRecommendations = [
            'Consult a healthcare provider immediately for comprehensive evaluation',
            'Monitor blood pressure and glucose levels daily',
            'Consider lifestyle modifications under medical supervision',
            'Discuss preventive medication options with your doctor'
        ];

        const moderateRiskRecommendations = [
            'Schedule a consultation with your healthcare provider',
            'Monitor blood pressure regularly',
            'Consider stress reduction techniques',
            'Review and optimize current medications if applicable'
        ];

        switch (riskLevel.toLowerCase()) {
            case 'very high':
            case 'high':
                return [...highRiskRecommendations, ...baseRecommendations];
            case 'moderate':
                return [...moderateRiskRecommendations, ...baseRecommendations];
            default:
                return baseRecommendations;
        }
    }
}

export const mlModelService = new MLModelService();

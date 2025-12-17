/**
 * Machine Learning Model Integration Service
 * Use this instead of geminiService.ts for actual ML predictions
 */

interface PatientData {
  age: number;
  gender: string;
  hypertension: number;
  heart_disease: number;
  ever_married: string;
  work_type: string;
  Residence_type: string;
  avg_glucose_level: number;
  bmi: number;
  smoking_status: string;
}

interface PredictionResult {
  prediction: number;  // 0 or 1
  probability: number;  // 0-1
  risk_level: string;  // Low, Medium, High
  confidence: number;  // 0-1
  probability_no_stroke: number;
  probability_stroke: number;
  model_used?: string;
}

interface BatchPredictionResult {
  model_used: string;
  count: number;
  results: PredictionResult[];
}

class MLModelService {
  private apiUrl: string;

  constructor(apiUrl: string = 'http://localhost:5000/api') {
    this.apiUrl = apiUrl;
  }

  /**
   * Predict stroke risk for a single patient
   */
  async predict(
    patientData: PatientData,
    modelName?: string
  ): Promise<PredictionResult> {
    const payload = {
      ...patientData,
      ...(modelName && { model: modelName })
    };

    const response = await fetch(`${this.apiUrl}/predict`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Prediction failed');
    }

    return await response.json();
  }

  /**
   * Predict stroke risk for multiple patients
   */
  async predictBatch(
    patients: PatientData[],
    modelName?: string
  ): Promise<BatchPredictionResult> {
    const payload = {
      patients,
      ...(modelName && { model: modelName })
    };

    const response = await fetch(`${this.apiUrl}/predict-batch`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Batch prediction failed');
    }

    return await response.json();
  }

  /**
   * Get list of available models
   */
  async getAvailableModels(): Promise<string[]> {
    const response = await fetch(`${this.apiUrl}/models`);
    
    if (!response.ok) {
      throw new Error('Failed to fetch models');
    }

    const data = await response.json();
    return data.models;
  }

  /**
   * Check API health
   */
  async healthCheck(): Promise<{ status: string; models_loaded: string[] }> {
    const response = await fetch(`${this.apiUrl}/health`);
    
    if (!response.ok) {
      throw new Error('Health check failed');
    }

    return await response.json();
  }

  /**
   * Format prediction result for UI display
   */
  formatResult(result: PredictionResult): {
    riskScore: number;
    riskLevel: string;
    hasPrediction: boolean;
    factors: string[];
    recommendations: string[];
  } {
    const riskScore = Math.round(result.probability * 100);
    
    // Determine risk factors based on input
    // This is a simplified version - you may want to enhance this
    const factors: string[] = [];
    
    if (result.probability > 0.7) {
      factors.push('High probability of stroke risk');
    } else if (result.probability > 0.4) {
      factors.push('Moderate stroke risk factors present');
    } else {
      factors.push('Low stroke risk profile');
    }

    // Generate recommendations
    const recommendations: string[] = [];
    
    if (riskScore > 50) {
      recommendations.push('Consult with a healthcare provider immediately');
      recommendations.push('Monitor blood pressure and glucose levels regularly');
      recommendations.push('Consider lifestyle modifications');
    } else if (riskScore > 30) {
      recommendations.push('Regular health check-ups recommended');
      recommendations.push('Maintain healthy lifestyle habits');
    } else {
      recommendations.push('Continue healthy lifestyle practices');
      recommendations.push('Regular preventive care');
    }

    return {
      riskScore,
      riskLevel: result.risk_level,
      hasPrediction: true,
      factors,
      recommendations,
    };
  }
}

// Export singleton instance
export const mlModelService = new MLModelService();

// Export types
export type { PatientData, PredictionResult, BatchPredictionResult };

/**
 * Machine Learning Model Integration Service
 * Replaces Gemini AI with actual trained ML models
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
  model_id?: string;
  model_name?: string;
  model_description?: string;
}

interface ModelInfo {
  id: string;
  name: string;
  description: string;
}

interface BatchPredictionResult {
  model_id: string;
  model_name: string;
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
    modelId?: string
  ): Promise<PredictionResult> {
    const payload = {
      ...patientData,
      ...(modelId && { model_id: modelId })
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
    modelId?: string
  ): Promise<BatchPredictionResult> {
    const payload = {
      patients,
      ...(modelId && { model_id: modelId })
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
   * Get list of available models with details
   */
  async getAvailableModels(): Promise<ModelInfo[]> {
    const response = await fetch(`${this.apiUrl}/models`);
    
    if (!response.ok) {
      throw new Error('Failed to fetch models');
    }

    const data = await response.json();
    return data.models;
  }

  /**
   * Compare predictions from multiple models
   */
  async compareModels(
    patientData: PatientData,
    modelIds?: string[]
  ): Promise<any> {
    const payload = {
      patient_data: patientData,
      ...(modelIds && { model_ids: modelIds })
    };

    const response = await fetch(`${this.apiUrl}/compare`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Model comparison failed');
    }

    return await response.json();
  }

  /**
   * Check API health
   */
  async healthCheck(): Promise<{ status: string; models_loaded: number; available_models: string[] }> {
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
    confidence?: number;
    modelUsed?: string;
    modelDescription?: string;
  } {
    const riskScore = Math.round(result.probability * 100);
    
    // Determine risk factors
    const factors: string[] = [];
    
    if (result.probability > 0.7) {
      factors.push('High probability of stroke risk detected');
      factors.push('Multiple risk factors present');
    } else if (result.probability > 0.4) {
      factors.push('Moderate stroke risk factors identified');
      factors.push('Some concerning indicators present');
    } else {
      factors.push('Low overall stroke risk profile');
      factors.push('Favorable clinical indicators');
    }

    // Add model confidence as a factor
    if (result.confidence) {
      factors.push(`Model confidence: ${(result.confidence * 100).toFixed(1)}%`);
    }

    // Generate recommendations
    const recommendations: string[] = [];
    
    if (riskScore >= 70) {
      recommendations.push('⚠️ URGENT: Consult with a healthcare provider immediately');
      recommendations.push('📊 Schedule comprehensive cardiovascular screening');
      recommendations.push('💊 Discuss preventive medication options');
      recommendations.push('🏃 Implement immediate lifestyle modifications');
      recommendations.push('📱 Consider continuous health monitoring');
    } else if (riskScore >= 40) {
      recommendations.push('🏥 Schedule routine health check-up within 2-4 weeks');
      recommendations.push('📈 Monitor blood pressure and glucose levels regularly');
      recommendations.push('🥗 Maintain healthy diet and exercise routine');
      recommendations.push('🚭 Avoid smoking and excessive alcohol consumption');
      recommendations.push('💤 Ensure adequate sleep and stress management');
    } else {
      recommendations.push('✅ Continue current healthy lifestyle practices');
      recommendations.push('📅 Maintain annual preventive care appointments');
      recommendations.push('🏋️ Regular physical activity recommended');
      recommendations.push('🥦 Balanced nutrition and hydration');
      recommendations.push('🧘 Stress management and mental wellness');
    }

    return {
      riskScore,
      riskLevel: result.risk_level,
      hasPrediction: true,
      factors,
      recommendations,
      confidence: result.confidence,
      modelUsed: result.model_name,
      modelDescription: result.model_description,
    };
  }
}

// Export singleton instance
export const mlModelService = new MLModelService();

// Export types
export type { PatientData, PredictionResult, BatchPredictionResult, ModelInfo };

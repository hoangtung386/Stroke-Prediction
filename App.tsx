import React, { useState, useCallback, useEffect } from 'react';
import { Header } from './components/Header';
import { PatientForm } from './components/PatientForm';
import { AnalysisResult } from './components/AnalysisResult';
import { ModelSelector } from './components/ModelSelector';
import { PatientData, RiskAnalysis, DEFAULT_PATIENT_DATA } from './types';
import { mlModelService } from './services/mlModelService';

// Model info interface
interface ModelInfo {
  id: string;
  name: string;
  description: string;
}

const App: React.FC = () => {
  const [patientData, setPatientData] = useState<PatientData>(DEFAULT_PATIENT_DATA);
  const [result, setResult] = useState<RiskAnalysis | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // Model selection state
  const [availableModels, setAvailableModels] = useState<ModelInfo[]>([]);
  const [selectedModelId, setSelectedModelId] = useState<string>('');
  const [isLoadingModels, setIsLoadingModels] = useState(true);

  // Load available models on mount
  useEffect(() => {
    loadAvailableModels();
  }, []);

  const loadAvailableModels = async () => {
    setIsLoadingModels(true);
    try {
      const models = await mlModelService.getAvailableModels();
      setAvailableModels(models);
      
      // Select first model by default
      if (models.length > 0) {
        setSelectedModelId(models[0].id);
      }
    } catch (err) {
      console.error('Failed to load models:', err);
      setError('Failed to load available models. Please ensure the API server is running.');
    } finally {
      setIsLoadingModels(false);
    }
  };

  const handleAnalyze = useCallback(async () => {
    if (!selectedModelId) {
      setError('Please select a model first');
      return;
    }

    setIsAnalyzing(true);
    setError(null);
    
    try {
      const prediction = await mlModelService.predict(patientData, selectedModelId);
      const formattedResult = mlModelService.formatResult(prediction);
      
      // Add model info to result
      const selectedModel = availableModels.find(m => m.id === selectedModelId);
      if (selectedModel) {
        formattedResult.modelUsed = selectedModel.name;
        formattedResult.modelDescription = selectedModel.description;
      }
      
      setResult(formattedResult);
    } catch (err: any) {
      setError(err.message || "An unexpected error occurred during analysis.");
    } finally {
      setIsAnalyzing(false);
    }
  }, [patientData, selectedModelId, availableModels]);

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <Header />
      
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        {/* Model Selector */}
        {!isLoadingModels && availableModels.length > 0 && (
          <div className="mb-6">
            <ModelSelector
              models={availableModels}
              selectedModelId={selectedModelId}
              onSelectModel={setSelectedModelId}
            />
          </div>
        )}

        {/* Loading models message */}
        {isLoadingModels && (
          <div className="mb-6 bg-blue-50 border border-blue-200 text-blue-700 px-4 py-3 rounded-lg">
            <span>Loading available models...</span>
          </div>
        )}

        {/* No models available warning */}
        {!isLoadingModels && availableModels.length === 0 && (
          <div className="mb-6 bg-yellow-50 border border-yellow-200 text-yellow-800 px-4 py-3 rounded-lg">
            <strong className="font-bold">No models available!</strong>
            <p className="mt-1">Please train models first or ensure the API server is running.</p>
            <p className="mt-2 text-sm">
              Run: <code className="bg-yellow-100 px-2 py-1 rounded">python ml_training/main.py --variant drop_imbalanced</code>
            </p>
          </div>
        )}
        
        {/* Error display */}
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg relative" role="alert">
            <strong className="font-bold">Error: </strong>
            <span className="block sm:inline">{error}</span>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* Left Column: Input Form */}
          <div className="lg:col-span-7 xl:col-span-8">
            <PatientForm 
              data={patientData} 
              onChange={setPatientData} 
              onSubmit={handleAnalyze}
              isAnalyzing={isAnalyzing}
              disabled={availableModels.length === 0}
            />
          </div>

          {/* Right Column: Result Dashboard */}
          <div className="lg:col-span-5 xl:col-span-4">
            {result ? (
              <AnalysisResult result={result} />
            ) : (
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8 h-full flex flex-col items-center justify-center text-center text-gray-500 min-h-[400px]">
                <div className="bg-gray-100 p-4 rounded-full mb-4">
                  <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                </div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">Ready to Analyze</h3>
                <p className="max-w-xs mx-auto">
                  {availableModels.length > 0 
                    ? "Fill out the patient demographics and clinical data on the left to generate a comprehensive stroke risk assessment."
                    : "Please train models first to enable predictions."}
                </p>
              </div>
            )}
          </div>
        </div>
      </main>

      <footer className="bg-white border-t border-gray-200 py-6 mt-auto">
        <div className="max-w-7xl mx-auto px-4 text-center text-sm text-gray-500">
          <p>© 2024 StrokeGuard AI System. All rights reserved.</p>
          <p className="mt-1">Powered by Dense Stacking Ensemble (DSE) Machine Learning Models</p>
        </div>
      </footer>
    </div>
  );
};

export default App;
import React, { useState, useCallback } from 'react';
import { Header } from './components/Header';
import { PatientForm } from './components/PatientForm';
import { AnalysisResult } from './components/AnalysisResult';
import { PatientData, RiskAnalysis, DEFAULT_PATIENT_DATA } from './types';
import { analyzeStrokeRisk } from './services/geminiService';

const App: React.FC = () => {
  const [patientData, setPatientData] = useState<PatientData>(DEFAULT_PATIENT_DATA);
  const [result, setResult] = useState<RiskAnalysis | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = useCallback(async () => {
    setIsAnalyzing(true);
    setError(null);
    try {
      const analysis = await analyzeStrokeRisk(patientData);
      setResult(analysis);
    } catch (err: any) {
        setError(err.message || "An unexpected error occurred.");
    } finally {
      setIsAnalyzing(false);
    }
  }, [patientData]);

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <Header />
      
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
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
                  Fill out the patient demographics and clinical data on the left to generate a comprehensive stroke risk assessment.
                </p>
              </div>
            )}
          </div>
        </div>
      </main>

      <footer className="bg-white border-t border-gray-200 py-6 mt-auto">
        <div className="max-w-7xl mx-auto px-4 text-center text-sm text-gray-500">
          <p>© 2024 StrokeGuard AI System. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};

export default App;
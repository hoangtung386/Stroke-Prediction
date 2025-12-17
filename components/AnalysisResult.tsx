import React from 'react';
import { RiskAnalysis } from '../types';
import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip } from 'recharts';
import { AlertTriangle, CheckCircle, Info, FileText, Cpu } from 'lucide-react';

interface AnalysisResultProps {
  result: RiskAnalysis;
}

export const AnalysisResult: React.FC<AnalysisResultProps> = ({ result }) => {
  const getRiskColor = (level: string) => {
    switch (level) {
      case 'Low': return '#22c55e';
      case 'Moderate': return '#eab308';
      case 'High': return '#f97316';
      case 'Critical': return '#ef4444';
      default: return '#3b82f6';
    }
  };

  const riskColor = getRiskColor(result.riskLevel);
  
  const chartData = [
    { name: 'Risk', value: result.riskScore },
    { name: 'Safe', value: 100 - result.riskScore }
  ];

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden h-full">
      <div className="p-6 border-b border-gray-100 bg-gray-50">
        <div className="flex justify-between items-start mb-2">
          <h2 className="text-lg font-semibold text-gray-800 flex items-center gap-2">
            <FileText className="text-medical-600" size={20} />
            Analysis Report
          </h2>
          <span 
            className={`px-3 py-1 rounded-full text-sm font-bold border`} 
            style={{ 
              borderColor: riskColor, 
              color: riskColor, 
              backgroundColor: `${riskColor}15` 
            }}
          >
            {result.riskLevel} Risk
          </span>
        </div>
        
        {/* Model Info */}
        {result.modelUsed && (
          <div className="flex items-center gap-2 text-sm text-gray-600 mt-2">
            <Cpu size={14} className="text-blue-500" />
            <span className="font-medium">{result.modelUsed}</span>
            {result.confidence && (
              <span className="text-xs text-gray-500">
                • Confidence: {(result.confidence * 100).toFixed(1)}%
              </span>
            )}
          </div>
        )}
      </div>

      <div className="p-6 space-y-8">
        
        {/* Gauge Chart */}
        <div className="flex flex-col items-center justify-center relative">
          <div className="h-48 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={chartData}
                  cx="50%"
                  cy="50%"
                  startAngle={180}
                  endAngle={0}
                  innerRadius={60}
                  outerRadius={80}
                  paddingAngle={5}
                  dataKey="value"
                  stroke="none"
                >
                  <Cell fill={riskColor} />
                  <Cell fill="#f1f5f9" />
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 mt-2 text-center">
            <span className="text-4xl font-bold block" style={{ color: riskColor }}>
              {result.riskScore}%
            </span>
            <span className="text-xs text-gray-500 uppercase tracking-wide">Stroke Probability</span>
          </div>
        </div>

        {/* Risk Factors */}
        <div>
          <h3 className="text-sm font-semibold text-gray-700 uppercase tracking-wider mb-4 flex items-center gap-2">
            <Info size={16} /> Risk Factors Detected
          </h3>
          <div className="space-y-2">
            {result.factors.map((factor, idx) => (
              <div key={idx} className="flex items-start gap-3 p-3 bg-gray-50 rounded-lg">
                <div className="mt-1 min-w-[6px] min-h-[6px] rounded-full bg-blue-500" />
                <span className="text-sm text-gray-700">{factor}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Clinical Reasoning (if available from contributingFactors) */}
        {result.contributingFactors && result.contributingFactors.length > 0 && (
          <div>
            <h3 className="text-sm font-semibold text-gray-700 uppercase tracking-wider mb-4 flex items-center gap-2">
              <Info size={16} /> Contributing Factors
            </h3>
            <div className="space-y-3">
              {result.contributingFactors.map((factor, idx) => (
                <div key={idx} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <span className="text-gray-700 font-medium">{factor.name}</span>
                  <span className={`text-xs font-bold px-2 py-1 rounded ${
                    factor.impact === 'High' ? 'bg-red-100 text-red-700' :
                    factor.impact === 'Medium' ? 'bg-yellow-100 text-yellow-700' :
                    'bg-blue-100 text-blue-700'
                  }`}>
                    {factor.impact} Impact
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Reasoning (if available) */}
        {result.reasoning && (
          <div className="p-4 bg-medical-50 rounded-xl border border-medical-100">
            <h3 className="text-medical-900 font-semibold mb-2 text-sm">Clinical Analysis</h3>
            <p className="text-medical-800 text-sm leading-relaxed">
              {result.reasoning}
            </p>
          </div>
        )}

        {/* Recommendations */}
        <div>
          <h3 className="text-sm font-semibold text-gray-700 uppercase tracking-wider mb-4 flex items-center gap-2">
            <CheckCircle size={16} /> Medical Recommendations
          </h3>
          <ul className="space-y-2">
            {result.recommendations.map((rec, idx) => (
              <li key={idx} className="flex items-start gap-3 text-sm text-gray-600">
                <div className="mt-1 min-w-[6px] min-h-[6px] rounded-full bg-green-500" />
                {rec}
              </li>
            ))}
          </ul>
        </div>
        
        {/* Disclaimer */}
        <div className="flex items-center gap-2 p-3 bg-yellow-50 text-yellow-800 text-xs rounded-lg border border-yellow-200">
          <AlertTriangle size={16} className="shrink-0" />
          <p>
            This analysis is generated by a Dense Stacking Ensemble (DSE) machine learning model trained on the Kaggle Stroke Prediction Dataset. 
            It provides risk estimation for educational and screening purposes only. 
            <strong> Always consult qualified healthcare professionals for medical diagnosis and treatment.</strong>
          </p>
        </div>

        {/* Model Description (if available) */}
        {result.modelDescription && (
          <div className="text-xs text-gray-500 text-center p-2 bg-gray-50 rounded-lg">
            {result.modelDescription}
          </div>
        )}

      </div>
    </div>
  );
};
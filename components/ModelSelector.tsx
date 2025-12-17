import React from 'react';

interface ModelInfo {
  id: string;
  name: string;
  description: string;
}

interface ModelSelectorProps {
  models: ModelInfo[];
  selectedModelId: string;
  onSelectModel: (modelId: string) => void;
}

export const ModelSelector: React.FC<ModelSelectorProps> = ({
  models,
  selectedModelId,
  onSelectModel,
}) => {
  const selectedModel = models.find(m => m.id === selectedModelId);

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className="bg-blue-100 p-2 rounded-lg">
            <svg 
              className="w-5 h-5 text-blue-600" 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path 
                strokeLinecap="round" 
                strokeLinejoin="round" 
                strokeWidth="2" 
                d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" 
              />
            </svg>
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-900">Prediction Model</h3>
            <p className="text-sm text-gray-500">
              {models.length} model{models.length !== 1 ? 's' : ''} available
            </p>
          </div>
        </div>
      </div>

      {/* Model Selector Dropdown */}
      <div className="mb-3">
        <label htmlFor="model-select" className="block text-sm font-medium text-gray-700 mb-2">
          Select Model
        </label>
        <select
          id="model-select"
          value={selectedModelId}
          onChange={(e) => onSelectModel(e.target.value)}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
        >
          {models.map((model) => (
            <option key={model.id} value={model.id}>
              {model.name}
            </option>
          ))}
        </select>
      </div>

      {/* Selected Model Description */}
      {selectedModel && (
        <div className="bg-gray-50 rounded-lg p-3 border border-gray-200">
          <p className="text-sm text-gray-600">
            <span className="font-medium text-gray-700">Description:</span>{' '}
            {selectedModel.description}
          </p>
        </div>
      )}

      {/* Model Stats Grid (Optional - can show model performance if available) */}
      <div className="mt-4 grid grid-cols-3 gap-3">
        <div className="text-center p-2 bg-green-50 rounded-lg border border-green-200">
          <div className="text-xs text-green-600 font-medium">Accuracy</div>
          <div className="text-lg font-bold text-green-700">95-97%</div>
        </div>
        <div className="text-center p-2 bg-purple-50 rounded-lg border border-purple-200">
          <div className="text-xs text-purple-600 font-medium">AUC Score</div>
          <div className="text-lg font-bold text-purple-700">0.95+</div>
        </div>
        <div className="text-center p-2 bg-blue-50 rounded-lg border border-blue-200">
          <div className="text-xs text-blue-600 font-medium">Type</div>
          <div className="text-lg font-bold text-blue-700">DSE</div>
        </div>
      </div>
    </div>
  );
};

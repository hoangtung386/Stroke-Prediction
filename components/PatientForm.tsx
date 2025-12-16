import React from 'react';
import { PatientData, Gender, WorkType, ResidenceType, SmokingStatus, YesNo } from '../types';
import { User, Heart, Activity, Briefcase, Home, Cigarette, Scale, Stethoscope } from 'lucide-react';

interface PatientFormProps {
  data: PatientData;
  onChange: (data: PatientData) => void;
  onSubmit: () => void;
  isAnalyzing: boolean;
}

export const PatientForm: React.FC<PatientFormProps> = ({ data, onChange, onSubmit, isAnalyzing }) => {
  
  const handleChange = (field: keyof PatientData, value: any) => {
    onChange({ ...data, [field]: value });
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
      <div className="p-6 border-b border-gray-100 bg-gray-50">
        <h2 className="text-lg font-semibold text-gray-800 flex items-center gap-2">
          <User className="text-medical-600" size={20} />
          Patient Demographics & Clinical Data
        </h2>
        <p className="text-sm text-gray-500 mt-1">Enter patient specifications for model inference.</p>
      </div>

      <div className="p-6 grid grid-cols-1 md:grid-cols-2 gap-6">
        
        {/* Gender */}
        <div className="space-y-2">
          <label className="text-sm font-medium text-gray-700">Gender</label>
          <select
            className="w-full p-2.5 bg-white border border-gray-300 rounded-lg focus:ring-2 focus:ring-medical-500 focus:border-medical-500 transition-all outline-none text-gray-900"
            value={data.gender}
            onChange={(e) => handleChange('gender', e.target.value)}
          >
            {Object.values(Gender).map((g) => (
              <option key={g} value={g}>{g}</option>
            ))}
          </select>
        </div>

        {/* Age */}
        <div className="space-y-2">
          <label className="text-sm font-medium text-gray-700">Age (Years)</label>
          <input
            type="number"
            min="0"
            max="120"
            className="w-full p-2.5 bg-white border border-gray-300 rounded-lg focus:ring-2 focus:ring-medical-500 focus:border-medical-500 transition-all outline-none text-gray-900"
            value={data.age}
            onChange={(e) => handleChange('age', parseInt(e.target.value) || 0)}
          />
        </div>

        {/* Hypertension */}
        <div className="space-y-2">
          <label className="text-sm font-medium text-gray-700 flex items-center gap-2">
            <Activity size={16} /> Hypertension
          </label>
          <div className="flex gap-4">
            <button
              onClick={() => handleChange('hypertension', true)}
              className={`flex-1 py-2 px-4 rounded-lg border text-sm font-medium transition-colors ${
                data.hypertension
                  ? 'bg-red-50 border-red-200 text-red-700'
                  : 'bg-white border-gray-200 text-gray-600 hover:bg-gray-50'
              }`}
            >
              Yes
            </button>
            <button
              onClick={() => handleChange('hypertension', false)}
              className={`flex-1 py-2 px-4 rounded-lg border text-sm font-medium transition-colors ${
                !data.hypertension
                  ? 'bg-green-50 border-green-200 text-green-700'
                  : 'bg-white border-gray-200 text-gray-600 hover:bg-gray-50'
              }`}
            >
              No
            </button>
          </div>
        </div>

        {/* Heart Disease */}
        <div className="space-y-2">
          <label className="text-sm font-medium text-gray-700 flex items-center gap-2">
            <Heart size={16} /> Heart Disease
          </label>
          <div className="flex gap-4">
            <button
              onClick={() => handleChange('heartDisease', true)}
              className={`flex-1 py-2 px-4 rounded-lg border text-sm font-medium transition-colors ${
                data.heartDisease
                  ? 'bg-red-50 border-red-200 text-red-700'
                  : 'bg-white border-gray-200 text-gray-600 hover:bg-gray-50'
              }`}
            >
              Yes
            </button>
            <button
              onClick={() => handleChange('heartDisease', false)}
              className={`flex-1 py-2 px-4 rounded-lg border text-sm font-medium transition-colors ${
                !data.heartDisease
                  ? 'bg-green-50 border-green-200 text-green-700'
                  : 'bg-white border-gray-200 text-gray-600 hover:bg-gray-50'
              }`}
            >
              No
            </button>
          </div>
        </div>

        {/* Glucose */}
        <div className="space-y-2">
          <label className="text-sm font-medium text-gray-700 flex items-center gap-2">
             <Stethoscope size={16} /> Avg. Glucose Level (mg/dL)
          </label>
          <input
            type="number"
            step="0.1"
            className="w-full p-2.5 bg-white border border-gray-300 rounded-lg focus:ring-2 focus:ring-medical-500 focus:border-medical-500 transition-all outline-none text-gray-900"
            value={data.avgGlucoseLevel}
            onChange={(e) => handleChange('avgGlucoseLevel', parseFloat(e.target.value) || 0)}
          />
        </div>

        {/* BMI */}
        <div className="space-y-2">
          <label className="text-sm font-medium text-gray-700 flex items-center gap-2">
            <Scale size={16} /> BMI
          </label>
          <input
            type="number"
            step="0.1"
            className="w-full p-2.5 bg-white border border-gray-300 rounded-lg focus:ring-2 focus:ring-medical-500 focus:border-medical-500 transition-all outline-none text-gray-900"
            value={data.bmi}
            onChange={(e) => handleChange('bmi', parseFloat(e.target.value) || 0)}
          />
        </div>

        {/* Work Type */}
        <div className="space-y-2">
          <label className="text-sm font-medium text-gray-700 flex items-center gap-2">
            <Briefcase size={16} /> Work Type
          </label>
          <select
            className="w-full p-2.5 bg-white border border-gray-300 rounded-lg focus:ring-2 focus:ring-medical-500 focus:border-medical-500 transition-all outline-none text-gray-900"
            value={data.workType}
            onChange={(e) => handleChange('workType', e.target.value)}
          >
            {Object.values(WorkType).map((w) => (
              <option key={w} value={w}>{w}</option>
            ))}
          </select>
        </div>

        {/* Residence Type */}
        <div className="space-y-2">
          <label className="text-sm font-medium text-gray-700 flex items-center gap-2">
            <Home size={16} /> Residence Type
          </label>
          <select
            className="w-full p-2.5 bg-white border border-gray-300 rounded-lg focus:ring-2 focus:ring-medical-500 focus:border-medical-500 transition-all outline-none text-gray-900"
            value={data.residenceType}
            onChange={(e) => handleChange('residenceType', e.target.value)}
          >
            {Object.values(ResidenceType).map((r) => (
              <option key={r} value={r}>{r}</option>
            ))}
          </select>
        </div>

        {/* Smoking Status */}
        <div className="space-y-2 md:col-span-2">
          <label className="text-sm font-medium text-gray-700 flex items-center gap-2">
            <Cigarette size={16} /> Smoking Status
          </label>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
            {Object.values(SmokingStatus).map((s) => (
              <button
                key={s}
                onClick={() => handleChange('smokingStatus', s)}
                className={`py-2 px-2 text-center rounded-lg border text-sm font-medium transition-colors ${
                  data.smokingStatus === s
                    ? 'bg-medical-50 border-medical-200 text-medical-700'
                    : 'bg-white border-gray-200 text-gray-600 hover:bg-gray-50'
                }`}
              >
                {s}
              </button>
            ))}
          </div>
        </div>

         {/* Ever Married */}
         <div className="space-y-2 md:col-span-2">
          <label className="text-sm font-medium text-gray-700">Ever Married</label>
          <div className="flex gap-4">
              {Object.values(YesNo).map((yn) => (
                   <button
                   key={yn}
                   onClick={() => handleChange('everMarried', yn)}
                   className={`flex-1 py-2 px-4 rounded-lg border text-sm font-medium transition-colors ${
                     data.everMarried === yn
                       ? 'bg-medical-50 border-medical-200 text-medical-700'
                       : 'bg-white border-gray-200 text-gray-600 hover:bg-gray-50'
                   }`}
                 >
                   {yn}
                 </button>
              ))}
          </div>
        </div>

      </div>

      <div className="p-6 bg-gray-50 border-t border-gray-100">
        <button
          onClick={onSubmit}
          disabled={isAnalyzing}
          className={`w-full py-3.5 px-6 rounded-xl text-white font-semibold text-lg shadow-lg shadow-medical-500/30 transition-all transform active:scale-[0.99] flex items-center justify-center gap-2 ${
            isAnalyzing ? 'bg-medical-400 cursor-not-allowed' : 'bg-medical-600 hover:bg-medical-700'
          }`}
        >
          {isAnalyzing ? (
            <>
               <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Processing Clinical Data...
            </>
          ) : (
            'Analyze Stroke Risk'
          )}
        </button>
      </div>
    </div>
  );
};
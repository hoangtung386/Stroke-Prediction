import React from 'react';
import { PatientData } from '../types';
import { User, Heart, Activity, Briefcase, Home, Cigarette, Scale, Stethoscope } from 'lucide-react';

interface PatientFormProps {
    data: PatientData;
    onChange: (data: PatientData) => void;
    onSubmit: () => void;
    isAnalyzing: boolean;
    disabled?: boolean;
}

const GENDERS = ['Male', 'Female', 'Other'] as const;
const WORK_TYPES = ['Private', 'Self-employed', 'Govt_job', 'children', 'Never_worked'] as const;
const RESIDENCE_TYPES = ['Urban', 'Rural'] as const;
const SMOKING_STATUSES = ['never smoked', 'formerly smoked', 'smokes', 'Unknown'] as const;

export const PatientForm: React.FC<PatientFormProps> = ({
    data,
    onChange,
    onSubmit,
    isAnalyzing,
    disabled = false
}) => {

    const handleChange = (field: keyof PatientData, value: unknown) => {
        onChange({ ...data, [field]: value });
    };

    return (
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
            <div className="p-6 border-b border-gray-100 bg-gray-50">
                <h2 className="text-lg font-semibold text-gray-800 flex items-center gap-2">
                    <User className="text-sky-600" size={20} />
                    Patient Demographics & Clinical Data
                </h2>
                <p className="text-sm text-gray-500 mt-1">Enter patient specifications for model inference.</p>
            </div>

            <div className="p-6 grid grid-cols-1 md:grid-cols-2 gap-6">

                {/* Gender */}
                <div className="space-y-2">
                    <label className="text-sm font-medium text-gray-700">Gender</label>
                    <select
                        className="w-full p-2.5 bg-white border border-gray-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500 transition-all outline-none text-gray-900"
                        value={data.gender}
                        onChange={(e) => handleChange('gender', e.target.value)}
                    >
                        {GENDERS.map((g) => (
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
                        className="w-full p-2.5 bg-white border border-gray-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500 transition-all outline-none text-gray-900"
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
                            type="button"
                            onClick={() => handleChange('hypertension', 1)}
                            className={`flex-1 py-2 px-4 rounded-lg border text-sm font-medium transition-colors ${data.hypertension === 1
                                    ? 'bg-red-50 border-red-200 text-red-700'
                                    : 'bg-white border-gray-200 text-gray-600 hover:bg-gray-50'
                                }`}
                        >
                            Yes
                        </button>
                        <button
                            type="button"
                            onClick={() => handleChange('hypertension', 0)}
                            className={`flex-1 py-2 px-4 rounded-lg border text-sm font-medium transition-colors ${data.hypertension === 0
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
                            type="button"
                            onClick={() => handleChange('heart_disease', 1)}
                            className={`flex-1 py-2 px-4 rounded-lg border text-sm font-medium transition-colors ${data.heart_disease === 1
                                    ? 'bg-red-50 border-red-200 text-red-700'
                                    : 'bg-white border-gray-200 text-gray-600 hover:bg-gray-50'
                                }`}
                        >
                            Yes
                        </button>
                        <button
                            type="button"
                            onClick={() => handleChange('heart_disease', 0)}
                            className={`flex-1 py-2 px-4 rounded-lg border text-sm font-medium transition-colors ${data.heart_disease === 0
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
                        className="w-full p-2.5 bg-white border border-gray-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500 transition-all outline-none text-gray-900"
                        value={data.avg_glucose_level}
                        onChange={(e) => handleChange('avg_glucose_level', parseFloat(e.target.value) || 0)}
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
                        className="w-full p-2.5 bg-white border border-gray-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500 transition-all outline-none text-gray-900"
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
                        className="w-full p-2.5 bg-white border border-gray-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500 transition-all outline-none text-gray-900"
                        value={data.work_type}
                        onChange={(e) => handleChange('work_type', e.target.value)}
                    >
                        {WORK_TYPES.map((w) => (
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
                        className="w-full p-2.5 bg-white border border-gray-300 rounded-lg focus:ring-2 focus:ring-sky-500 focus:border-sky-500 transition-all outline-none text-gray-900"
                        value={data.Residence_type}
                        onChange={(e) => handleChange('Residence_type', e.target.value)}
                    >
                        {RESIDENCE_TYPES.map((r) => (
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
                        {SMOKING_STATUSES.map((s) => (
                            <button
                                type="button"
                                key={s}
                                onClick={() => handleChange('smoking_status', s)}
                                className={`py-2 px-2 text-center rounded-lg border text-sm font-medium transition-colors ${data.smoking_status === s
                                        ? 'bg-sky-50 border-sky-200 text-sky-700'
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
                        {(['Yes', 'No'] as const).map((yn) => (
                            <button
                                type="button"
                                key={yn}
                                onClick={() => handleChange('ever_married', yn)}
                                className={`flex-1 py-2 px-4 rounded-lg border text-sm font-medium transition-colors ${data.ever_married === yn
                                        ? 'bg-sky-50 border-sky-200 text-sky-700'
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
                    disabled={isAnalyzing || disabled}
                    className={`w-full py-3.5 px-6 rounded-xl text-white font-semibold text-lg shadow-lg shadow-sky-500/30 transition-all transform active:scale-[0.99] flex items-center justify-center gap-2 ${isAnalyzing || disabled ? 'bg-sky-400 cursor-not-allowed' : 'bg-sky-600 hover:bg-sky-700'
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

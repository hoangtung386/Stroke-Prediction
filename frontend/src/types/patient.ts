export interface PatientData {
    gender: 'Male' | 'Female' | 'Other';
    age: number;
    hypertension: 0 | 1;
    heart_disease: 0 | 1;
    ever_married: 'Yes' | 'No';
    work_type: 'Private' | 'Self-employed' | 'Govt_job' | 'children' | 'Never_worked';
    Residence_type: 'Urban' | 'Rural';
    avg_glucose_level: number;
    bmi: number;
    smoking_status: 'never smoked' | 'formerly smoked' | 'smokes' | 'Unknown';
}

export const DEFAULT_PATIENT_DATA: PatientData = {
    gender: 'Male',
    age: 50,
    hypertension: 0,
    heart_disease: 0,
    ever_married: 'Yes',
    work_type: 'Private',
    Residence_type: 'Urban',
    avg_glucose_level: 100,
    bmi: 25,
    smoking_status: 'never smoked',
};

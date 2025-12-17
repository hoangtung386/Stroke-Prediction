export enum Gender {
  Male = 'Male',
  Female = 'Female',
}

export enum WorkType {
  Private = 'Private',
  SelfEmployed = 'Self-employed',
  GovtJob = 'Govt_job',
  Children = 'children',
  NeverWorked = 'Never_worked',
}

export enum ResidenceType {
  Urban = 'Urban',
  Rural = 'Rural',
}

export enum SmokingStatus {
  FormerlySmoked = 'formerly smoked',
  NeverSmoked = 'never smoked',
  Smokes = 'smokes',
  Unknown = 'Unknown',
}

export enum YesNo {
  Yes = 'Yes',
  No = 'No',
}

export interface PatientData {
  gender: Gender;
  age: number;
  hypertension: boolean;
  heartDisease: boolean;
  everMarried: YesNo;
  workType: WorkType;
  residenceType: ResidenceType;
  avgGlucoseLevel: number;
  bmi: number;
  smokingStatus: SmokingStatus;
}

export interface RiskAnalysis {
  riskScore: number; // 0 to 100
  riskLevel: 'Low' | 'Moderate' | 'High' | 'Critical';
  hasPrediction: boolean;
  factors: string[];
  recommendations: string[];
  
  // Optional fields for backward compatibility
  reasoning?: string;
  contributingFactors?: { name: string; impact: 'High' | 'Medium' | 'Low' }[];
  
  // ML Model specific fields
  confidence?: number;
  modelUsed?: string;
  modelDescription?: string;
}

export const DEFAULT_PATIENT_DATA: PatientData = {
  gender: Gender.Male,
  age: 45,
  hypertension: false,
  heartDisease: false,
  everMarried: YesNo.Yes,
  workType: WorkType.Private,
  residenceType: ResidenceType.Urban,
  avgGlucoseLevel: 85.0,
  bmi: 24.5,
  smokingStatus: SmokingStatus.NeverSmoked,
};

import { GoogleGenAI, Type } from "@google/genai";
import { PatientData, RiskAnalysis } from "../types";

const apiKey = process.env.API_KEY;

// Fallback logic if API key is missing, to prevent app crash on init
const getAIClient = () => {
  if (!apiKey) {
    console.warn("Gemini API Key is missing. Please set process.env.API_KEY.");
    return null;
  }
  return new GoogleGenAI({ apiKey });
};

export const analyzeStrokeRisk = async (data: PatientData): Promise<RiskAnalysis> => {
  const ai = getAIClient();
  if (!ai) {
    throw new Error("API configuration error: Missing API Key.");
  }

  // We use the Python paper's context to inform the AI how to evaluate.
  // This simulates the trained model but adds reasoning capabilities.
  const prompt = `
    Act as a specialized medical AI trained on stroke prediction datasets (like the Kaggle Stroke Prediction Dataset).
    Analyze the following patient clinical data and determine the risk of stroke.

    Patient Data:
    - Gender: ${data.gender}
    - Age: ${data.age}
    - Hypertension: ${data.hypertension ? "Yes" : "No"}
    - Heart Disease: ${data.heartDisease ? "Yes" : "No"}
    - Ever Married: ${data.everMarried}
    - Work Type: ${data.workType}
    - Residence Type: ${data.residenceType}
    - Average Glucose Level: ${data.avgGlucoseLevel} mg/dL
    - BMI: ${data.bmi}
    - Smoking Status: ${data.smokingStatus}

    Context:
    High glucose (>200), high BMI (>30), advanced age, hypertension, and heart disease are significant risk factors.

    Return the analysis in strict JSON format.
  `;

  try {
    const response = await ai.models.generateContent({
      model: "gemini-2.5-flash",
      contents: prompt,
      config: {
        responseMimeType: "application/json",
        responseSchema: {
          type: Type.OBJECT,
          properties: {
            riskScore: {
              type: Type.NUMBER,
              description: "A probability score from 0 to 100 representing stroke risk.",
            },
            riskLevel: {
              type: Type.STRING,
              description: "Categorical risk level: Low, Moderate, High, or Critical.",
              enum: ["Low", "Moderate", "High", "Critical"]
            },
            reasoning: {
              type: Type.STRING,
              description: "A concise medical explanation of why this score was given, citing specific patient factors.",
            },
            recommendations: {
              type: Type.ARRAY,
              items: { type: Type.STRING },
              description: "List of 3-5 actionable medical or lifestyle recommendations.",
            },
            contributingFactors: {
              type: Type.ARRAY,
              items: {
                type: Type.OBJECT,
                properties: {
                  name: { type: Type.STRING },
                  impact: { type: Type.STRING, enum: ["High", "Medium", "Low"] }
                }
              },
              description: "List of factors that negatively impacted the score."
            }
          }
        }
      }
    });

    const resultText = response.text;
    if (!resultText) {
        throw new Error("Empty response from AI");
    }

    return JSON.parse(resultText) as RiskAnalysis;

  } catch (error) {
    console.error("Error analyzing stroke risk:", error);
    throw new Error("Failed to analyze risk. Please try again.");
  }
};
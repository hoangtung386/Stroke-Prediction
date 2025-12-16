# StrokeGuard AI

**StrokeGuard AI** is a cutting-edge medical analysis web application designed to evaluate stroke risk factors using advanced Generative AI. By leveraging the **Google Gemini 2.5** model, the system analyzes clinical patient parameters—such as age, BMI, glucose levels, and medical history—to provide an immediate risk assessment, detailed reasoning, and personalized health recommendations.

The application translates complex medical data patterns (inspired by the Kaggle Stroke Prediction Dataset) into an accessible, user-friendly interface for preliminary health screening.

---

## 🚀 Key Features

*   **Interactive Patient Profiling:** Comprehensive form for entering demographic and clinical data (Age, Gender, BMI, Hypertension, Heart Disease, etc.).
*   **AI-Powered Analysis:** Utilizes Google's **Gemini 2.5 Flash** model to process inputs and reason about stroke risk based on medical contexts.
*   **Visual Risk Dashboard:**
    *   **Risk Score Gauge:** Immediate visual representation of stroke probability.
    *   **Contributing Factors:** Identifies specific variables (e.g., High Glucose, Smoking) driving the risk.
*   **Explainable AI:** Provides a natural language explanation of *why* a specific risk score was assigned.
*   **Actionable Recommendations:** Generates personalized lifestyle and medical advice based on the analysis.
*   **Responsive Design:** Built with Tailwind CSS for a seamless experience on desktop and mobile devices.

---

## 🛠️ Technology Stack

*   **Frontend:** React (TypeScript)
*   **Styling:** Tailwind CSS
*   **AI Model:** Google Gemini API (`@google/genai`)
*   **Visualization:** Recharts
*   **Icons:** Lucide React
*   **Build Tool:** Vite / Parcel (depending on environment)

---

## ⚙️ Prerequisites

Before you begin, ensure you have the following installed:

*   **Node.js** (v18 or higher)
*   **npm** or **yarn**
*   **Google Gemini API Key** (Get one at [aistudio.google.com](https://aistudio.google.com/))

---

## 📥 Installation & Setup

Follow these steps to set up the project locally:

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/strokeguard-ai.git
cd strokeguard-ai
```

### 2. Install Dependencies

```bash
npm install
# or
yarn install
```

### 3. Configure Environment Variables

This project requires a Google Gemini API Key to function.

1.  Create a file named `.env` in the root directory.
2.  Add your API key to the file:

```env
API_KEY=your_actual_google_gemini_api_key_here
```

> **Note:** The application uses `process.env.API_KEY` to authenticate requests. Ensure your build tool is configured to expose this variable (e.g., in Vite, use `VITE_API_KEY` and update the code accordingly, or use a bundler that supports `process.env` injection).

### 4. Run the Development Server

```bash
npm start
# or
npm run dev
```

Open your browser and navigate to `http://localhost:1234` (or the port specified in your terminal).

---

## 🚀 Deployment

To deploy this application to a production environment (e.g., Vercel, Netlify, or AWS Amplify):

### 1. Build the Project

Generate the optimized production build:

```bash
npm run build
```

This will create a `dist` or `build` folder containing the static files.

### 2. Set Environment Variables on the Host

When deploying, do not commit your `.env` file. Instead, go to your hosting provider's dashboard (e.g., Vercel Project Settings) and add the Environment Variable:

*   **Key:** `API_KEY`
*   **Value:** `your_google_gemini_api_key`

### 3. Deploy

*   **Vercel:** Connect your GitHub repository and import the project. Vercel automatically detects the build settings.
*   **Netlify:** Drag and drop the `dist` folder or connect via Git.

---

## ⚠️ Medical Disclaimer

**StrokeGuard AI is for demonstration and educational purposes only.**

The AI model provides estimates based on statistical patterns found in datasets. It is **not** a diagnostic tool and should **not** replace professional medical advice, diagnosis, or treatment. Always consult with a qualified healthcare provider for any medical concerns.

---

## 📄 License

This project is licensed under the MIT License.

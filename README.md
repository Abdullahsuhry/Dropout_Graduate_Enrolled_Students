# Student Dropout Predictor - Setup Instructions

## Project Structure
```
dropout-predictor/
│
├── app.py                    # Flask backend
├── requirements.txt          # Python dependencies
├── predictor.pickle          # Trained ML model (from your notebook)
├── index.html               # Frontend (HTML/CSS/JS)
└── README.md                # This file
```

## Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Your trained model file: `predictor.pickle`

## Backend Setup

### Step 1: Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Prepare the Model File
1. Make sure you have run your Jupyter notebook (`Droput.ipynb`)
2. Ensure the file `predictor.pickle` was created
3. Place `predictor.pickle` in the same directory as `app.py`

### Step 4: Run the Flask Backend
```bash
python app.py
```

The backend will start on `http://localhost:5000`

You should see:
```
============================================================
Student Dropout Prediction API
Model loaded successfully!
Server running on http://localhost:5000
============================================================
```

## Frontend Setup

### Step 1: Open the HTML File
Simply open `index.html` in your web browser. You can:
- Double-click the file
- Right-click → Open with → Your browser
- Or use a local server (recommended):

```bash
# Using Python
python -m http.server 8000

# Then open: http://localhost:8000
```

## Testing the Application

### Step 1: Fill in Student Information
The form is pre-filled with default values. You can modify:
- **Academic Performance**: Grades, approved units
- **Financial Status**: Debtor status, tuition fees
- **Demographics**: Age, gender, marital status
- **Economic Factors**: Unemployment rate, inflation, GDP

### Step 2: Click "Predict Student Outcome"
The system will:
1. Send data to the Flask backend
2. Process it through the Random Forest model
3. Return prediction with confidence score

### Step 3: View Results
You'll see:
- **Prediction**: Dropout Risk (0), Enrolled (1), or Graduate Likely (2)
- **Confidence Score**: Model's certainty (0-100%)
- **Probability Breakdown**: Chances for each outcome
- **Key Factors**: Risk factors identified

## API Endpoints

### 1. Health Check
```
GET http://localhost:5000/health
```
Response:
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

### 2. Prediction
```
POST http://localhost:5000/predict
Content-Type: application/json
```

Request Body Example:
```json
{
  "maritalStatus": 1,
  "applicationMode": 1,
  "applicationOrder": 1,
  "course": 171,
  "daytimeAttendance": 1,
  "previousQualification": 1,
  "previousQualificationGrade": 120,
  "nationality": 1,
  "mothersQualification": 1,
  "fathersQualification": 1,
  "mothersOccupation": 1,
  "fathersOccupation": 1,
  "admissionGrade": 120,
  "displaced": 0,
  "educationalSpecialNeeds": 0,
  "debtor": 0,
  "tuitionFeesUpToDate": 1,
  "gender": 1,
  "scholarshipHolder": 0,
  "ageAtEnrollment": 18,
  "international": 0,
  "curricularUnits1stSemCredited": 0,
  "curricularUnits1stSemEnrolled": 6,
  "curricularUnits1stSemEvaluations": 6,
  "curricularUnits1stSemApproved": 6,
  "curricularUnits1stSemGrade": 12,
  "curricularUnits1stSemWithoutEvaluations": 0,
  "curricularUnits2ndSemCredited": 0,
  "curricularUnits2ndSemEnrolled": 6,
  "curricularUnits2ndSemEvaluations": 6,
  "curricularUnits2ndSemApproved": 6,
  "curricularUnits2ndSemGrade": 12,
  "curricularUnits2ndSemWithoutEvaluations": 0,
  "unemploymentRate": 10.8,
  "inflationRate": 1.4,
  "gdp": 1.74
}
```

Response:
```json
{
  "prediction": 2,
  "prediction_label": "Graduate",
  "confidence": 0.85,
  "probabilities": [0.05, 0.10, 0.85],
  "risk_factors": [
    "Strong academic performance (grades above 14)",
    "High admission grade (positive factor)"
  ]
}
```

## Troubleshooting

### Issue: "Model not loaded" error
**Solution**: Ensure `predictor.pickle` is in the same directory as `app.py`

### Issue: CORS errors in browser
**Solution**: Make sure `flask-cors` is installed:
```bash
pip install flask-cors
```

### Issue: Connection refused
**Solution**: Ensure Flask backend is running on port 5000

### Issue: ModuleNotFoundError
**Solution**: Install missing packages:
```bash
pip install -r requirements.txt
```

### Issue: Frontend can't connect to backend
**Solution**: 
1. Check if backend is running (`http://localhost:5000`)
2. Verify the API_URL in `index.html` matches your backend URL
3. Check browser console for errors

## Model Information

- **Algorithm**: Random Forest Classifier
- **Accuracy**: 76.95%
- **Classes**: 
  - 0: Dropout
  - 1: Enrolled
  - 2: Graduate
- **Features**: 36 input features including academic performance, demographics, and economic indicators

## Key Features Analyzed

The model considers:
- Academic performance (grades, approved units)
- Financial status (debtor, tuition payment)
- Demographics (age, gender, marital status)
- Parental background (education, occupation)
- Economic context (unemployment, inflation, GDP)
- Enrollment patterns (attendance, course selection)

## Notes

- The model is trained on historical data with 76.95% accuracy
- Predictions should be used for early intervention, not definitive judgments
- Regular model retraining with new data is recommended
- Consider implementing authentication for production use

## Support

For issues or questions:
1. Check the console logs (browser and Flask)
2. Verify all dependencies are installed
3. Ensure model file is present and valid
4. Check that all required fields are filled in the form

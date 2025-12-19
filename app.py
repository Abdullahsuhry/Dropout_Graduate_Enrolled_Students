from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the trained model
MODEL_PATH = 'predictor.pickle'

try:
    with open(MODEL_PATH, 'rb') as file:
        model = pickle.load(file)
    print("Model loaded successfully!")
except FileNotFoundError:
    print(f"Error: {MODEL_PATH} not found. Please make sure the model file exists.")
    model = None

@app.route('/')
def home():
    return jsonify({
        'message': 'Student Dropout Prediction API',
        'status': 'running',
        'model_loaded': model is not None
    })

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({
            'error': 'Model not loaded. Please ensure predictor.pickle exists.'
        }), 500
    
    try:
        # Get data from request
        data = request.get_json()
        
        # Feature names in the exact order as your training data
        feature_names = [
            'maritalStatus',
            'applicationMode',
            'applicationOrder',
            'course',
            'daytimeAttendance',
            'previousQualification',
            'previousQualificationGrade',
            'nationality',
            'mothersQualification',
            'fathersQualification',
            'mothersOccupation',
            'fathersOccupation',
            'admissionGrade',
            'displaced',
            'educationalSpecialNeeds',
            'debtor',
            'tuitionFeesUpToDate',
            'gender',
            'scholarshipHolder',
            'ageAtEnrollment',
            'international',
            'curricularUnits1stSemCredited',
            'curricularUnits1stSemEnrolled',
            'curricularUnits1stSemEvaluations',
            'curricularUnits1stSemApproved',
            'curricularUnits1stSemGrade',
            'curricularUnits1stSemWithoutEvaluations',
            'curricularUnits2ndSemCredited',
            'curricularUnits2ndSemEnrolled',
            'curricularUnits2ndSemEvaluations',
            'curricularUnits2ndSemApproved',
            'curricularUnits2ndSemGrade',
            'curricularUnits2ndSemWithoutEvaluations',
            'unemploymentRate',
            'inflationRate',
            'gdp'
        ]
        
        # Extract features in the correct order
        features = []
        for feature in feature_names:
            if feature not in data:
                return jsonify({
                    'error': f'Missing required field: {feature}'
                }), 400
            features.append(float(data[feature]))
        
        # Convert to numpy array and reshape
        features_array = np.array(features).reshape(1, -1)
        
        # Make prediction
        prediction = model.predict(features_array)[0]
        probabilities = model.predict_proba(features_array)[0]
        
        # Get confidence (probability of predicted class)
        confidence = float(probabilities[prediction])
        
        # Map prediction to label
        labels = {
            0: 'Dropout',
            1: 'Enrolled',
            2: 'Graduate'
        }
        
        # Analyze risk factors
        risk_factors = analyze_risk_factors(data, prediction)
        
        return jsonify({
            'prediction': int(prediction),
            'prediction_label': labels[prediction],
            'confidence': confidence,
            'probabilities': probabilities.tolist(),
            'risk_factors': risk_factors
        })
    
    except Exception as e:
        print(f"Error during prediction: {str(e)}")
        return jsonify({
            'error': f'Prediction error: {str(e)}'
        }), 500

def analyze_risk_factors(data, prediction):
    """Analyze and return key risk factors based on the data"""
    factors = []
    
    # Academic performance analysis
    first_sem_grade = data.get('curricularUnits1stSemGrade', 0)
    second_sem_grade = data.get('curricularUnits2ndSemGrade', 0)
    
    if first_sem_grade < 10 or second_sem_grade < 10:
        factors.append("Low academic grades (below 10)")
    elif first_sem_grade > 14 and second_sem_grade > 14:
        factors.append("Strong academic performance (grades above 14)")
    
    # Approval rate analysis
    first_sem_enrolled = data.get('curricularUnits1stSemEnrolled', 1)
    first_sem_approved = data.get('curricularUnits1stSemApproved', 0)
    second_sem_enrolled = data.get('curricularUnits2ndSemEnrolled', 1)
    second_sem_approved = data.get('curricularUnits2ndSemApproved', 0)
    
    if first_sem_enrolled > 0:
        first_sem_rate = first_sem_approved / first_sem_enrolled
        if first_sem_rate < 0.5:
            factors.append(f"Low first semester approval rate ({first_sem_rate*100:.0f}%)")
    
    if second_sem_enrolled > 0:
        second_sem_rate = second_sem_approved / second_sem_enrolled
        if second_sem_rate < 0.5:
            factors.append(f"Low second semester approval rate ({second_sem_rate*100:.0f}%)")
    
    # Financial factors
    if data.get('debtor', 0) == 1:
        factors.append("Student has outstanding debts")
    
    if data.get('tuitionFeesUpToDate', 1) == 0:
        factors.append("Tuition fees not up to date")
    
    if data.get('scholarshipHolder', 0) == 1:
        factors.append("Scholarship holder (positive factor)")
    
    # Age factor
    age = data.get('ageAtEnrollment', 18)
    if age > 25:
        factors.append(f"Mature student (age {age})")
    
    # Admission grade
    admission_grade = data.get('admissionGrade', 0)
    if admission_grade < 100:
        factors.append("Low admission grade")
    elif admission_grade > 150:
        factors.append("High admission grade (positive factor)")
    
    # Evaluations without passing
    if data.get('curricularUnits1stSemEvaluations', 0) > data.get('curricularUnits1stSemApproved', 0):
        factors.append("Multiple evaluation attempts in first semester")
    
    if data.get('curricularUnits2ndSemEvaluations', 0) > data.get('curricularUnits2ndSemApproved', 0):
        factors.append("Multiple evaluation attempts in second semester")
    
    # If no specific factors identified
    if not factors:
        if prediction == 2:
            factors.append("Overall strong academic profile")
        elif prediction == 1:
            factors.append("Mixed performance indicators")
        else:
            factors.append("Multiple concerning factors detected")
    
    return factors

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None
    })

if __name__ == '__main__':
    if model is None:
        print("\n" + "="*60)
        print("WARNING: Model file not found!")
        print("Please ensure 'predictor.pickle' is in the same directory")
        print("="*60 + "\n")
    else:
        print("\n" + "="*60)
        print("Student Dropout Prediction API")
        print("Model loaded successfully!")
        print("Server running on http://localhost:5000")
        print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
from flask import Flask, request, render_template, redirect, url_for
import numpy as np
import pandas as pd
import pickle
import warnings
from dashboard import dashboard_bp

# Flask app
app = Flask(__name__)
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')

# Load database datasets
sym_des = pd.read_csv("datasets/symtoms_df.csv")
precautions = pd.read_csv("datasets/precautions_df.csv")
workout = pd.read_csv("datasets/workout_df.csv")
description = pd.read_csv("datasets/description.csv")
medications = pd.read_csv('datasets/medications.csv')
diets = pd.read_csv("datasets/diets.csv")

# Load model
svc = pickle.load(open('datasets/svc.pkl', 'rb'))
le = pickle.load(open('datasets/label_encoder.pkl', 'rb'))

#Advance Load models
pregnancy_model = pickle.load(open("datasets/advance/models/pregnancy_model.pkl", 'rb'))
heart_model = pickle.load(open("datasets/advance/models/Heart.sav", 'rb'))
diabetic_model = pickle.load(open("datasets/advance/models/Diabetes.sav", 'rb'))


# Normalize column names and data to handle inconsistencies
workout.rename(columns={'disease': 'Disease'}, inplace=True)

def normalize_column(df, column_name):
    df[column_name] = df[column_name].str.strip().str.lower()

for df in [description, precautions, medications, workout, diets]:
    normalize_column(df, 'Disease')

# Function to predict disease based on symptoms
def predict_disease(symptoms):
    symptoms_dict = {symptom: 0 for symptom in svc.feature_names_in_}
    for symptom in symptoms:
        symptom = symptom.strip().lower()
        if symptom in symptoms_dict:
            symptoms_dict[symptom] = 1

    input_data = pd.DataFrame([symptoms_dict])
    predicted_disease = svc.predict(input_data)
    disease_name = le.inverse_transform(predicted_disease)[0].strip().lower()

    return disease_name

# Helper function to fetch recommendations
def helper(dis):
    desc = description[description['Disease'] == dis]['Description'].values[0]
    pre = precautions[precautions['Disease'] == dis][['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']].values[0]
    med = medications[medications['Disease'] == dis]['Medication'].values[0].split(',')
    die = diets[diets['Disease'] == dis]['Diet'].values[0].split(',')
    wrkout = workout[workout['Disease'] == dis]['workout'].values[0].split(',')

    return desc, pre, med, die, wrkout

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/developer')
def developer():
    return render_template("developer.html")

@app.route('/blog')
def blog():
    return render_template("blog.html")

@app.route('/search', methods=['POST'])
def submit():
    if request.method == 'POST':
        selected_values = request.form.getlist('options')
        print("Selected values:", selected_values)  # Debugging print statement
        predicted_disease = predict_disease(selected_values)
        return redirect(url_for('result', predicted_disease=predicted_disease,))
    else:
        return "Invalid request method"

@app.route('/result')
def result():
    predicted_disease = request.args.get('predicted_disease')
    print("Predicted disease:", predicted_disease)  # Debugging print statement
    if not predicted_disease:
        return "No predicted disease received."

    dis_des, precautions_list, medications, diet, workout = helper(predicted_disease)
    my_precautions = [precaution for precaution in precautions_list]
    return render_template('result.html', predicted_disease=predicted_disease.capitalize(), dis_des=dis_des, my_precautions=my_precautions, medications=medications, my_diet=diet, workout=workout,)

#advance
@app.route('/pregnancy', methods=['GET', 'POST'])
def pregnancy():
    risk_level = None
    color = None
    if request.method == 'POST':
        age = request.form['age']
        diastolicBP = request.form['diastolicBP']
        BS = request.form['BS']
        bodyTemp = request.form['bodyTemp']
        heartRate = request.form['heartRate']
        
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            predicted_risk = pregnancy_model.predict([[age, diastolicBP, BS, bodyTemp, heartRate]])
        
        if predicted_risk[0] == 0:
            risk_level = "Low Risk"
            color = "green"
        elif predicted_risk[0] == 1:
            risk_level = "Medium Risk"
            color = "orange"
        else:
            risk_level = "High Risk"
            color = "red"
    
    return render_template('pregnancy.html', risk_level=risk_level, color=color)




@app.route('/heart', methods=['GET', 'POST'])
def heart():
    prediction_text = None
    if request.method == 'POST':
        # Convert 'sex' and 'cp' inputs to the required integer values
        sex = 0 if request.form['sex'] == 'Male' else 1
        cp_dict = {
            'Low pain': 0,
            'Mild pain': 1,
            'Moderate pain': 2,
            'Extreme pain': 3
        }
        cp = cp_dict[request.form['cp']]

        data = [
            request.form['age'],
            sex,
            cp,
            request.form['trestbps'],
            request.form['chol'],
            request.form['fbs'],
            request.form['restecg'],
            request.form['thalach'],
            request.form['exang'],
            request.form['oldpeak'],
            request.form['slope'],
            request.form['ca'],
            request.form['thal']
        ]

        input_data = [data]
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            heart_prediction = heart_model.predict(input_data)
        
        if heart_prediction[0] == 1:
            prediction_text = 'The person is having heart disease'
        else:
            prediction_text = 'The person does not have any heart disease'
    
    return render_template('heart.html', prediction_text=prediction_text)


@app.route('/diabetes', methods=['GET', 'POST'])
def diabetes():
    prediction_text = None
    if request.method == 'POST':
        data = [
            request.form['Pregnancies'],
            request.form['Glucose'],
            request.form['BloodPressure'],
            request.form['SkinThickness'],
            request.form['Insulin'],
            request.form['BMI'],
            request.form['DiabetesPedigreeFunction'],
            request.form['Age']
        ]

        input_data = [data]
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            prediction = diabetic_model.predict(input_data)

        if prediction[0] == 1:
            prediction_text = 'The person is diabetic'
        else:
            prediction_text = 'The person is not diabetic'
    
    return render_template('diabetes.html', prediction_text=prediction_text,active_page='index')

if __name__ == '__main__':
    app.run(debug=True)

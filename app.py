from flask import Flask, request, render_template, redirect, url_for
import numpy as np
import pandas as pd
import pickle

# Flask app
app = Flask(__name__)

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
    return render_template('result.html', predicted_disease=predicted_disease.capitalize(), dis_des=dis_des, my_precautions=my_precautions, medications=medications, my_diet=diet, workout=workout,selected_values)

if __name__ == '__main__':
    app.run(debug=True,port=8000)

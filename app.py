from flask import Flask, render_template, request
import pickle
import numpy as np

from sklearn.preprocessing import StandardScaler

application = Flask(__name__)
standard_to = StandardScaler()

# Assuming you have your features stored in a variable called feature_names
feature_names = ['Kilometers_Driven', 'Mileage', 'Engine', 'Power', 'Seats', 'Year',
                 'Fuel_Type_Diesel', 'Fuel_Type_Electric', 'Fuel_Type_LPG', 'Fuel_Type_Petrol',
                 'Transmission_Manual', 'Owner_Type_Fourth', 'Owner_Type_Second',
                 'Owner_Type_Third']

# Load the trained model
with open('random_forest_regression_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)
    model.feature_names = feature_names

@application.route('/', methods=['GET'])
def Home():
    return render_template('index.html')

@application.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        Year = int(request.form['Year'])
        Kilometers_Driven = int(request.form['Kilometers_Driven'])
        Mileage = float(request.form['Mileage'])
        Engine = float(request.form['Engine'])
        Power = float(request.form['Power'])
        Seats = int(request.form['Seats'])

        Fuel_Type_Diesel = 1 if request.form['Fuel_Type'] == 'Diesel' else 0
        Fuel_Type_Electric = 1 if request.form['Fuel_Type'] == 'Electric' else 0
        Fuel_Type_LPG = 1 if request.form['Fuel_Type'] == 'LPG' else 0
        Fuel_Type_Petrol = 1 if request.form['Fuel_Type'] == 'Petrol' else 0

        Owner_Type_Fourth= 1 if request.form['Owner_Type'] == 'Fourth' else 0
        Owner_Type_Second = 1 if request.form['Owner_Type'] == 'Second' else 0
        Owner_Type_Third = 1 if request.form['Owner_Type'] == 'Third' else 0

        Year = 2024 - Year
        
        # Check if Transmission_Manual field is in the form data
        if 'Transmission_Manual' in request.form:
            Transmission_Manual = 1 if request.form['Transmission_Manual'] == 'Manual' else 0
        else:
            # Default value if Transmission_Manual is not provided
            Transmission_Manual = 0

        prediction = model.predict([[Kilometers_Driven, Mileage, Engine, Power, Seats, Year,
                                     Fuel_Type_Diesel, Fuel_Type_Electric, Fuel_Type_LPG, Fuel_Type_Petrol,
                                     Transmission_Manual, Owner_Type_Fourth, Owner_Type_Second,
                                     Owner_Type_Third]])

        output = round(prediction[0], 2)
        if output <=0:
            return render_template('index.html', prediction_text="Sorry you cannot sell this car")
        else:
            return render_template('index.html', prediction_text="You Can Sell The Car at {} Lakhs".format(output))
    else:
        return render_template('index.html')

if __name__ == "__main__":
    application.run(debug=True)

from flask import Flask, render_template, request
import numpy as np
from sklearn.preprocessing import StandardScaler
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = " "
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]
header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}



app = Flask(__name__,template_folder="templates")
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    Fuel_Type_Diesel=0
    if request.method == 'POST':
        Year = int(request.form['Year'])
        Kms_Driven=int(request.form['Kms_Driven'])
        Kms_Driven2=np.log(Kms_Driven)
        Owner=int(request.form['Owner'])
        Fuel_Type_Petrol=request.form['Fuel_Type_Petrol']
        engine=int(request.form['engine'])
        if(Fuel_Type_Petrol=='Petrol'):
            Fuel_Type_Petrol=1
            Fuel_Type_Diesel=0
            Fuel_Type_LPG=0
        elif(Fuel_Type_Petrol=='Diesel'):
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=1
            Fuel_type_LPG=0
        elif(Fuel_Type_Petrol=='LPG'):
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=0
            Fuel_Type_LPG=1
        else:
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=0
            Fuel_Type_LPG=0
            
        Year=2020-Year
        Seller_Type_Individual=request.form['Seller_Type_Individual']
        if(Seller_Type_Individual=='Individual'):
            Seller_Type_Individual=1
            Seller_Type_Trustmark_Dealer=0
        elif(Seller_Type_Individual=='Seller_Type_Trustmark Dealer'):
            Seller_Type_Individual=0 
            Seller_Type_Trustmark_Dealer=1
        else:
            Seller_Type_Individual=0 
            Seller_Type_Trustmark_Dealer=0
            
        Transmission_Manual=request.form['Transmission_Manual']
        if(Transmission_Manual=='Manual'):
            Transmission_Manual=1
        else:
            Transmission_Manual=0
        feilds=[Kms_Driven,Owner,engine,Year,Fuel_Type_Diesel,Fuel_Type_LPG,Fuel_Type_Petrol,Seller_Type_Individual, Seller_Type_Trustmark_Dealer,Transmission_Manual]
        payload_scoring = {"input_data": [{"fields": [['Kms_driven', 'owner', 'engine', 'Years_old','Fuel_type_Diesel', 'Fuel_type_LPG', 'Fuel_type_Petrol','Seller_Type_Individual', 'Seller_Type_Trustmark Dealer','Transmission_Manual']], "values": [feilds]}]}
        response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/6be01e68-290f-4f45-a4fc-ec5e75238db9/predictions?version=2022-11-07', json=payload_scoring,headers={'Authorization': 'Bearer ' + mltoken})
        pred=response_scoring.json()
        out=pred['predictions'][0]['values'][0][0]
        if out<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="You Can Sell The Car at {}".format(out))
    else:
        return render_template('index.html')

if __name__=='__main__':
    app.run(debug=False)

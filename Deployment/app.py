# from crypt import methods
from flask import Flask, render_template, request
import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score

model = joblib.load('pipe_model.pkl')

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/predict', methods = ['POST', 'GET'])
def predict():
    gender = int(request.form['gender'])
    married = int(request.form['Married'])
    dependents = int(request.form['Dependents'])
    education = int(request.form['Education'])
    self_emp = int(request.form['emp'])
    applicant_income = int(request.form['applicant-income'])
    coapplicant_income = int(request.form['coapplicant-income'])
    loan_amount = int(request.form['loan-amount'])
    credit_history = int(request.form['credit'])
    loan_amount_term = int(request.form['loan-amount-term'])
    ppt = request.form['property']
    urban = 0
    semiurban = 0
    rural = 0
    total_income = applicant_income + coapplicant_income
    total_income = np.log(total_income)
    loan_amount = np.log(loan_amount)
    
    if ppt == 'Urban':
        urban = 1
    elif ppt == 'Semiurban':
        semiurban = 1
    else:
        rural = 1
    
    test = np.array([[gender, married, dependents, education, self_emp,loan_amount, loan_amount_term,
     credit_history, rural, urban, semiurban, total_income]])

    df = pd.DataFrame(test, columns=['Gender','Married','Dependents','Education',
    'Self_Employed','LoanAmount','Loan_Amount_Term','Credit_History',
    'Property_Rural','Property_Urban','Property_Semiurban','TotalIncome'])
    
    result = model.predict(df)
    return render_template('predict.html', data=result)

@app.route('/predict_csv_file', methods=['POST', 'GET'])
def predict_csv_file():
    file = request.form['file']
    X_test = pd.read_csv('~/Projects/Loan-Eligibility/Data/' + str(file), index_col=0)
    y_test = pd.read_csv('~/Projects/Loan-Eligibility/y_test.csv', index_col=0)
    
    pred = model.predict(X_test)
    result = accuracy_score(y_test, pred)
    print(result)

    return render_template('predict_csv_file.html', data1=result)

if __name__ == '__main__':
    app.run(debug = True)
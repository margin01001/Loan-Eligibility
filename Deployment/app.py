from flask import Flask, render_template, redirect, url_for
import pickle
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods = ['POST', 'GET'])
def predict():
    result = ""
    # pickle.loads()
    result = "yes"
    
    return redirect(url_for('result'))

#@app.route('/yes')
#def yes():

# @app.route('/no')
#def no():

if __name__ == '__main__':
    app.run(debug = True)
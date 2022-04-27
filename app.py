from flask import Flask, render_template, request
import os
import numpy as np
import pickle

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/'
result = ""

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in [ 'jpg', 'png']

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print(request.form)
        age = request.form['age']
        sex = request.form['sex']
        job = request.form['job']
        housing = request.form['housing']
        saving_account = request.form['saving_account']
        checking_amount = request.form['checking_amount']
        credit_amount = request.form['credit_amount']
        duration = request.form['duration']
        purpose = request.form['purpose']

        test_arr = np.array([age, sex, job, housing, saving_account, checking_amount, credit_amount, duration, purpose])
        model = pickle.load(open('german_credit.pkl', 'rb'))
        prediction = model.predict(test_arr)
        result = f"The model has predicted that the result is: {prediction}"

        return render_template('index.html', result=result)

    return render_template('index.html')
    
app.run(host='0.0.0.0', port=81)

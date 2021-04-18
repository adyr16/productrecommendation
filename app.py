from flask import Flask, render_template, request, redirect, url_for
from scipy import sparse
import pandas as pd
import numpy as np
import pickle
import warnings
warnings.filterwarnings("ignore")
import model as model

app = Flask(__name__)  # intitialize the flaks app  # common 

@app.route('/')
def home():
    return render_template('view.html')
    
@app.route("/recommendations", methods=['POST'])
def recommendations():
    if (request.method == 'POST'):
        user_id = request.form.get('user_id')
        print("USER ID is " + user_id)
        output = model.get_recommendations(user_id)
        return render_template('view.html', recommendation_text='{}'.format(output))
    else:
        return render_template('view.html')

if __name__ == '__main__' :
    app.run(debug=True )  # this command will enable the run of your flask app or api
    
    #,host="0.0.0.0")







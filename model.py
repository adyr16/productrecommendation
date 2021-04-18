from flask import Flask, render_template, request, redirect, url_for
from scipy import sparse
import pandas as pd
import numpy as np
import pickle
import warnings
warnings.filterwarnings("ignore")


app = Flask(__name__)  # intitialize the flaks app  # common 
model = pickle.load(open('pickle/lr_model.pkl', 'rb'))
user_rating = pickle.load(open('pickle/user_final_rating.pkl','rb'))
vectorizer = pickle.load(open('pickle/vectorizer.pkl','rb'))

file=pd.read_csv("dataset/sample30.csv")
data=pd.read_csv("dataset/corrdata.csv")
common_user_predicted_ratings = pd.read_csv("dataset/common_user_predicted_ratings.csv")
data = pd.read_csv("dataset/cleandata.csv")

def get_recommendations(user_id):
        common_user_predicted_ratings.set_index('reviews_username',inplace=True)
        top20 = pd.DataFrame(common_user_predicted_ratings.loc[user_id].sort_values(ascending=False)[0:20])
        top20.reset_index(inplace=True)
        top20.columns =['name','rating']
        top20_rev_df = pd.merge(top20,data,left_on='name',right_on='name', how = 'left')
        top20_rev_df = top20_rev_df[['name', 'review_all_text']]
        names = set(top20_rev_df.loc[:,"name"])
        print(names)
        top20reco_df = pd.DataFrame()
        print(top20_rev_df)

        for name in names:
                review = top20_rev_df[top20_rev_df["name"]==name]
                review_text = review['review_all_text']
                X_data = vectorizer.transform(review_text)
                y_pred = model.predict(X_data)
                df = pd.DataFrame(y_pred, columns = ['sentiment'])
                val = df['sentiment'].value_counts(normalize=True) * 100
                top20reco_df = top20reco_df.append({'product' : name,
                    'rating' : val.positive} , 
                     ignore_index=True)

        top20reco_df = top20reco_df.sort_values(by=['rating'], ascending=False)
        top20reco_df.reset_index(drop=True, inplace=True)
        products = top20reco_df.iloc[0:5]
        top5rec = products['product'].tolist()
        print(top5rec)
        return top5rec

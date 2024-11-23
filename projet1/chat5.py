import os
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split,cross_val_score,validation_curve,GridSearchCV,StratifiedKFold
from sklearn.metrics import accuracy_score
from flask import Flask, request,render_template,jsonify
from flask_cors import CORS
from datetime import datetime
import json
import random

detect_lan=""
conver=os.path.dirname(os.path.abspath(__file__))
data=open(conver + "/conver.json","r",encoding="utf-8").read()
data=json.loads(data)
x=np.array(data.get("x"))
y=np.array(data.get("y"))

   
model=make_pipeline(CountVectorizer(),MultinomialNB())

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.16,random_state=12)
x_train_av=x_train
y_train_av=y_train
model.fit(x_train,y_train)
score_model=model.score(x_test,y_test)

def chatbot(message):
    response=model.predict([message])
    return response[0]

def train_model(quest,resp):
    model1=make_pipeline(CountVectorizer(),MultinomialNB())
    data=open("conver.json","r",encoding="utf-8").read()
    data=json.loads(data)
    x=np.array(data.get("x"))
    y=np.array(data.get("y"))
    new_x=x.tolist()
    new_y=y.tolist()
    new_x.append(quest)
    new_y.append(resp)
    x=np.array(new_x)
    y=np.array(new_y)
    x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.16,random_state=12)
    model1.fit(x_train,y_train)
    score=model1.score(x_test,y_test)
    return score


chat5=Flask(__name__)
CORS(chat5)
@chat5.errorhandler(404)
def page_not_found(error):
    return 'This page does not exist', 404
@chat5.route('/')
def home():
    return render_template('index.html')

@chat5.route('/chat',methods=["POST"])
def chat():
    resp_robot="Vous pouvez continuer à me parler"
    qr_robot=["Ce quoi la bonne reponse","Ce quoi La reponse correct ?","C'était quoi la bonne reponse ?"]
    qr=["Je bien repondu ?\n<strong>Oui</strong> ou <strong>Non</strong>","La reponse est-elle correct ?\n<strong>Oui</strong> ou <strong>Non</strong>","C'était la bonne reponse ?\n<strong>Oui</strong> ou <strong>Non</strong>"]
    dem_robot="Veuillez d'abord à me repondre par oui ou non"
    att="Veuillez patienter"
    response=""
    operation=request.form["operation"]
    if operation=="request":
        user_input=request.form["message"]
        user_input_copy=request.form["message"]
        response=model.predict([user_input])
        response=response[0]
        qr=random.choice(qr)
        qr_robot=random.choice(qr_robot)
        all_response={
                    "response_trans":response ,
                    "qr":qr,
                    "resp":["Oui","Non"],
                    "resp_robot":resp_robot,
                    "qr_robot":qr_robot,
                    "dem_robot":dem_robot,
                    "dem_robot":dem_robot,
                    "att":att
                    
                }
        response=all_response
    elif operation=="add_données":
        user_name_value=request.form["user_name_value"].upper()
        question_user=request.form["question_user"]
        reponse_user=request.form["reponse_user"]
        add_données_valid=""
        
        file_script=os.path.dirname(os.path.abspath(__file__))
        dossier=os.path.join(file_script,"user",user_name_value)
        if not os.path.exists(dossier):
            os.makedirs(dossier)
        add_données=os.path.join(dossier,"add_données.json")
                
        if not os.path.exists(add_données):
            convert={
            "x":[question_user],
            "y":[reponse_user]
            }
            convert=json.dumps(convert,ensure_ascii=False)
            with open(add_données,"w",encoding="utf-8") as f:
                f.write(convert)
        else:
            f=open(add_données,"r",encoding="utf-8").read()
            convert=json.loads(f)
            q=convert.get("x")
            r=convert.get("y")
            l=len(q)
            i=0
            while i<l:
                if ((q[i].lower()==question_user.lower())&(r[i].lower()==reponse_user.lower())) :
                    add_données_valid=False
                    break
                i=i+1
            
            if add_données_valid!=False:
                q.append(question_user)
                r.append(reponse_user)
                convert={
                "x":q,
                "y":r
                }
                convert=json.dumps(convert,ensure_ascii=False)
                with open(add_données,"w",encoding="utf-8") as f:
                    f.write(convert)
            
        response="Les Données ont été enregistrer avec succès \n\n Vous pouvez continuer à me parler"
        all_response={
                    "response_trans":response ,
                    "qr":qr,
                    "resp":["Oui","Non"],
                    "resp_robot":resp_robot,
                    "qr_robot":qr_robot,
                    "dem_robot":dem_robot,
                    "dem_robot":dem_robot,
                    "att":att
                    
                }
        response=json.dumps(all_response,ensure_ascii=False)
    elif operation=="login":
        user_name_value=request.form["user_name_value"].upper()
        file_script=os.path.dirname(os.path.abspath(__file__))
        dossier=os.path.join(file_script,"user",user_name_value) 
        last_login=datetime.now()
        last_login=last_login.strftime("%Y-%m-%d %H:%M:%S")
        if not os.path.exists(dossier):
            os.makedirs(dossier)
        fichier_login=os.path.join(dossier,"Last_login.txt")
        with open(fichier_login,"w",encoding="utf-8") as f:
            f.write(last_login,)
        response="login"
    return response
if __name__=="__main__":
    chat5.run(host='0.0.0.0')
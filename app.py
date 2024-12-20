# -*- coding: utf-8 -*-
"""Disease_Prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-ThiQAdsy-Fqm_YKzmFPwloJ8HlvGYwq

**Importing necessory libraries**
"""

import numpy as np
import pandas as pd
import math

"""**Reading DataSet containing symptoms and diseases**"""

df=pd.read_csv("./data/dataset.csv")
df['Disease']=df['Disease'].str.strip()
df.head()

"""**Describing data to understand it**"""

df.describe()

# df.info()

"""**Reading symptom weights**"""

df2=pd.read_csv("./data/Symptom-severity.csv")
df2=df2.set_index('Symptom')
df2.head()

"""Reading Disease Precautions"""

precaution=pd.read_csv("./data/symptom_precaution.csv")
precaution['Disease']= precaution['Disease'].str.strip()
precaution=precaution.set_index('Disease')

precaution.head()

"""Reading Disease Description"""

description=pd.read_csv("./data/symptom_Description.csv")
description['Disease']= description['Disease'].str.strip()
description=description.set_index('Disease')
description.head()

"""Reading Disease Specialist"""
specialists=pd.read_csv("./data/symptom_Specialist.csv")
specialists['Disease']= specialists['Disease'].str.strip()
specialists=specialists.set_index('Disease')
specialists.head()


"""**Extracting unique symptoms**"""

columns=df[['Symptom_1', 'Symptom_2', 'Symptom_3', 'Symptom_4',
       'Symptom_5', 'Symptom_6', 'Symptom_7', 'Symptom_8', 'Symptom_9',
       'Symptom_10', 'Symptom_11', 'Symptom_12', 'Symptom_13', 'Symptom_14',
       'Symptom_15', 'Symptom_16', 'Symptom_17']].values.flatten()
columns=pd.unique(columns)
columns=[str(s).strip().replace(" ","_").replace("__","_") for s in columns]
columns.remove('nan')
columns

"""**Creating new DataFrame**
**Performing Data Pre Processing and data cleaning**
"""

adjusted_data=[]
for r in range(len(df)):
  ls=dict()
  ls["Disease"]=df.iloc[r]["Disease"]
  for s in df.iloc[r][1:]:
    s=str(s).strip().replace(" ","_").replace("__","_")
    if s=="nan":
      continue
    ls[s]=1
    if s in df2.index:
      if isinstance(df2.loc[s]['weight'],np.int64):
        ls[s]=int(df2.loc[s]['weight'])
  adjusted_data.append(ls.copy())

adjusted_data=pd.DataFrame.from_dict(adjusted_data)

diseases=adjusted_data["Disease"]
symptoms=adjusted_data.drop(["Disease"],axis=1)
symptoms=symptoms.fillna(0)

print(symptoms)
"""**Import Classifier model and metrics from sklearn library**"""

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score,confusion_matrix,f1_score,classification_report
import seaborn as sns
import matplotlib.pyplot as plt

"""**Splitting into training and testing data**"""

x_train,x_test,y_train,y_test=train_test_split(symptoms,diseases,test_size=0.1,random_state=42)
x_train

y_train

"""**Using Decision Tree Classifier, fitting the model to training data and predicting result for test data**"""

model=KNeighborsClassifier()
model.fit(symptoms,diseases)
y_pred=model.predict(x_test)
y_pred

"""**Checking accuracy of our model**"""

print(accuracy_score(y_pred,y_test))
print(classification_report(y_pred,y_test))
print(confusion_matrix(y_pred,y_test))
sns.heatmap(confusion_matrix(y_pred,y_test),xticklabels=df['Disease'].unique(),yticklabels=df['Disease'].unique())
# plt.show()







"""Creating python flask server

"""
u_diseases=pd.unique(diseases)
disease_details={}
for disease in u_diseases:
  pre=precaution.loc[disease]
  pre=pre.dropna()
  pre=pre.values.tolist()

  specialist=specialists.loc[disease].values.tolist()

  desc=description.loc[disease]
  desc=desc.values.tolist()

  sym=df[df['Disease']==disease].values.flatten()
  sym=pd.unique(sym)[1:].tolist()
  sym=list(filter(lambda x:isinstance(x,str),sym))
  
  obj={}
  obj['symptoms']=sym
  obj['disease']=disease
  obj['precautions']=pre
  obj['description']=desc
  obj['specialist']=specialist
  disease_details[disease]=obj



from flask import Flask,jsonify,request,Response,json
from flask_cors import CORS
app = Flask(__name__)
CORS(app)


@app.route("/")
def getSymptoms():
    return jsonify([columns,disease_details])

@app.route("/",methods=['POST'])
def predict():
  syms=json.loads(request.data)
  ndf=pd.DataFrame(index=[1],columns=columns)
  for s in syms:
    sym=str(s).strip().replace(" ","_").replace("__","_")
    ndf[sym]=10
    
    if sym in df2.index:
      if isinstance(df2.loc[sym]['weight'],np.int64):
        ndf[sym]=int(df2.loc[sym]['weight'])
  ndf=ndf.fillna(0)
  disease=model.predict(ndf)[0];
  print(disease)

  return jsonify(disease)

# app.run()


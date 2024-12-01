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

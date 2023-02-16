# import necessary libraries
import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

# load the model
RF=pickle.load(open('model.pkl','rb'))


def predict(data):
    # convert the data into a numpy array
    input_data = np.array([[data['feature1'], data['feature2'], ..., data['feature15']]])
    # scale the input data
    input_data = scaler.transform(input_data)
    # make a prediction
    prediction = model.predict(input_data)[0]
    return prediction

# create a Streamlit app
st.title('Lung Cancer Detection')

# add a header and a subheader
st.header('Input patient information')
st.subheader('Please enter the patient\'s risk factors')

# create a form for the patient's risk factors
GENDER = st.number_input('Risk factor 1', value=0)
AGE = st.number_input('Risk factor 1', value=0)
SMOKING = st.number_input('Risk factor 1', value=0)
YELLOW_FINGERS = st.number_input('Risk factor 1', value=0)
ANXIETY= st.number_input('Risk factor 1', value=0)
PEER_PRESSURE = st.number_input('Risk factor 1', value=0)
CHRONIC DISEASE = st.number_input('Risk factor 1', value=0)
FATIGUE = st.number_input('Risk factor 1', value=0)
ALLERGY = st.number_input('Risk factor 1', value=0)
WHEEZING = st.number_input('Risk factor 2', value=0)
ALCOHOL CONSUMING = st.number_input('Risk factor 15', value=0)
COUGHING = st.number_input('Risk factor 15', value=0)
SHORTNESS OF BREATH = st.number_input('Risk factor 15', value=0)
CHEST PAIN = st.number_input('Risk factor 15', value=0)
LUNG_CANCER = st.number_input('Risk factor 15', value=0)

# add a submit button
if st.button('Submit'):
    # get the patient's risk factors
    data = {
        'feature1': feature1,
        'feature2': feature2,
        ...
        'feature15': feature15
    }
    # make a prediction
    prediction = predict(data)
    # display the prediction
    if prediction == 0:
        st.write('The person is unlikely to have lung cancer.')
    else:
        st.write('The person is likely to have lung cancer.')

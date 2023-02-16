# Import necessary libraries
import pickle
import numpy as np
import streamlit as st

st.markdown("""
<body>
  <h1>Lung Cancer Prediction App</h1>
  <form>
    Age: <input type="number" name="age"><br><br>
    Gender:
    <input type="radio" name="gender" value="Male">Male
    <input type="radio" name="gender" value="Female">Female<br><br>
    Do you smoke?
    <input type="radio" name="smoking" value="Yes">Yes
    <input type="radio" name="smoking" value="No">No<br><br>
    Do you have persistent allergy?
    <input type="radio" name="allergy" value="Yes">Yes
    <input type="radio" name="allergy" value="No">No<br><br>
    Do you have persistent fatigue?
    <input type="radio" name="fatigue" value="Yes">Yes
    <input type="radio" name="fatigue" value="No">No<br><br>
    Do you have a persistent cough?
    <input type="radio" name="coughing" value="Yes">Yes
    <input type="radio" name="coughing" value="No">No<br><br>
    Do you consume alcohol?
    <input type="radio" name="alcohol" value="Yes">Yes
    <input type="radio" name="alcohol" value="No">No<br><br>
    Do you experience wheezing?
    <input type="radio" name="wheezing" value="Yes">Yes
    <input type="radio" name="wheezing" value="No">No<br><br>
    Do you experience shortness of breath?
    <input type="radio" name="breath" value="Yes">Yes
    <input type="radio" name="breath" value="No">No<br><br>
    Do you experience chest pain?
    <input type="radio" name="pain" value="Yes">Yes
    <input type="radio" name="pain" value="No">No<br><br>
    Do you experience difficulty swallowing?
    <input type="radio" name="swallowing" value="Yes">Yes
    <input type="radio" name="swallowing" value="No">No<br><br>
    Do you have any chronic disease?
    <input type="radio" name="disease" value="Yes">Yes
    <input type="radio" name="disease" value="No">No<br><br>
    Do you have yellow fingers or nails?
    <input type="radio" name="fingers" value="Yes">Yes
    <input type="radio" name="fingers" value="No">No<br><br>
    <input type="submit" value="Submit">
  </form>
</body>
""", unsafe_allow_html=True)

# Load the trained model
loaded_model = pickle.load(open("modelll.pkl", "rb"))

# Create a Streamlit app
def predict_app():
    st.title("Lung Cancer Prediction App")
   
    
       # Get the user inputs for the 13 features
    AGE = st.number_input("Age:", min_value=0,max_value=100)
    GENDER = st.radio("Gender:", ["Male", "Female"])
    SMOKING = st.radio("Do you smoke?", ["Yes", "No"])
    ALLERGY=st.radio("Do you have persistent allergy?",['Yes','No'])
    FATIGUE=st.radio("Do you have persistent fatigue?",['Yes','No'])
    COUGHING = st.radio("Do you have a persistent cough?", ["Yes", "No"])
    ALCOHOL_CONSUMING = st.radio("Do you consume alcohol?", ["Yes", "No"])
    WHEEZING = st.radio("Do you experience wheezing?", ["Yes", "No"])
    SHORTNESS_OF_BREATH = st.radio("Do you experience shortness of breath?", ["Yes", "No"])
    CHEST_PAIN = st.radio("Do you experience chest pain?", ["Yes", "No"])
    SWALLOWING_DIFFICULTY = st.radio("Do you experience difficulty swallowing?", ["Yes", "No"])
    CHRONIC_DISEASE = st.radio("Do you have any chronic disease?", ["Yes", "No"])
    YELLOW_FINGERS = st.radio("Do you have yellow fingers or nails?", ["Yes", "No"])
    #End the form
    
    
     # Preprocess the features
    features = [
        AGE,
        1 if GENDER == "Male" else 0,
        1 if SMOKING == "Yes" else 0,
        1 if ALLERGY== "Yes" else 0,
        1 if FATIGUE == "Yes" else 0,
        1 if COUGHING == "Yes" else 0,
        1 if ALCOHOL_CONSUMING == "Yes" else 0,
        1 if WHEEZING == "Yes" else 0,
        1 if SHORTNESS_OF_BREATH == "Yes" else 0,
        1 if CHEST_PAIN == "Yes" else 0,
        1 if SWALLOWING_DIFFICULTY == "Yes" else 0,
        1 if CHRONIC_DISEASE == "Yes" else 0,
        1 if YELLOW_FINGERS == "Yes" else 0
    ]
    
    # Make the prediction
    prediction = loaded_model.predict([features])[0]
    probability = loaded_model.predict_proba([features])[0][1]
    
    # Show the results
    if prediction == 0:
        st.write("You are unlikely to have lung cancer.")
    else:
        st.write("You are likely to have lung cancer.")
    st.write(f"Probability: {probability:.2f}")
    

# Run the Streamlit app
if __name__ == "__main__":
    predict_app()


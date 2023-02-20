# Import necessary libraries
import pickle
import streamlit as st
st.set_page_config()
st.markdown("""
<style>

  h1 {
    color: black;
    font-family: Arial, sans-serif;
    font-size: 36px;
    text-align: center;
    margin: 20px 0;
    font-family: Arial, sans-serif;
    backgorund-color:lightgray;

  }
 
 
  </style>
""", unsafe_allow_html=True)
# Load the trained model
loaded_model = pickle.load(open("modelll.pkl", "rb"))

# Create a Streamlit app
def predict_app():
    #st.title("Lung Cancer Prediction App")
    #Add the h1 heading
    st.markdown("<h1>Lung Cancer Prediction</h1>", unsafe_allow_html=True)
    
    
    
       # Get the user inputs for the 13 features
       
    AGE = st.number_input("Age:", min_value=0,max_value=100)
    GENDER = st.radio("Gender:", ["Male", "Female"])
    TOBACCO_SMOKING = st.radio("Do you smoke?", ["Yes", "No"])
    ALLERGY=st.radio("Do you have persistent allergy?",['Yes','No'],on_click=None)
    FATIGUE=st.radio("Do you have persistent fatigue?",['Yes','No'])
    COUGHING = st.radio("Do you have a persistent cough?", ["Yes", "No"])
    ALCOHOL_CONSUMING = st.radio("Do you consume alcohol?", ["Yes", "No"])
    WHEEZING = st.radio("Do you experience wheezing?", ["Yes", "No"])
    SHORTNESS_OF_BREATH = st.radio("Do you experience shortness of breath?", ["Yes", "No"])
    CHEST_PAIN = st.radio("Do you experience chest pain?", ["Yes", "No"])
    SWALLOWING_DIFFICULTY = st.radio("Do you experience difficulty swallowing?", ["Yes", "No"])
    CHRONIC_DISEASE = st.radio("Do you have any chronic disease?", ["Yes", "No"])
    YELLOW_FINGERS = st.radio("Do you have yellow fingers or nails?", ["Yes", "No"])
     
    
    # Preprocess the features
    features = [
        AGE,
        1 if GENDER == "Male" else 0,
        1 if TOBACCO_SMOKING == "Yes" else 0,
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
    #Add a prediction button
    if st.button("Predict"):
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




  





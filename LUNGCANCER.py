# Import necessary libraries
import pickle
import streamlit as st
st.set_page_config()
st.markdown("""<style>

    </style>

""", unsafe_allow_html=True)
# Load the trained model
loaded_model = pickle.load(open("modelll.pkl", "rb"))
def validate_inputs(AGE, GENDER, TOBACCO_SMOKING, ALLERGY, FATIGUE, COUGHING, ALCOHOL_CONSUMING, WHEEZING, SHORTNESS_OF_BREATH, CHEST_PAIN, SWALLOWING_DIFFICULTY, CHRONIC_DISEASE, YELLOW_FINGERS):
    if AGE is None or GENDER is None or TOBACCO_SMOKING is None or ALLERGY is None or FATIGUE is None or COUGHING is None or ALCOHOL_CONSUMING is None or WHEEZING is None or SHORTNESS_OF_BREATH is None or CHEST_PAIN is None or SWALLOWING_DIFFICULTY is None or CHRONIC_DISEASE is None or YELLOW_FINGERS is None:
        return False
    return True

# Create a Streamlit app
def predict_app():
    #st.title("Lung Cancer Prediction App")
    #Add the h1 heading
    st.markdown("<h1>Lung Cancer Prediction Tool</h1>", unsafe_allow_html=True)

    
    
       # Get the user inputs for the 13 features
       
    AGE = st.number_input("Age:", min_value=0,max_value=100)
    GENDER = st.radio("Gender:", ["Male", "Female",'Not_specified'],index=2)
    #conditional statement to print

    TOBACCO_SMOKING = st.radio("Do you smoke?", ["Yes", "No","Not_specified"],index=2)
    ALLERGY=st.radio("Do you have persistent allergy?",['Yes','No',"Not_specified"],index=2)
    FATIGUE=st.radio("Do you have persistent fatigue?",['Yes','No','Not_specified'],index=2)
    COUGHING = st.radio("Do you have a persistent cough?", ["Yes", "No",'Not_specified'],index=2)
    ALCOHOL_CONSUMING = st.radio("Do you consume alcohol?", ["Yes", "No",'Not_specified'],index=2)
    WHEEZING = st.radio("Do you experience wheezing?", ["Yes", "No",'Not_specified'],index=2)
    SHORTNESS_OF_BREATH = st.radio("Do you experience shortness of breath?", ["Yes", "No",'Not_specified'],index=2)
    CHEST_PAIN = st.radio("Do you experience chest pain?", ["Yes", "No",'Not_specified'],index=2)
    SWALLOWING_DIFFICULTY = st.radio("Do you experience difficulty swallowing?", ["Yes", "No",'Not_specified'],index=2)
    CHRONIC_DISEASE = st.radio("Do you have any chronic disease?", ["Yes", "No",'Not_specified'],index=2)
    YELLOW_FINGERS = st.radio("Do you have yellow fingers or nails?", ["Yes", "No",'Not_specified'],index=2)
    # Preprocess the features only if the user has selected an option
    #if GENDER is not None and TOBACCO_SMOKING is not None and ALLERGY is not None and FATIGUE is not None and COUGHING is not None and ALCOHOL_CONSUMING is not None and WHEEZING is not None and SHORTNESS_OF_BREATH is not None and CHEST_PAIN is not None and SWALLOWING_DIFFICULTY is not None and CHRONIC_DISEASE is not None and YELLOW_FINGERS is not None:
    #inputs = [AGE, GENDER, TOBACCO_SMOKING, ALLERGY, FATIGUE, COUGHING, ALCOHOL_CONSUMING, WHEEZING, SHORTNESS_OF_BREATH, CHEST_PAIN, SWALLOWING_DIFFICULTY, CHRONIC_DISEASE, YELLOW_FINGERS]

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
    def check_fields(AGE, GENDER, TOBACCO_SMOKING, ALLERGY, FATIGUE, COUGHING, ALCOHOL_CONSUMING, WHEEZING, SHORTNESS_OF_BREATH, CHEST_PAIN, SWALLOWING_DIFFICULTY, YELLOW_FINGERS):
        if not AGE:
           return False
        if not GENDER:
           return False
        if not TOBACCO_SMOKING:
           return False
        if ALLERGY is None:
           return False
        if FATIGUE is None:
           return False
        if COUGHING is None:
           return False
        if ALCOHOL_CONSUMING is None:
           return False
        if WHEEZING is None:
           return False
        if SHORTNESS_OF_BREATH is None:
           return False
        if CHEST_PAIN is None:
           return False
        if SWALLOWING_DIFFICULTY is None:
           return False
        if not YELLOW_FINGERS:
           return False
        return True
    if st.button('Predict'):
        # Check if all required fields have been filled
        if check_fields(AGE, GENDER, TOBACCO_SMOKING, ALLERGY, FATIGUE, COUGHING, ALCOHOL_CONSUMING, WHEEZING, SHORTNESS_OF_BREATH, CHEST_PAIN, SWALLOWING_DIFFICULTY, YELLOW_FINGERS):
        # Make prediction
            prediction =loaded_model.predict([features])[0]
            probability=loaded_model.predict_proba([features])[0][1]
            #show results
            if prediction==0:
                st.write("You are unlikely to have lung cancer.")
            else:
                st.write("You are likely to have lung cancer")
            st.write(f"probability:{probability:.2f}")
            st.write(prediction)
        else:
            st.warning('Please fill in all the required fields before making a prediction.')



     
        
        

    
#Run the Streamlit app
if __name__ == "__main__":
    predict_app()




  





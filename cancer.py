import pickle
import numpy as np
import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Simplified user credentials
USER_CREDENTIALS = {"user1": "password123"}  # Modify username and password here

# Initialize session state for login status
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Function to handle login
def login(username, password):
    if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
        st.session_state.logged_in = True
        st.session_state.username = username
    else:
        st.error("Invalid username or password.")

# Function for the login page
def login_page():
    st.title("Login")

    username_input = st.text_input("Username")
    password_input = st.text_input("Password", type="password")

    if st.button("Login"):
        login(username_input, password_input)

# Function for the home page (lung cancer prediction app)
def home_page():
    st.title(f"Welcome {st.session_state.username}!")
    
    # Load the trained model
    loaded_model = pickle.load(open("modelll.pkl", "rb"))

    # Lung cancer prediction function
    def predict_app():
        st.title("Lung Cancer Prediction App")

        # Get the user inputs for the 13 features
        AGE = st.number_input("Age:", min_value=0, max_value=100)
        GENDER = st.radio("Gender:", ["Male", "Female"])
        SMOKING = st.radio("Do you smoke?", ["Yes", "No"])
        ANXIETY = st.radio("Do you have anxiety?", ["Yes", "No"])
        ALLERGY = st.radio("Do you have persistent allergy?", ["Yes", "No"])
        FATIGUE = st.radio("Do you have persistent fatigue?", ["Yes", "No"])
        COUGHING = st.radio("Do you have a persistent cough?", ["Yes", "No"])
        ALCOHOL_CONSUMING = st.radio("Do you consume alcohol?", ["Yes", "No"])
        WHEEZING = st.radio("Do you experience wheezing?", ["Yes", "No"])
        SHORTNESS_OF_BREATH = st.radio("Do you experience shortness of breath?", ["Yes", "No"])
        CHEST_PAIN = st.radio("Do you experience chest pain?", ["Yes", "No"])
        SWALLOWING_DIFFICULTY = st.radio("Do you experience difficulty swallowing?", ["Yes", "No"])
        CHRONIC_DISEASE = st.radio("Do you have any chronic disease?", ["Yes", "No"])
        YELLOW_FINGERS = st.radio("Do you have yellow fingers or nails?", ["Yes", "No"])
        
        email = st.text_input("Enter your email to receive results:")

        # Preprocess the features
        features = [
            AGE,
            1 if GENDER == "Male" else 0,
            1 if SMOKING == "Yes" else 0,
            1 if ALLERGY == "Yes" else 0,
            1 if ANXIETY=='Yes' else 0,
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
        if st.button("Submit"):
            prediction = loaded_model.predict([features])[0]
            probability = loaded_model.predict_proba([features])[0][1]

            # Show the results
            if prediction == 0:
                result = "You are unlikely to have lung cancer."
            else:
                result = "You are likely to have lung cancer."

            st.write(result)
            st.write(f"Probability: {probability:.2f}")

            # Send the result via email
            if email:
                send_email(email, result, probability)

    def send_email(recipient, result, probability):
        sender_email = "your_email@example.com"
        sender_password = "your_email_password"

        subject = "Lung Cancer Prediction Result"
        body = f"Result: {result}\nProbability: {probability:.2f}"

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.example.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            text = msg.as_string()
            server.sendmail(sender_email, recipient, text)
            server.quit()
            st.success("Email sent successfully!")
        except Exception as e:
            st.error(f"Failed to send email: {e}")

    # Run the prediction app
    predict_app()

# Navigation logic
if not st.session_state.logged_in:
    login_page()
else:
    home_page()

# Import necessary libraries
import pickle
import numpy as np
import streamlit as st
import streamlit_authenticator as stauth
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Set up Streamlit Authenticator with hashed passwords
users = {
    "usernames": {
        "user1": {
            "name": "User One",
            "password": "$2b$12$KIXAsEDN4b1TtZOH1FOx6u/XI1GpPUu2.F5vOwSjdOFmfy6imwkmG"  # Pre-hashed password
        }
    }
}

authenticator = stauth.Authenticate(
    users,
    "my_app",
    "auth",
    cookie_expiry_days=30,
)

name, authentication_status, username = authenticator.login("Login", "main", "Submit")

if authentication_status:
    st.sidebar.title(f"Welcome {name}")
    authenticator.logout("Logout", "sidebar")

    # Load the trained model
    loaded_model = pickle.load(open("modelll.pkl", "rb"))

    # Create a Streamlit app
    def predict_app():
        st.title("Lung Cancer Prediction App")

        # Get the user inputs for the 13 features
        AGE = st.number_input("Age:", min_value=0, max_value=100)
        GENDER = st.radio("Gender:", ["Male", "Female"])
        SMOKING = st.radio("Do you smoke?", ["Yes", "No"])
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

    # Run the app
    if __name__ == "__main__":
        predict_app()

elif authentication_status == False:
    st.error("Username/password is incorrect")
elif authentication_status == None:
    st.warning("Please enter your username and password")

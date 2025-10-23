import streamlit as st
import requests

# Replace with your actual ngrok URL
API_BASE_URL = "https://unscabbed-unwarrantably-dyan.ngrok-free.dev"

st.set_page_config(page_title="Utility Assistant", layout="wide")

# Header Section
st.markdown("""
    <style>
    .main-title {
        font-size: 36px;
        font-weight: bold;
        color: #2c3e50;
        text-align: center;
    }
    .section-header {
        font-size: 24px;
        color: #34495e;
        margin-top: 30px;
    }
    .response-box {
        background-color: #ecf0f1;
        padding: 15px;
        border-radius: 10px;
        margin-top: 10px;
    }
    </style>
    <div class="main-title">🔌 Utility Self-Service Assistant</div>
""", unsafe_allow_html=True)

st.markdown("<div class='section-header'>Ask a Question</div>", unsafe_allow_html=True)
query = st.text_input("Enter your question:", placeholder="e.g. What is the late payment fee?")

if st.button("Submit Query", help="Send your question to the assistant"):
    if query:
        try:
            response = requests.post(f"{API_BASE_URL}/ask", json={"query": query})
            if response.status_code == 200:
                answer = response.json().get("answer", "No answer returned.")
                st.markdown(f"<div class='response-box'>{answer}</div>", unsafe_allow_html=True)
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Request failed: {e}")
    else:
        st.warning("Please enter a question before submitting.")

st.markdown("<div class='section-header'>Mock Transactions</div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📍 Report Outage"):
        payload = {"account_id": "1234567890", "location": "SW1A 1AA", "issue": "No power"}
        try:
            response = requests.post(f"{API_BASE_URL}/report_outage", json=payload)
            st.success(response.json().get("message", "Outage report submitted."))
        except Exception as e:
            st.error(f"Failed to report outage: {e}")

with col2:
    if st.button("🛠️ Book Appointment"):
        payload = {"account_id": "1234567890", "date": "2025-10-25", "reason": "Meter check"}
        try:
            response = requests.post(f"{API_BASE_URL}/book_appointment", json=payload)
            st.success(response.json().get("message", "Appointment booked."))
        except Exception as e:
            st.error(f"Failed to book appointment: {e}")

with col3:
    if st.button("🚚 Schedule Move-Out"):
        payload = {"account_id": "1234567890", "move_out_date": "2025-11-01"}
        try:
            response = requests.post(f"{API_BASE_URL}/move_out", json=payload)
            st.success(response.json().get("message", "Move-out scheduled."))
        except Exception as e:
            st.error(f"Failed to schedule move-out: {e}")
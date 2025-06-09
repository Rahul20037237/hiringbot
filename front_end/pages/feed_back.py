import streamlit as st

st.set_page_config(page_title="Feedback Form", layout="centered")
st.title("📝 Feedback Form")

# Optional User Info
name = st.text_input("Your Name (optional)")
email = st.text_input("Your Email (optional)")

# Feedback Type
feedback_type = st.selectbox("Type of Feedback", ["General", "Bug Report", "Feature Request", "Other"])

# Rating
rating = st.slider("Rate your experience (1 = Bad, 5 = Excellent)", 1, 5, 3)

# Comments
comments = st.text_area("Additional Comments")

# Submit Button
if st.button("Submit Feedback"):
    feedback_data = {
        "name": name,
        "email": email,
        "type": feedback_type,
        "rating": rating,
        "comments": comments
    }
    st.success("✅ Thank you for your feedback!")
    st.subheader("📦 Your Submitted Data")
    st.json(feedback_data)


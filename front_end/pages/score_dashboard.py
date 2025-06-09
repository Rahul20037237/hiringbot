import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="Interview Score Card",
    page_icon="📊",
    layout="centered"
)

st.markdown("""
<style>
.score-header {
    text-align: center;
    color: #2E86AB;
    margin-bottom: 2rem;
}
.score-card {
    background-color: #f8f9fa;
    padding: 2rem;
    border-radius: 15px;
    border: 2px solid #e9ecef;
    margin: 1rem 0;
}
.pass-result {
    background-color: #d4edda;
    color: #155724;
    padding: 1rem;
    border-radius: 10px;
    border-left: 5px solid #28a745;
    margin: 1rem 0;
}
.fail-result {
    background-color: #f8d7da;
    color: #721c24;
    padding: 1rem;
    border-radius: 10px;
    border-left: 5px solid #dc3545;
    margin: 1rem 0;
}
.feedback-box {
    background-color: #e3f2fd;
    padding: 1.5rem;
    border-radius: 10px;
    border-left: 5px solid #2196f3;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# Fallback defaults if direct access
if "name" not in st.session_state:
    st.session_state.name = "Guest"
if "candidate_name" not in st.session_state:
    st.session_state.candidate_name = st.session_state.name
if "total_questions" not in st.session_state:
    st.session_state.total_questions = 4
if "correct_answers" not in st.session_state:
    st.session_state.correct_answers = 3
if "score_data" not in st.session_state:
    st.session_state.score_data = {
        "score": round((st.session_state.correct_answers / st.session_state.total_questions) * 100),
        "result": "Pass" if (st.session_state.correct_answers / st.session_state.total_questions) >= 0.6 else "Fail",
        "feedback": "Thank you for completing the interview!"
    }
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = "N/A"

# Header
st.markdown("<h1 class='score-header'>📊 Interview Score Card</h1>", unsafe_allow_html=True)
st.markdown("---")

# Score Card Container
st.markdown("<div class='score-card'>", unsafe_allow_html=True)

# User Details Section
st.subheader("👤 Candidate Information")
col1, col2 = st.columns(2)
with col1:
    st.write(f"**Name:** {st.session_state.candidate_name}")
    st.write(
        f"**Session ID:** {st.session_state.conversation_id[:8] if st.session_state.conversation_id != 'N/A' else 'N/A'}...")
with col2:
    st.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d')}")
    st.write(f"**Time:** {datetime.now().strftime('%H:%M:%S')}")

st.markdown("---")

# Interview Performance Summary
st.subheader("📋 Interview Summary")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Questions",
        value=st.session_state.total_questions,
        help="Number of questions asked during the interview"
    )

with col2:
    st.metric(
        label="Responses Given",
        value=st.session_state.correct_answers,
        help="Number of satisfactory responses provided"
    )

with col3:
    st.metric(
        label="Score",
        value=f"{st.session_state.score_data['score']}%",
        delta=f"{st.session_state.score_data['score'] - 60}%" if st.session_state.score_data[
                                                                     'score'] >= 60 else f"{st.session_state.score_data['score'] - 60}%"
    )

with col4:
    pass_threshold = 60
    st.metric(
        label="Pass Threshold",
        value=f"{pass_threshold}%",
        help="Minimum score required to pass"
    )

st.markdown("---")

# Final Result Section
st.subheader("🎯 Interview Result")

# Display result with appropriate styling
if st.session_state.score_data['result'].lower() == 'pass':
    st.markdown(f"""
    <div class='pass-result'>
        <h3>🎉 Congratulations! You PASSED the interview!</h3>
        <p><strong>Final Score:</strong> {st.session_state.score_data['score']}/100</p>
    </div>
    """, unsafe_allow_html=True)
    st.balloons()
else:
    st.markdown(f"""
    <div class='fail-result'>
        <h3>📚 Interview Result: Did not meet the pass threshold</h3>
        <p><strong>Final Score:</strong> {st.session_state.score_data['score']}/100</p>
        <p>Don't worry! Consider this as a learning experience and try again.</p>
    </div>
    """, unsafe_allow_html=True)

# Performance Breakdown
st.subheader("📈 Performance Analysis")
score = st.session_state.score_data['score']

if score >= 90:
    performance_level = "Excellent"
    performance_color = "#28a745"
    performance_message = "Outstanding performance! You demonstrated exceptional skills and knowledge."
elif score >= 75:
    performance_level = "Good"
    performance_color = "#17a2b8"
    performance_message = "Good performance! You showed solid understanding and competence."
elif score >= 60:
    performance_level = "Satisfactory"
    performance_color = "#ffc107"
    performance_message = "Satisfactory performance. You met the basic requirements with room for improvement."
else:
    performance_level = "Needs Improvement"
    performance_color = "#dc3545"
    performance_message = "There's room for improvement. Consider strengthening your skills in the assessed areas."

st.markdown(f"""
<div style="background-color: {performance_color}20; padding: 1rem; border-radius: 10px; border-left: 5px solid {performance_color};">
    <h4 style="color: {performance_color}; margin: 0;">Performance Level: {performance_level}</h4>
    <p style="margin: 0.5rem 0 0 0;">{performance_message}</p>
</div>
""", unsafe_allow_html=True)

# Detailed Feedback
st.subheader("💬 Detailed Feedback")
st.markdown(f"""
<div class='feedback-box'>
    <p>{st.session_state.score_data['feedback']}</p>
</div>
""", unsafe_allow_html=True)

# Additional recommendations based on score
st.subheader("🎯 Recommendations")
if score >= 75:
    st.success("✅ You're well-prepared! Continue building on your strengths.")
elif score >= 60:
    st.info("💡 Consider reviewing technical concepts and practicing more coding problems.")
else:
    st.warning("📚 Focus on strengthening fundamental concepts and gaining more hands-on experience.")

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("---")

# Navigation buttons
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("🔄 New Interview", type="secondary"):
        # Clear relevant session state
        keys_to_clear = ['messages', 'current_stage', 'interview_complete', 'name_entered',
                         'candidate_name', 'score_prepared', 'conversation_id']
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
        try:
            st.switch_page("main.py")  # Adjust path as needed
        except Exception:
            st.rerun()

with col2:
    if st.button("📧 Email Results", type="secondary"):
        st.info("Email functionality would be implemented here. Results can be sent to HR or the candidate.")

with col3:
    if st.button("➡️ Next: Feedback", type="primary"):
        try:
            st.switch_page("pages/feed_back.py")  # Adjust the path to your feedback page
        except Exception as e:
            st.error(f"Navigation error: {str(e)}")
            st.info("Please check if the feed_back.py file exists in the pages folder.")

# Export functionality
st.markdown("---")
st.subheader("📄 Export Options")

col1, col2 = st.columns(2)

with col1:
    # Generate detailed report
    report_text = f"""
INTERVIEW SCORE REPORT
=====================

Candidate Information:
- Name: {st.session_state.candidate_name}
- Session ID: {st.session_state.conversation_id}
- Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Interview Summary:
- Total Questions: {st.session_state.total_questions}
- Satisfactory Responses: {st.session_state.correct_answers}
- Final Score: {st.session_state.score_data['score']}/100
- Result: {st.session_state.score_data['result']}
- Performance Level: {performance_level}

Feedback:
{st.session_state.score_data['feedback']}

Performance Analysis:
{performance_message}

Generated by AI Hiring Assistant
    """

    st.download_button(
        label="📄 Download Score Report",
        data=report_text,
        file_name=f"interview_score_{st.session_state.candidate_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
        mime="text/plain"
    )

with col2:
    # Generate CSV for HR systems
    csv_data = f"Name,Session_ID,Date,Total_Questions,Correct_Answers,Score,Result,Performance_Level\n"
    csv_data += f"{st.session_state.candidate_name},{st.session_state.conversation_id},{datetime.now().strftime('%Y-%m-%d')},{st.session_state.total_questions},{st.session_state.correct_answers},{st.session_state.score_data['score']},{st.session_state.score_data['result']},{performance_level}"

    st.download_button(
        label="📊 Download CSV Data",
        data=csv_data,
        file_name=f"interview_data_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )
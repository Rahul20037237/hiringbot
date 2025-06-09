import time

import streamlit as st
import asyncio
# Page Configuration
st.set_page_config(page_title="Hiring Agent", layout="centered")

# Custom CSS for aesthetics
with open(r"D:\WORKSPACE\pg_agi\front_end\css\main.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Main Content Box
with st.container():
    st.markdown('<div class="main">', unsafe_allow_html=True)

    st.markdown("<h1>Hiring Agent</h1>", unsafe_allow_html=True)

    st.markdown('''
    <div class="caption">
        This is developed by Rahul A — 
        <a href="https://www.linkedin.com/in/rahul-anandhan" target="_blank" style="text-decoration: none; color: #2980b9;">
            Click here
        </a>
    </div>
    ''', unsafe_allow_html=True)
    st.markdown("""
        <div class="description">
            <b>WELCOME TO TALENT SCOUT</b><br><br>
            Lorem Ipsum is simply dummy text of the printing and typesetting industry. 
            Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, 
            when an unknown printer took a galley of type and scrambled it to make a type specimen book. 
            It has survived not only five centuries, but also the leap into electronic typesetting, 
            remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset 
            sheets containing Lorem Ipsum passages, and more recently with desktop publishing software 
            like Aldus PageMaker including versions of Lorem Ipsum.
        </div>
    """, unsafe_allow_html=True)

    # Centered Start Button
    st.markdown('<div class="center">', unsafe_allow_html=True)
    if st.button("Start"):
        st.success("Let's begin the screening process!")
        time.sleep(2)
        st.switch_page(r'pages/exam_portal.py')
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

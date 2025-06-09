import streamlit as st
import uuid
from datetime import datetime
from back_end.bot import LangGraphHiringBot

@st.cache_resource
def get_bot():
    return LangGraphHiringBot()

def main():
    st.set_page_config(
        page_title="AI Hiring Bot",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # --- Initialize session state only if not already initialized ---
    if "conversation_id" not in st.session_state:
        st.session_state.conversation_id = str(uuid.uuid4())
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "current_stage" not in st.session_state:
        st.session_state.current_stage = "greeting"
    if "interview_complete" not in st.session_state:
        st.session_state.interview_complete = False
    if "candidate_name" not in st.session_state:
        st.session_state.candidate_name = ""
    if "name_entered" not in st.session_state:
        st.session_state.name_entered = False
    if "show_scorecard" not in st.session_state:
        st.session_state.show_scorecard = False
    if "reset_chat" not in st.session_state:
        st.session_state.reset_chat = False

    # --- CSS Styles (replace with your actual styles) ---
    st.markdown("""<style>
        /* Your CSS styles here */
        .main-header { font-size: 2em; text-align: center; }
        .welcome-message { padding: 1em; background-color: #f0f0f0; margin-bottom: 1em; }
        .user-message { background-color: #DCF8C6; padding: 0.5em; border-radius: 5px; margin-bottom: 0.5em; }
        .bot-message { background-color: #E6E6E6; padding: 0.5em; border-radius: 5px; margin-bottom: 0.5em; }
        .stage-indicator { font-weight: bold; margin-top: 1em; }
    </style>""", unsafe_allow_html=True)

    # --- Header ---
    st.markdown("<h1 class='main-header'>🤖 AI Hiring Assistant</h1>", unsafe_allow_html=True)

    # --- Handle Reset ---
    if st.session_state.get("reset_chat"):
        st.session_state.conversation_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.session_state.current_stage = "greeting"
        st.session_state.interview_complete = False
        st.session_state.candidate_name = ""
        st.session_state.name_entered = False
        st.session_state.reset_chat = False

    bot = get_bot()

    # --- Candidate Name Entry ---
    if not st.session_state.name_entered:
        st.markdown(
            "<div class='welcome-message'><h3>Welcome to the AI Hiring Interview!</h3><p>Please enter your full name to begin the interview process.</p></div>",
            unsafe_allow_html=True)

        with st.form(key="name_form"):
            candidate_name_input = st.text_input("Enter your full name:", placeholder="e.g., John Doe", key="name_input")
            submitted = st.form_submit_button("Start Interview 🚀", type="primary")
            if submitted:
                if candidate_name_input.strip():
                    st.session_state.candidate_name = candidate_name_input.strip()
                    st.session_state.name_entered = True

                    # Save candidate name as first message
                    st.session_state.messages.append({
                        "role": "user",
                        "content": st.session_state.candidate_name,
                        "timestamp": datetime.now().isoformat()
                    })

                    # Bot responds to name
                    try:
                        response = bot.process_message(st.session_state.candidate_name, st.session_state.conversation_id)
                        if not response or "response" not in response or "stage" not in response:
                            raise ValueError(f"Invalid response: {response}")
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": response["response"],
                            "stage": response["stage"],
                            "timestamp": datetime.now().isoformat()
                        })
                        st.session_state.current_stage = response["stage"]
                    except Exception as e:
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": f"Error: {str(e)}. Please try again later.",
                            "stage": "error",
                            "timestamp": datetime.now().isoformat()
                        })
                    st.experimental_rerun()
                else:
                    st.error("Please enter your name to continue.")
        return

    # --- Main Chat Interface ---
    # After name is entered, proceed with interview
    col1, col2 = st.columns([3, 1])

    with col1:
        st.subheader("Chat Interface")
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.messages:
                if message["role"] == "user":
                    st.markdown(f"""<div class="user-message"><strong>You:</strong> {message["content"]}</div>""",
                                unsafe_allow_html=True)
                else:
                    stage_display = message.get("stage", "").title()
                    if stage_display:
                        st.markdown(f"""<div class="stage-indicator">{stage_display}</div>""", unsafe_allow_html=True)
                    st.markdown(f"""<div class="bot-message"><strong>Bot:</strong> {message["content"]}</div>""",
                                unsafe_allow_html=True)

        if not st.session_state.interview_complete:
            with st.form(key="chat_form", clear_on_submit=True):
                user_input = st.text_input("Your message:", placeholder="Type your response here...", key="user_input")
                col_send, col_clear = st.columns([1, 1])
                with col_send:
                    send_button = st.form_submit_button("Send 📤", type="primary")
                with col_clear:
                    if st.form_submit_button("Clear Chat 🗑️"):
                        st.session_state.reset_chat = True
                        st.experimental_rerun()

            if send_button and user_input.strip():
                # Append user message
                st.session_state.messages.append({
                    "role": "user",
                    "content": user_input,
                    "timestamp": datetime.now().isoformat()
                })

                # Process bot response
                try:
                    response = bot.process_message(user_input, st.session_state.conversation_id)
                    if not response or "response" not in response or "stage" not in response:
                        raise ValueError("Invalid bot response")
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response["response"],
                        "stage": response["stage"],
                        "timestamp": datetime.now().isoformat()
                    })
                    st.session_state.current_stage = response["stage"]
                    if response["stage"] == "complete":
                        st.session_state.interview_complete = True
                except Exception as e:
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"Error: {str(e)}. Please try again later.",
                        "stage": "error",
                        "timestamp": datetime.now().isoformat()
                    })
                st.experimental_rerun()

        else:
            st.success("🎉 Interview Complete! Thank you for your time.")
            if st.button("➡️ View Interview Summary", type="primary"):
                st.session_state.show_scorecard = True
                st.experimental_rerun()

    # --- Scorecard or Summary ---
    if st.session_state.show_scorecard:
        # Implement your scorecard rendering here
        st.write("### Interview Summary (Placeholder)")
        # Add your scorecard display logic
        return

    # --- Sidebar ---
    with st.sidebar:
        # Sidebar logic (unchanged)...
        pass

if __name__ == "__main__":
    main()
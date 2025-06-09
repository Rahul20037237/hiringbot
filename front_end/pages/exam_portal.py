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

    # --- Safe Reset Check ---
    if st.session_state.get("reset_chat"):
        st.session_state.conversation_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.session_state.current_stage = "greeting"
        st.session_state.interview_complete = False
        st.session_state.candidate_name = ""
        st.session_state.name_entered = False
        st.session_state.reset_chat = False

    # --- Custom CSS ---
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        margin-bottom: 2rem;
    }
    .chat-container {
        max-height: 500px;
        overflow-y: auto;
        padding: 1rem;
        border: 1px solid #ddd;
        border-radius: 10px;
        background-color: #f8f9fa;
    }
    .user-message {
        background-color: #007bff;
        color: white;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        text-align: right;
    }
    .bot-message {
        background-color: #28a745;
        color: white;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        text-align: left;
    }
    .stage-indicator {
        background-color: #ffc107;
        color: black;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 12px;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 10px;
    }
    .welcome-message {
        background-color: #17a2b8;
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

    # --- Header ---
    st.markdown("<h1 class='main-header'>🤖 AI Hiring Assistant</h1>", unsafe_allow_html=True)

    # --- Session Initialization ---
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

    # --- Name Entry Screen ---
    if not st.session_state.name_entered:
        st.markdown(
            "<div class='welcome-message'><h3>Welcome to the AI Hiring Interview!</h3><p>Please enter your name to begin the interview process.</p></div>",
            unsafe_allow_html=True)

        with st.form(key="name_form"):
            candidate_name = st.text_input(
                "Enter your full name:",
                placeholder="e.g., John Doe",
                key="name_input"
            )

            if st.form_submit_button("Start Interview 🚀", type="primary"):
                if candidate_name.strip():
                    st.session_state.candidate_name = candidate_name.strip()
                    st.session_state.name_entered = True
                    # Add welcome message to chat
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"Hello {candidate_name}! Welcome to the AI Hiring Interview. I'm excited to learn more about you and your technical background. Let's begin!",
                        "stage": "greeting",
                        "timestamp": datetime.now().isoformat()
                    })
                    st.experimental_rerun()
                else:
                    st.error("Please enter your name to continue.")

        return

    # --- Sidebar ---
    with st.sidebar:
        st.header("Interview Progress")

        # Display candidate name
        if st.session_state.candidate_name:
            st.info(f"👤 **Candidate:** {st.session_state.candidate_name}")
            st.divider()

        stages = ["greeting", "info", "tech_stack", "hiring", "complete"]
        stage_names = ["Greeting", "Background Info", "Tech Stack", "Technical Questions", "Complete"]

        current_stage_index = stages.index(
            st.session_state.current_stage) if st.session_state.current_stage in stages else 0

        for i, (stage, name) in enumerate(zip(stages, stage_names)):
            if i <= current_stage_index:
                st.success(f"✅ {name}")
            else:
                st.info(f"⏳ {name}")

        st.divider()

        st.subheader("Session Info")
        st.write(f"**Session ID:** {st.session_state.conversation_id[:8]}...")
        st.write(f"**Messages:** {len(st.session_state.messages)}")
        st.write(f"**Current Stage:** {st.session_state.current_stage}")

        if st.button("🔄 Start New Interview", type="secondary"):
            st.session_state.reset_chat = True
            st.experimental_rerun()

    # --- Main Chat Interface ---
    col1, col2 = st.columns([3, 1])

    with col1:
        st.subheader("Chat Interface")

        chat_container = st.container()
        with chat_container:
            for message in st.session_state.messages:
                if message["role"] == "user":
                    st.markdown(f"""
                    <div class="user-message">
                        <strong>You:</strong> {message["content"]}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="stage-indicator">{message.get("stage", "").title()}</div>
                    <div class="bot-message">
                        <strong>Bot:</strong> {message["content"]}
                    </div>
                    """, unsafe_allow_html=True)

        if not st.session_state.interview_complete:
            with st.form(key="chat_form", clear_on_submit=True):
                user_input = st.text_input(
                    "Your message:",
                    placeholder="Type your response here...",
                    key="user_input"
                )
                col_send, col_clear = st.columns([1, 1])

                with col_send:
                    send_button = st.form_submit_button("Send 📤", type="primary")

                with col_clear:
                    if st.form_submit_button("Clear Chat 🗑️"):
                        st.session_state.reset_chat = True
                        st.experimental_rerun()

            if send_button and user_input.strip():
                st.session_state.messages.append({
                    "role": "user",
                    "content": user_input,
                    "timestamp": datetime.now().isoformat()
                })

                bot = get_bot()
                try:
                    response = bot.process_message(user_input, st.session_state.conversation_id)

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
                    st.error(f"Error processing message: {str(e)}")
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": "Sorry, I encountered an error. Please try again.",
                        "stage": "error",
                        "timestamp": datetime.now().isoformat()
                    })

                st.experimental_rerun()

        else:
            st.success("🎉 Interview Complete! Thank you for your time.")
            st.info("You can start a new interview using the sidebar button.")

            if st.button("➡️ Next: Score Card"):
                # Switch page to 'score_card' (filename without .py)
                st.switch_page("score_card")

    with col2:
        st.subheader("Tips")
        st.info("""
        **Interview Tips:**
        - Be honest and specific in your responses
        - Take your time to think through technical questions
        - Ask for clarification if needed
        - Show your problem-solving process
        """)

        if st.session_state.current_stage == "hiring":
            st.warning("""
            **Technical Round:**
            You're now in the technical interview phase. 
            Focus on demonstrating your coding knowledge and experience.
            """)

        st.subheader("Quick Actions")
        if st.button("💾 Export Chat", type="secondary"):
            chat_text = f"Interview Chat - {st.session_state.candidate_name}\n"
            chat_text += f"Session ID: {st.session_state.conversation_id}\n"
            chat_text += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            chat_text += "=" * 50 + "\n\n"
            chat_text += "\n".join([
                f"{msg['role'].title()}: {msg['content']}"
                for msg in st.session_state.messages
            ])
            st.download_button(
                label="Download Chat History",
                data=chat_text,
                file_name=f"interview_chat_{st.session_state.candidate_name.replace(' ', '_')}_{st.session_state.conversation_id[:8]}.txt",
                mime="text/plain"
            )


if __name__ == "__main__":
    main()

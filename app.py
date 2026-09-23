import streamlit as st

from agent import create_agent
from memory import (
    initialize_memory,
    add_message,
    get_messages,
    clear_memory,
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Study Tutor AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# CUSTOM CSS — MODERN AI / NEON BLUE THEME
# =========================================================

st.markdown(
    """
    <style>

    /* =====================================================
       GLOBAL
       ===================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(0, 180, 255, 0.12),
                transparent 28%
            ),
            radial-gradient(
                circle at 90% 20%,
                rgba(100, 60, 255, 0.10),
                transparent 30%
            ),
            linear-gradient(
                135deg,
                #050816 0%,
                #071225 50%,
                #030712 100%
            );

        color: #f4f8ff;
    }


    /* =====================================================
       REMOVE DEFAULT STREAMLIT SPACING
       ===================================================== */

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }


    /* =====================================================
       SIDEBAR
       ===================================================== */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #071426 0%,
                #040914 100%
            );

        border-right: 1px solid rgba(0, 200, 255, 0.20);
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #ffffff;
    }


    /* =====================================================
       HERO HEADER
       ===================================================== */

    .hero {
        padding: 28px 32px;
        border-radius: 24px;

        background:
            linear-gradient(
                135deg,
                rgba(7, 24, 48, 0.95),
                rgba(9, 20, 45, 0.88)
            );

        border: 1px solid rgba(0, 208, 255, 0.28);

        box-shadow:
            0 0 35px rgba(0, 174, 255, 0.10),
            inset 0 0 25px rgba(0, 174, 255, 0.03);

        margin-bottom: 24px;
    }

    .hero-title {
        font-size: clamp(2rem, 5vw, 3.4rem);
        font-weight: 800;
        line-height: 1.05;

        background:
            linear-gradient(
                90deg,
                #ffffff,
                #4ddcff,
                #7a8cff
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;

        margin-bottom: 10px;
    }

    .hero-subtitle {
        color: #9fb3cc;
        font-size: 1.05rem;
        line-height: 1.6;
        max-width: 800px;
    }


    /* =====================================================
       STATUS BADGE
       ===================================================== */

    .status {
        display: inline-flex;
        align-items: center;
        gap: 8px;

        padding: 7px 13px;

        border-radius: 999px;

        background: rgba(0, 217, 255, 0.08);

        border: 1px solid rgba(0, 217, 255, 0.25);

        color: #58e7ff;

        font-size: 0.82rem;
        font-weight: 600;

        margin-bottom: 15px;
    }

    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;

        background: #26e6ff;

        box-shadow:
            0 0 8px #26e6ff,
            0 0 16px rgba(38, 230, 255, 0.6);
    }


    /* =====================================================
       FEATURE CARDS
       ===================================================== */

    .feature-card {
        padding: 20px;

        min-height: 150px;

        border-radius: 18px;

        background:
            linear-gradient(
                145deg,
                rgba(12, 31, 57, 0.90),
                rgba(5, 14, 29, 0.95)
            );

        border: 1px solid rgba(80, 190, 255, 0.16);

        box-shadow:
            0 10px 35px rgba(0, 0, 0, 0.18);

        transition: all 0.2s ease;
    }

    .feature-icon {
        font-size: 1.8rem;
        margin-bottom: 10px;
    }

    .feature-title {
        font-size: 1rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 6px;
    }

    .feature-text {
        font-size: 0.84rem;
        line-height: 1.5;
        color: #8fa7c2;
    }


    /* =====================================================
       SECTION TITLES
       ===================================================== */

    .section-title {
        font-size: 1.15rem;
        font-weight: 700;

        color: #eaf8ff;

        margin-top: 24px;
        margin-bottom: 12px;
    }


    /* =====================================================
       CHAT AREA
       ===================================================== */

    [data-testid="stChatMessage"] {
        background: rgba(8, 22, 42, 0.55);

        border: 1px solid rgba(72, 181, 255, 0.10);

        border-radius: 18px;

        padding: 10px 14px;

        margin-bottom: 10px;
    }


    /* =====================================================
       CHAT INPUT
       ===================================================== */

    [data-testid="stChatInput"] {
        border: 1px solid rgba(0, 207, 255, 0.35);

        border-radius: 18px;

        background: rgba(5, 15, 30, 0.95);

        box-shadow:
            0 0 20px rgba(0, 187, 255, 0.08);
    }


    /* =====================================================
       BUTTONS
       ===================================================== */

    .stButton > button {
        border-radius: 12px;

        border: 1px solid rgba(0, 210, 255, 0.35);

        background:
            linear-gradient(
                135deg,
                #087ea4,
                #3159c9
            );

        color: white;

        font-weight: 700;

        transition: all 0.2s ease;

        box-shadow:
            0 0 15px rgba(0, 191, 255, 0.10);
    }

    .stButton > button:hover {
        border-color: #4deaff;

        box-shadow:
            0 0 20px rgba(0, 207, 255, 0.28);

        transform: translateY(-1px);
    }


    /* =====================================================
       SELECTBOXES
       ===================================================== */

    div[data-baseweb="select"] > div {
        background-color: rgba(5, 16, 31, 0.90);

        border-color: rgba(76, 189, 255, 0.25);

        border-radius: 10px;
    }


    /* =====================================================
       FILE UPLOADER
       ===================================================== */

    [data-testid="stFileUploader"] {
        background: rgba(5, 17, 32, 0.60);

        border: 1px dashed rgba(0, 204, 255, 0.30);

        border-radius: 16px;

        padding: 8px;
    }


    /* =====================================================
       DIVIDER
       ===================================================== */

    hr {
        border-color: rgba(84, 175, 255, 0.12);
    }


    /* =====================================================
       MOBILE RESPONSIVE
       ===================================================== */

    @media (max-width: 768px) {

        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .hero {
            padding: 22px;
            border-radius: 18px;
        }

        .hero-title {
            font-size: 2rem;
        }

        .hero-subtitle {
            font-size: 0.92rem;
        }

        .feature-card {
            min-height: auto;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# INITIALIZE MEMORY
# =========================================================

initialize_memory()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            padding: 10px 0 20px 0;
        ">
            <div style="
                font-size: 1.7rem;
                font-weight: 800;
                color: white;
            ">
                🧠 Study Tutor
            </div>

            <div style="
                color: #6edfff;
                font-size: 0.85rem;
                margin-top: 4px;
            ">
                AI Learning Assistant
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 🎓 Student Profile")

    student_level = st.selectbox(
        "Education Level",
        [
            "School",
            "College",
            "University",
        ],
    )

    difficulty = st.selectbox(
        "Learning Level",
        [
            "Beginner",
            "Intermediate",
            "Advanced",
        ],
    )

    st.markdown("### 📚 Study Mode")

    study_mode = st.selectbox(
        "Choose a mode",
        [
            "Explain",
            "Summary",
            "Quiz",
            "Practice",
            "Study Plan",
        ],
    )

    st.divider()

    st.markdown(
        """
        <div style="
            color: #8098b5;
            font-size: 0.78rem;
            line-height: 1.5;
        ">
            <b style="color:#b8eaff;">AI Tutor</b><br>
            Powered by Groq and GPT-OSS-120B.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True,
    ):

        clear_memory()

        st.rerun()


# =========================================================
# HERO
# =========================================================

st.markdown(
    """
    <div class="hero">

        <div class="status">
            <span class="status-dot"></span>
            AI TUTOR ONLINE
        </div>

        <div class="hero-title">
            Learn Smarter. Understand Faster.
        </div>

        <div class="hero-subtitle">
            Your personal AI study companion for explanations,
            summaries, quizzes, practice questions and study planning.
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# FEATURE CARDS
# =========================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">💡</div>
            <div class="feature-title">Explain</div>
            <div class="feature-text">
                Understand difficult concepts with
                simple step-by-step explanations.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


with col2:

    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">📝</div>
            <div class="feature-title">Summarize</div>
            <div class="feature-text">
                Turn long study material into
                concise learning notes.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


with col3:

    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">Practice</div>
            <div class="feature-text">
                Test your understanding with
                questions and feedback.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


with col4:

    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">🚀</div>
            <div class="feature-title">Study Plan</div>
            <div class="feature-text">
                Organize your learning with
                simple personalized study plans.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# CHAT SECTION
# =========================================================

st.markdown(
    '<div class="section-title">💬 Your Study Session</div>',
    unsafe_allow_html=True,
)


# =========================================================
# DISPLAY CHAT HISTORY
# =========================================================

for message in get_messages():

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# =========================================================
# CHAT INPUT
# =========================================================

user_input = st.chat_input(
    "Ask your Study Tutor anything..."
)


# =========================================================
# PROCESS QUESTION
# =========================================================

if user_input:

    # Add user message
    add_message(
        "user",
        user_input,
    )

    with st.chat_message("user"):

        st.markdown(
            user_input
        )

    enhanced_question = f"""
Student education level:
{student_level}

Learning difficulty:
{difficulty}

Study mode:
{study_mode}

Student question:
{user_input}
"""

    try:

        agent = create_agent()

        with st.chat_message("assistant"):

            with st.spinner(
                "🧠 Thinking..."
            ):

                conversation = get_messages()[:-1]

                answer = agent.chat(
                    [
                        *conversation,
                        {
                            "role": "user",
                            "content": enhanced_question,
                        },
                    ]
                )

            st.markdown(answer)

        add_message(
            "assistant",
            answer,
        )

    except Exception as e:

        st.error(
            f"⚠️ Something went wrong: {str(e)}"
        )

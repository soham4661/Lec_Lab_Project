import streamlit as st
from config import languages,levels
from gemini_client import get_client, extract_notes, make_flashcards, make_quiz
from helpers import grade_quiz, youtube_id, validate_quiz

Defaults = {
    "link": None,
    "notes": None,
    "cards": None,
    "card_pos": 0,
    "flipped": False,
    "quiz": None,
    "quiz_problems": [],
    "quiz_submitted": False,
    "log": [],
}

def init_state():
    for key, value in Defaults.items():
        if key not in st.session_state:
            if isinstance(value, list):
                st.session_state[key] = value.copy()
            else:
                st.session_state[key] = value


def reset_state():
    for key, value in Defaults.items():
        if isinstance(value, list):
            st.session_state[key] = value.copy()
        else:
            st.session_state[key] = value
    st.rerun()



def flip_card():
    st.session_state.flipped = not st.session_state.flipped 

def next_card():
    st.session_state.card_pos = st.session_state.card_pos + 1
    st.session_state.flipped = False

def retake_quiz():
    st.session_state.quiz_submitted = False
    for i in range(len(st.session_state.quiz)):
        st.session_state.pop(f"q_{i}", None)

            


st.set_page_config(
    page_title="Lecture Labs",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_state()
client = get_client()

# 2 Theme and styling of app

st.markdown(
    """
    <style>
    /* Global Page Styling & Dark Theme Background */
    .stApp {
        background-color: #0B1120 !important;
        color: #F8FAFC !important;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    
    /* Global Reset for Sidebar Background */
    section[data-testid="stSidebar"] {
        background-color: #0F172A !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    /* Modern Glassmorphic Card Styling */
    .dashboard-card {
        background: rgba(15, 23, 42, 0.65);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
    }

    .card-title {
        color: #F8FAFC;
        font-size: 1.15rem;
        font-weight: 600;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .card-subtitle {
        color: #94A3B8;
        font-size: 0.875rem;
        margin-bottom: 16px;
    }

    /* Streamlit Metric Card Customization */
    [data-testid="stMetric"] {
        background: rgba(15, 23, 42, 0.65);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 16px 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    [data-testid="stMetricLabel"] {
        color: #94A3B8 !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
    }

    [data-testid="stMetricValue"] {
        color: #22D3EE !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
    }

    /* Customized Gradient Primary Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 14px 0 rgba(59, 130, 246, 0.35) !important;
        width: 100%;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #2563EB 0%, #7C3AED 100%) !important;
        box-shadow: 0 6px 20px 0 rgba(139, 92, 246, 0.5) !important;
        transform: translateY(-2px);
    }

    .stButton > button:active {
        transform: translateY(0);
    }

    /* Customized Inputs, Selectboxes & Text Area */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div {
        background-color: #0F172A !important;
        color: #F8FAFC !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 10px !important;
        padding: 10px 14px !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #3B82F6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2) !important;
    }

        /* Customizing Sliders */
    div[data-baseweb="slider"] {
        padding-top: 10px;
    }

    /* 1. Value bubble above the handle: no box, white text */
    [data-testid="stSliderThumbValue"] {
        background: transparent !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }

    /* 2. Min and max labels under the track: no box */
    [data-testid="stSliderTickBarMin"],
    [data-testid="stSliderTickBarMax"] {
        background: transparent !important;
        color: #94A3B8 !important;
    }

    /* 3. Round handle: blue, matching the title */
    div[role="slider"] {
        background-color: #3B82F6 !important;
        border: 2px solid #FFFFFF !important;
        box-shadow: 0 0 10px rgba(59, 130, 246, 0.6) !important;
    }

    /* Custom Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(15, 23, 42, 0.8);
        padding: 6px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }

    .stTabs [data-baseweb="tab"] {
        height: 44px;
        border-radius: 8px;
        color: #94A3B8;
        font-weight: 500;
        padding: 0px 20px;
        background-color: transparent;
        border: none !important;
    }

    .stTabs [aria-selected="true"] {
        background-color: rgba(59, 130, 246, 0.15) !important;
        color: #22D3EE !important;
        font-weight: 600;
        border: 1px solid rgba(34, 211, 238, 0.3) !important;
    }
    
    /* Status Badge styling */
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
    .badge-cyan {
        background: rgba(34, 211, 238, 0.12);
        color: #22D3EE;
        border: 1px solid rgba(34, 211, 238, 0.3);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div style="padding: 10px 0 25px 0; text-align: left;">
        <h1 style="
            font-size: 3rem;
            font-weight: 900;
            letter-spacing: -1px;
            margin: 0;
            background: linear-gradient(135deg, #F8FAFC 20%, #3B82F6 60%, #8B5CF6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: inline-block;
        ">
            LECTURE LABS <span>🎓</span>
        </h1>
        <p style="
            color: #94A3B8;
            font-size: 1.1rem;
            font-weight: 400;
            margin-top: 6px;
            letter-spacing: 0.2px;
        ">
            Learn Smarter. Explore Better. Achieve More.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

#Functions for app

def show_input_screen(client, level, language):
    link = st.text_input("Paste a YouTube lecture link")
    if (st.button("Build Study Kit")):
        if client is None:
            st.error("API key missing. Add GEMINI_API_KEY to your .env file.")
            return

        video_id = youtube_id(link)
        if video_id is None:
            st.error("That doesn't look like a YouTube video link.")
            return

        clean_link = "https://www.youtube.com/watch?v=" + video_id
        st.session_state.link = clean_link

        with st.spinner("Watching the lecture..."):
            notes = extract_notes(client, clean_link, level, language, st.session_state.log)
            st.session_state.notes = notes

        st.rerun()

def show_flashcards_tab(client, count, language):
    cards = st.session_state.cards

    if cards is None:
        if st.button("Generate flashcards"):
            with st.spinner("Making flashcards..."):
                st.session_state.cards = make_flashcards(
                    client, st.session_state.notes, count, language, st.session_state.log
                )
            st.rerun()
        return

    card = cards[st.session_state.card_pos % len(cards)]
    number = st.session_state.card_pos % len(cards) + 1

    if st.session_state.flipped:
        label = "ANSWER"
        text = card["back"]
    else:
        label = "QUESTION"
        text = card["front"]

    st.caption(f"Card {number} of {len(cards)} · {label}")
    st.info(text)

    col1, col2 = st.columns(2)
    with col1:
        st.button("Flip", on_click=flip_card)
    with col2:
        st.button("Next", on_click=next_card)

def show_quiz_tab(client, count, language):
    quiz = st.session_state.quiz

    # 1. Generate part
    if quiz is None:
        if st.button("Generate quiz"):
            with st.spinner("Making quiz..."):
                questions = make_quiz(client, st.session_state.notes, count, language, st.session_state.log)
                good_questions, problems = validate_quiz(questions)
                st.session_state.quiz = good_questions
                st.session_state.quiz_problems = problems
            st.rerun()
        return

    # 2. Warning if some questions were dropped
    if st.session_state.quiz_problems:
        st.warning(f"{len(st.session_state.quiz_problems)} question(s) were dropped because they were broken.")

    # 3. The form
    with st.form("quiz_form"):
        for i, q in enumerate(quiz):
            st.radio(q["question"], q["options"], index=None, key=f"q_{i}")
        submitted = st.form_submit_button("Submit answers")

    # 4. On submit
    if submitted:
        st.session_state.quiz_submitted = True

    #5. Show results if submitted
    if st.session_state.quiz_submitted:
        answers = [st.session_state.get(f"q_{i}") for i in range(len(quiz))]
        score, results = grade_quiz(quiz, answers)

        for i, (q, result) in enumerate(zip(quiz, results),start =1):
            if result["is_correct"]:
                st.success(f"Q{i}: Correct")
            else:
                st.error(f"Q{i}: Wrong. Correct answer: {result['correct']}")
                st.info(q["explanation"])

        percent = round(score / len(quiz) * 100)
        st.metric("Score", f"{score} / {len(quiz)} · {percent}%")
        st.button("Retake quiz", on_click=retake_quiz)

    
#Main APP Code.
st.set_page_config(page_title="LectureLab", page_icon="🎓", layout="wide")
init_state()
client = get_client()

language = st.sidebar.selectbox("Language", languages)
level = st.sidebar.selectbox("Level", levels)
flashcard_count = st.sidebar.slider("Flashcards", 5, 20, 10)
quiz_count = st.sidebar.slider("Quiz questions", 3, 15, 5)
if st.sidebar.button("New video"):
    reset_state()

if st.session_state.notes is None:
    show_input_screen(client, level, language)
else:
    left, right = st.columns(2)

    with left:
        st.video(st.session_state.link)

    with right:
        st.header(st.session_state.notes["title"])
        st.write(st.session_state.notes["summary"])

    tab1, tab2, tab3 = st.tabs(["Flashcards", "Quiz", "Usage"])

    with tab1:
        show_flashcards_tab(client, flashcard_count, language)
    with tab2:
        st.write("Coming soon")
    with tab3:
        st.write("Coming soon")




    
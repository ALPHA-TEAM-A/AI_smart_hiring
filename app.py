import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import re
import shutil
import random
import hashlib
import tempfile
import os
import json
import auth
from pathlib import Path
from datetime import datetime


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Smart Hiring",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)
# ============================================================
# PROFESSIONAL UI / UX STYLING
# ============================================================

# ============================================================
# PROFESSIONAL UI / UX STYLING
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       MAIN APPLICATION
       ======================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(59, 130, 246, 0.10),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 20%,
                rgba(124, 58, 237, 0.10),
                transparent 30%
            ),
            #07101d;

        color: #f1f5ff;
    }


    /* ========================================================
       REMOVE DEFAULT WHITE HEADER
       ======================================================== */

    header[data-testid="stHeader"] {
        background: #07101d !important;
    }

    [data-testid="stToolbar"] {
        background: transparent !important;
    }


    /* ========================================================
       MAIN CONTENT TEXT
       ======================================================== */

    .stApp p,
    .stApp label,
    .stMarkdown,
    .stMarkdown p,
    .stMarkdown span {
        color: #e8edf8 !important;
    }

    h1,
    h2,
    h3,
    h4,
    h5,
    h6 {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    strong,
    b {
        color: #ffffff !important;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #111827 0%,
                #172554 55%,
                #1e1b4b 100%
            ) !important;

        border-right: 1px solid rgba(255,255,255,0.08);
    }

    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] div {
        color: #e8edf8 !important;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }

    section[data-testid="stSidebar"] .stCaption {
        color: #aebbd4 !important;
    }


    /* ========================================================
       SIDEBAR NAVIGATION BUTTONS
       ======================================================== */

    section[data-testid="stSidebar"] button {
        width: 100% !important;

        color: #e8edf8 !important;

        background: rgba(
            255,
            255,
            255,
            0.055
        ) !important;

        border: 1px solid rgba(
            255,
            255,
            255,
            0.14
        ) !important;

        border-radius: 12px !important;

        min-height: 42px !important;

        transition:
            background 0.2s ease,
            border 0.2s ease,
            transform 0.2s ease;
    }

    section[data-testid="stSidebar"] button:hover {
        background: rgba(
            99,
            102,
            241,
            0.22
        ) !important;

        border-color: rgba(
            129,
            140,
            248,
            0.55
        ) !important;

        transform: translateX(2px);
    }

    section[data-testid="stSidebar"] button p,
    section[data-testid="stSidebar"] button span {
        color: #e8edf8 !important;
        font-weight: 500 !important;
    }


    /* ========================================================
       SIDEBAR DIVIDERS
       ======================================================== */

    section[data-testid="stSidebar"] hr {
        border-color: rgba(
            255,
            255,
            255,
            0.12
        ) !important;
    }


    /* ========================================================
       METRIC CARDS
       ======================================================== */

    [data-testid="stMetric"] {
        background:
            linear-gradient(
                145deg,
                rgba(20, 36, 63, 0.90),
                rgba(11, 25, 45, 0.90)
            );

        border: 1px solid rgba(
            100,
            116,
            139,
            0.20
        );

        border-radius: 18px;

        padding: 20px;

        box-shadow:
            0 10px 30px rgba(
                0,
                0,
                0,
                0.18
            );
    }

    [data-testid="stMetricLabel"] {
        color: #aebbd4 !important;
    }

    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    [data-testid="stMetricDelta"] {
        color: #a7f3d0 !important;
    }


    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {
        background:
            linear-gradient(
                135deg,
                #4f46e5,
                #6366f1
            ) !important;

        color: #ffffff !important;

        border: none !important;

        border-radius: 12px !important;

        min-height: 44px !important;

        font-weight: 600 !important;

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);

        box-shadow:
            0 8px 24px rgba(
                79,
                70,
                229,
                0.30
            );
    }

    .stButton > button p,
    .stButton > button span {
        color: #ffffff !important;
    }


    /* ========================================================
       TEXT INPUT
       ======================================================== */

    .stTextInput input {
        color: #ffffff !important;

        background: #101a2e !important;

        border: 1px solid #344363 !important;

        border-radius: 10px !important;
    }

    .stTextInput input:focus {
        border-color: #6366f1 !important;

        box-shadow:
            0 0 0 1px #6366f1 !important;
    }

    .stTextInput input::placeholder {
        color: #8797b8 !important;
    }


    /* ========================================================
       TEXT AREA
       ======================================================== */

    .stTextArea textarea {
        color: #f5f7ff !important;

        background: #101a2e !important;

        border: 1px solid #344363 !important;

        border-radius: 10px !important;
    }

    .stTextArea textarea:focus {
        border-color: #6366f1 !important;

        box-shadow:
            0 0 0 1px #6366f1 !important;
    }

    .stTextArea textarea::placeholder {
        color: #8797b8 !important;
    }


    /* ========================================================
       SELECTBOX
       ======================================================== */

    div[data-baseweb="select"] > div {
        background: #101a2e !important;

        border-color: #344363 !important;

        color: #ffffff !important;

        border-radius: 10px !important;
    }

    div[data-baseweb="select"] span {
        color: #ffffff !important;
    }


    /* ========================================================
       FILE UPLOADER
       ======================================================== */

    [data-testid="stFileUploader"] {
        background:
            rgba(
                16,
                26,
                46,
                0.75
            ) !important;

        border: 1px dashed rgba(
            129,
            140,
            248,
            0.50
        ) !important;

        border-radius: 16px !important;

        padding: 10px !important;
    }

    [data-testid="stFileUploader"] label {
        color: #e8edf8 !important;
    }

    [data-testid="stFileUploader"] section {
        background: transparent !important;
    }


    /* ========================================================
       EXPANDERS
       ======================================================== */

    [data-testid="stExpander"] {
        background:
            rgba(
                18,
                29,
                50,
                0.85
            ) !important;

        border: 1px solid rgba(
            120,
            140,
            190,
            0.20
        ) !important;

        border-radius: 16px !important;
    }

    [data-testid="stExpander"] p,
    [data-testid="stExpander"] span {
        color: #e8edf8 !important;
    }

    [data-testid="stExpander"] strong {
        color: #ffffff !important;
    }


    /* ========================================================
       PLOTLY CHARTS
       ======================================================== */

    [data-testid="stPlotlyChart"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        border-radius: 16px !important;
    }

    /* ========================================================
       DATAFRAME
       ======================================================== */

    [data-testid="stDataFrame"] {
        border-radius: 14px !important;

        overflow: hidden !important;

        color: #ffffff !important;
    }


    /* ========================================================
       ALERTS
       ======================================================== */

    .stAlert {
        border-radius: 12px !important;
    }

    .stAlert p,
    .stAlert span {
        color: #edf2ff !important;
    }


    /* ========================================================
       SUCCESS / WARNING / INFO TEXT
       ======================================================== */

    [data-testid="stNotification"] p {
        color: #edf2ff !important;
    }


    /* ========================================================
       CAPTIONS
       ======================================================== */

    .stCaption {
        color: #aebbd4 !important;
    }


    /* ========================================================
       DIVIDERS
       ======================================================== */

    hr {
        border-color: rgba(
            255,
            255,
            255,
            0.08
        ) !important;
    }


    /* ========================================================
       TABS
       ======================================================== */

    button[data-baseweb="tab"] {
        color: #aebbd4 !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #ffffff !important;
    }


    /* ========================================================
       SCROLLBAR
       ======================================================== */

    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #07101d;
    }

    ::-webkit-scrollbar-thumb {
        background: #334155;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #475569;
    }


    /* ========================================================
       REMOVE EXCESS TOP SPACE
       ======================================================== */

    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
    }


    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
RESUME_DIR = BASE_DIR / "resumes"
RESUME_DIR.mkdir(exist_ok=True)

# Persistent application data.
# Streamlit session_state survives page reruns, but it is reset when the
# browser session/application is started again. This JSON snapshot keeps
# the hiring data available across logout/login and application restarts.
PERSISTENCE_FILE = BASE_DIR / "smart_hiring_data.json"

PERSISTENT_KEYS = [
    "candidates",
    "ats_db",
    "last_uploaded",
    "interview_questions",
    "interview_meta",
    "interview_answers",
    "interview_current",
    "interview_history",
    "interview_context_key",
    "interview_evaluations",
    "interview_session_active",
    "interview_mcq_score",
    "processed_resume_batch",
    "saved_job_description",
    "voice_question_index",
    "voice_history",
    "voice_last_audio_hash",
    "voice_session_active",
    "voice_completed",
    "voice_context_key",
    "candidate_applications",
]

def _json_safe(value):
    """Convert common session-state values into JSON-safe values."""
    if isinstance(value, dict):
        return {str(k): _json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(v) for v in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def save_persistent_data():
    """Save application data without touching login/session identity."""
    data = {key: _json_safe(st.session_state.get(key)) for key in PERSISTENT_KEYS}
    temp_file = PERSISTENCE_FILE.with_suffix(".tmp")
    try:
        temp_file.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        temp_file.replace(PERSISTENCE_FILE)
    except Exception:
        # Persistence must never break the hiring application.
        try:
            if temp_file.exists():
                temp_file.unlink()
        except Exception:
            pass


def load_persistent_data():
    """Restore the last saved hiring state when the app starts."""
    if not PERSISTENCE_FILE.exists():
        return
    try:
        data = json.loads(PERSISTENCE_FILE.read_text(encoding="utf-8"))
        for key in PERSISTENT_KEYS:
            if key in data:
                st.session_state[key] = data[key]
        # This value is normally a tuple during the current session.
        batch = st.session_state.get("processed_resume_batch")
        if isinstance(batch, list):
            st.session_state.processed_resume_batch = tuple(
                tuple(item) if isinstance(item, list) else item
                for item in batch
            )
    except Exception:
        # If an old/corrupt snapshot exists, start clean rather than
        # preventing the application from opening.
        return


# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "user_role" not in st.session_state:
    st.session_state.user_role = ""

if "auth_user" not in st.session_state:
    st.session_state.auth_user = None

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if "candidates" not in st.session_state:
    st.session_state.candidates = []

if "candidate_applications" not in st.session_state:
    st.session_state.candidate_applications = []

# Ensure previously loaded candidates always have a hiring status.
for _candidate in st.session_state.candidates:
    if not _candidate.get("status"):
        _candidate["status"] = "New"

if "last_uploaded" not in st.session_state:
    st.session_state.last_uploaded = ""

if "interview_questions" not in st.session_state:
    st.session_state.interview_questions = []

if "interview_meta" not in st.session_state:
    st.session_state.interview_meta = {}

if "interview_answers" not in st.session_state:
    st.session_state.interview_answers = {}

if "interview_current" not in st.session_state:
    st.session_state.interview_current = 0

if "interview_history" not in st.session_state:
    st.session_state.interview_history = []
if "interview_context_key" not in st.session_state:
    st.session_state.interview_context_key = ""
if "interview_evaluations" not in st.session_state:
    st.session_state.interview_evaluations = {}
if "interview_session_active" not in st.session_state:
    st.session_state.interview_session_active = False
if "interview_mcq_score" not in st.session_state:
    st.session_state.interview_mcq_score = None

if "ats_db" not in st.session_state:
    st.session_state.ats_db = []

if "processed_resume_batch" not in st.session_state:
    st.session_state.processed_resume_batch = None

if "saved_job_description" not in st.session_state:
    st.session_state.saved_job_description = ""

# Milestone 4 - voice screening state
if "voice_question_index" not in st.session_state:
    st.session_state.voice_question_index = 0
if "voice_history" not in st.session_state:
    st.session_state.voice_history = []
if "voice_last_audio_hash" not in st.session_state:
    st.session_state.voice_last_audio_hash = ""
if "voice_session_active" not in st.session_state:
    st.session_state.voice_session_active = False
if "voice_completed" not in st.session_state:
    st.session_state.voice_completed = False
if "voice_context_key" not in st.session_state:
    st.session_state.voice_context_key = ""

# Load once on the first run. On every later Streamlit rerun, save the
# previous in-memory data first. This also catches changes made immediately
# before st.rerun() calls (for example logout or interview actions).
if "_persistent_data_loaded" not in st.session_state:
    load_persistent_data()
    st.session_state._persistent_data_loaded = True
else:
    save_persistent_data()


# ============================================================
# SKILLS
# ============================================================

SKILLS = [
    "Python",
    "Java",
    "C++",
    "C#",
    "C",
    "JavaScript",
    "TypeScript",
    "R",
    "MATLAB",
    "HTML",
    "CSS",
    "React",
    "React.js",
    "Node.js",
    "Django",
    "Flask",
    "FastAPI",
    "Streamlit",
    "SQL",
    "MySQL",
    "PostgreSQL",
    "SQLite",
    "MongoDB",
    "Oracle",
    "AWS",
    "Azure",
    "GCP",
    "Docker",
    "Kubernetes",
    "Git",
    "GitHub",
    "Linux",
    "Machine Learning",
    "Deep Learning",
    "Artificial Intelligence",
    "AI",
    "NLP",
    "Natural Language Processing",
    "Data Science",
    "Data Analysis",
    "Pandas",
    "NumPy",
    "Scikit-learn",
    "TensorFlow",
    "PyTorch",
    "Keras",
    "OpenCV",
    "Power BI",
    "Tableau",
    "Excel",
    "DSA",
    "Data Structures",
    "Algorithms",
    "DBMS",
    "OOP",
    "Operating Systems",
    "Computer Networks",
    "REST API",
    "Tailwind CSS",
    "Next.js",
    "Express.js",
    "Spring Boot"
]


# ============================================================
# NAME FILTERING
# ============================================================

BLOCKED_NAME_WORDS = {
    "resume",
    "curriculum",
    "vitae",
    "cv",
    "career",
    "objective",
    "summary",
    "profile",
    "education",
    "skills",
    "experience",
    "projects",
    "project",
    "certifications",
    "certificates",
    "achievements",
    "contact",
    "internship",
    "internships",
    "technical",
    "professional",
    "declaration",
    "references",
    "phone",
    "email",
    "address",
    "linkedin",
    "github",
    "developer",
    "engineer",
    "student",
    "candidate"
}


# ============================================================
# RESUME FUNCTIONS
# ============================================================

def clear_old_resumes():

    if not RESUME_DIR.exists():
        RESUME_DIR.mkdir(exist_ok=True)
        return

    for item in RESUME_DIR.iterdir():

        try:

            if item.is_file():
                item.unlink()

            elif item.is_dir():
                shutil.rmtree(item)

        except Exception:
            pass


def save_resume(uploaded_file):

    file_path = RESUME_DIR / uploaded_file.name

    with open(file_path, "wb") as file:
        file.write(uploaded_file.getbuffer())

    return file_path


def extract_pdf(file_path):

    try:

        import pymupdf

        document = pymupdf.open(str(file_path))

        text = ""

        for page in document:
            text += page.get_text() + "\n"

        document.close()

        return text

    except Exception:

        try:

            import fitz

            document = fitz.open(str(file_path))

            text = ""

            for page in document:
                text += page.get_text() + "\n"

            document.close()

            return text

        except Exception as error:

            return "ERROR: " + str(error)


def extract_docx(file_path):

    try:

        from docx import Document

        document = Document(str(file_path))

        text = []

        for paragraph in document.paragraphs:

            if paragraph.text.strip():
                text.append(paragraph.text.strip())

        for table in document.tables:

            for row in table.rows:

                for cell in row.cells:

                    if cell.text.strip():
                        text.append(cell.text.strip())

        return "\n".join(text)

    except Exception as error:

        return "ERROR: " + str(error)


def extract_txt(file_path):

    try:

        return file_path.read_text(
            encoding="utf-8",
            errors="ignore"
        )

    except Exception as error:

        return "ERROR: " + str(error)


def extract_resume_text(file_path):

    extension = file_path.suffix.lower()

    if extension == ".pdf":
        return extract_pdf(file_path)

    if extension == ".docx":
        return extract_docx(file_path)

    if extension == ".txt":
        return extract_txt(file_path)

    return ""


def clean_text(text):

    text = text.replace("\x00", " ")

    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    return text.strip()


# ============================================================
# NAME EXTRACTION
# ============================================================

def valid_name(name):

    name = name.strip()

    name = re.sub(
        r"[^A-Za-z.\-'\s]",
        "",
        name
    )

    name = re.sub(
        r"\s+",
        " ",
        name
    ).strip()

    if not name:
        return False

    words = name.split()

    if len(words) < 2 or len(words) > 5:
        return False

    for word in words:

        if len(word) < 2:
            return False

        if len(word) > 25:
            return False

    lower_words = {
        word.lower().strip(".")
        for word in words
    }

    if lower_words.intersection(BLOCKED_NAME_WORDS):
        return False

    return True


def extract_name(text):

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    first_lines = lines[:20]

    # --------------------------------------------------------
    # 1. Explicit "Name:" field
    # --------------------------------------------------------

    for line in first_lines:

        match = re.match(
            r"^(?:name|candidate name|full name)\s*[:\-]\s*(.+)$",
            line,
            re.IGNORECASE
        )

        if match:

            name = match.group(1).strip()

            if valid_name(name):
                return name.title()


    # --------------------------------------------------------
    # 2. Look for a name close to the email address
    # --------------------------------------------------------

    email_index = None

    for index, line in enumerate(lines[:30]):

        if re.search(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            line
        ):

            email_index = index
            break

    if email_index is not None:

        start = max(
            0,
            email_index - 8
        )

        nearby_lines = lines[start:email_index]

        for line in reversed(nearby_lines):

            if valid_name(line):

                return line.title()


    # --------------------------------------------------------
    # 3. Use spaCy PERSON detection if available
    # --------------------------------------------------------

    try:

        import spacy

        nlp = spacy.load("en_core_web_sm")

        sample_text = "\n".join(
            first_lines[:15]
        )

        doc = nlp(sample_text)

        for entity in doc.ents:

            if entity.label_ == "PERSON":

                possible_name = entity.text.strip()

                if valid_name(possible_name):

                    return possible_name.title()

    except Exception:
        pass


    # --------------------------------------------------------
    # 4. Detect uppercase names
    # --------------------------------------------------------

    for line in first_lines:

        cleaned = re.sub(
            r"[^A-Za-z.\-'\s]",
            "",
            line
        ).strip()

        if (
            cleaned
            and cleaned.upper() == cleaned
            and valid_name(cleaned)
        ):

            return cleaned.title()


    # --------------------------------------------------------
    # 5. Detect normal capitalized names
    # --------------------------------------------------------

    for line in first_lines:

        cleaned = re.sub(
            r"[^A-Za-z.\-'\s]",
            "",
            line
        ).strip()

        if not valid_name(cleaned):
            continue

        words = cleaned.split()

        capitalized_count = 0

        for word in words:

            if word and word[0].isupper():
                capitalized_count += 1

        if capitalized_count >= 2:

            return cleaned


    # --------------------------------------------------------
    # 6. Last fallback: derive a readable name from email
    # --------------------------------------------------------

    email_match = re.search(
        r"([A-Za-z]+)[._-]?([A-Za-z]+)\d*@",
        text
    )

    if email_match:

        first = email_match.group(1)
        second = email_match.group(2)

        possible_name = (
            first + " " + second
        ).strip()

        if len(possible_name.split()) >= 2:

            return possible_name.title()


    return "Unknown Candidate"


# ============================================================
# CONTACT EXTRACTION
# ============================================================

def extract_email(text):

    match = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    if match:
        return match.group(0)

    return "Not found"


def extract_phone(text):

    patterns = [
        r"\+91[\s\-]?[6-9]\d{9}",
        r"\b[6-9]\d{9}\b",
        r"\+?\d[\d\s\-]{9,14}\d"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text
        )

        if match:
            return match.group(0).strip()

    return "Not found"


# ============================================================
# SKILL EXTRACTION
# ============================================================

def extract_skills(text):

    text_lower = text.lower()

    found = []

    for skill in SKILLS:

        pattern = (
            r"(?<![a-zA-Z0-9])"
            + re.escape(skill.lower())
            + r"(?![a-zA-Z0-9])"
        )

        if re.search(pattern, text_lower):

            if skill not in found:
                found.append(skill)

    return found


# ============================================================
# SECTION EXTRACTION
# ============================================================

SECTION_ALIASES = {

    "Education": [
        "education",
        "academic background",
        "educational qualifications"
    ],

    "Experience": [
        "experience",
        "work experience",
        "professional experience",
        "internship",
        "internships"
    ],

    "Projects": [
        "projects",
        "academic projects",
        "personal projects"
    ],

    "Certifications": [
        "certifications",
        "certificates",
        "certification"
    ]
}


def extract_section(text, section_name):

    lines = text.splitlines()

    aliases = SECTION_ALIASES.get(
        section_name,
        []
    )

    start = None

    for index, line in enumerate(lines):

        normalized = line.strip().lower()

        for alias in aliases:

            if (
                normalized == alias
                or normalized.startswith(alias + ":")
            ):

                start = index + 1
                break

        if start is not None:
            break

    if start is None:
        return "Not detected"


    all_sections = []

    for values in SECTION_ALIASES.values():
        all_sections.extend(values)


    result = []

    for line in lines[start:]:

        normalized = line.strip().lower()

        if normalized in all_sections:
            break

        if line.strip():
            result.append(line.strip())

        if len(result) >= 12:
            break

    if result:
        return "\n".join(result)

    return "Not detected"


# ============================================================
# ATS SCORE
# ============================================================

ACTION_WORDS = [
    "developed",
    "created",
    "implemented",
    "designed",
    "built",
    "optimized",
    "analyzed",
    "managed",
    "led",
    "improved",
    "automated",
    "engineered",
    "deployed",
    "tested"
]


def calculate_ats_score(
    text,
    name,
    email,
    phone,
    skills
):

    score = 0

    text_lower = text.lower()

    # Contact information
    if name != "Unknown Candidate":
        score += 3

    if email != "Not found":
        score += 7

    if phone != "Not found":
        score += 5

    # Skills
    score += min(
        len(skills) * 2.5,
        25
    )

    # Resume structure
    sections = [
        "education",
        "experience",
        "projects",
        "skills",
        "certification"
    ]

    for section in sections:

        if section in text_lower:
            score += 4

    # Action words
    action_count = 0

    for word in ACTION_WORDS:

        if word in text_lower:
            action_count += 1

    score += min(
        action_count * 1.5,
        15
    )

    # Content length
    word_count = len(text.split())

    if word_count >= 400:
        score += 15

    elif word_count >= 250:
        score += 11

    elif word_count >= 150:
        score += 8

    else:
        score += 4

    # Keyword richness
    score += min(
        len(set(skills)),
        10
    )

    return round(
        min(score, 100),
        1
    )


# ============================================================
# JOB MATCHING
# ============================================================

def normalize_skill(skill):

    return (
        skill.lower()
        .replace(".js", "")
        .strip()
    )


def calculate_match(
    candidate_skills,
    job_description
):

    job_lower = job_description.lower()

    required = []

    for skill in SKILLS:

        if skill.lower() in job_lower:

            if normalize_skill(skill) not in [
                normalize_skill(x)
                for x in required
            ]:

                required.append(skill)

    if not required:
        return 0, [], []

    candidate_skills_normalized = {
        normalize_skill(skill)
        for skill in candidate_skills
    }

    matched = []
    missing = []

    for skill in required:

        if normalize_skill(skill) in candidate_skills_normalized:
            matched.append(skill)

        else:
            missing.append(skill)

    score = (
        len(matched)
        / len(required)
    ) * 100

    return (
        round(score, 1),
        matched,
        missing
    )


# ============================================================
# CANDIDATE STORAGE
# ============================================================

def add_candidate(candidate):

    email = candidate.get(
        "email",
        "Not found"
    )

    for existing in st.session_state.candidates:

        if (
            email != "Not found"
            and existing.get("email") == email
        ):

            existing.update(candidate)

            return

    candidate["id"] = (
        len(st.session_state.candidates) + 1
    )

    candidate["created_at"] = (
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )

    st.session_state.candidates.append(
        candidate
    )


# ============================================================
# ============================================================
# LOGIN PAGE
# ============================================================

def login_page():
    # Role-based authentication only.
    # The rest of the application remains unchanged.
    st.title("🤖 AI Smart Hiring")
    st.caption("Intelligent Hiring Platform")
    st.divider()

    left, center, right = st.columns([1, 2, 1])

    with center:
        st.header("🔐 Welcome Back")
        st.caption("Choose your account type to continue.")

        role_labels = {
            "👨‍💼 Recruiter": "recruiter",
            "👤 Candidate / User": "user",
            "🛡️ Administrator": "admin",
        }

        selected_label = st.radio(
            "Login as",
            list(role_labels.keys()),
            horizontal=True,
            key="login_role_selector",
        )
        selected_role = role_labels[selected_label]

        with st.form("role_login_form", clear_on_submit=False):
            username = st.text_input(
                "Username / Email",
                placeholder="Enter username or email",
                key="login_username",
            )
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter password",
                key="login_password",
            )

            submitted = st.form_submit_button(
                "🔐 Sign In",
                use_container_width=True,
            )

        if submitted:
            if not username.strip():
                st.error("Please enter your username or email.")
            elif not password.strip():
                st.error("Please enter your password.")
            else:
                user = auth.login_user(
                    username.strip(),
                    password,
                    selected_role,
                )

                if user:
                    # Keep the existing session variables used by the app.
                    st.session_state.logged_in = True
                    st.session_state.username = user["username"]
                    st.session_state.user_role = user["role"]
                    st.session_state.auth_user = user
                    st.session_state.user = user
                    st.session_state.page = (
                        "Admin Portal" if user["role"] == "admin"
                        else "Candidate Portal" if user["role"] == "user"
                        else "Dashboard"
                    )
                    st.rerun()
                else:
                    st.error(
                        f"Invalid {selected_role} login. "
                        "Check the username, password, and selected account type."
                    )

        with st.expander("ℹ️ Demo Login Accounts"):
            st.markdown(
                """
                **Administrator**  
                Username: `admin`  
                Password: `Admin@123`

                **Recruiter**  
                Username: `recruiter`  
                Password: `Recruiter@123`

                **Candidate / User**  
                Username: `user`  
                Password: `User@123`
                """
            )

        st.caption(
            "New Candidate and Recruiter accounts can be created through the "
            "authentication system. Administrator accounts are restricted."
        )


# ============================================================
# ROLE-SPECIFIC PORTALS
# ============================================================

def candidate_portal():
    """Candidate-facing application portal. Recruiter pages remain unchanged."""
    st.title("👤 Candidate Portal")
    st.caption("Apply for opportunities, track your application, and follow your interview progress.")

    username = st.session_state.get("username", "Candidate")
    auth_user = st.session_state.get("auth_user") or {}
    account_email = str(auth_user.get("email", "")).strip().lower()
    applications = st.session_state.get("candidate_applications", [])
    candidates = st.session_state.get("candidates", [])

    my_apps = [
        a for a in applications
        if str(a.get("username", "")).strip().lower() == username.strip().lower()
        or (account_email and str(a.get("email", "")).strip().lower() == account_email)
    ]

    # Keep compatibility with an already-created recruiter candidate record.
    mine = None
    for item in candidates:
        email = str(item.get("email", "")).strip().lower()
        if account_email and email == account_email:
            mine = item
            break
        if not mine and str(item.get("applicant_username", "")).strip().lower() == username.strip().lower():
            mine = item
            break

    # ------------------------------------------------------------
    # Candidate summary cards
    # ------------------------------------------------------------
    latest = my_apps[-1] if my_apps else None
    if mine:
        status = mine.get("status", "Applied")
        match = float(mine.get("match_score", 0) or 0)
        ats = float(mine.get("ats_score", 0) or 0)
        interview_done = bool(mine.get("interview_completed"))
    elif latest:
        status = latest.get("status", "Applied")
        match = float(latest.get("match_score", 0) or 0)
        ats = float(latest.get("ats_score", 0) or 0)
        interview_done = bool(latest.get("interview_completed"))
    else:
        status, match, ats, interview_done = "Not Applied", 0, 0, False

    st.markdown(f"### Welcome, {username} 👋")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Application Status", status)
    c2.metric("Job Match", f"{match:.1f}%" if match else "—")
    c3.metric("ATS Score", f"{ats:.1f}%" if ats else "—")
    c4.metric("Interview", "Completed" if interview_done else "Pending")

    st.divider()

    tab_apply, tab_application, tab_progress = st.tabs([
        "📝 Apply for a Job",
        "📄 My Application",
        "📈 Application Progress",
    ])

    # ------------------------------------------------------------
    # Candidate's own application process
    # ------------------------------------------------------------
    with tab_apply:
        st.subheader("📝 Submit a Job Application")
        st.caption("This application area is available only to candidates. Recruiter hiring tools remain separate.")

        with st.form("candidate_application_form", clear_on_submit=False):
            a1, a2 = st.columns(2)
            with a1:
                full_name = st.text_input("Full Name *", value=(mine or {}).get("name", username))
                email = st.text_input("Email *", value=(mine or {}).get("email", account_email))
                phone = st.text_input("Phone Number", value=(mine or {}).get("phone", ""))
                position = st.text_input("Position Applying For *", value=(mine or {}).get("job_applied", ""), placeholder="e.g. Data Scientist")
            with a2:
                education = st.text_input("Highest Education", value=(mine or {}).get("education", ""), placeholder="e.g. B.Tech CSE")
                experience = st.text_input("Experience", value=(mine or {}).get("experience", ""), placeholder="e.g. Fresher / 1 year")
                skills_text = st.text_input("Skills", value=", ".join((mine or {}).get("skills", [])) if isinstance((mine or {}).get("skills", []), list) else str((mine or {}).get("skills", "")), placeholder="Python, SQL, AWS")
                resume_file = st.file_uploader("Resume (PDF / DOCX / TXT)", type=["pdf", "docx", "txt"], key="candidate_resume_upload")

            cover_note = st.text_area("Short Introduction / Cover Note", placeholder="Briefly tell the recruiter why you are suitable for this role.")
            submitted = st.form_submit_button("🚀 Submit Application", use_container_width=True)

        if submitted:
            if not full_name.strip() or not email.strip() or not position.strip():
                st.error("Please fill in Full Name, Email, and Position Applying For.")
            else:
                resume_path = ""
                resume_text = ""
                parsed_skills = [x.strip() for x in skills_text.split(",") if x.strip()]

                if resume_file is not None:
                    safe_user = re.sub(r"[^A-Za-z0-9_-]+", "_", username).strip("_") or "candidate"
                    suffix = Path(resume_file.name).suffix.lower()
                    filename = f"candidate_{safe_user}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{suffix}"
                    resume_path_obj = RESUME_DIR / filename
                    resume_path_obj.write_bytes(resume_file.getbuffer())
                    resume_path = str(resume_path_obj)
                    resume_text = extract_resume_text(resume_path_obj)
                    if resume_text and not parsed_skills:
                        parsed_skills = extract_skills(resume_text)

                application = {
                    "application_id": f"APP-{datetime.now().strftime('%Y%m%d%H%M%S')}-{len(applications)+1:03d}",
                    "username": username,
                    "email": email.strip().lower(),
                    "name": full_name.strip(),
                    "phone": phone.strip(),
                    "job_applied": position.strip(),
                    "education": education.strip(),
                    "experience": experience.strip(),
                    "skills": parsed_skills,
                    "cover_note": cover_note.strip(),
                    "resume_path": resume_path,
                    "status": "Applied",
                    "match_score": 0,
                    "ats_score": 0,
                    "interview_completed": False,
                    "submitted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "source": "candidate_portal",
                }

                # Update an existing application for the same candidate + role,
                # otherwise create a new application. Existing recruiter data is untouched.
                existing = next(
                    (a for a in applications
                     if str(a.get("username", "")).lower() == username.lower()
                     and str(a.get("job_applied", "")).strip().lower() == position.strip().lower()),
                    None
                )
                if existing:
                    existing.update(application)
                else:
                    applications.append(application)

                # Also make the application visible to the existing recruiter workflow.
                candidate_record = dict(application)
                candidate_record["applicant_username"] = username
                add_candidate(candidate_record)
                st.session_state.candidate_applications = applications
                save_persistent_data()
                st.success("Application submitted successfully. You can track it from My Application and Application Progress.")
                st.rerun()

    # ------------------------------------------------------------
    # Candidate's own application details
    # ------------------------------------------------------------
    with tab_application:
        st.subheader("📄 My Application")
        if latest:
            left, right = st.columns([1.1, 0.9])
            with left:
                st.write(f"**Application ID:** {latest.get('application_id', 'Not available')}")
                st.write(f"**Position:** {latest.get('job_applied', 'Not assigned')}")
                st.write(f"**Submitted:** {latest.get('submitted_at', 'Not available')}")
                st.write(f"**Education:** {latest.get('education', 'Not provided')}")
                st.write(f"**Experience:** {latest.get('experience', 'Not provided')}")
                st.write(f"**Email:** {latest.get('email', account_email or 'Not available')}")
                st.write(f"**Phone:** {latest.get('phone', 'Not provided')}")
                st.subheader("🧠 Skills")
                skills = latest.get("skills", [])
                st.write(" • ".join(str(x) for x in skills) if skills else "Skills not provided.")
                if latest.get("cover_note"):
                    st.subheader("💬 Cover Note")
                    st.info(latest.get("cover_note"))
            with right:
                st.subheader("Current Status")
                current_status = str(latest.get("status", "Applied"))
                if current_status.lower() == "selected":
                    st.success("🎉 Selected")
                elif current_status.lower() == "rejected":
                    st.error("Application Rejected")
                elif "interview" in current_status.lower():
                    st.warning("🎤 Interview Stage")
                else:
                    st.info(f"📌 {current_status}")
                st.metric("Match Score", f"{float(latest.get('match_score', 0) or 0):.1f}%" if latest.get('match_score') else "—")
                st.metric("ATS Score", f"{float(latest.get('ats_score', 0) or 0):.1f}%" if latest.get('ats_score') else "—")
        else:
            st.info("You have not submitted an application yet. Use 'Apply for a Job' to begin.")

    # ------------------------------------------------------------
    # Candidate progress / interview status
    # ------------------------------------------------------------
    with tab_progress:
        st.subheader("📈 Application Progress")
        if latest:
            current = str(latest.get("status", "Applied")).lower()
            interview_done = bool(latest.get("interview_completed"))
            stages = [
                ("Application Submitted", True),
                ("Recruiter Review", current not in {"applied", "new"}),
                ("Interview", interview_done or "interview" in current or current == "selected"),
                ("Final Decision", current in {"selected", "rejected"}),
            ]
            for label, done in stages:
                st.write(("✅ " if done else "◻️ ") + label)

            if current == "selected":
                st.success("🎉 Congratulations! Your application has been selected.")
            elif current == "rejected":
                st.warning("Your application has been marked as rejected.")
            else:
                st.info("Your application is currently under review.")
        else:
            st.info("Application progress will appear here after you submit an application.")

    st.divider()
    st.caption("Candidate access is focused on applying for opportunities and tracking your own hiring progress. Recruiter operations and administrative controls remain restricted to their respective roles.")

def admin_portal():
    """Administrator-only platform oversight dashboard."""
    st.title("🛡️ Administrator Dashboard")
    st.caption("Platform governance, account oversight, system health and recruitment monitoring.")

    try:
        users = auth.get_all_users()
    except Exception:
        users = []

    candidates = st.session_state.get("candidates", [])
    applications = st.session_state.get("candidate_applications", [])
    ats_records = st.session_state.get("ats_db", [])

    admin_count = sum(1 for u in users if u.get("role") == "admin")
    recruiter_count = sum(1 for u in users if u.get("role") == "recruiter")
    candidate_count = sum(1 for u in users if u.get("role") == "user")
    selected_count = sum(1 for c in candidates if str(c.get("status", "")).lower() == "selected")
    interview_count = sum(1 for c in candidates if c.get("interview_completed"))
    pending_apps = sum(1 for a in applications if str(a.get("status", "Applied")).lower() in {"applied", "new", "screening"})

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Accounts", len(users))
    c2.metric("Recruiters", recruiter_count)
    c3.metric("Candidates", candidate_count)
    c4.metric("Applications", len(applications))

    st.divider()
    h1, h2, h3, h4 = st.columns(4)
    h1.metric("Pending Applications", pending_apps)
    h2.metric("Candidate Records", len(candidates))
    h3.metric("Interviews Completed", interview_count)
    h4.metric("Selected Candidates", selected_count)

    tab_overview, tab_accounts, tab_applications, tab_health = st.tabs([
        "📊 Platform Overview",
        "👥 Account Management",
        "📋 Application Oversight",
        "⚙️ System Health",
    ])

    with tab_overview:
        st.subheader("📊 Recruitment Platform Overview")
        if candidates:
            status_counts = {}
            for c in candidates:
                status = c.get("status", "New")
                status_counts[status] = status_counts.get(status, 0) + 1
            fig = px.bar(
                x=list(status_counts.keys()),
                y=list(status_counts.values()),
                labels={"x": "Candidate Status", "y": "Candidates"},
                title="Candidate Pipeline by Status",
            )
            st.plotly_chart(style_chart(fig, 340), use_container_width=True)
        else:
            st.info("Candidate pipeline data will appear here as applications are processed.")

        left, right = st.columns(2)
        with left:
            st.subheader("🔐 Role Distribution")
            role_rows = [
                {"Role": "Administrator", "Accounts": admin_count},
                {"Role": "Recruiter", "Accounts": recruiter_count},
                {"Role": "Candidate", "Accounts": candidate_count},
            ]
            st.dataframe(role_rows, use_container_width=True, hide_index=True)
        with right:
            st.subheader("⭐ Hiring Snapshot")
            st.write(f"**ATS Records:** {len(ats_records)}")
            st.write(f"**Selected Candidates:** {selected_count}")
            st.write(f"**Completed Interviews:** {interview_count}")
            st.write(f"**Pending Applications:** {pending_apps}")

    with tab_accounts:
        st.subheader("👥 Registered Accounts")
        if users:
            rows = []
            for u in users:
                role = u.get("role", "user")
                role_label = {
                    "admin": "🛡️ Administrator",
                    "recruiter": "👨‍💼 Recruiter",
                    "user": "👤 Candidate / User",
                }.get(role, role.title())
                rows.append({
                    "Username": u.get("username", ""),
                    "Email": u.get("email", ""),
                    "Role": role_label,
                    "Created": u.get("created_at", ""),
                })
            st.dataframe(rows, use_container_width=True, hide_index=True)
        else:
            st.info("No registered accounts found.")
        st.caption("Account creation and authentication remain controlled by the authentication layer. This dashboard provides administrator-level visibility without exposing recruiter tools.")

    with tab_applications:
        st.subheader("📋 Application Oversight")
        if applications:
            rows = []
            for a in applications:
                rows.append({
                    "Application ID": a.get("application_id", ""),
                    "Candidate": a.get("name", "Unknown"),
                    "Position": a.get("job_applied", "Not assigned"),
                    "Status": a.get("status", "Applied"),
                    "Submitted": a.get("submitted_at", ""),
                })
            st.dataframe(rows, use_container_width=True, hide_index=True)
        else:
            st.info("No candidate applications have been submitted yet.")

        st.subheader("🕒 Recent Candidate Activity")
        if candidates:
            recent = []
            for c in candidates[-8:][::-1]:
                recent.append({
                    "Candidate": c.get("name", "Unknown Candidate"),
                    "Job": c.get("job_applied") or "Not assigned",
                    "Match": f"{float(c.get('match_score', 0) or 0):.1f}%",
                    "ATS": f"{float(c.get('ats_score', 0) or 0):.1f}%",
                    "Status": c.get("status", "New"),
                })
            st.dataframe(recent, use_container_width=True, hide_index=True)
        else:
            st.info("No candidate activity is available yet.")

    with tab_health:
        st.subheader("⚙️ Platform Health")
        st.success("Authentication service: Active")
        st.success("Persistent application data: Active")
        st.success("Recruiter workflow: Active")
        st.success("Candidate application portal: Active")
        st.success("ATS integration: Active")
        st.success("Voice screening module: Available")
        st.info("Administrator access is limited to platform monitoring and oversight. Recruiter pages are not exposed in this role.")


# ============================================================
# SIDEBAR
# ============================================================

def create_sidebar():

    with st.sidebar:

        st.title("🤖 AI Smart Hiring")

        st.caption(
            "Intelligent Hiring Platform"
        )

        st.divider()

        st.write("SIGNED IN AS")

        role_display = {
            "admin": "🛡️ Administrator",
            "recruiter": "👨‍💼 Recruiter",
            "user": "👤 Candidate / User",
        }.get(st.session_state.get("user_role", ""), "👤 User")

        st.write(
            "👤 " + st.session_state.username
        )
        st.caption(role_display)

        st.divider()

        current_role = st.session_state.get("user_role", "")

        if current_role == "recruiter":
            pages = [
                "🏠 Dashboard",
                "📄 Resume Analyzer",
                "🎯 Job Matching",
                "👥 Candidates",
                "📊 Analytics",
                "💬 Interview Assistant"
            ]
        elif current_role == "admin":
            pages = [
                "🛡️ Admin Portal"
            ]
        else:
            pages = [
                "👤 Candidate Portal"
            ]

        for page in pages:

            clean_page = page[2:]

            if st.button(
                page,
                use_container_width=True,
                key="nav_" + clean_page
            ):

                st.session_state.page = (
                    clean_page
                )

                st.rerun()

        st.divider()

        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):

            save_persistent_data()
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.user_role = ""
            st.session_state.auth_user = None
            st.session_state.user = None
            st.session_state.page = "Dashboard"

            st.rerun()



# ============================================================
# CHART STYLING
# ============================================================

def style_chart(chart, height=380):
    chart.update_layout(
        template="none",
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            color="#e8edf8",
            family="Arial"
        ),
        title=dict(
            font=dict(
                color="#ffffff",
                size=20
            ),
            x=0.02
        ),
        legend=dict(
            font=dict(color="#dbe5f5"),
            bgcolor="rgba(0,0,0,0)",
            borderwidth=0
        ),
        margin=dict(
            l=30,
            r=20,
            t=60,
            b=40
        ),
        xaxis=dict(
            color="#cbd5e1",
            title_font=dict(color="#e8edf8"),
            tickfont=dict(color="#cbd5e1"),
            gridcolor="rgba(148,163,184,0.08)",
            zerolinecolor="rgba(148,163,184,0.12)",
            linecolor="rgba(148,163,184,0.18)"
        ),
        yaxis=dict(
            color="#cbd5e1",
            title_font=dict(color="#e8edf8"),
            tickfont=dict(color="#cbd5e1"),
            gridcolor="rgba(148,163,184,0.08)",
            zerolinecolor="rgba(148,163,184,0.12)",
            linecolor="rgba(148,163,184,0.18)"
        ),
        hoverlabel=dict(
            bgcolor="#111827",
            font_color="#ffffff"
        )
    )
    return chart


# ============================================================
# MILESTONE 4 - VOICE SCREENING
# ============================================================

VOICE_SCREENING_QUESTIONS = {
    "Senior ML Engineer": [
        ("Please introduce yourself and briefly describe your machine learning experience.", ["machine learning", "python", "model", "experience"]),
        ("How would you monitor a machine learning model after deploying it to production?", ["monitor", "drift", "production", "model"]),
        ("Describe a machine learning project where you improved model performance.", ["model", "accuracy", "feature", "optimization", "performance"]),
    ],
    "Data Scientist": [
        ("Please introduce yourself and describe your data science experience.", ["data", "python", "analysis", "experience"]),
        ("How would you handle missing values and outliers in a dataset?", ["missing", "outlier", "median", "mean", "imputation"]),
        ("How do you select evaluation metrics for a classification problem?", ["precision", "recall", "f1", "accuracy", "metric"]),
    ],
    "Machine Learning Engineer": [
        ("Tell me about your experience building and deploying machine learning models.", ["machine learning", "deploy", "model", "python"]),
        ("What steps would you take to detect model drift in production?", ["drift", "monitor", "production", "data"]),
        ("How would you optimize an ML pipeline for reliable inference?", ["pipeline", "latency", "optimization", "inference"]),
    ],
    "Python Developer": [
        ("Please introduce yourself and explain your Python development experience.", ["python", "development", "project", "experience"]),
        ("How do you handle exceptions and errors in a Python application?", ["exception", "try", "except", "error", "logging"]),
        ("How would you improve the performance of a Python application?", ["profiling", "optimization", "algorithm", "cache", "performance"]),
    ],
    "Software Developer": [
        ("Tell me about a software project you developed and your contribution to it.", ["software", "project", "development", "testing"]),
        ("How do you approach debugging a production issue?", ["debug", "logs", "reproduce", "testing", "issue"]),
        ("How do you ensure code quality in a team project?", ["testing", "review", "git", "quality", "standards"]),
    ],
    "Full Stack Developer": [
        ("Describe a full-stack application you have worked on.", ["frontend", "backend", "database", "api", "application"]),
        ("How does a REST API connect a frontend application with a backend service?", ["api", "http", "backend", "frontend", "json"]),
        ("How would you secure a web application?", ["authentication", "authorization", "https", "validation", "security"]),
    ],
}


@st.cache_data(show_spinner=False, ttl=3600)
def _voice_tts_audio(text):
    """Generate a natural AI-interviewer voice prompt.

    Primary engine: Microsoft Edge neural TTS through edge-tts.
    Fallback: local Windows/pyttsx3 voice when edge-tts is unavailable.

    Returns:
        (audio_bytes, mime_type) or (None, None)
    """
    text = str(text or "").strip()
    if not text:
        return None, None

    # ------------------------------------------------------------
    # 1) Natural neural voice - preferred for the demo
    # ------------------------------------------------------------
    try:
        import asyncio
        import edge_tts

        async def _generate():
            communicate = edge_tts.Communicate(
                text=text,
                voice="en-IN-NeerjaNeural",
                rate="-5%",
                pitch="+0Hz",
                volume="+0%",
            )
            chunks = []
            async for chunk in communicate.stream():
                if chunk.get("type") == "audio":
                    chunks.append(chunk.get("data", b""))
            return b"".join(chunks)

        try:
            data = asyncio.run(_generate())
        except RuntimeError:
            # Safe fallback if an event loop already exists.
            loop = asyncio.new_event_loop()
            try:
                asyncio.set_event_loop(loop)
                data = loop.run_until_complete(_generate())
            finally:
                loop.close()
                asyncio.set_event_loop(None)

        if data:
            return data, "audio/mpeg"
    except Exception:
        pass

    # ------------------------------------------------------------
    # 2) Offline/local fallback - keeps the feature usable
    # ------------------------------------------------------------
    path = None
    try:
        import pyttsx3

        fd, path = tempfile.mkstemp(suffix=".wav")
        os.close(fd)
        engine = pyttsx3.init()
        engine.setProperty("rate", 155)
        engine.setProperty("volume", 1.0)

        # Prefer an English voice when Windows exposes one.
        try:
            voices = engine.getProperty("voices") or []
            for voice in voices:
                voice_text = (
                    f"{getattr(voice, 'name', '')} "
                    f"{getattr(voice, 'id', '')}"
                ).lower()
                if "english" in voice_text or "en-in" in voice_text or "en-us" in voice_text:
                    engine.setProperty("voice", voice.id)
                    break
        except Exception:
            pass

        engine.save_to_file(text, path)
        engine.runAndWait()

        with open(path, "rb") as audio_file:
            data = audio_file.read()

        return (data, "audio/wav") if data else (None, None)
    except Exception:
        return None, None
    finally:
        if path and os.path.exists(path):
            try:
                os.remove(path)
            except OSError:
                pass


@st.cache_resource(show_spinner=False)
def _load_whisper_model():
    """Load Whisper only once so every interview answer reuses the same model."""
    import whisper

    # base is a practical CPU-friendly model for a college-project demo.
    # It is noticeably more accurate than tiny while still being manageable.
    return whisper.load_model("base")


def _voice_transcribe(uploaded_audio):
    """Transcribe a recorded interview answer locally with OpenAI Whisper.

    The browser recorder stays exactly the same. Whisper runs locally, so the
    answer is not sent to Google Speech Recognition and does not depend on the
    SpeechRecognition Google endpoint understanding the browser WAV correctly.
    """
    path = None
    try:
        import wave
        import whisper

        audio_bytes = (
            uploaded_audio.getvalue()
            if hasattr(uploaded_audio, "getvalue")
            else bytes(uploaded_audio)
        )

        if not audio_bytes:
            return None, "The recording is empty. Please record an answer first."

        # Browser Streamlit audio_input normally returns WAV. For uploaded files,
        # preserve the original extension so FFmpeg can decode the format.
        suffix = ".wav"
        name = getattr(uploaded_audio, "name", "") or ""
        if "." in name:
            candidate_suffix = os.path.splitext(name)[1].lower()
            if candidate_suffix in {".wav", ".mp3", ".m4a", ".flac", ".ogg", ".webm"}:
                suffix = candidate_suffix

        fd, path = tempfile.mkstemp(suffix=suffix)
        os.close(fd)
        with open(path, "wb") as audio_file:
            audio_file.write(audio_bytes)

        # Give a useful message for a silent/near-silent WAV instead of making
        # the user wait for a model that cannot possibly find speech.
        if suffix == ".wav":
            try:
                with wave.open(path, "rb") as wav_file:
                    frames = wav_file.readframes(wav_file.getnframes())
                    sample_width = wav_file.getsampwidth()
                    channels = wav_file.getnchannels()

                if frames and sample_width in (1, 2, 4):
                    import audioop
                    rms = audioop.rms(frames, sample_width)
                    if rms < 80:
                        return None, (
                            "The recording is almost silent. Please speak clearly "
                            "toward the microphone and record again."
                        )
            except Exception:
                # If the WAV metadata is unusual, let Whisper/FFmpeg handle it.
                pass

        model = _load_whisper_model()

        result = model.transcribe(
            path,
            language="en",
            task="transcribe",
            fp16=False,
            temperature=0.0,
            condition_on_previous_text=False,
            beam_size=5,
            best_of=5,
            initial_prompt=(
                "This is a professional job interview. The candidate may discuss "
                "data science, machine learning, Python, SQL, statistics, "
                "software development, projects, education, internships, "
                "cloud, deployment, APIs, analytics and technical skills."
            ),
        )

        transcript = " ".join((result.get("text") or "").split()).strip()

        if not transcript:
            return None, (
                "Whisper could not detect clear spoken words. Please speak for "
                "at least 3–5 seconds and record the answer again."
            )

        # Reject a few common hallucinations that can appear on very short/silent clips.
        normalized = transcript.lower().strip(" .!?\"'")
        hallucinations = {
            "thank you",
            "thanks for watching",
            "thank you for watching",
            "you",
            "bye",
        }
        if normalized in hallucinations and len(transcript.split()) <= 5:
            return None, (
                "The recording did not contain enough clear speech. "
                "Please give a complete spoken answer and try again."
            )

        return transcript, None

    except ImportError as exc:
        if "whisper" in str(exc).lower():
            return None, (
                "OpenAI Whisper is not installed. Run:\n"
                "python -m pip install openai-whisper"
            )
        return None, f"Required audio package is missing: {exc}"
    except Exception as exc:
        message = str(exc)
        lower_message = message.lower()
        if "ffmpeg" in lower_message or "filenotfounderror" in lower_message:
            return None, (
                "Whisper needs FFmpeg to decode the recorded audio. "
                "Install FFmpeg, make sure `ffmpeg -version` works in PowerShell, "
                "then restart Streamlit."
            )
        return None, f"Whisper transcription failed: {type(exc).__name__}: {exc}"
    finally:
        if path and os.path.exists(path):
            try:
                os.remove(path)
            except OSError:
                pass


def _voice_assessment(transcript, keywords):
    words = transcript.split()
    lower = transcript.lower()
    matched = [k for k in keywords if k in lower]
    word_count = len(words)
    if word_count >= 45 and len(matched) >= 2:
        rating = "Strong"
        message = "The response contains useful detail and role-relevant terminology."
    elif word_count >= 20 and matched:
        rating = "Good"
        message = "The response is relevant; adding a concrete example would strengthen it."
    else:
        rating = "Needs Improvement"
        message = "The response is brief or misses important role-specific points."
    return rating, message, matched, word_count


def voice_screening_module():
    """Milestone 4 voice screening demo embedded in the Dashboard."""
    candidates = st.session_state.candidates
    if not candidates:
        st.info("🎙️ Voice Screening becomes available after resumes are analyzed.")
        return

    st.divider()
    st.header("🎙️ Voice Screening Module")
    st.caption("Speech-to-text screening with an AI interviewer voice and preliminary response assessment.")

    left, right = st.columns([1.05, 1.2])

    with left:
        candidate_options = list(range(len(candidates)))
        voice_candidate = st.selectbox(
            "Candidate",
            candidate_options,
            format_func=lambda i: f'{candidates[i].get("name", "Unknown Candidate")} — {candidates[i].get("email", "No email")}',
            key="voice_candidate_selector"
        )
        candidate = candidates[voice_candidate]
        default_role = candidate.get("job_applied") or "Data Scientist"
        roles = list(VOICE_SCREENING_QUESTIONS.keys())
        role = st.selectbox("Screening Role", roles, index=roles.index(default_role) if default_role in roles else 1, key="voice_role_selector")

        # Reset the voice interview whenever the recruiter changes candidate or role.
        # This prevents the next candidate from inheriting the previous candidate's
        # question number, recording history, or completed state.
        voice_context_key = f"{voice_candidate}|{candidate.get('email', '')}|{role}"
        if st.session_state.get("voice_context_key") != voice_context_key:
            st.session_state.voice_context_key = voice_context_key
            st.session_state.voice_question_index = 0
            st.session_state.voice_history = []
            st.session_state.voice_last_audio_hash = ""
            st.session_state.voice_session_active = False
            st.session_state.voice_completed = False

        if st.button("▶ Start Voice Screening", use_container_width=True, key="start_voice_screening"):
            st.session_state.voice_question_index = 0
            st.session_state.voice_history = []
            st.session_state.voice_last_audio_hash = ""
            st.session_state.voice_session_active = True
            st.session_state.voice_completed = False
            st.rerun()

        if st.button("↻ Reset Screening", use_container_width=True, key="reset_voice_screening"):
            st.session_state.voice_question_index = 0
            st.session_state.voice_history = []
            st.session_state.voice_last_audio_hash = ""
            st.session_state.voice_session_active = False
            st.session_state.voice_completed = False
            st.rerun()

        if st.session_state.voice_history:
            st.markdown("**Screening Progress**")
            st.progress(min(len(st.session_state.voice_history) / len(VOICE_SCREENING_QUESTIONS[role]), 1.0))
            st.caption(f'{len(st.session_state.voice_history)} of {len(VOICE_SCREENING_QUESTIONS[role])} questions completed')

    with right:
        if not st.session_state.voice_session_active:
            st.markdown("### 🎙️ Ready for Screening")
            st.info("Start a screening session to ask the candidate questions using voice.")
            return

        questions = VOICE_SCREENING_QUESTIONS[role]
        q_index = st.session_state.voice_question_index

        if q_index >= len(questions):
            st.success("🎉 Voice screening completed.")
            if st.session_state.voice_history:
                last = st.session_state.voice_history[-1]
                st.markdown(f"**Final assessment:** {last.get('rating', 'Completed')}")
            st.session_state.voice_completed = True
            st.session_state.voice_session_active = False
            return

        question, keywords = questions[q_index]
        st.markdown(f"**Question {q_index + 1} of {len(questions)}**")
        st.markdown(f'<div class="chat-ai">🤖 {question}</div>', unsafe_allow_html=True)

        tts, tts_format = _voice_tts_audio(question)
        if tts:
            st.audio(tts, format=tts_format)
            st.caption("🔊 AI interviewer voice")
        else:
            st.caption("🔊 AI interviewer voice is unavailable. Install edge-tts or keep pyttsx3 enabled for the local fallback.")

        # Browser microphone recorder. The recording is intentionally kept on the
        # current question until the recruiter explicitly analyzes it.
        audio_input = None
        if hasattr(st, "audio_input"):
            st.caption("🎙️ Click the microphone, allow browser microphone access, speak, then stop the recording.")
            try:
                audio_input = st.audio_input(
                    "🎙️ Record Candidate Response",
                    sample_rate=16000,
                    key=f"voice_record_{voice_candidate}_{q_index}"
                )
            except TypeError:
                # Compatibility with Streamlit versions that do not accept sample_rate.
                audio_input = st.audio_input(
                    "🎙️ Record Candidate Response",
                    key=f"voice_record_{voice_candidate}_{q_index}"
                )
        else:
            st.error("Browser voice recording is unavailable in this Streamlit version.")
            st.code("python -m pip install --upgrade streamlit", language="powershell")
            st.caption("Restart Streamlit after upgrading, then allow microphone access for localhost:8501.")

        # Fallback for systems/browsers where microphone permission or browser recording
        # is unavailable: the recruiter can upload a WAV/MP3/M4A recording and use the
        # exact same speech-to-text pipeline.
        uploaded_audio = st.file_uploader(
            "Or upload a recorded answer",
            type=["wav", "mp3", "m4a", "flac"],
            key=f"voice_upload_{voice_candidate}_{q_index}",
            help="Use this if the browser microphone is blocked or unavailable."
        )

        audio_source = audio_input if audio_input is not None else uploaded_audio
        if audio_source is not None:
            recorded_bytes = audio_source.getvalue()
            audio_hash = hashlib.md5(recorded_bytes).hexdigest()
            st.session_state.voice_last_audio_hash = audio_hash
            st.success("🎙️ Recording captured. Preview it below before transcription.")
            st.audio(recorded_bytes)

            if st.button("📝 Analyze Recorded Answer", use_container_width=True, key=f"analyze_voice_{voice_candidate}_{q_index}"):
                with st.spinner("Converting speech to text..."):
                    transcript, error = _voice_transcribe(audio_source)
                if transcript:
                    rating, message, matched, word_count = _voice_assessment(transcript, keywords)
                    st.session_state.voice_history.append({
                        "question": question,
                        "response": transcript,
                        "rating": rating,
                        "message": message,
                        "matched_keywords": matched,
                        "word_count": word_count,
                        "candidate": candidate.get("name", "Candidate"),
                        "role": role,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    st.session_state.voice_question_index += 1
                    st.session_state.voice_last_audio_hash = ""
                    candidate["voice_screened"] = True
                    candidate["voice_screening_completed_at"] = datetime.now().isoformat(timespec="seconds")
                    st.success("✅ Speech converted to text and evaluated.")
                    st.rerun()
                else:
                    st.error("Speech-to-text could not process this recording.")
                    st.caption(f"Reason: {error}")

        fallback = st.text_area(
            "Text fallback / transcript",
            placeholder="If speech recognition is unavailable, enter the candidate response here.",
            key=f"voice_fallback_{voice_candidate}_{q_index}"
        )
        if st.button("Save Response & Next Question", use_container_width=True, key=f"voice_next_{voice_candidate}_{q_index}"):
            if not fallback.strip():
                st.warning("Please record and analyze a voice response, or enter a transcript.")
            else:
                rating, message, matched, word_count = _voice_assessment(fallback.strip(), keywords)
                st.session_state.voice_history.append({
                    "question": question,
                    "response": fallback.strip(),
                    "rating": rating,
                    "message": message,
                    "matched_keywords": matched,
                    "word_count": word_count,
                    "candidate": candidate.get("name", "Candidate"),
                    "role": role,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                st.session_state.voice_question_index += 1
                st.session_state.voice_last_audio_hash = ""
                candidate["voice_screened"] = True
                candidate["voice_screening_completed_at"] = datetime.now().isoformat(timespec="seconds")
                st.rerun()

        if st.session_state.voice_history:
            st.markdown("### 📋 Preliminary Assessment")
            latest = st.session_state.voice_history[-1]
            st.write(f"**Candidate:** {latest['candidate']}")
            st.write(f"**Response quality:** {latest['rating']}")
            st.write(f"**Word count:** {latest['word_count']}")
            if latest["matched_keywords"]:
                st.write("**Relevant terms detected:** " + ", ".join(latest["matched_keywords"]))
            st.info(latest["message"])


# ============================================================
# DASHBOARD
# ============================================================

def dashboard():

    st.title(
        "Dashboard & Recruitment Operations"
    )

    st.write(
        "Recruitment analytics, candidate ranking, interview status, "
        "voice screening and hiring operations in one place."
    )

    st.caption("Milestone 4 • Dashboard + Voice Screening + End-to-End Recruitment")

    st.divider()

    candidates = st.session_state.candidates
    total = len(candidates)

    if total > 0:
        average_match = round(
            sum(float(c.get("match_score", 0) or 0) for c in candidates) / total,
            1
        )
        average_ats = round(
            sum(float(c.get("ats_score", 0) or 0) for c in candidates) / total,
            1
        )
        selected = sum(
            1 for c in candidates
            if str(c.get("status", "New")).strip().lower() == "selected"
        )
    else:
        average_match = 0
        average_ats = 0
        selected = 0

    interview_statuses = {"Interview", "Interview Scheduled", "Interview Completed"}
    interviews_scheduled = sum(
        1 for c in candidates
        if str(c.get("status", "")).strip() in interview_statuses
        or c.get("interview_started_at")
        or c.get("interview_completed_at")
        or c.get("voice_screening_completed_at")
    )
    hiring_success = round((selected / total) * 100, 1) if total else 0

    # Average time-to-hire is calculated only for candidates who reached
    # Selected status, using their stored pipeline-entry and selection times.
    hire_days = []
    for c in candidates:
        if str(c.get("status", "")).strip().lower() != "selected":
            continue
        created = c.get("created_at")
        selected_at = c.get("selected_at")
        if created and selected_at:
            try:
                start = datetime.fromisoformat(created)
                end = datetime.fromisoformat(selected_at)
                hire_days.append(max((end - start).total_seconds() / 86400, 0))
            except Exception:
                pass
    avg_time_to_hire = round(sum(hire_days) / len(hire_days), 1) if hire_days else None

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("👥 Total Candidates", total)
    with col2:
        st.metric("🎙️ Interviews", interviews_scheduled)
    with col3:
        st.metric("📈 Hiring Success", f"{hiring_success}%")
    with col4:
        if avg_time_to_hire is None:
            time_to_hire_label = "Not yet available"
        elif avg_time_to_hire < 1:
            time_to_hire_label = f"{round(avg_time_to_hire * 24, 1)}h"
        else:
            time_to_hire_label = f"{avg_time_to_hire}d"
        st.metric("⏱️ Avg. Time to Hire", time_to_hire_label)

    mini1, mini2, mini3 = st.columns(3)
    with mini1:
        st.metric("🎯 Average Match", f"{average_match}%")
    with mini2:
        st.metric("📄 Average ATS", f"{average_ats}%")
    with mini3:
        st.metric("⭐ Selected", selected)

    # Milestone 4: keep Voice Screening directly above the analytics section
    # so the recruiter can screen a candidate before reviewing the charts.
    voice_screening_module()

    # --------------------------------------------------------
    # ANALYTICS / CHARTS
    # --------------------------------------------------------

    if not candidates:
        return

    df = pd.DataFrame(candidates)

    st.divider()
    st.header("📊 Hiring Overview")

    col_left, col_right = st.columns(2)

    with col_left:
        chart_df = df.copy()
        chart_df["Candidate"] = chart_df["name"].fillna("Unknown Candidate")
        chart_df["Match Score"] = pd.to_numeric(
            chart_df.get("match_score", 0), errors="coerce"
        ).fillna(0)

        chart = px.bar(
            chart_df,
            x="Candidate",
            y="Match Score",
            title="🎯 Candidate Match Scores",
            text="Match Score"
        )
        chart.update_yaxes(range=[0, 100])
        chart.update_traces(texttemplate="%{text}%", textposition="outside")
        chart = style_chart(chart, 400)
        st.plotly_chart(
            chart,
            use_container_width=True,
            config={"displayModeBar": False}
        )

    with col_right:
        status_counts = df.get("status", pd.Series(["New"] * len(df))).fillna("New").value_counts()
        status_df = status_counts.reset_index()
        status_df.columns = ["Status", "Candidates"]

        chart = px.pie(
            status_df,
            names="Status",
            values="Candidates",
            hole=0.55,
            title="📌 Hiring Pipeline"
        )
        chart = style_chart(chart, 400)
        st.plotly_chart(
            chart,
            use_container_width=True,
            config={"displayModeBar": False}
        )

    score_df = df.copy()
    score_df["Candidate"] = score_df["name"].fillna("Unknown Candidate")
    score_df["Job Match"] = pd.to_numeric(score_df.get("match_score", 0), errors="coerce").fillna(0)
    score_df["ATS Score"] = pd.to_numeric(score_df.get("ats_score", 0), errors="coerce").fillna(0)

    score_long = score_df[["Candidate", "Job Match", "ATS Score"]].melt(
        id_vars=["Candidate"],
        value_vars=["Job Match", "ATS Score"],
        var_name="Metric",
        value_name="Score"
    )

    chart = px.bar(
        score_long,
        x="Candidate",
        y="Score",
        color="Metric",
        barmode="group",
        title="📈 Candidate Job Match vs ATS Score"
    )
    chart.update_yaxes(range=[0, 100])
    chart = style_chart(chart, 400)

    st.plotly_chart(
        chart,
        use_container_width=True,
        config={"displayModeBar": False}
    )

    st.header("👥 Candidate Overview")

    display_columns = [
        "name",
        "email",
        "match_score",
        "ats_score",
        "status"
    ]

    display_columns = [
        column for column in display_columns
        if column in df.columns
    ]

    st.dataframe(
        df[display_columns],
        use_container_width=True,
        hide_index=True
    )

# ============================================================
# RESUME ANALYZER
# ============================================================

def resume_analyzer():

    st.title("📄 Resume Analyzer")
    st.write(
        "Upload multiple PDF, DOCX or TXT resumes. "
        "All uploaded resumes will be analyzed together."
    )

    st.info(
        "💡 Uploading a new batch automatically replaces "
        "the previous batch of resumes. Your analyzed candidates "
        "remain available when you move between pages."
    )

    uploaded_files = st.file_uploader(
        "Choose Resumes",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
        key="resume_uploader"
    )

    # --------------------------------------------------------
    # Process a new upload batch only when files are present.
    # If the user returns to this page and the uploader is empty,
    # keep showing the already-analyzed candidates from session state.
    # --------------------------------------------------------
    if uploaded_files:

        current_batch = tuple(
            sorted(
                (file.name, file.size)
                for file in uploaded_files
            )
        )

        previous_batch = st.session_state.get(
            "processed_resume_batch",
            None
        )

        if current_batch != previous_batch:

            with st.spinner(
                "🔍 Clearing previous resumes and analyzing "
                "the new batch..."
            ):

                # Replace the previous physical resume batch.
                clear_old_resumes()

                # Replace the previous candidate batch.
                st.session_state.candidates = []

                # A new resume batch also starts a fresh ATS integration batch.
                st.session_state.ats_db = []

                processed_candidates = []

                for uploaded_file in uploaded_files:

                    try:
                        file_path = save_resume(uploaded_file)
                        text = extract_resume_text(file_path)
                        text = clean_text(text)

                        if (
                            not text
                            or text.startswith("ERROR")
                            or len(text) < 30
                        ):
                            st.warning(
                                f"⚠️ Could not extract sufficient "
                                f"text from {uploaded_file.name}"
                            )
                            continue

                        # Resume parsing + ATS analysis happen together.
                        # ATS analysis is integrated directly into this page.
                        name = extract_name(text)
                        email = extract_email(text)
                        phone = extract_phone(text)
                        skills = extract_skills(text)

                        ats_score = calculate_ats_score(
                            text,
                            name,
                            email,
                            phone,
                            skills
                        )

                        candidate = {
                            "name": name,
                            "email": email,
                            "phone": phone,
                            "skills": skills,
                            "ats_score": ats_score,
                            "match_score": 0,
                            "matched_skills": [],
                            "missing_skills": [],
                            "status": "New",
                            "job_applied": "",
                            "job_description": "",
                            "resume_file": uploaded_file.name,
                            "resume_text": text,
                            "created_at": datetime.now().isoformat(timespec="seconds")
                        }

                        processed_candidates.append(candidate)

                    except Exception as error:
                        st.error(
                            f"❌ Error processing "
                            f"{uploaded_file.name}: {error}"
                        )

                st.session_state.candidates = processed_candidates
                st.session_state.processed_resume_batch = current_batch

    # --------------------------------------------------------
    # Results remain visible after navigating away and returning.
    # --------------------------------------------------------
    candidates = st.session_state.candidates

    if not candidates:
        st.info(
            "📂 Please upload one or more resumes to begin."
        )
        return

    st.success(
        f"✅ Successfully analyzed {len(candidates)} resume(s)."
    )

    # --------------------------------------------------------
    # Summary metrics — ATS is part of resume analysis.
    # --------------------------------------------------------
    total_candidates = len(candidates)

    total_skills = sum(
        len(candidate.get("skills", []))
        for candidate in candidates
    )

    average_ats = round(
        sum(float(candidate.get("ats_score", 0) or 0) for candidate in candidates)
        / total_candidates,
        1
    ) if total_candidates else 0

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("👥 Resumes Analyzed", total_candidates)

    with col2:
        st.metric("🛠️ Skills Detected", total_skills)

    with col3:
        st.metric("📄 Average ATS Score", f"{average_ats}%")

    st.caption(
        "ATS compatibility is automatically analyzed when each resume is processed."
    )

    st.divider()

    # --------------------------------------------------------
    # Candidate overview table — no ATS score here.
    # --------------------------------------------------------
    st.subheader("👥 Candidate Overview")

    overview_data = []

    for candidate in candidates:
        overview_data.append({
            "Candidate": candidate.get(
                "name", "Unknown Candidate"
            ),
            "Email": candidate.get(
                "email", "Not found"
            ),
            "Phone": candidate.get(
                "phone", "Not found"
            ),
            "Skills": len(candidate.get("skills", [])),
            "ATS Score": f'{candidate.get("ats_score", 0)}%',
            "Job Applied": candidate.get(
                "job_applied", ""
            ) or "Not assigned",
            "Resume": candidate.get(
                "resume_file", ""
            )
        })

    overview_df = pd.DataFrame(overview_data)

    st.dataframe(
        overview_df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # --------------------------------------------------------
    # Detailed profiles
    # --------------------------------------------------------
    st.subheader("📋 Detailed Candidate Profiles")

    for index, candidate in enumerate(candidates, 1):

        name = candidate.get(
            "name", "Unknown Candidate"
        )

        resume_file = candidate.get(
            "resume_file", "Resume"
        )

        with st.expander(
            f"👤 {index}. {name}  •  {resume_file}",
            expanded=(index == 1)
        ):

            col1, col2, col3 = st.columns(3)

            with col1:
                st.write("### 👤 Candidate")
                st.write(
                    f'**Name:** {candidate.get("name", "Not found")}'
                )
                st.write(
                    f'**Email:** {candidate.get("email", "Not found")}'
                )
                st.write(
                    f'**Phone:** {candidate.get("phone", "Not found")}'
                )

            with col2:
                st.write("### 📄 Resume")
                st.write(f"**File:** {resume_file}")
                st.write(
                    f'**Job:** {candidate.get("job_applied", "") or "Not assigned"}'
                )
                st.write(
                    f'**Skills Found:** {len(candidate.get("skills", []))}'
                )

            with col3:
                st.write("### 📊 Hiring Status")
                st.write(
                    f'**Status:** {candidate.get("status", "New")}'
                )
                st.write(
                    f'**ATS Score:** {candidate.get("ats_score", 0)}%'
                )
                st.write(
                    f'**Match:** {candidate.get("match_score", 0)}%'
                )

            st.divider()

            st.write("### 🛠️ Detected Skills")

            skills = candidate.get("skills", [])

            if skills:
                st.write(" • ".join(skills))
            else:
                st.warning(
                    "No predefined technical skills detected."
                )

            # ----------------------------------------------------
            # ATS analysis + simple ATS integration are part of
            # Resume Analyzer. No separate ATS Analyzer page is used.
            # ----------------------------------------------------
            st.divider()
            st.write("### 📄 ATS Analysis & Integration")
            st.caption("The resume is checked for basic ATS readiness and can be synchronized with the mock ATS.")

            resume_text_lower = candidate.get("resume_text", "").lower()
            ats_checks = {
                "Candidate Name": candidate.get("name") not in (None, "", "Unknown Candidate"),
                "Email": candidate.get("email") not in (None, "", "Not found"),
                "Phone": candidate.get("phone") not in (None, "", "Not found"),
                "Technical Skills": len(candidate.get("skills", [])) >= 3,
                "Education Section": "education" in resume_text_lower,
                "Experience Section": ("experience" in resume_text_lower or "internship" in resume_text_lower),
                "Projects Section": "projects" in resume_text_lower,
                "Certifications": "certification" in resume_text_lower
            }

            ats_col1, ats_col2, ats_col3 = st.columns(3)
            with ats_col1:
                st.metric("📊 ATS Compatibility", f'{candidate.get("ats_score", 0)}%')
            with ats_col2:
                passed_count = sum(1 for value in ats_checks.values() if value)
                st.metric("✅ Checks Passed", f"{passed_count}/{len(ats_checks)}")
            with ats_col3:
                email = str(candidate.get("email", "")).strip().lower()
                synced_record = next((r for r in st.session_state.ats_db if str(r.get("email", "")).strip().lower() == email), None)
                st.metric("🔗 ATS Status", "Synced" if synced_record else "Not Synced")

            st.progress(passed_count / len(ats_checks) if ats_checks else 0)

            ats_results = pd.DataFrame([
                {"ATS Check": check, "Result": "PASS" if passed else "IMPROVE"}
                for check, passed in ats_checks.items()
            ])
            st.dataframe(ats_results, use_container_width=True, hide_index=True)

            # Simple recommendations, not an advanced ATS system.
            improvements = [check for check, passed in ats_checks.items() if not passed]
            if improvements:
                st.warning("🛠️ Improve: " + ", ".join(improvements))
            else:
                st.success("✅ Basic ATS checks passed successfully.")

            # Basic ATS record details and synchronization.
            with st.expander("🔗 ATS Candidate Record", expanded=True):
                st.write(f"**Candidate:** {candidate.get('name', 'Unknown Candidate')}")
                st.write(f"**Email:** {candidate.get('email', 'Not found')}")
                st.write(f"**Job Applied:** {candidate.get('job_applied') or 'Not assigned yet'}")
                st.write(f"**Hiring Status:** {candidate.get('status', 'New')}")
                st.write(f"**Match Score:** {candidate.get('match_score', 0)}%")
                st.write(f"**ATS Score:** {candidate.get('ats_score', 0)}%")

                if synced_record:
                    st.success(f"🟢 Synced with ATS • Last updated: {synced_record.get('updated_at', 'Not available')}")
                    st.caption("The ATS record contains the candidate's contact details, job, scores, status, and saved job description.")
                    if st.button("🔄 Update ATS Record", key=f"resume_ats_update_{index}", use_container_width=True):
                        ok, message = ats_add_candidate(candidate)
                        if ok:
                            st.success("ATS record updated successfully.")
                            st.rerun()
                else:
                    st.info("Candidate is not yet in the mock ATS.")
                    if st.button("➕ Add Candidate to ATS", key=f"resume_ats_add_{index}", use_container_width=True):
                        ok, message = ats_add_candidate(candidate)
                        if ok:
                            st.success("Candidate added to ATS successfully.")
                            st.rerun()
                        else:
                            st.error(message)

            col1, col2 = st.columns(2)

            with col1:
                st.write("### 🎓 Education")
                education = extract_section(
                    candidate["resume_text"],
                    "Education"
                )
                st.text_area(
                    "Education Details",
                    education,
                    height=180,
                    key=f"education_{index}",
                    label_visibility="collapsed"
                )

            with col2:
                st.write("### 💼 Experience")
                experience = extract_section(
                    candidate["resume_text"],
                    "Experience"
                )
                st.text_area(
                    "Experience Details",
                    experience,
                    height=180,
                    key=f"experience_{index}",
                    label_visibility="collapsed"
                )

            st.write("### 🚀 Projects")
            projects = extract_section(
                candidate["resume_text"],
                "Projects"
            )
            st.text_area(
                "Project Details",
                projects,
                height=180,
                key=f"projects_{index}",
                label_visibility="collapsed"
            )

            st.write("### 🏆 Certifications")
            certifications = extract_section(
                candidate["resume_text"],
                "Certifications"
            )
            st.text_area(
                "Certification Details",
                certifications,
                height=150,
                key=f"certifications_{index}",
                label_visibility="collapsed"
            )

# ============================================================
# JOB MATCHING
# ============================================================

def job_matching():

    st.title("🎯 Candidate–Job Matching")

    candidates = st.session_state.candidates

    if not candidates:
        st.warning("Please upload a resume first.")
        return

    candidate_options = list(range(len(candidates)))

    selected_index = st.selectbox(
        "👤 Select Candidate for this Job",
        candidate_options,
        format_func=lambda i: (
            f'{candidates[i].get("name", "Unknown Candidate")} '
            f'— {candidates[i].get("email", "No email")}'
        ),
        key="job_candidate_selector"
    )

    candidate = candidates[selected_index]

    st.info(
        f'Analyzing: **{candidate.get("name", "Unknown Candidate")}**'
    )

    # --------------------------------------------------------
    # Persist the job description both globally and per candidate.
    # This prevents it from disappearing when the user changes pages.
    # --------------------------------------------------------
    jd_key = f"job_description_{selected_index}"

    if jd_key not in st.session_state:
        st.session_state[jd_key] = (
            candidate.get("job_description", "")
            or st.session_state.get("saved_job_description", "")
        )

    job_description = st.text_area(
        "Job Description",
        height=280,
        placeholder=(
            "Enter the complete job description here.\n\n"
            "Example skills: Python, Java, SQL, "
            "Machine Learning, AI, Git, GitHub, AWS, "
            "React, Node.js, Data Science..."
        ),
        key=jd_key
    )

    if job_description.strip():
        candidate["job_description"] = job_description
        st.session_state.saved_job_description = job_description

        st.caption(
            "💾 Job Description saved for this candidate and will "
            "remain available when you navigate to another page."
        )

    if st.button(
        "🚀 Analyze Candidate Match",
        use_container_width=True,
        key="analyze_candidate_match"
    ):

        if not job_description.strip():
            st.warning("Please enter a Job Description.")
            return

        score, matched, missing = calculate_match(
            candidate["skills"],
            job_description
        )

        candidate["job_description"] = job_description
        candidate["match_score"] = score
        candidate["matched_skills"] = matched
        candidate["missing_skills"] = missing
        candidate["job_applied"] = "Current Job"

        st.session_state.saved_job_description = job_description
        st.session_state.candidates = list(st.session_state.candidates)

        st.success(
            f'✅ Matching completed for {candidate.get("name", "Candidate")}. '
            "Job Description saved."
        )

    candidate = st.session_state.candidates[selected_index]

    if candidate.get("match_score", 0) == 0:
        st.info(
            "Enter a Job Description and click Analyze Candidate Match."
        )
        return

    score = candidate["match_score"]

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.metric("🎯 Compatibility Score", f"{score}%")

    with col2:
        if score >= 85:
            st.success("High skill alignment")
        elif score >= 70:
            st.info("Moderate skill alignment")
        else:
            st.warning("Several skill gaps detected")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✅ Matched Skills")
        if candidate["matched_skills"]:
            for skill in candidate["matched_skills"]:
                st.success(skill)
        else:
            st.info("No matched skills detected.")

    with col2:
        st.subheader("⚠️ Skill Gaps")
        if candidate["missing_skills"]:
            for skill in candidate["missing_skills"]:
                st.warning(skill)
        else:
            st.success("No major skill gaps detected.")

    # Keep the saved JD visible after the analysis.
    with st.expander("📄 Saved Job Description", expanded=False):
        st.text_area(
            "Saved Job Description",
            candidate.get("job_description", ""),
            height=220,
            key=f"saved_jd_view_{selected_index}",
            disabled=True,
            label_visibility="collapsed"
        )

# ============================================================
# ATS INTEGRATION + ANALYZER
# ============================================================

def ats_add_candidate(candidate):
    """Mock ATS POST /ats/add_candidate endpoint."""
    email = str(candidate.get("email", "Not found")).strip().lower()
    if not email or email == "not found":
        return False, "Candidate email is required for ATS integration."

    for record in st.session_state.ats_db:
        if str(record.get("email", "")).strip().lower() == email:
            record.update({
                "name": candidate.get("name", "Unknown Candidate"),
                "job_applied": candidate.get("job_applied", "Not specified"),
                "status": candidate.get("status", "New"),
                "match_score": candidate.get("match_score", 0),
                "ats_score": candidate.get("ats_score", 0),
                "job_description": candidate.get("job_description", ""),
                "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            return True, "Candidate already existed in the mock ATS and was updated."

    st.session_state.ats_db.append({
        "name": candidate.get("name", "Unknown Candidate"),
        "email": candidate.get("email", "Not found"),
        "job_applied": candidate.get("job_applied", "Not specified"),
        "status": candidate.get("status", "New"),
        "match_score": candidate.get("match_score", 0),
        "ats_score": candidate.get("ats_score", 0),
        "job_description": candidate.get("job_description", ""),
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    return True, f'Candidate {candidate.get("name", "Candidate")} added successfully.'


def ats_update_status(email, status):
    """Mock ATS PUT /ats/update_status/{email} endpoint."""
    for record in st.session_state.ats_db:
        if str(record.get("email", "")).strip().lower() == str(email).strip().lower():
            record["status"] = status
            record["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return True, f"Status updated for {email} to {status}."
    return False, "Candidate not found in the mock ATS."


def ats_list_candidates():
    """Mock ATS GET /ats/list_candidates endpoint."""
    return st.session_state.ats_db


# ============================================================
# CANDIDATES PAGE
# ============================================================

def candidates_page():

    st.title("👥 Candidates")

    candidates = st.session_state.candidates

    if not candidates:
        st.info("📂 No candidates available. Upload resumes from Resume Analyzer first.")
        return

    # Make sure every candidate has a valid hiring status.
    for candidate in candidates:
        if not candidate.get("status"):
            candidate["status"] = "New"

    df = pd.DataFrame(candidates)

    columns = [
        "name",
        "email",
        "phone",
        "match_score",
        "ats_score",
        "status"
    ]

    columns = [column for column in columns if column in df.columns]

    st.dataframe(
        df[columns],
        use_container_width=True,
        hide_index=True
    )

    st.divider()
    st.subheader("🎯 Select Candidate for Hiring")
    st.caption(
        "This is the actual hiring selection. Choose a candidate below, "
        "set the hiring status to Selected, and update it."
    )

    candidate_options = list(range(len(candidates)))

    selected_index = st.selectbox(
        "👤 Candidate",
        candidate_options,
        format_func=lambda i: (
            f'{candidates[i].get("name", "Unknown Candidate")} — '
            f'{candidates[i].get("email", "No email")}'
        ),
        key="candidates_page_selector"
    )

    selected_candidate = candidates[selected_index]
    selected_name = selected_candidate.get("name", "Unknown Candidate")

    current_status = str(
        selected_candidate.get("status", "New")
    ).strip()

    statuses = [
        "New",
        "Screening",
        "Interview",
        "Selected",
        "Rejected"
    ]

    status_index = (
        statuses.index(current_status)
        if current_status in statuses
        else 0
    )

    new_status = st.selectbox(
        "📌 Hiring Status",
        statuses,
        index=status_index,
        key="candidates_page_status"
    )

    if st.button(
        "⭐ Update Hiring Status",
        use_container_width=True,
        key="candidates_page_update_status"
    ):
        st.session_state.candidates[selected_index]["status"] = new_status
        if new_status == "Selected":
            st.session_state.candidates[selected_index]["selected_at"] = datetime.now().isoformat(timespec="seconds")
        st.session_state.candidates = list(st.session_state.candidates)

        st.success(
            f'✅ {selected_name} is now **{new_status}**.'
        )

        st.rerun()

    selected_count = sum(
        1 for candidate in st.session_state.candidates
        if str(candidate.get("status", "New")).strip().lower() == "selected"
    )

    st.metric(
        "⭐ Total Selected Candidates",
        selected_count
    )

# ============================================================
# ANALYTICS
# ============================================================

def analytics():

    st.title("📊 Hiring Analytics")

    candidates = st.session_state.candidates

    if not candidates:
        st.info(
            "Analyze a resume to view analytics."
        )
        return

    df = pd.DataFrame(candidates)

    # --------------------------------------------------------
    # MATCH SCORE DISTRIBUTION
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        chart = px.histogram(
            df,
            x="match_score",
            nbins=10,
            title="🎯 Match Score Distribution",
            labels={
                "match_score": "Match Score (%)",
                "count": "Candidates"
            }
        )

        chart.update_xaxes(range=[0, 100])

        chart = style_chart(chart, 360)

        st.plotly_chart(
            chart,
            use_container_width=True,
            config={"displayModeBar": False}
        )

    with col2:

        chart = px.histogram(
            df,
            x="ats_score",
            nbins=10,
            title="🤖 ATS Score Distribution",
            labels={
                "ats_score": "ATS Score (%)",
                "count": "Candidates"
            }
        )

        chart.update_xaxes(range=[0, 100])

        chart = style_chart(chart, 360)

        st.plotly_chart(
            chart,
            use_container_width=True,
            config={"displayModeBar": False}
        )

    # --------------------------------------------------------
    # HIRING PIPELINE
    # --------------------------------------------------------

    status_df = (
        df["status"]
        .value_counts()
        .reset_index()
    )

    status_df.columns = [
        "Status",
        "Count"
    ]

    chart = px.pie(
        status_df,
        names="Status",
        values="Count",
        hole=0.50,
        title="🔄 Hiring Pipeline"
    )

    chart.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    chart = style_chart(chart, 400)

    st.plotly_chart(
        chart,
        use_container_width=True,
        config={"displayModeBar": False}
    )

    # --------------------------------------------------------
    # CANDIDATE SCORE LINE CHART
    # --------------------------------------------------------

    score_df = df[
        ["name", "match_score", "ats_score"]
    ].copy()

    score_df.columns = [
        "Candidate",
        "Job Match",
        "ATS Score"
    ]

    score_long = score_df.melt(
        id_vars=["Candidate"],
        value_vars=["Job Match", "ATS Score"],
        var_name="Metric",
        value_name="Score"
    )

    chart = px.line(
        score_long,
        x="Candidate",
        y="Score",
        color="Metric",
        markers=True,
        title="📈 Candidate Match & ATS Trend"
    )

    chart.update_yaxes(
        range=[0, 100],
        title="Score (%)"
    )

    chart.update_xaxes(
        title="Candidates"
    )

    chart.update_traces(
        line=dict(width=3),
        marker=dict(size=9)
    )

    chart = style_chart(chart, 400)

    st.plotly_chart(
        chart,
        use_container_width=True,
        config={"displayModeBar": False}
    )

    # --------------------------------------------------------
    # TOP CANDIDATE SKILLS
    # --------------------------------------------------------

    skill_counts = {}

    for candidate in candidates:

        for skill in candidate.get(
            "skills",
            []
        ):

            skill_counts[skill] = (
                skill_counts.get(skill, 0) + 1
            )

    if skill_counts:

        skill_df = pd.DataFrame(
            list(skill_counts.items()),
            columns=[
                "Skill",
                "Candidates"
            ]
        )

        skill_df = skill_df.sort_values(
            "Candidates",
            ascending=False
        ).head(15)

        chart = px.bar(
            skill_df,
            x="Skill",
            y="Candidates",
            title="🛠️ Top Candidate Skills"
        )

        chart.update_traces(
            marker_line_width=0,
            opacity=0.88
        )

        chart = style_chart(chart, 420)

        st.plotly_chart(
            chart,
            use_container_width=True,
            config={"displayModeBar": False}
        )

# ============================================================
# INTERVIEW ASSISTANT
# ============================================================

def evaluate_descriptive_answer(answer, keywords):
    """Simple, transparent content check for descriptive interview answers."""
    text = re.sub(r"[^a-z0-9+#. ]", " ", answer.lower())
    matched = [k for k in keywords if k.lower() in text]
    missing = [k for k in keywords if k.lower() not in text]
    coverage = len(matched) / max(len(keywords), 1)
    word_count = len(answer.split())

    if coverage >= 0.60 and word_count >= 30:
        result = "Likely Correct"
        feedback = "The answer covers the main expected concepts and provides reasonable detail."
    elif coverage >= 0.40 and word_count >= 15:
        result = "Partially Correct"
        feedback = "The answer contains some expected concepts, but more explanation is needed."
    else:
        result = "Needs Improvement"
        feedback = "The answer does not cover enough of the expected concepts. Add technical details or an example."

    score = round(coverage * 100)
    return result, score, feedback, matched, missing


def interview_assistant():

    st.title("💬 Interview Assistance & ATS Integration")
    st.caption("Generate descriptive and multiple-choice questions, simulate interviews, and manage ATS records")

    if not st.session_state.candidates:
        st.info("Upload a resume first.")
        return

    candidates = st.session_state.candidates

    # The selected candidate is stored in the widget state. When the recruiter
    # switches candidates, start a completely fresh interview session instead
    # of showing the previous person's last question.
    current_selected_index = int(st.session_state.get("interview_candidate_selector", 0) or 0)
    current_selected_index = max(0, min(current_selected_index, len(candidates) - 1))
    current_candidate = candidates[current_selected_index]

    # ------------------------------------------------------------
    # Simple role-specific question bank for Milestone 3.
    # Each role has descriptive questions and beginner/intermediate
    # MCQs. This is intentionally rule-based and easy to demonstrate.
    # ------------------------------------------------------------
    question_bank = {
        "Senior ML Engineer": {
            "descriptive": [
                {"question": "Describe a machine learning project where you optimized model performance. What techniques did you use?", "keywords": ["optimization", "model", "performance", "hyperparameter"]},
                {"question": "How would you deploy a machine learning model in production? What considerations would you check?", "keywords": ["deployment", "api", "monitoring", "scalability"]},
                {"question": "Explain how you would monitor an ML model in production and handle model drift.", "keywords": ["monitor", "drift", "data", "retrain"]},
                {"question": "How would you design a reliable ML pipeline from training to production inference?", "keywords": ["pipeline", "training", "validation", "deployment"]},
                {"question": "How would you choose between different machine learning algorithms for a business problem?", "keywords": ["business", "data", "metric", "algorithm", "interpretability"]}
            ],
            "mcq": [
                {"question": "Which technique is commonly used to reduce overfitting?", "options": ["Increasing model complexity", "Cross-validation", "Removing validation data", "Adding irrelevant features"], "answer": "Cross-validation"},
                {"question": "Which metric is especially useful when false negatives are costly?", "options": ["Recall", "R-squared", "MAE", "Silhouette score"], "answer": "Recall"},
                {"question": "Which method is commonly used to serve an ML model through a web application?", "options": ["REST API", "Spreadsheet", "Text editor", "PDF reader"], "answer": "REST API"},
                {"question": "What is model drift?", "options": ["A change in data patterns that can reduce model performance", "A faster CPU", "A database backup", "A coding style"], "answer": "A change in data patterns that can reduce model performance"},
                {"question": "Which technique can help tune model hyperparameters?", "options": ["Grid search", "File compression", "HTML parsing", "Database normalization"], "answer": "Grid search"}
            ]
        },
        "Data Scientist": {
            "descriptive": [
                {"question": "Walk me through your approach to feature engineering for a prediction problem.", "keywords": ["features", "encoding", "scaling", "selection"]},
                {"question": "How do you select evaluation metrics for a classification problem?", "keywords": ["precision", "recall", "f1", "accuracy", "business"]},
                {"question": "Explain how you would handle an imbalanced dataset.", "keywords": ["smote", "sampling", "class", "weights", "imbalance"]},
                {"question": "How would you identify and handle outliers in a dataset?", "keywords": ["outlier", "iqr", "z-score", "median", "remove"]},
                {"question": "How would you communicate data-driven findings to a non-technical stakeholder?", "keywords": ["visualization", "business", "simple", "insight", "story"]}
            ],
            "mcq": [
                {"question": "Which library is widely used for tabular data manipulation in Python?", "options": ["Pandas", "Flask", "Tkinter", "Requests"], "answer": "Pandas"},
                {"question": "Which metric combines precision and recall?", "options": ["F1-score", "MSE", "RMSLE", "R-squared"], "answer": "F1-score"},
                {"question": "What is a common technique for handling class imbalance?", "options": ["SMOTE", "Deleting all labels", "Removing the target", "Ignoring the minority class"], "answer": "SMOTE"},
                {"question": "Which chart is commonly used to show the distribution of a numeric variable?", "options": ["Histogram", "Pie chart only", "Network diagram", "Gantt chart"], "answer": "Histogram"},
                {"question": "Which method is commonly used to split data for model evaluation?", "options": ["Train-test split", "Only training", "Only testing", "No split"], "answer": "Train-test split"}
            ]
        },
        "Machine Learning Engineer": {
            "descriptive": [
                {"question": "What is overfitting and how can you prevent it?", "keywords": ["overfitting", "regularization", "validation", "dropout"]},
                {"question": "How would you choose between different machine learning algorithms for a business problem?", "keywords": ["business", "data", "metric", "algorithm", "validation"]},
                {"question": "What is cross-validation and why is it useful?", "keywords": ["cross-validation", "fold", "validation", "generalization"]},
                {"question": "How would you monitor a deployed machine learning model?", "keywords": ["monitor", "drift", "latency", "accuracy"]},
                {"question": "How would you improve the inference speed of an ML model?", "keywords": ["optimization", "latency", "batch", "model", "cache"]}
            ],
            "mcq": [
                {"question": "Which algorithm is commonly used for classification?", "options": ["Logistic Regression", "Linear Search", "Merge Sort", "Hashing only"], "answer": "Logistic Regression"},
                {"question": "What does cross-validation mainly help estimate?", "options": ["Model generalization", "File size", "CPU temperature", "Database storage"], "answer": "Model generalization"},
                {"question": "Which is an example of a regularization technique?", "options": ["L2 regularization", "Increasing noise only", "Deleting validation data", "Removing all features"], "answer": "L2 regularization"},
                {"question": "Which metric is often used for regression error?", "options": ["RMSE", "Recall", "Precision", "Accuracy"], "answer": "RMSE"},
                {"question": "Which tool is commonly used to expose a model as a service?", "options": ["FastAPI", "PowerPoint", "Notepad", "Paint"], "answer": "FastAPI"}
            ]
        },
        "Python Developer": {
            "descriptive": [
                {"question": "Explain decorators in Python and give a practical use case.", "keywords": ["decorator", "function", "wrapper", "reuse"]},
                {"question": "How does exception handling work in Python?", "keywords": ["try", "except", "finally", "error"]},
                {"question": "How would you optimize a slow Python program?", "keywords": ["profiling", "algorithm", "cache", "optimization"]},
                {"question": "Explain the difference between a list, tuple, set, and dictionary in Python.", "keywords": ["list", "tuple", "set", "dictionary"]},
                {"question": "How would you structure a Python application for maintainability?", "keywords": ["module", "package", "testing", "separation", "documentation"]}
            ],
            "mcq": [
                {"question": "Which data type is immutable in Python?", "options": ["Tuple", "List", "Dictionary", "Set"], "answer": "Tuple"},
                {"question": "Which keyword is used to handle exceptions?", "options": ["try", "loop", "check", "catcher"], "answer": "try"},
                {"question": "Which package is commonly used for numerical arrays?", "options": ["NumPy", "Flask", "BeautifulSoup", "PyGame"], "answer": "NumPy"},
                {"question": "Which keyword defines a function in Python?", "options": ["def", "func", "function", "method"], "answer": "def"},
                {"question": "Which collection stores unique values?", "options": ["Set", "List", "Tuple", "String"], "answer": "Set"}
            ]
        },
        "Full Stack Developer": {
            "descriptive": [
                {"question": "What is a REST API and how would you design one?", "keywords": ["rest", "api", "http", "endpoint", "json"]},
                {"question": "Explain the difference between frontend and backend development.", "keywords": ["frontend", "backend", "ui", "server", "database"]},
                {"question": "How does authentication work in a web application?", "keywords": ["authentication", "token", "session", "password", "authorization"]},
                {"question": "How would you improve the performance of a full-stack application?", "keywords": ["cache", "database", "frontend", "api", "optimization"]},
                {"question": "How would you secure a web application?", "keywords": ["https", "authentication", "authorization", "validation", "security"]}
            ],
            "mcq": [
                {"question": "Which HTTP method is commonly used to create a resource?", "options": ["POST", "GET", "DELETE", "HEAD"], "answer": "POST"},
                {"question": "Which technology is primarily used for page structure?", "options": ["HTML", "SQL", "Python", "Git"], "answer": "HTML"},
                {"question": "Which database is relational?", "options": ["MySQL", "MongoDB", "Redis", "Neo4j"], "answer": "MySQL"},
                {"question": "Which status code means Not Found?", "options": ["404", "200", "201", "500"], "answer": "404"},
                {"question": "Which protocol secures HTTP traffic?", "options": ["HTTPS", "FTP", "SMTP", "Telnet"], "answer": "HTTPS"}
            ]
        },
        "Software Developer": {
            "descriptive": [
                {"question": "What is object-oriented programming? Explain its main principles.", "keywords": ["class", "object", "inheritance", "encapsulation", "polymorphism"]},
                {"question": "How do you analyze the time complexity of an algorithm?", "keywords": ["big o", "complexity", "input", "time", "space"]},
                {"question": "How do you systematically debug a software application?", "keywords": ["reproduce", "logs", "debugger", "test", "fix"]},
                {"question": "How do you ensure code quality in a team project?", "keywords": ["testing", "review", "git", "standards", "quality"]},
                {"question": "How would you design a maintainable software application?", "keywords": ["modular", "testing", "documentation", "separation", "design"]}
            ],
            "mcq": [
                {"question": "Which principle hides internal implementation details?", "options": ["Encapsulation", "Inheritance", "Compilation", "Iteration"], "answer": "Encapsulation"},
                {"question": "Which data structure follows FIFO?", "options": ["Queue", "Stack", "Tree", "Graph"], "answer": "Queue"},
                {"question": "Which tool is commonly used for version control?", "options": ["Git", "Excel", "PowerPoint", "Paint"], "answer": "Git"},
                {"question": "What does O(n) describe?", "options": ["Linear time complexity", "Constant time", "No complexity", "Database size"], "answer": "Linear time complexity"},
                {"question": "Which practice helps detect defects early?", "options": ["Unit testing", "Deleting tests", "Skipping reviews", "Removing logs"], "answer": "Unit testing"}
            ]
        },
        "Java Developer": {
            "descriptive": [
                {"question": "Explain the four main principles of object-oriented programming in Java.", "keywords": ["encapsulation", "inheritance", "polymorphism", "abstraction"]},
                {"question": "What is the difference between an interface and an abstract class in Java?", "keywords": ["interface", "abstract", "implementation", "inheritance"]},
                {"question": "How does exception handling work in Java?", "keywords": ["try", "catch", "finally", "exception"]},
                {"question": "How does Java manage memory and garbage collection?", "keywords": ["heap", "garbage collection", "memory", "object"]},
                {"question": "How would you make a Java application more maintainable?", "keywords": ["classes", "interfaces", "testing", "design", "documentation"]}
            ],
            "mcq": [
                {"question": "Which keyword is used to inherit a class in Java?", "options": ["extends", "inherits", "implements-only", "using"], "answer": "extends"},
                {"question": "Which collection stores key-value pairs?", "options": ["HashMap", "ArrayList", "HashSet", "Queue"], "answer": "HashMap"},
                {"question": "Which method is the usual entry point of a Java application?", "options": ["main", "startApp", "runProgram", "begin"], "answer": "main"},
                {"question": "Which keyword is used to create an object?", "options": ["new", "make", "create", "object"], "answer": "new"},
                {"question": "Which feature allows the same method name with different parameters?", "options": ["Method overloading", "Garbage collection", "Compilation", "Serialization"], "answer": "Method overloading"}
            ]
        }
    }

    current_role = st.session_state.get("interview_role_selector", list(question_bank.keys())[0])
    current_context_key = f"{current_selected_index}|{current_candidate.get('email', '')}|{current_role}"
    if st.session_state.get("interview_context_key") != current_context_key:
        st.session_state.interview_context_key = current_context_key
        st.session_state.interview_questions = []
        st.session_state.interview_meta = {}
        st.session_state.interview_answers = {}
        st.session_state.interview_mcq_answers = {}
        st.session_state.interview_current = 0
        st.session_state.interview_history = []
        st.session_state.interview_evaluations = {}
        st.session_state.interview_session_active = False
        st.session_state.interview_mcq_score = None
        st.session_state.interview_started_at = None

    st.markdown("""
    <style>
        .interview-card { background: rgba(16,26,46,.72); border:1px solid rgba(129,140,248,.16); border-radius:16px; padding:18px; margin-bottom:14px; box-shadow:0 8px 24px rgba(0,0,0,.12); }
        .interview-card-title { font-size:18px; font-weight:700; color:#fff; margin-bottom:12px; }
        .question-card { background:rgba(30,41,59,.58); border:1px solid rgba(148,163,184,.12); border-radius:12px; padding:13px 14px; margin:9px 0; color:#e8edf8; line-height:1.45; }
        .question-number { display:inline-flex; width:25px; height:25px; align-items:center; justify-content:center; border-radius:50%; background:#2563eb; color:white; font-weight:700; margin-right:9px; }
        .question-meta { margin-left:35px; margin-top:5px; font-size:12px; color:#9fb0ca; }
        .chat-ai { background:rgba(30,41,59,.60); border:1px solid rgba(148,163,184,.12); border-radius:12px; padding:13px; margin:8px 0; color:#e8edf8; }
        .chat-user { background:rgba(59,130,246,.20); border:1px solid rgba(96,165,250,.18); border-radius:12px; padding:11px 13px; margin:8px 0 8px 28px; color:#eef5ff; }
        .ats-mini { background:rgba(30,41,59,.48); border:1px solid rgba(148,163,184,.12); border-radius:12px; padding:11px; margin:7px 0; }
        .ats-connected { color:#34d399; font-weight:600; }
        .ats-muted { color:#9fb0ca; font-size:12px; }
    </style>
    """, unsafe_allow_html=True)

    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown('<div class="interview-card">', unsafe_allow_html=True)
        st.markdown('<div class="interview-card-title">📝 Interview Question Generator</div>', unsafe_allow_html=True)

        role = st.selectbox("Job Position", list(question_bank.keys()), key="interview_role_selector")
        question_mode = st.selectbox(
            "Question Mode",
            ["Descriptive", "Multiple Choice", "Mixed"],
            key="interview_question_mode"
        )
        num_questions = st.selectbox("Number of Questions", [3, 4, 5], index=0, key="interview_num_questions")

        if st.button("🎲 Generate Interview Questions", use_container_width=True, key="generate_role_questions"):
            bank = question_bank[role]
            items = []
            if question_mode == "Descriptive":
                selected = random.sample(bank["descriptive"], num_questions)
                items = [{"type": "descriptive", **q} for q in selected]
            elif question_mode == "Multiple Choice":
                selected = random.sample(bank["mcq"], num_questions)
                items = [{"type": "mcq", **q} for q in selected]
            else:
                # Mixed mode always returns exactly the requested number.
                desc_count = (num_questions + 1) // 2
                mcq_count = num_questions - desc_count
                selected_desc = random.sample(bank["descriptive"], desc_count)
                selected_mcq = random.sample(bank["mcq"], mcq_count)
                items = ([{"type": "descriptive", **q} for q in selected_desc] +
                         [{"type": "mcq", **q} for q in selected_mcq])
                random.shuffle(items)

            st.session_state.interview_questions = items
            st.session_state.interview_meta = {"role": role, "mode": question_mode, "candidate_index": selected_index if "selected_index" in locals() else current_selected_index}
            st.session_state.interview_context_key = f"{current_selected_index}|{current_candidate.get('email', '')}|{role}"
            st.session_state.interview_current = 0
            st.session_state.interview_answers = {}
            st.session_state.interview_mcq_answers = {}
            st.session_state.interview_history = []
            st.session_state.interview_evaluations = {}
            st.session_state.interview_session_active = True
            st.session_state.interview_started_at = datetime.now().isoformat(timespec="seconds")
            st.session_state.interview_mcq_score = None
            st.rerun()

        questions = st.session_state.get("interview_questions", [])
        meta = st.session_state.get("interview_meta", {})

        if questions:
            for number, item in enumerate(questions, 1):
                q_type = "Descriptive" if item["type"] == "descriptive" else "Multiple Choice"
                st.markdown(
                    f'<div class="question-card"><span class="question-number">{number}</span><span>{item["question"]}</span><div class="question-meta">{q_type} • Role-specific interview question</div></div>',
                    unsafe_allow_html=True
                )
        else:
            st.markdown('<div class="question-card">Select a role and question mode, then generate questions.</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Simple MCQ answer sheet. This is intentionally basic for the demo.
        mcq_items = [item for item in questions if item.get("type") == "mcq"]
        if mcq_items:
            st.markdown('<div class="interview-card">', unsafe_allow_html=True)
            st.markdown('<div class="interview-card-title">☑️ Choose the Correct Answers</div>', unsafe_allow_html=True)
            for idx, item in enumerate(mcq_items):
                st.radio(
                    f"{idx + 1}. {item['question']}",
                    item["options"],
                    key=f"mcq_answer_{meta.get('role','role')}_{idx}"
                )

            if st.button("✅ Submit MCQ Answers", use_container_width=True, key="submit_mcq_answers"):
                correct = 0
                for idx, item in enumerate(mcq_items):
                    selected = st.session_state.get(f"mcq_answer_{meta.get('role','role')}_{idx}")
                    st.session_state.interview_mcq_answers[idx] = selected
                    if selected == item["answer"]:
                        correct += 1
                st.session_state.interview_mcq_score = f"{correct}/{len(mcq_items)}"
                st.success(f"MCQ score: {correct}/{len(mcq_items)}")
            elif st.session_state.get("interview_mcq_score"):
                st.info(f"Last MCQ score: {st.session_state.interview_mcq_score}")
            st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="interview-card">', unsafe_allow_html=True)
        st.markdown('<div class="interview-card-title">⚙️ AI Interview Simulation</div>', unsafe_allow_html=True)

        candidate_options = list(range(len(candidates)))
        selected_index = st.selectbox(
            "Candidate",
            candidate_options,
            index=current_selected_index,
            format_func=lambda i: f'{candidates[i].get("name", "Unknown Candidate")} — {candidates[i].get("email", "No email")}',
            key="interview_candidate_selector"
        )
        candidate = candidates[selected_index]
        candidate_name = candidate.get("name", "Candidate")

        # If the selectbox changed during this rerun, reset immediately so the
        # visible interview starts from Question 1 for the newly selected candidate.
        live_role = st.session_state.get("interview_role_selector", list(question_bank.keys())[0])
        live_context_key = f"{selected_index}|{candidate.get('email', '')}|{live_role}"
        if st.session_state.get("interview_context_key") != live_context_key:
            st.session_state.interview_context_key = live_context_key
            st.session_state.interview_questions = []
            st.session_state.interview_meta = {}
            st.session_state.interview_answers = {}
            st.session_state.interview_mcq_answers = {}
            st.session_state.interview_current = 0
            st.session_state.interview_history = []
            st.session_state.interview_evaluations = {}
            st.session_state.interview_session_active = False
            st.session_state.interview_mcq_score = None
            st.rerun()

        status_text = "Active Session" if st.session_state.get("interview_session_active", False) else "Ready"
        status_color = "#34d399" if status_text == "Active Session" else "#93c5fd"
        st.markdown(
            f'<div style="display:flex;justify-content:space-between;align-items:center;margin:5px 0 12px 0;"><span style="color:#e8edf8;font-weight:600;">Candidate: {candidate_name}</span><span style="background:rgba(59,130,246,.15);color:{status_color};padding:5px 9px;border-radius:10px;font-size:12px;">{status_text}</span></div>',
            unsafe_allow_html=True
        )

        current = st.session_state.get("interview_current", 0)
        history = st.session_state.get("interview_history", [])

        for item in history:
            st.markdown(f'<div class="chat-ai">🤖 {item["question"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="chat-user">{item["response"]}</div>', unsafe_allow_html=True)
            if item.get("feedback"):
                st.info(f'🔎 **Answer Check:** {item["feedback"]}')

        descriptive_questions = [item for item in questions if item.get("type") == "descriptive"]
        descriptive_current = [item for item in questions[:current] if item.get("type") == "descriptive"]

        if questions and current < len(questions):
            current_item = questions[current]
            if current_item.get("type") == "descriptive":
                st.markdown(f'<div class="chat-ai">🤖 <strong>{current_item["question"]}</strong></div>', unsafe_allow_html=True)
                response_col, send_col = st.columns([5, 1])
                with response_col:
                    response = st.text_area("Your answer", height=110, placeholder="Type your descriptive answer...", key=f"interview_response_{selected_index}_{current}")
                with send_col:
                    st.write("")
                    send = st.button("➤ Send", use_container_width=True, key=f"send_interview_{selected_index}_{current}")
                if send:
                    if not response.strip():
                        st.warning("Please enter a response before sending.")
                    else:
                        result, score, feedback, matched, missing = evaluate_descriptive_answer(response.strip(), current_item.get("keywords", []))
                        answer_check = f"{result} • {score}% concept coverage. {feedback}"
                        if matched:
                            answer_check += " Matched: " + ", ".join(matched) + "."
                        if missing:
                            answer_check += " Missing: " + ", ".join(missing[:3]) + ("..." if len(missing) > 3 else ".")
                        st.session_state.interview_answers[current] = response.strip()
                        st.session_state.interview_evaluations[current] = {"result": result, "score": score, "matched": matched, "missing": missing, "feedback": feedback}
                        st.session_state.interview_history.append({"question": current_item["question"], "response": response.strip(), "feedback": answer_check})
                        st.session_state.interview_current = current + 1
                        st.session_state.interview_session_active = True
                        st.rerun()
            else:
                st.markdown(f'<div class="chat-ai">🤖 <strong>{current_item["question"]}</strong></div>', unsafe_allow_html=True)
                selected = st.radio("Choose your answer", current_item["options"], key=f"sim_mcq_{selected_index}_{current}")
                if st.button("✅ Submit Answer", use_container_width=True, key=f"submit_sim_mcq_{selected_index}_{current}"):
                    is_correct = selected == current_item["answer"]
                    feedback = "✅ Correct answer" if is_correct else f"❌ Incorrect. Correct answer: {current_item['answer']}"
                    st.session_state.interview_evaluations[current] = {"result": "Correct" if is_correct else "Incorrect", "score": 100 if is_correct else 0}
                    st.session_state.interview_history.append({"question": current_item["question"], "response": selected, "feedback": feedback})
                    st.session_state.interview_current = current + 1
                    st.session_state.interview_session_active = True
                    st.rerun()

        elif questions and current >= len(questions):
            candidate["interview_completed_at"] = datetime.now().isoformat(timespec="seconds")
            candidate["interview_started_at"] = candidate.get("interview_started_at") or st.session_state.get("interview_started_at")
            candidate["interview_completed"] = True
            candidate["status"] = "Interview" if candidate.get("status") not in {"Selected", "Rejected"} else candidate.get("status")
            st.session_state.interview_session_active = False
            st.success("🎉 Interview completed successfully.")
            st.caption("Descriptive responses and MCQ answers were recorded and checked.")
            if st.session_state.get("interview_mcq_score"):
                st.info(f"MCQ result: {st.session_state.interview_mcq_score}")
            if st.button("🔄 Start New Interview", use_container_width=True, key="restart_interview"):
                st.session_state.interview_questions = []
                st.session_state.interview_answers = {}
                st.session_state.interview_mcq_answers = {}
                st.session_state.interview_current = 0
                st.session_state.interview_history = []
                st.session_state.interview_evaluations = {}
                st.session_state.interview_session_active = False
                st.session_state.interview_mcq_score = None
                st.rerun()
        else:
            st.markdown("<div class='chat-ai'>🤖 Hello! I'm your AI interviewer. Generate questions on the left to start the session.</div>", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # --------------------------------------------------------
        # Simple ATS integration: show an actual candidate record,
        # sync/update it, and display useful fields instead of only
        # showing the ATS score.
        # --------------------------------------------------------
        st.markdown('<div class="interview-card">', unsafe_allow_html=True)
        st.markdown('<div style="display:flex;justify-content:space-between;align-items:center;"><div class="interview-card-title" style="margin-bottom:0;">🔗 ATS Integration</div><span class="ats-connected">● Connected</span></div>', unsafe_allow_html=True)

        ats_records = ats_list_candidates()
        email = str(candidate.get("email", "")).strip().lower()
        record = next((r for r in ats_records if str(r.get("email", "")).strip().lower() == email), None)

        if record:
            st.success("Candidate is synchronized with the mock ATS.")
            ats_cols = st.columns(3)
            ats_cols[0].metric("ATS Status", record.get("status", "New"))
            ats_cols[1].metric("Match", f'{record.get("match_score", 0)}%')
            ats_cols[2].metric("ATS Score", f'{record.get("ats_score", 0)}%')
            st.caption(f"Job: {record.get('job_applied') or 'Not assigned'}  •  Last updated: {record.get('updated_at', 'Not available')}")

            new_ats_status = st.selectbox(
                "Update ATS Status",
                ["New", "Screening", "Interview Scheduled", "Interview Completed", "Selected", "Rejected"],
                index=["New", "Screening", "Interview Scheduled", "Interview Completed", "Selected", "Rejected"].index(record.get("status", "New")) if record.get("status", "New") in ["New", "Screening", "Interview Scheduled", "Interview Completed", "Selected", "Rejected"] else 0,
                key=f"ats_status_{selected_index}"
            )
            if st.button("🔄 Update ATS Record", use_container_width=True, key=f"ats_update_{selected_index}"):
                ok, message = ats_update_status(email, new_ats_status)
                if ok:
                    candidate["status"] = new_ats_status if new_ats_status in ["New", "Screening", "Interview", "Selected", "Rejected"] else candidate.get("status", "New")
                    if new_ats_status == "Selected":
                        candidate["selected_at"] = datetime.now().isoformat(timespec="seconds")
                    st.success(message)
                    st.rerun()
        else:
            st.info("Candidate is not yet synchronized with ATS.")
            st.write(f"**Candidate:** {candidate.get('name', 'Unknown Candidate')}")
            st.write(f"**Email:** {candidate.get('email', 'Not found')}")
            st.write(f"**Job:** {candidate.get('job_applied') or 'Not assigned'}")
            st.write(f"**Match Score:** {candidate.get('match_score', 0)}%  |  **ATS Score:** {candidate.get('ats_score', 0)}%")
            if st.button("🔄 Sync Candidate to ATS", use_container_width=True, key=f"interview_ats_sync_{selected_index}"):
                ok, message = ats_add_candidate(candidate)
                if ok:
                    st.success(message)
                    st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# MAIN PROGRAM
# ============================================================

if not st.session_state.logged_in:

    login_page()

else:

    create_sidebar()

    current_page = (
        st.session_state.page
    )

    current_role = st.session_state.get("user_role", "")

    if current_role == "admin":
        if current_page != "Admin Portal":
            st.session_state.page = "Admin Portal"
            current_page = "Admin Portal"
        admin_portal()

    elif current_role == "user":
        if current_page != "Candidate Portal":
            st.session_state.page = "Candidate Portal"
            current_page = "Candidate Portal"
        candidate_portal()

    else:
        if current_page == "Dashboard":
            dashboard()
        elif current_page == "Resume Analyzer":
            resume_analyzer()
        elif current_page == "Job Matching":
            job_matching()
        elif current_page == "Candidates":
            candidates_page()
        elif current_page == "Analytics":
            analytics()
        elif current_page == "Interview Assistant":
            interview_assistant()

# Save the latest application data after rendering the current page.
# This does not reset or modify any existing UI/session behaviour.
save_persistent_data()

import streamlit as st
import time

st.set_page_config(
    page_title="AeroGuide – Airport AI Assistant",
    page_icon="✈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── GLOBAL CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Outfit:wght@300;400;500;600&display=swap');

/* ── LIGHT THEME (default) ── */
:root, [data-theme="light"] {
    --bg0: #F4F7F9;
    --bg1: #FFFFFF;
    --bg2: #EBF0F4;
    --bg3: #F0F5F8;
    --bg4: #E2ECF2;
    --border: rgba(0,145,210,0.15);
    --border2: rgba(0,145,210,0.30);
    --accent: #0091D2;
    --accent2: #0073AA;
    --glow: rgba(0,145,210,0.18);
    --glow2: rgba(0,145,210,0.07);
    --text0: #0D1F2D;
    --text1: #2E5F7A;
    --text2: #7A9FB5;
    --text3: #B0CCDA;
    --green: #00A86B;
    --amber: #E07B00;
    --red: #D93025;
    --topbar-bg: rgba(255,255,255,0.95);
    --topbar-shadow: 0 1px 12px rgba(0,100,180,0.08);
    --scrollbar-track: #E8EFF4;
    --font-head: 'Syne', sans-serif;
    --font-body: 'Outfit', sans-serif;
    --r1: 8px; --r2: 14px; --r3: 22px;
}

/* ── DARK THEME ── */
[data-theme="dark"] {
    --bg0: #080E0F;
    --bg1: #0D1617;
    --bg2: #111E20;
    --bg3: #162628;
    --bg4: #1C3033;
    --border: rgba(0,210,180,0.12);
    --border2: rgba(0,210,180,0.28);
    --accent: #00D4B4;
    --accent2: #00A891;
    --glow: rgba(0,212,180,0.20);
    --glow2: rgba(0,212,180,0.07);
    --text0: #E8FAF7;
    --text1: #7EC8BC;
    --text2: #3D7A72;
    --text3: #234D48;
    --green: #4DFFC3;
    --amber: #FFB347;
    --red: #FF5566;
    --topbar-bg: rgba(8,14,15,0.95);
    --topbar-shadow: 0 1px 12px rgba(0,0,0,0.4);
    --scrollbar-track: #0D1617;
    --font-head: 'Syne', sans-serif;
    --font-body: 'Outfit', sans-serif;
    --r1: 8px; --r2: 14px; --r3: 22px;
}

/* Smooth transitions for everything */
*, *::before, *::after {
    transition: background-color 0.3s ease, border-color 0.3s ease, color 0.3s ease, box-shadow 0.3s ease !important;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"], .stApp {
    font-family: var(--font-body) !important;
    background-color: var(--bg0) !important;
    color: var(--text0) !important;
}
/* Force theme vars to cascade into all Streamlit containers */
[data-theme="dark"] .stApp,
[data-theme="dark"] body,
[data-theme="dark"] html {
    background-color: var(--bg0) !important;
    color: var(--text0) !important;
}
[data-theme="light"] .stApp,
[data-theme="light"] body,
[data-theme="light"] html {
    background-color: var(--bg0) !important;
    color: var(--text0) !important;
}

#MainMenu, footer, .stDeployButton { visibility: hidden !important; display: none !important; }
/* Keep header visible for sidebar toggle, but style it cleanly */
header[data-testid="stHeader"] {
    background: rgba(3,8,15,0.0) !important;
    border-bottom: none !important;
}
/* Show sidebar toggle button */
button[data-testid="stSidebarCollapseButton"],
button[kind="header"] {
    visibility: visible !important;
    display: flex !important;
}
.block-container { padding: 0 !important; max-width: 100% !important; }

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--scrollbar-track); }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 4px; }

/* ── Theme Toggle ── */
.theme-toggle {
    display: flex; align-items: center; gap: 8px;
    padding: 6px 14px;
    background: var(--glow2);
    border: 1px solid var(--border2);
    border-radius: 50px;
    cursor: pointer;
    font-size: 13px; font-weight: 500; color: var(--text1);
    transition: all 0.2s;
    user-select: none;
    white-space: nowrap;
}
.theme-toggle:hover { background: var(--glow); color: var(--accent); border-color: var(--accent); }
.theme-toggle-icon { font-size: 15px; }

/* ── Top Bar ── */
.topbar {
    position: fixed; top: 0; left: 0; right: 0; z-index: 1000;
    height: 58px;
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 28px;
    background: var(--topbar-bg);
    backdrop-filter: blur(16px);
    box-shadow: var(--topbar-shadow);
    border-bottom: 1px solid var(--border);
}
.topbar-brand { display: flex; align-items: center; gap: 11px; }
.brand-mark {
    width: 34px; height: 34px;
    background: linear-gradient(135deg, #005A8A, var(--accent));
    border-radius: var(--r1);
    display: flex; align-items: center; justify-content: center;
    font-size: 17px;
    box-shadow: 0 0 18px var(--glow);
}
.brand-name { font-family: var(--font-head); font-size: 18px; font-weight: 700; color: var(--text0); letter-spacing: -0.2px; }
.brand-name em { color: var(--accent); font-style: normal; }
.topbar-nav { display: flex; align-items: center; gap: 4px; }
.nav-link {
    padding: 6px 14px; border-radius: 50px;
    font-size: 13px; font-weight: 500; color: var(--text2);
    border: 1px solid transparent; transition: all 0.18s;
}
.nav-link:hover { color: var(--accent); border-color: var(--border2); background: var(--glow2); }
.nav-active { color: var(--accent) !important; border-color: var(--border2) !important; background: var(--glow2) !important; }
.live-badge {
    display: flex; align-items: center; gap: 6px;
    padding: 5px 13px;
    background: rgba(0,229,160,0.07);
    border: 1px solid rgba(0,229,160,0.18);
    border-radius: 50px;
    font-size: 12px; font-weight: 500; color: var(--green);
}
.live-dot { width: 6px; height: 6px; background: var(--green); border-radius: 50%; animation: blink 2s ease infinite; }
@keyframes blink { 0%,100% { opacity:1; transform:scale(1); } 50% { opacity:0.4; transform:scale(0.7); } }
.main-offset { height: 58px; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: var(--bg1) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] > div:first-child {
    padding: 0 !important;
    background: var(--bg1) !important;
}
.sb-section { padding: 18px 18px 16px; border-bottom: 1px solid var(--border); }
.sb-label {
    font-family: var(--font-head);
    font-size: 9.5px; font-weight: 700;
    letter-spacing: 2.5px; text-transform: uppercase;
    color: var(--text3); margin-bottom: 13px;
}

/* Hide ALL native radio widgets in sidebar */
section[data-testid="stSidebar"] [data-testid="stRadio"] { display: none !important; }

/* Journey selector - use st.columns which ARE side by side */
section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] {
    gap: 7px !important;
}
section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] [data-testid="stVerticalBlock"] {
    padding: 0 !important;
    min-width: 0 !important;
}
/* All journey buttons */
.jbtn .stButton > button {
    width: 100% !important;
    background: var(--bg3) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r2) !important;
    color: var(--text2) !important;
    font-size: 22px !important;
    padding: 12px 0 6px !important;
    text-align: center !important;
    white-space: nowrap !important;
    height: 54px !important;
    transition: all 0.18s !important;
    transform: none !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    line-height: 1 !important;
}
.jbtn .stButton > button:hover {
    border-color: var(--accent) !important;
    background: var(--glow2) !important;
    color: var(--accent) !important;
    transform: none !important;
    box-shadow: none !important;
}
.jbtn-active .stButton > button {
    border-color: var(--accent) !important;
    background: var(--glow2) !important;
    color: var(--accent) !important;
    box-shadow: 0 0 12px var(--glow), 0 0 24px var(--glow) !important;
    filter: drop-shadow(0 0 6px var(--accent)) !important;
}
.jbtn-label {
    font-size: 11px;
    text-align: center;
    margin-top: 3px;
    margin-bottom: 4px;
    font-weight: 500;
    letter-spacing: 0.2px;
}

/* override the global stButton transform for qq buttons */
.qq-wrap .stButton > button:hover {
    transform: none !important;
}

/* ── Quick Questions redesign — pure Streamlit button styling ── */
.qq-wrap .stButton > button {
    display: flex !important;
    align-items: center !important;
    gap: 0 !important;
    width: 100% !important;
    background: var(--bg3) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r2) !important;
    padding: 10px 13px !important;
    text-align: left !important;
    color: var(--text1) !important;
    font-size: 13px !important;
    font-weight: 400 !important;
    line-height: 1.4 !important;
    transition: all 0.2s !important;
    white-space: normal !important;
    height: auto !important;
    position: relative !important;
    overflow: hidden !important;
}
.qq-wrap .stButton > button::before {
    content: '' !important;
    position: absolute !important;
    left: 0 !important; top: 0 !important; bottom: 0 !important;
    width: 3px !important;
    background: var(--accent) !important;
    opacity: 0 !important;
    transition: opacity 0.2s !important;
    border-radius: 0 2px 2px 0 !important;
}
.qq-wrap .stButton > button:hover {
    border-color: var(--border2) !important;
    background: var(--glow2) !important;
    color: var(--text0) !important;
    transform: translateX(3px) !important;
    box-shadow: none !important;
}
.qq-wrap .stButton > button:hover::before { opacity: 1 !important; }

/* Standard buttons */
.stButton > button {
    width: 100% !important;
    background: var(--bg3) !important;
    color: var(--text1) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r2) !important;
    font-family: var(--font-body) !important;
    font-size: 13px !important; font-weight: 400 !important;
    padding: 10px 14px !important;
    text-align: left !important;
    transition: all 0.18s !important;
    white-space: normal !important; height: auto !important; line-height: 1.4 !important;
}
.stButton > button:hover {
    border-color: var(--accent) !important; color: var(--text0) !important;
    background: var(--glow2) !important; box-shadow: none !important; transform: translateX(3px) !important;
}
.stButton > button:focus { box-shadow: none !important; outline: none !important; }
.clear-wrap .stButton > button {
    background: rgba(255,68,85,0.05) !important;
    border-color: rgba(255,68,85,0.18) !important;
    color: rgba(255,100,115,0.8) !important;
    text-align: center !important; font-size: 12.5px !important;
}
.clear-wrap .stButton > button:hover {
    background: rgba(255,68,85,0.1) !important;
    border-color: rgba(255,68,85,0.35) !important;
    transform: none !important;
}

/* Theme toggle button */
[data-testid="stMainBlockContainer"] > div:first-child .stButton > button,
div[style*="position:fixed"] .stButton > button {
    background: var(--glow2) !important;
    border: 1px solid var(--border2) !important;
    border-radius: 50px !important;
    color: var(--text1) !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    padding: 6px 14px !important;
    text-align: center !important;
    white-space: nowrap !important;
    transform: none !important;
}
div[style*="position:fixed"] .stButton > button:hover {
    background: var(--glow) !important;
    color: var(--accent) !important;
    border-color: var(--accent) !important;
    transform: none !important;
}

/* Disclaimer */
.disclaimer {
    margin: 14px 16px; padding: 13px 15px;
    background: rgba(224,123,0,0.05);
    border: 1px solid rgba(224,123,0,0.20);
    border-radius: var(--r2);
    font-size: 11.5px; color: rgba(255,176,32,0.7); line-height: 1.65;
}
.disclaimer strong { display: block; margin-bottom: 4px; font-size: 10.5px; letter-spacing: 0.6px; text-transform: uppercase; color: var(--amber); }

/* Language selectbox */
[data-testid="stSelectbox"] > div > div {
    background: var(--bg3) !important; border: 1px solid var(--border) !important;
    border-radius: var(--r2) !important; color: var(--text1) !important;
    font-family: var(--font-body) !important; font-size: 13px !important;
}

/* ── Chat topbar ── */
.chat-top {
    display: flex; align-items: center; justify-content: space-between;
    padding: 14px 26px;
    background: var(--bg1);
    border-bottom: 1px solid var(--border);
    box-shadow: 0 1px 6px rgba(0,80,160,0.05);
}
.chat-agent { display: flex; align-items: center; gap: 12px; }
.agent-av {
    width: 40px; height: 40px; border-radius: 11px;
    background: linear-gradient(135deg, #004E7A, #0091D2);
    display: flex; align-items: center; justify-content: center;
    font-size: 18px; border: 1px solid var(--border2);
}
.agent-nm { font-family: var(--font-head); font-size: 14px; font-weight: 600; color: var(--text0); }
.agent-st { font-size: 11.5px; color: var(--green); display: flex; align-items: center; gap: 5px; margin-top: 2px; }
.agent-st::before { content:''; width:5px; height:5px; background:var(--green); border-radius:50%; display:inline-block; }
.journey-pill { padding: 5px 13px; background: var(--glow2); border: 1px solid var(--border2); border-radius: 50px; font-size: 12px; font-weight: 500; color: var(--accent); }

/* ── Welcome card ── */
.welcome {
    background: linear-gradient(145deg, var(--bg2), var(--bg3));
    border: 1px solid var(--border2); border-radius: var(--r3);
    padding: 28px; margin: 24px; position: relative; overflow: hidden;
    animation: fadeUp 0.5s ease forwards;
}
.welcome::before {
    content:''; position:absolute; top:-60px; right:-60px;
    width:180px; height:180px;
    background: radial-gradient(circle, var(--glow) 0%, transparent 70%);
    pointer-events:none;
}
.welcome-title { font-family: var(--font-head); font-size: 22px; font-weight: 700; color: var(--text0); margin-bottom: 8px; line-height: 1.3; }
.welcome-title span { color: var(--accent); }
.welcome-sub { font-size: 14px; color: var(--text1); line-height: 1.65; margin-bottom: 20px; }
.cap-grid { display: grid; grid-template-columns: repeat(2,1fr); gap: 9px; }
.cap-item { display: flex; align-items: center; gap: 9px; padding: 10px 13px; background: var(--bg0); border: 1px solid var(--border); border-radius: var(--r1); font-size: 12.5px; color: var(--text1); }
.cap-dot { width: 6px; height: 6px; background: var(--accent); border-radius: 50%; flex-shrink: 0; }

/* ── Messages ── */
[data-testid="stChatMessage"] { background: transparent !important; border: none !important; padding: 4px 24px !important; }
[data-testid="stChatMessage"] p { font-family: var(--font-body) !important; font-size: 14px !important; line-height: 1.7 !important; color: var(--text0) !important; }

/* ── Step block ── */
.step-block {
    background: var(--bg2); border: 1px solid var(--border);
    border-radius: var(--r2); padding: 16px 18px; margin: 10px 0;
    animation: fadeUp 0.3s ease forwards;
}
.step-title { font-family: var(--font-head); font-size: 12.5px; font-weight: 600; color: var(--accent); margin-bottom: 10px; letter-spacing: 0.5px; text-transform: uppercase; }
.step-item { display: flex; align-items: flex-start; gap: 12px; padding: 9px 0; border-bottom: 1px solid var(--border); font-size: 13.5px; color: var(--text1); line-height: 1.65; }
.step-item:last-child { border-bottom: none; padding-bottom: 0; }
.step-num { min-width: 22px; height: 22px; background: var(--glow2); border: 1px solid var(--border2); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: 700; color: var(--accent); flex-shrink: 0; margin-top: 2px; }
.step-head { font-weight: 500; color: var(--text0); font-size: 13.5px; }

/* ── Source card ── */
.src-card {
    margin-top: 10px; padding: 11px 15px;
    background: rgba(0,145,210,0.06);
    border: 1px solid rgba(0,168,255,0.14);
    border-left: 3px solid var(--accent);
    border-radius: var(--r1);
    font-size: 12px; color: var(--text1); line-height: 1.6;
}
.src-card strong { color: var(--accent); font-size: 10.5px; text-transform: uppercase; letter-spacing: 1px; display: block; margin-bottom: 3px; }

/* ── Refusal card ── */
.refusal {
    background: rgba(217,48,37,0.04);
    border: 1px solid rgba(255,68,85,0.16);
    border-radius: var(--r2); padding: 14px 18px; margin: 8px 0;
    font-size: 13.5px; color: rgba(255,150,160,0.9); line-height: 1.65;
}
.refusal strong { display: block; margin-bottom: 5px; color: var(--red); font-size: 11px; text-transform: uppercase; letter-spacing: 0.8px; }

/* ── Follow-ups ── */
.followups { display: flex; flex-wrap: wrap; gap: 7px; margin-top: 12px; }
.fchip {
    padding: 6px 13px; background: var(--bg3);
    border: 1px solid var(--border2); border-radius: 50px;
    font-size: 12px; color: var(--text1);
    cursor: pointer; transition: all 0.15s;
}
.fchip:hover { background: var(--glow2); color: var(--accent); border-color: var(--accent); }

/* ── Feedback ── */
.fb-row { display: flex; align-items: center; gap: 8px; margin-top: 10px; padding-top: 10px; border-top: 1px solid var(--border); }
.fb-lbl { font-size: 11.5px; color: var(--text3); margin-right: 2px; }

/* ── Typing dots ── */
.dots { display: flex; align-items: center; gap: 5px; padding: 12px 4px; }
.dots span { width: 7px; height: 7px; background: var(--accent); border-radius: 50%; opacity: 0.4; animation: bounce 1.2s ease-in-out infinite; }
.dots span:nth-child(2) { animation-delay: 0.2s; }
.dots span:nth-child(3) { animation-delay: 0.4s; }
@keyframes bounce { 0%,100%{transform:translateY(0);opacity:0.3;} 50%{transform:translateY(-5px);opacity:1;} }

/* ── Chat input ── */
[data-testid="stChatInputContainer"],
[data-testid="stChatInputContainer"] *,
[data-testid="stBottom"],
[data-testid="stBottom"] > div,
[data-testid="stBottomBlockContainer"],
[data-testid="stBottomBlockContainer"] > div {
    background: var(--bg1) !important;
}
[data-testid="stChatInputContainer"] {
    border-top: 1px solid var(--border) !important;
    padding: 14px 22px !important;
}
[data-testid="stChatInputContainer"] > div {
    background: var(--bg3) !important;
    border: 1px solid var(--border2) !important;
    border-radius: var(--r3) !important;
}
[data-testid="stChatInputContainer"] textarea {
    background: var(--bg3) !important; color: var(--text0) !important;
    font-family: var(--font-body) !important; font-size: 14px !important;
    caret-color: var(--accent) !important;
}
[data-testid="stChatInputContainer"] textarea::placeholder { color: var(--text3) !important; }
[data-testid="stChatInputContainer"] button { background: var(--accent) !important; border-radius: 50% !important; border: none !important; }
[data-testid="stChatInputContainer"] button:hover { background: var(--accent2) !important; }

/* Force main content area background to follow theme */
[data-testid="stMain"],
[data-testid="stMainBlockContainer"],
section.main,
.main .block-container,
[data-testid="stVerticalBlock"] {
    background-color: var(--bg0) !important;
}

@keyframes fadeUp { from { opacity:0; transform:translateY(8px); } to { opacity:1; transform:translateY(0); } }
.fadein { animation: fadeUp 0.4s ease forwards; }
</style>
""", unsafe_allow_html=True)

# ─── SESSION STATE ─────────────────────────────────────────────────────────────
if "messages"      not in st.session_state: st.session_state.messages = []
if "theme"         not in st.session_state: st.session_state.theme = "light"
if "journey"       not in st.session_state: st.session_state.journey = "Departure"
if "pending_query" not in st.session_state: st.session_state.pending_query = None
if "feedback"      not in st.session_state: st.session_state.feedback = {}

# ─── DATA ──────────────────────────────────────────────────────────────────────
QUICK_QUESTIONS = [
    ("🪪", "Check-in Process", "Explain the airport check-in process"),
    ("🔍", "Security Screening", "What happens at security screening?"),
    ("🚪", "Boarding Procedure", "Walk me through the boarding procedure"),
    ("🧳", "Baggage Claim", "How does baggage claim work?"),
]

RESPONSES = {
    "check-in": {
        "type": "steps",
        "answer": "The check-in process registers you for your flight and involves document verification, baggage drop, and issuance of your boarding pass.",
        "steps": [
            ("Arrive at Terminal", "Reach the airport at least 2–3 hours before international flights, or 1.5 hours before domestic."),
            ("Locate Check-in Counter", "Find your airline's designated check-in zone. Look for your flight number on overhead display boards."),
            ("Present Documents", "Hand over your valid photo ID (Aadhaar / Passport) and booking confirmation to the check-in agent."),
            ("Baggage Drop", "Place checked baggage on the conveyor. Domestic limit: 15–25 kg. International: 20–30 kg depending on class."),
            ("Receive Boarding Pass", "Collect your boarding pass. Verify flight number, gate, seat, and boarding time before proceeding."),
        ],
        "source": "DGCA CAR Section 3, Series C — Ground Handling Requirements",
        "followups": ["What documents do I need for check-in?", "Can I do web check-in?", "What are baggage weight limits?"],
    },
    "security": {
        "type": "steps",
        "answer": "Security screening is mandatory and conducted by CISF at all Indian airports under BCAS regulations. Allow at least 30 minutes for this step.",
        "steps": [
            ("Join Security Queue", "Proceed to the security hold area post check-in. Keep your boarding pass and photo ID accessible."),
            ("Document Check", "Show boarding pass and ID to the CISF officer at the entry checkpoint for initial verification."),
            ("Baggage X-Ray", "Place all cabin baggage, laptop, and electronics separately on the conveyor belt for X-ray scanning."),
            ("Personal Frisking", "Walk through the Door Frame Metal Detector (DFMD). A hand-held detector check may follow."),
            ("Collect Belongings", "Retrieve items from the conveyor belt, reassemble your bag, and proceed to the departure gate."),
        ],
        "source": "BCAS Security Circular No. 04/2023 — Pre-Embarkation Security Check Procedures",
        "followups": ["What items are prohibited?", "Can I carry liquids through security?", "What is DFMD?"],
    },
    "boarding": {
        "type": "steps",
        "answer": "Boarding is organised in structured groups to ensure smooth passenger flow onto the aircraft. Reach your gate 30 minutes before departure.",
        "steps": [
            ("Gate Announcement", "Listen for boarding announcements on the PA system or monitor departure boards for your gate number."),
            ("Proceed to Gate", "Walk to your assigned departure gate. Allow 15–20 minutes buffer from security to gate."),
            ("Priority Boarding", "Passengers with special needs, families with infants, and business class board first."),
            ("Group Boarding", "Economy passengers board by row group. Check your boarding pass for your assigned group (A / B / C)."),
            ("Board Aircraft", "Present boarding pass at the gate scanner. Proceed through the jet bridge or airside bus to the aircraft."),
        ],
        "source": "AAI Aerodrome Operations Manual — Passenger Handling Procedures, Section 7.4",
        "followups": ["How early should I be at the gate?", "What if I miss boarding?", "Can I upgrade at the gate?"],
    },
    "baggage": {
        "type": "steps",
        "answer": "Baggage claim is the final step after landing. Follow the signs from the aircraft to the baggage reclaim hall and collect your bags from the designated carousel.",
        "steps": [
            ("Deplane and Follow Signs", "After landing, follow 'Baggage Claim' or 'Baggage Reclaim' signs through the terminal corridors."),
            ("Check Carousel Display", "Find your flight number on the overhead display board to identify your assigned carousel number."),
            ("Wait for Baggage", "Bags typically arrive 15–25 minutes after landing. Wait alongside the carousel without blocking others."),
            ("Identify Your Bag", "Collect your bag when it appears on the carousel. Verify the baggage tag number against your claim stub."),
            ("Report Issues Immediately", "If baggage is delayed or damaged, proceed to the airline's Baggage Services counter before exiting the terminal."),
        ],
        "source": "Passenger Rights Charter — Ministry of Civil Aviation, India (2022), Section 5",
        "followups": ["What if my bag is lost?", "How do I file a baggage damage claim?", "What are compensation rules?"],
    },
}

RESTRICTED = ["book", "cancel", "refund", "boarding pass", "modify", "change flight", "reschedule", "ticket price", "buy ticket", "purchase"]

def get_response(query: str) -> dict:
    q = query.lower()
    if any(k in q for k in RESTRICTED):
        return {"type": "refusal", "message": "This assistant is designed to explain airport processes only. For bookings, cancellations, or flight modifications please contact your airline directly or visit the ticketing counter inside the terminal."}
    if "check" in q and "in" in q: return RESPONSES["check-in"]
    if any(k in q for k in ["secur", "frisking", "screening", "cisf", "xray", "x-ray"]): return RESPONSES["security"]
    if any(k in q for k in ["board", "gate", "embark"]): return RESPONSES["boarding"]
    if any(k in q for k in ["baggage", "luggage", "claim", "carousel", "bag"]): return RESPONSES["baggage"]
    return {"type": "text", "answer": "I can explain airport check-in, security screening, boarding, and baggage claim procedures. Please use the quick questions on the left or type your question below.", "followups": [q[2] for q in QUICK_QUESTIONS]}

def render_response(resp: dict, msg_idx: int):
    rtype = resp.get("type")
    if rtype == "refusal":
        st.markdown(f'<div class="refusal"><strong>Outside Scope</strong>{resp["message"]}</div>', unsafe_allow_html=True)
    elif rtype == "steps":
        st.markdown(f'<p style="margin-bottom:10px;color:var(--text1);font-size:13.5px;">{resp["answer"]}</p>', unsafe_allow_html=True)
        items = "".join([f'<div class="step-item"><div class="step-num">{i+1}</div><div><div class="step-head">{t}</div>{d}</div></div>' for i,(t,d) in enumerate(resp["steps"])])
        st.markdown(f'<div class="step-block"><div class="step-title">Step-by-Step Process</div>{items}</div>', unsafe_allow_html=True)
        if resp.get("source"):
            st.markdown(f'<div class="src-card"><strong>Source</strong>{resp["source"]}</div>', unsafe_allow_html=True)
        if resp.get("followups"):
            chips = "".join([f'<div class="fchip" onclick="setInput(this)">{f}</div>' for f in resp["followups"]])
            st.markdown(f'<div class="followups">{chips}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<p>{resp.get("answer","")}</p>', unsafe_allow_html=True)
        if resp.get("followups"):
            chips = "".join([f'<div class="fchip">{f}</div>' for f in resp["followups"][:4]])
            st.markdown(f'<div class="followups">{chips}</div>', unsafe_allow_html=True)

    # Feedback row
    fkey = f"fb_{msg_idx}"
    fb = st.session_state.feedback.get(fkey)
    if fb is None:
        c1, c2, c3 = st.columns([3, 1, 1])
        with c1: st.markdown('<div class="fb-lbl">Was this helpful?</div>', unsafe_allow_html=True)
        with c2:
            if st.button("Helpful", key=f"up_{msg_idx}"):
                st.session_state.feedback[fkey] = "up"; st.rerun()
        with c3:
            if st.button("Not Clear", key=f"dn_{msg_idx}"):
                st.session_state.feedback[fkey] = "down"; st.rerun()
    elif fb == "up":
        st.markdown('<div style="font-size:12px;color:var(--green);margin-top:8px;">Glad I could help.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="font-size:12px;color:var(--text2);margin-top:8px;">Thank you for the feedback.</div>', unsafe_allow_html=True)

# ─── TOP BAR ───────────────────────────────────────────────────────────────────
_theme = st.session_state.theme
_toggle_icon = "🌙" if _theme == "light" else "☀️"
_toggle_label = "Dark Mode" if _theme == "light" else "Light Mode"

st.markdown(f"""
<div class="topbar fadein" id="topbar">
  <div class="topbar-brand">
    <div class="brand-mark">✈</div>
    <div class="brand-name">Aero<em>Guide</em></div>
  </div>
  <div class="topbar-nav">
    <div class="nav-link nav-active">Assistant</div>
    <div class="nav-link">How It Works</div>
    <div class="nav-link">About</div>
  </div>
  <div style="display:flex;align-items:center;gap:12px;">
    <div class="live-badge"><div class="live-dot"></div>AI Online</div>
  </div>
</div>
<div class="main-offset"></div>
""", unsafe_allow_html=True)

# Theme toggle button — placed via Streamlit so it actually works
_tcol1, _tcol2, _tcol3 = st.columns([6, 1, 1])
with _tcol3:
    st.markdown(f'<div style="position:fixed;top:10px;right:16px;z-index:2000;">', unsafe_allow_html=True)
    if st.button(f"{_toggle_icon} {_toggle_label}", key="theme_toggle"):
        st.session_state.theme = "dark" if _theme == "light" else "light"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ─── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    # Journey selector — st.columns keeps them truly side-by-side
    j = st.session_state.journey
    st.markdown('<div class="sb-section"><div class="sb-label">Passenger Journey</div>', unsafe_allow_html=True)
    journey_options = [("🛫", "Departure"), ("🛬", "Arrival"), ("🔄", "Transit")]
    col1, col2, col3 = st.columns(3, gap="small")
    for col, (icon, label) in zip([col1, col2, col3], journey_options):
        with col:
            active_cls = "jbtn-active" if j == label else ""
            st.markdown(f'<div class="jbtn {active_cls}">', unsafe_allow_html=True)
            if st.button(icon, key=f"journey_{label}"):
                st.session_state.journey = label
                st.rerun()
            lc = "var(--accent)" if j == label else "var(--text2)"
            st.markdown(f'<div class="jbtn-label" style="color:{lc};">{label}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Quick Questions — redesigned ──
    st.markdown('<div class="sb-section"><div class="sb-label">Quick Questions</div>', unsafe_allow_html=True)
    st.markdown('<div class="qq-wrap">', unsafe_allow_html=True)
    for icon, label, query in QUICK_QUESTIONS:
        if st.button(f"{icon}  {label}", key=f"qq_{label}"):
            st.session_state.pending_query = query
    st.markdown('</div></div>', unsafe_allow_html=True)

    # Clear
    st.markdown('<div class="sb-section" style="border-bottom:none;"><div class="clear-wrap">', unsafe_allow_html=True)
    if st.button("Clear Conversation", key="clear"):
        st.session_state.messages = []
        st.session_state.pending_query = None
        st.rerun()
    st.markdown('</div></div>', unsafe_allow_html=True)

    # Disclaimer
    st.markdown("""
    <div class="disclaimer">
      <strong>Important Notice</strong>
      This assistant provides informational guidance only. It cannot issue boarding passes, make bookings, cancel flights, or modify reservations. For operational assistance please contact airport staff or your airline.
    </div>
    """, unsafe_allow_html=True)

# ─── CHAT AREA ─────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="chat-top fadein">
  <div class="chat-agent">
    <div class="agent-av">✈</div>
    <div>
      <div class="agent-nm">AeroGuide AI Assistant</div>
      <div class="agent-st">Ready to assist</div>
    </div>
  </div>
  <div class="journey-pill">{st.session_state.journey} Mode</div>
</div>
""", unsafe_allow_html=True)

# Welcome state
if not st.session_state.messages:
    st.markdown("""
    <div class="welcome">
      <div class="welcome-title">Welcome to <span>AeroGuide</span></div>
      <div class="welcome-sub">Your intelligent airport companion. Ask me anything about check-in, security screening, boarding procedures, or baggage claim — I will guide you step by step with cited sources.</div>
      <div class="cap-grid">
        <div class="cap-item"><div class="cap-dot"></div>Check-in procedures</div>
        <div class="cap-item"><div class="cap-dot"></div>Security screening</div>
        <div class="cap-item"><div class="cap-dot"></div>Boarding process</div>
        <div class="cap-item"><div class="cap-dot"></div>Baggage claim</div>
        <div class="cap-item"><div class="cap-dot"></div>Transit guidance</div>
        <div class="cap-item"><div class="cap-dot"></div>Document requirements</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# Render history
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        if msg["role"] == "user":
            st.markdown(f'<p>{msg["content"]}</p>', unsafe_allow_html=True)
        else:
            render_response(msg["response"], i)

# ─── INPUT HANDLING ────────────────────────────────────────────────────────────
user_input = st.chat_input("Ask about check-in, security, boarding, baggage...")

if st.session_state.pending_query:
    user_input = st.session_state.pending_query
    st.session_state.pending_query = None

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(f'<p>{user_input}</p>', unsafe_allow_html=True)

    with st.chat_message("assistant"):
        ph = st.empty()
        ph.markdown('<div class="dots"><span></span><span></span><span></span></div>', unsafe_allow_html=True)
        time.sleep(1.1)
        ph.empty()
        response = get_response(user_input)
        idx = len(st.session_state.messages)
        render_response(response, idx)

    st.session_state.messages.append({"role": "assistant", "content": user_input, "response": response})

# ─── THEME JS ─────────────────────────────────────────────────────────────────
_theme_val = st.session_state.theme
st.components.v1.html(f"""
<script>
  (function() {{
    var theme = "{_theme_val}";
    function applyTheme() {{
      var root = window.parent.document.documentElement;
      root.setAttribute("data-theme", theme);
      // also apply to body and stApp for full coverage
      var body = window.parent.document.body;
      if (body) body.setAttribute("data-theme", theme);
      var app = window.parent.document.querySelector(".stApp");
      if (app) app.setAttribute("data-theme", theme);
    }}
    applyTheme();
    setTimeout(applyTheme, 100);
    setTimeout(applyTheme, 400);
  }})();
</script>
""", height=0)

# ─── AUTO-SCROLL JS ────────────────────────────────────────────────────────────
st.components.v1.html("""
<script>
  (function() {
    function scroll() {
      const main = window.parent.document.querySelector('section.main');
      if (main) main.scrollTop = main.scrollHeight;
    }
    setTimeout(scroll, 150);
    setTimeout(scroll, 500);
  })();
</script>
""", height=0)
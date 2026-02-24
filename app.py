import streamlit as st
import re
import os
import streamlit.components.v1 as components
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# --- 1. CONFIG & STYLING ---
st.set_page_config(page_title="Cyfer Pro: Secret Language", layout="centered")

raw_pepper = st.secrets.get("MY_SECRET_PEPPER") or "default_fallback_spice_2026"
PEPPER = str(raw_pepper)

st.markdown(f"""
    <style>
    /* Periwinkle Background */
    .stApp {{ background-color: #DBDCFF !important; }}
    
    /* Remove the App Status box and extra space */
    div[data-testid="stWidgetLabel"], label {{ display: none !important; }}

    /* INPUTS - FIXED DEEP PURPLE TEXT */
    .stTextInput > div > div > input, 
    .stTextArea > div > div > textarea {{
        background-color: #FEE2E9 !important;
        color: #5D5379 !important; /* Deep Purple for maximum readability */
        border: 2px solid #B4A7D6 !important;
        font-family: "Courier New", Courier, monospace !important;
        font-size: 18px !important;
        font-weight: bold !important;
        -webkit-text-fill-color: #5D5379 !important; /* Fix for mobile browser ghosting */
    }}

    /* BUTTONS - FORCED FULL WIDTH STACK */
    .stButton {{
        width: 100% !important;
        margin-bottom: 0px !important;
    }}

    .stButton > button {{
        width: 100% !important;
        background-color: #B4A7D6 !important; 
        color: #FFD4E5 !important;
        border-radius: 15px !important;
        min-height: 90px !important; 
        border: none !important;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
        margin: 5px 0px !important;
    }}

    .stButton > button p {{
        font-size: 34px !important; 
        font-weight: 850 !important;
        line-height: 1.1 !important;
        color: #FFD4E5 !important;
    }}

    /* RESULT BOX */
    .result-box {{
        background-color: #FEE2E9; 
        color: #B4A7D6;
        padding: 15px;
        border-radius: 10px;
        font-family: "Courier New", Courier, monospace !important;
        border: 2px solid #B4A7D6;
        font-weight: bold;
        margin-bottom: 20px;
    }}

    /* FOOTER - SIMPLE CENTERING */
    .custom-footer {{
        text-align: center;
        margin-top: 40px;
        width: 100%;
    }}

    .created-by {{
        color: #B4A7D6;
        font-family: "Courier New", Courier, monospace;
        font-size: 20px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 10px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE PRO ENGINE ---
char_to_coord = {
    'Q': (2, 25), 'W': (5, 25), 'E': (8, 25), 'R': (11, 25), 'T': (14, 25), 'Y': (17, 25), 'U': (20, 25), 'I': (23, 25), 'O': (26, 25), 'P': (29, 25),
    'A': (3, 20), 'S': (6, 20), 'D': (9, 20), 'F': (12, 20), 'G': (15, 20), 'H': (18, 20), 'J': (21, 20), 'K': (24, 20), 'L': (27, 20),
    'Z': (4, 15), 'X': (7, 15), 'C': (10, 15), 'V': (13, 15), 'B': (16, 15), 'N': (19, 15), 'M': (22, 15),
    '1': (2, 10), '2': (5, 10), '3': (8, 10), '4': (11, 10), '5': (14, 10), '6': (17, 10), '7': (20, 10), '8': (23, 10), '9': (26, 10), '0': (29, 10),
    '!': (5, 5),  ',': (10, 5), '.': (15, 5), ' ': (20, 5), '?': (25, 5)
}
coord_to_char = {v: k for k, v in char_to_coord.items()}
EMOJI_MAP = {'1': '🦄', '2': '🍼', '3': '🩷', '4': '🧸', '5': '🎀', '6': '🍓', '7': '🌈', '8': '🌸', '9': '💕', '0': '🫐'}

def get_matrix_elements(key_string):
    salt = b"sweet_parity_salt_v2" 
    combined_input = key_string + PEPPER 
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=4, salt=salt, iterations=100000, backend=default_backend())
    a, b, c, d = list(kdf.derive(combined_input.encode()))
    return (a % 10 + 2, b % 7 + 1, c % 5 + 1, d % 13 + 2)

# --- 3. UI LAYOUT ---
if os.path.exists("CYPHER.png"): st.image("CYPHER.png")
if os.path.exists("Lock Lips.png"): st.image("Lock Lips.png")

kw = st.text_input("Key", type="password", key="lips", placeholder="SECRET KEY").upper().strip()
hint_text = st.text_input("Hint", key="hint", placeholder="KEY HINT (Optional)")

if os.path.exists("Kiss Chemistry.png"): st.image("Kiss Chemistry.png")
user_input = st.text_area("Message", height=120, key="chem", placeholder="YOUR MESSAGE")

output_placeholder = st.empty()

# FORCE VERTICAL STACK FOR BUTTONS
kiss_btn = st.button("KISS")
tell_btn = st.button("TELL")
destroy_btn = st.button("DESTROY CHEMISTRY")

if destroy_btn:
    st.session_state.lips = ""
    st.session_state.chem = ""
    st.session_state.hint = ""
    st.rerun()

# THE CLEAN FOOTER
st.markdown('<div class="custom-footer">', unsafe_allow_html=True)
if os.path.exists("LPB.png"):
    st.image("LPB.png", width=180)
st.markdown('<div class="created-by">CREATED BY</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- 4. ENGINE LOGIC ---
# (Rest of code continues)

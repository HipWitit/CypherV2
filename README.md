import streamlit as st
import re
import os
import streamlit.components.v1 as components

# --- 1. CONFIG & STYLING ---
st.set_page_config(page_title="Cyfer's Secret Love Language", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #E6E1F2 !important; }
    div[data-testid="stWidgetLabel"], label { display: none !important; }

    /* INPUT BOX CUSTOMIZATION */
    .stTextInput > div > div > input, 
    .stTextArea > div > div > textarea,
    input::placeholder, textarea::placeholder {
        background-color: #FEE2E9 !important;
        color: #B4A7D6 !important; 
        border: 2px solid #B4A7D6 !important;
        font-family: "Courier New", Courier, monospace !important;
        font-size: 18px !important;
        font-weight: bold !important;
    }

    /* THE "GOLDILOCKS" BUTTONS */
    div.stButton > button p {
        font-size: 55px !important;
        font-weight: 800 !important;
        line-height: 1.1 !important;
        margin: 0 !important;
    }

    div.stButton > button {
        background-color: #B4A7D6 !important; 
        color: #FFD4E5 !important;
        border-radius: 15px !important;
        min-height: 110px !important; 
        height: auto !important;     
        border: none !important;
        width: 100% !important;
        text-transform: uppercase;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    }

    /* DESTROY BUTTON */
    div[data-testid="stVerticalBlock"] > div:last-child .stButton > button p {
        font-size: 22px !important;
    }
    div[data-testid="stVerticalBlock"] > div:last-child .stButton > button {
        min-height: 60px !important;
    }

    .result-box {
        background-color: #FEE2E9; 
        color: #B4A7D6;
        padding: 15px;
        border-radius: 10px;
        font-family: "Courier New", Courier, monospace !important;
        border: 2px solid #B4A7D6;
        word-wrap: break-word;
        margin-top: 10px;
        font-weight: bold;
    }

    .whisper-text {
        color: #B4A7D6;
        font-family: "Courier New", Courier, monospace !important;
        font-weight: bold;
        font-size: 28px;
        margin-top: 15px;
        border-top: 2px dashed #B4A7D6;
        padding-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. MATH & EMOJI ENGINE ---
char_to_coord = {
    'Q': (2, 25), 'W': (5, 25), 'E': (8, 25), 'R': (11, 25), 'T': (14, 25), 'Y': (17, 25), 'U': (20, 25), 'I': (23, 25), 'O': (26, 25), 'P': (29, 25),
    'A': (3, 20), 'S': (6, 20), 'D': (9, 20), 'F': (12, 20), 'G': (15, 20), 'H': (18, 20), 'J': (21, 20), 'K': (24, 20), 'L': (27, 20),
    'Z': (4, 15), 'X': (7, 15), 'C': (10, 15), 'V': (13, 15), 'B': (16, 15), 'N': (19, 15), 'M': (22, 15),
    '1': (2, 10), '2': (5, 10), '3': (8, 10), '4': (11, 10), '5': (14, 10), '6': (17, 10), '7': (20, 10), '8': (23, 10), '9': (26, 10), '0': (29, 10),
    '!': (5, 5),  ',': (10, 5), '.': (15, 5), ' ': (20, 5), '?': (25, 5)
}
coord_to_char = {v: k for k, v in char_to_coord.items()}
EMOJI_MAP = {'1': '🦄', '2': '🍼', '3': '🩷', '4': '🧸', '5': '🎀', '6': '🍓', '7': '🌈', '8': '🌸', '9': '💕', '0': '🫐'}

def apply_sweet_parity(val_str):
    def replacer(match):
        digit = match.group(2)
        candy = '🍭' if int(digit) % 2 == 0 else '🍬'
        return candy + digit
    return re.sub(r'(-)(\d)', replacer, val_str)

def get_matrix_elements(key):
    seed = sum(ord(c) for c in key)
    return (seed % 7 + 2, seed % 5 + 1, seed % 3 + 1, seed % 11 + 2)

def modInverse(n, m=31):
    for x in range(1, m):
        if (((n % m) * (x % m)) % m == 1): return x
    return None

def clear_everything():
    st.session_state.lips = ""
    st.session_state.chem = ""
    st.session_state.hint = ""

# --- 3. UI LAYOUT (RESTORED) ---
if os.path.exists("CYPHER.png"): st.image("CYPHER.png", width="stretch")
if os.path.exists("Lock Lips.png"): st.image("Lock Lips.png", width="stretch")

kw = st.text_input("Key", type="password", key="lips", placeholder="SECRET KEY").upper().strip()
hint_text = st.text_input("Hint", key="hint", placeholder="KEY HINT (Optional)")

if os.path.exists("Kiss Chemistry.png"): st.image("Kiss Chemistry.png", width="stretch")
user_input = st.text_area("Message", height=120, key="chem", placeholder="YOUR MESSAGE")

output_placeholder = st.empty()

col1, col2 = st.columns(2)
with col1:
    kiss_btn = st.button("KISS", width="stretch")
with col2:
    tell_btn = st.button("TELL", width="stretch")

st.button("DESTROY CHEMISTRY", width="stretch", on_click=clear_everything)

# --- 4. PROCESSING LOGIC (ADVANCED) ---
if kw and (kiss_btn or tell_btn):
    a, b, c, d = get_matrix_elements(kw)
    det_inv = modInverse((a * d - b * c) % 31)
    
    if det_inv:
        if kiss_btn:
            points = []
            for char in user_input.upper():
                if char in char_to_coord:
                    x, y = char_to_coord[char]
                    nx, ny = (a*x + b*y) % 31, (c*x + d*y) % 31
                    points.append((nx, ny))
            
            if points:
                # 1. Header (Index 0) -> Reverse
                h_x = "".join(EMOJI_MAP.get(c, c) for c in apply_sweet_parity(str(points[0][0])))
                h_y = "".join(EMOJI_MAP.get(c, c) for c in apply_sweet_parity(str(points[0][1])))
                header = f"{h_x[::-1]},{h_y[::-1]}"
                
                # 2. Moves
                moves_list = []
                for i in range(len(points)-1):
                    dx_v = points[i+1][0] - points[i][0]
                    dy_v = points[i+1][1] - points[i][1]
                    
                    dx = "".join(EMOJI_MAP.get(c, c) for c in apply_sweet_parity(str(dx_v)))
                    dy = "".join(EMOJI_MAP.get(c, c) for c in apply_sweet_parity(str(dy_v)))
                    
                    # Mirror Rule: Every second move reversed
                    if (i + 1) % 2 == 0:
                        moves_list.append(f"({dx[::-1]},{dy[::-1]})")
                    else:
                        moves_list.append(f"({dx},{dy})")
                
                emoji_res = f"{header} | MOVES: {' '.join(moves_list)}"
                with output_placeholder.container():
                    st.markdown(f'<div class="result-box">{emoji_res}</div>', unsafe_allow_html=True)
                    if hint_text: st.caption(f"Hint: {hint_text}")
                    share_html = f"""<button onclick="navigator.share({{title:'Secret',text:`{emoji_res}\\n\\nHint: {hint_text}`}})" style="background-color:#B4A7D6; color:#FFD4E5; font-weight:bold; border-radius:20px; min-height:80px; width:100%; cursor:pointer; font-size: 32px; border:none; text-transform:uppercase;">SHARE OPTIONS ✨</button>"""
                    components.html(share_html, height=100)

        if tell_btn:
            try:
                clean_input = user_input.split("Hint:")[0].strip()
                header_part, moves_part = clean_input.split("|")
                rev_map = {v: k for k, v in EMOJI_MAP.items()}
                
                def emoji_to_math(s):
                    s = "".join(rev_map.get(c, c) for c in s)
                    return int(s.replace('🍭', '-').replace('🍬', '-'))

                # Decode Header (Always Reversed)
                hx_e, hy_e = header_part.strip().split(",")
                curr_x, curr_y = emoji_to_math(hx_e[::-1]), emoji_to_math(hy_e[::-1])
                
                inv_a, inv_b = (d * det_inv) % 31, (-b * det_inv) % 31
                inv_c, inv_d = (-c * det_inv) % 31, (a * det_inv) % 31
                ux, uy = (inv_a * curr_x + inv_b * curr_y) % 31, (inv_c * curr_x + inv_d * curr_y) % 31
                decoded = [coord_to_char.get((ux, uy), "?")]
                
                # Decode Moves
                moves = re.findall(r"\(([^)]+)\)", moves_part)
                for i, m in enumerate(moves):
                    dx_e, dy_e = m.split(",")
                    if (i + 1) % 2 == 0:
                        dx, dy = emoji_to_math(dx_e[::-1]), emoji_to_math(dy_e[::-1])
                    else:
                        dx, dy = emoji_to_math(dx_e), emoji_to_math(dy_e)
                    curr_x += dx
                    curr_y += dy
                    ux, uy = (inv_a * curr_x + inv_b * curr_y) % 31, (inv_c * curr_x + inv_d * curr_y) % 31
                    decoded.append(coord_to_char.get((ux, uy), "?"))
                
                output_placeholder.markdown(f'<div class="whisper-text">Cypher Whispers: {"".join(decoded)}</div>', unsafe_allow_html=True)
            except:
                st.error("Chemistry Error!")

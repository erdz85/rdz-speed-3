import streamlit as st
import pandas as pd
import os

# ==========================================
# 1. KINEMATIC ENGINE (Math Logic)
# ==========================================
def get_unified_projection(session_type, fat_time, block_val, fly_val, gender):
    is_female = 'female' in str(gender).lower()
    f_val = fly_val if (fly_val and fly_val > 0) else fat_time
    b_val = block_val if (block_val and block_val > 0) else None
    
    if b_val is not None:
        base_proj = b_val + (3.5 * f_val)
        c = (0.15 if base_proj < 12.2 else 0.25) if is_female else (0.12 if base_proj < 11.0 else 0.18)
        return round(b_val + (3.5 * f_val) + c, 2)
    else:
        gender_const = 1.15 if is_female else 1.05 
        projection = (f_val / 2 * 10) + gender_const
        return round(projection, 2)

def get_go_mark_logic(f, b, gen):
    steps = (((20 / (f if f != 99.0 else 2.20)) * ((b if b != 99.0 else 4.20) * 0.71)) - 20 - 0.70) * 3.28
    raw = int(round(steps))
    if 'female' in str(gen).lower():
        tier = "Varsity" if (15 <= raw <= 22) else "Developing"
    else:
        tier = "Varsity" if (19 <= raw <= 26) else "Developing"
    return raw, tier

# ==========================================
# 2. DATA PERSISTENCE (Foundation)
# ==========================================
def init_app():
    if not os.path.exists("roster.csv"):
        pd.DataFrame(columns=["name", "gender", "grade"]).to_csv("roster.csv", index=False)
    if "roster" not in st.session_state:
        st.session_state.roster = pd.read_csv("roster.csv")

def save_data():
    st.session_state.roster.to_csv("roster.csv", index=False)

# ==========================================
# 3. ROSTER MODULE (The Interface)
# ==========================================
def roster_module():
    st.header("👤 Roster Management")
    
    with st.form("add_athlete"):
        name = st.text_input("Athlete Name")
        gender = st.selectbox("Gender", ["Male", "Female"])
        grade = st.selectbox("Grade", [9, 10, 11, 12])
        if st.form_submit_button("Add Athlete"):
            new_row = pd.DataFrame({"name": [name], "gender": [gender], "grade": [grade]})
            st.session_state.roster = pd.concat([st.session_state.roster, new_row], ignore_index=True)
            save_data()
            st.success(f"Added {name}!")

    if not st.session_state.roster.empty:
        st.dataframe(st.session_state.roster)
        delete_name = st.selectbox("Select athlete to remove", st.session_state.roster["name"].unique())
        if st.button("Delete Athlete"):
            st.session_state.roster = st.session_state.roster[st.session_state.roster["name"] != delete_name]
            save_data()
            st.rerun()

# ==========================================
# MAIN EXECUTION (Where the app actually runs)
# ==========================================
init_app()
st.title("Track Performance Tracker")
roster_module()

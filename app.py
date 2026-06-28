import streamlit as st
import pandas as pd
import os

# ==========================================
# 1. KINEMATIC ENGINE
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
    tier = "Varsity" if (15 <= raw <= 22 if 'female' in str(gen).lower() else 19 <= raw <= 26) else "Developing"
    return raw, tier

# ==========================================
# 2. DATA PERSISTENCE (Updated)
# ==========================================
def init_app():
    # 1. Roster
    if not os.path.exists("roster.csv"):
        pd.DataFrame(columns=["name", "gender", "grade"]).to_csv("roster.csv", index=False)
    if "roster" not in st.session_state:
        st.session_state.roster = pd.read_csv("roster.csv")
    
    # 2. Fly Sessions
    if not os.path.exists("fly_sessions.csv"):
        pd.DataFrame(columns=["name", "fly_time", "mph", "projection", "date"]).to_csv("fly_sessions.csv", index=False)
    if "fly_sessions" not in st.session_state:
        st.session_state.fly_sessions = pd.read_csv("fly_sessions.csv")
        
    # 3. Block Sessions
    if not os.path.exists("block_sessions.csv"):
        pd.DataFrame(columns=["name", "block_time", "date"]).to_csv("block_sessions.csv", index=False)
    if "block_sessions" not in st.session_state:
        st.session_state.block_sessions = pd.read_csv("block_sessions.csv")


def save_block_data():
    st.session_state.block_sessions.to_csv("block_sessions.csv", index=False)

def save_data():
    st.session_state.roster.to_csv("roster.csv", index=False)

def save_fly_data(): # Add this new save function
    st.session_state.fly_sessions.to_csv("fly_sessions.csv", index=False)


# ==========================================
# 3. MODULES
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
    
    st.dataframe(st.session_state.roster)
    if not st.session_state.roster.empty:
        delete_name = st.selectbox("Select athlete to remove", st.session_state.roster["name"].unique())
        if st.button("Delete Athlete"):
            st.session_state.roster = st.session_state.roster[st.session_state.roster["name"] != delete_name]
            save_data()
            st.rerun()

def fly_module():
    st.header("🪰 20m Fly Log")
    
    with st.form("add_fly"):
        athlete = st.selectbox("Select Athlete", st.session_state.roster["name"].unique())
        fly_time = st.number_input("20m Fly Time (seconds)", min_value=1.0, step=0.01)
        if st.form_submit_button("Log Session"):
            # Calculate metrics using the Engine
            mph = round((20 / fly_time) * 2.237, 2)
            proj = get_unified_projection("Fly", fly_time, None, fly_time, "Male") 
            
            new_entry = pd.DataFrame({
                "name": [athlete], "fly_time": [fly_time], 
                "mph": [mph], "projection": [proj], "date": [pd.Timestamp.now().date()]
            })
            st.session_state.fly_sessions = pd.concat([st.session_state.fly_sessions, new_entry], ignore_index=True)
            save_fly_data()
            st.success(f"Logged {fly_time}s for {athlete}")

    st.subheader("Recent Sessions")
    st.dataframe(st.session_state.fly_sessions)
    
    if not st.session_state.fly_sessions.empty:
        idx_to_del = st.selectbox("Select row to delete", st.session_state.fly_sessions.index)
        if st.button("Delete Selected Session"):
            st.session_state.fly_sessions = st.session_state.fly_sessions.drop(idx_to_del)
            save_fly_data()
            st.rerun()
            
def block_module():
    st.header("🚀 30m Block Start Log")
    
    with st.form("add_block"):
        athlete = st.selectbox("Select Athlete", st.session_state.roster["name"].unique())
        block_time = st.number_input("30m Block Time (seconds)", min_value=1.0, step=0.01)
        if st.form_submit_button("Log Session"):
            new_entry = pd.DataFrame({
                "name": [athlete], "block_time": [block_time], 
                "date": [pd.Timestamp.now().date()]
            })
            st.session_state.block_sessions = pd.concat([st.session_state.block_sessions, new_entry], ignore_index=True)
            save_block_data()
            st.success(f"Logged {block_time}s for {athlete}")

    st.subheader("Recent Sessions")
    st.dataframe(st.session_state.block_sessions)
    
    if not st.session_state.block_sessions.empty:
        idx_to_del = st.selectbox("Select row to delete", st.session_state.block_sessions.index)
        if st.button("Delete Selected Block Session"):
            st.session_state.block_sessions = st.session_state.block_sessions.drop(idx_to_del)
            save_block_data()
            st.rerun()

def combined_module():
    st.header("🔗 Combined 100m Projection")
    
    # Check if we have data to avoid errors
    if st.session_state.fly_sessions.empty or st.session_state.block_sessions.empty:
        st.warning("Please log both a Fly and a Block session to see a projection.")
        return

    athlete = st.selectbox("Select Athlete for Projection", st.session_state.roster["name"].unique())
    
    # Filter data for this athlete
    athlete_fly = st.session_state.fly_sessions[st.session_state.fly_sessions["name"] == athlete]
    athlete_block = st.session_state.block_sessions[st.session_state.block_sessions["name"] == athlete]
    
    if not athlete_fly.empty and not athlete_block.empty:
        # Get most recent values
        latest_fly = athlete_fly.iloc[-1]["fly_time"]
        latest_block = athlete_block.iloc[-1]["block_time"]
        gender = st.session_state.roster[st.session_state.roster["name"] == athlete]["gender"].values[0]
        
        # Calculate
        proj = get_unified_projection("Combined", 0, latest_block, latest_fly, gender)
        
        st.metric(label="Projected 100m Time", value=f"{proj} seconds")
        st.write(f"Based on: {latest_fly}s Fly and {latest_block}s Block Start")
    else:
        st.warning("Selected athlete needs data in both modules.")
def meet_module(): st.header("📅 Official Meet Results")
def progress_module(): st.header("📈 Athlete Progress")
def leaderboard_module(): st.header("🏆 Team Leaderboard")
def relay_module(): st.header("⚡ Relay Optimizer & Go Marks")

# ==========================================
# 4. MAIN EXECUTION
# ==========================================
init_app()
st.title("Track Performance Tracker")

tabs = st.tabs(["👤 Roster", "🪰 Fly", "🚀 Block", "🔗 Combined", "📅 Meets", "📈 Progress", "🏆 Leaderboard", "⚡ Relay"])

with tabs[0]: roster_module()
with tabs[1]: fly_module()
with tabs[2]: block_module()
with tabs[3]: combined_module()
with tabs[4]: meet_module()
with tabs[5]: progress_module()
with tabs[6]: leaderboard_module()
with tabs[7]: relay_module()
    

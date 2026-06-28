import streamlit as st
import pandas as pd
import os
from fpdf import FPDF

def get_unified_projection(session_type, fat_time, block_val, fly_val, gender):
    is_female = 'female' in str(gender).lower()
    
    # 1. Logic for Fly or Combined sessions
    if session_type in ["Fly", "Combined"]:
        # Use precision Kinematic math if a block start exists
        if block_val and block_val > 0:
            base_proj = block_val + (3.5 * fly_val)
            c = (0.15 if base_proj < 12.2 else 0.25) if is_female else (0.12 if base_proj < 11.0 else 0.18)
            return round(base_proj + c, 2)
        # Otherwise, use your 10m Split Equivalent formula
        else:
            gender_const = 1.15 if is_female else 1.05
            return round(((fly_val / 2) * 10) + gender_const, 2)
            
    return 0.0

def get_go_mark_logic(f, b, gen):
    # Keeping your existing go mark logic intact as requested
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
   
    # --- Add to init_app ---
    if not os.path.exists("meet_results.csv"):
        pd.DataFrame(columns=["name", "race", "time", "meet_name", "date"]).to_csv("meet_results.csv", index=False)
    if "meet_results" not in st.session_state:
        st.session_state.meet_results = pd.read_csv("meet_results.csv")

# --- Add new save function ---
def save_meet_data():
    st.session_state.meet_results.to_csv("meet_results.csv", index=False)

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
            # Look up gender from roster (Keeping your feature)
            gender = st.session_state.roster.loc[st.session_state.roster['name'] == athlete, 'gender'].iloc[0]
            
            # Calculate metrics
            mph = round((20 / fly_time) * 2.237, 2)
            # Pass 0 for block_time to trigger the Fly-only formula
            proj = get_unified_projection(fly_time, 0, gender) 
            
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
        idx_to_del = st.selectbox("Select row to delete", st.session_state.fly_sessions.index, key="del_fly")
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
        idx_to_del = st.selectbox("Select row to delete", st.session_state.block_sessions.index, key="del_block")
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
        # Add this section at the bottom of your combined_module function
    st.subheader("Delete Combined Session")
    if not st.session_state.combined_sessions.empty:
        idx_to_del = st.selectbox("Select row to delete", st.session_state.combined_sessions.index, key="del_combined")
        if st.button("Delete Selected Combined Session"):
            st.session_state.combined_sessions = st.session_state.combined_sessions.drop(idx_to_del)
            # Make sure your save function is called here
            save_combined_data() 
            st.rerun()
            
def meet_module():
    st.header("📅 Official Meet Results")
    
    with st.form("add_meet_result"):
        athlete = st.selectbox("Select Athlete", st.session_state.roster["name"].unique())
        race = st.selectbox("Race", ["100m", "200m", "400m"])
        time = st.number_input("Time (seconds)", min_value=5.0, step=0.01)
        meet_name = st.text_input("Meet Name")
        date = st.date_input("Date")
        
        if st.form_submit_button("Log Result"):
            new_entry = pd.DataFrame({
                "name": [athlete], "race": [race], "time": [time], 
                "meet_name": [meet_name], "date": [date]
            })
            st.session_state.meet_results = pd.concat([st.session_state.meet_results, new_entry], ignore_index=True)
            save_meet_data()
            st.success("Result logged!")

    st.subheader("Results Database")
    st.dataframe(st.session_state.meet_results)
        # Add this section at the bottom of your meet_module function
    st.subheader("Delete Meet Result")
    if not st.session_state.meet_results.empty:
        idx_to_del = st.selectbox("Select row to delete", st.session_state.meet_results.index, key="del_meets")
        if st.button("Delete Selected Meet Result"):
            st.session_state.meet_results = st.session_state.meet_results.drop(idx_to_del)
            # Make sure your save function is called here
            save_meet_data() 
            st.rerun()
            
def progress_module():
    st.header("📈 Athlete Progress & PRs")
    
    if st.session_state.roster.empty:
        st.warning("No athletes in roster.")
        return

    athlete = st.selectbox("Select Athlete", st.session_state.roster["name"].unique())
    
    # --- PR CALCULATION ---
    # We find the min time for each metric
    fly_pr = st.session_state.fly_sessions[st.session_state.fly_sessions["name"] == athlete]["fly_time"].min()
    block_pr = st.session_state.block_sessions[st.session_state.block_sessions["name"] == athlete]["block_time"].min()
    
    # Meet PRs
    meet_data = st.session_state.meet_results[st.session_state.meet_results["name"] == athlete]
    pr_100 = meet_data[meet_data["race"] == "100m"]["time"].min()
    pr_200 = meet_data[meet_data["race"] == "200m"]["time"].min()
    pr_400 = meet_data[meet_data["race"] == "400m"]["time"].min()

    # --- DISPLAY PRs ---
    st.subheader(f"🏆 {athlete}'s Personal Records")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("20m Fly", f"{fly_pr}s" if pd.notnull(fly_pr) else "N/A")
    col2.metric("30m Block", f"{block_pr}s" if pd.notnull(block_pr) else "N/A")
    col3.metric("100m", f"{pr_100}s" if pd.notnull(pr_100) else "N/A")
    col4.metric("200m", f"{pr_200}s" if pd.notnull(pr_200) else "N/A")
    col5.metric("400m", f"{pr_400}s" if pd.notnull(pr_400) else "N/A")

    # --- LOGIC FLOW VISUALIZATION ---
    st.markdown("---")
    with st.expander("View Metric Logic Flow"):
        st.write("Current Tracking Workflow:")
        st.info("Input (Fly/Block) ➔ Kinematic Engine ➔ Precise 100m Projection")
        
def leaderboard_module():
    st.header("🏆 Team Leaderboard")
    
    # 1. 100m Projected Leaderboard (Dynamic Calculation)
    st.subheader("Top 20: 100m Projected")
    if not st.session_state.fly_sessions.empty and not st.session_state.block_sessions.empty:
        projections = []
        for a in st.session_state.roster["name"].unique():
            f = st.session_state.fly_sessions[st.session_state.fly_sessions["name"] == a]
            b = st.session_state.block_sessions[st.session_state.block_sessions["name"] == a]
            if not f.empty and not b.empty:
                # Running the engine logic
                proj = get_unified_projection("Combined", 0, b.iloc[-1]["block_time"], f.iloc[-1]["fly_time"], "Male")
                projections.append({"name": a, "projection": proj})
        
        if projections:
            st.table(pd.DataFrame(projections).sort_values("projection").head(20))
    else:
        st.info("Log Fly and Block sessions to generate projections.")

    # 2. Training Metric Leaderboards
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Top 20: 20m Fly")
        if not st.session_state.fly_sessions.empty:
            st.table(st.session_state.fly_sessions.sort_values("fly_time").head(20)[["name", "fly_time"]])
    
    with col2:
        st.subheader("Top 20: 30m Block")
        if not st.session_state.block_sessions.empty:
            st.table(st.session_state.block_sessions.sort_values("block_time").head(20)[["name", "block_time"]])

    # 3. Official Race Leaderboards
    for race in ["100m", "200m", "400m"]:
        st.subheader(f"Top 20: {race}")
        if not st.session_state.meet_results.empty:
            race_data = st.session_state.meet_results[st.session_state.meet_results["race"] == race]
            if not race_data.empty:
                st.table(race_data.sort_values("time").head(20)[["name", "time"]])

def generate_relay_pdf(order, go_marks):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Weekly Relay Report", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, txt="Proposed Relay Order:", ln=True)
    for leg, name in order.items():
        pdf.cell(200, 10, txt=f"{leg}: {name}", ln=True)
    pdf.ln(5)
    pdf.cell(200, 10, txt="Calculated Go Marks:", ln=True)
    for name, mark in go_marks.items():
        pdf.cell(200, 10, txt=f"{name}: {mark} feet", ln=True)
    pdf.output("relay_report.pdf")

def relay_optimizer_module():
    st.header("⚡ Relay Optimizer")
    
    # 1. Suggested Order Logic
    st.subheader("Data-Driven Suggestions")
    
    all_metrics = []
    for a in st.session_state.roster["name"].unique():
        f = st.session_state.fly_sessions[st.session_state.fly_sessions["name"]==a]["fly_time"].min()
        b = st.session_state.block_sessions[st.session_state.block_sessions["name"]==a]["block_time"].min()
        if pd.notnull(f) and pd.notnull(b):
            all_metrics.append({"name": a, "fly": f, "block": b})
            
    if all_metrics:
        df_metrics = pd.DataFrame(all_metrics)
        suggested = pd.DataFrame({
            "Leg": ["1st (Starter)", "2nd (Flyer)", "3rd", "4th (Anchor)"],
            "Suggested Athlete": [
                df_metrics.sort_values("block").iloc[0]["name"],
                df_metrics.sort_values("fly").iloc[0]["name"],
                df_metrics.sort_values("fly").iloc[1]["name"],
                df_metrics.sort_values("fly").iloc[2]["name"]
            ]
        })
        st.write("Suggested Order (Prioritizing Best Fly for 2nd Leg):")
        st.table(suggested)
        
    st.markdown("---")
    
    # 2. Manual Override
    st.subheader("Manual Lineup Override")
    selected_runners = st.multiselect("Select 4 runners:", st.session_state.roster["name"].unique(), max_selections=4)
    
    if len(selected_runners) == 4:
        col1, col2, col3, col4 = st.columns(4)
        order = {
            "1st": col1.selectbox("1st Leg", selected_runners),
            "2nd": col2.selectbox("2nd Leg", selected_runners),
            "3rd": col3.selectbox("3rd Leg", selected_runners),
            "4th": col4.selectbox("4th Leg", selected_runners)
        }
        if st.button("Confirm Manual Order"):
            # Calculate go marks for the report
            go_marks_report = {}
            for leg, name in order.items():
                f = st.session_state.fly_sessions[st.session_state.fly_sessions["name"]==name]["fly_time"].iloc[-1]
                b = st.session_state.block_sessions[st.session_state.block_sessions["name"]==name]["block_time"].iloc[-1]
                gen = st.session_state.roster[st.session_state.roster["name"]==name]["gender"].iloc[0]
                raw, _ = get_go_mark_logic(f, b, gen)
                go_marks_report[name] = raw
            
            generate_relay_pdf(order, go_marks_report)
            st.success(f"Final Order: {order}")
            with open("relay_report.pdf", "rb") as f:
                st.download_button("Download Relay Report (PDF)", f, "relay_report.pdf")

    # 3. Go Mark Calculator
    st.markdown("---")
    st.subheader("Go Mark Calculator")
    selected_name = st.selectbox("Select Outgoing Runner", selected_runners if selected_runners else st.session_state.roster["name"].unique())
    
    f_time = st.session_state.fly_sessions[st.session_state.fly_sessions["name"] == selected_name]["fly_time"].tail(1).values
    b_time = st.session_state.block_sessions[st.session_state.block_sessions["name"] == selected_name]["block_time"].tail(1).values
    gen = st.session_state.roster[st.session_state.roster["name"] == selected_name]["gender"].values
    
    if f_time.size > 0 and b_time.size > 0:
        raw, tier = get_go_mark_logic(f_time[0], b_time[0], gen[0])
        st.metric("Calculated Go Mark", f"{raw} feet")
        st.write(f"Category: **{tier}**")

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
with tabs[7]: relay_optimizer_module()

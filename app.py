import streamlit as st
import pandas as pd
import os
from fpdf import FPDF
import io

def generate_training_pdf():
    pdf = FPDF()
    pdf.add_page()
    
    # --- BRAND COLOR PALETTE ---
    PRIMARY_DARK = (20, 24, 33)    # Athletic charcoal
    ACCENT_YELLOW = (255, 204, 0)  # Speed lab lightning yellow
    TEXT_DARK = (30, 30, 30)       # Main body text
    TEXT_MUTED = (100, 105, 115)   # Subtitles
    BG_LIGHT = (245, 247, 250)     # Clean card backgrounds

    # --- TOP BRANDING HEADER ---
    pdf.set_fill_color(*PRIMARY_DARK)
    pdf.rect(0, 0, 210, 42, 'F')
    
    # Yellow Accent Bar
    pdf.set_fill_color(*ACCENT_YELLOW)
    pdf.rect(0, 42, 210, 2, 'F')
    
        # Main Header Text
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(255, 255, 255)
    pdf.text(15, 16, "RDZ SPEED DEVELOPMENT FLYS DATA V0.13.5")
    
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(200, 205, 215)
    pdf.text(15, 24, "Summer Training Plan Block")
    pdf.text(15, 30, "Microcycle: Week 1 Consolidation")
    
    # Athlete & Phase Info (Right Aligned layout positions)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*ACCENT_YELLOW)
    pdf.text(130, 16, "ATLETA: Aisa Rodriguez (10th)")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(255, 255, 255)
    pdf.text(130, 24, "Fase: Phase 1 (Force & Coordination)")
    pdf.text(130, 30, "Objetivo: Sub-14 Transition (Target: 13s Hunt)")

    # --- WORKOUT BLOCKS ---
    y_pos = 52

    # 1. MIÉRCOLES BLOCK
    pdf.set_fill_color(*BG_LIGHT)
    pdf.rect(12, y_pos, 186, 44, 'F')
    pdf.set_text_color(*PRIMARY_DARK)
    pdf.set_font("Helvetica", "B", 11)
    [span_8](start_span)pdf.text(16, y_pos + 6, "MIERCOLES: MAX VELOCITY & POSTURE") #[span_8](end_span)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(*TEXT_MUTED)
    [span_9](start_span)pdf.text(16, y_pos + 11, "Focus: Vertical mechanics and transitioning raw 18.4 mph power into an efficient upright stride.") #[span_9](end_span)
    
    pdf.set_font("Helvetica", "", 9.5)
    pdf.set_text_color(*TEXT_DARK)
    [span_10](start_span)pdf.text(16, y_pos + 18, "• Pre-Session Prep: 3 Dynamic Mobility Movements + Fence Drills / Wall Knee Drives (3x10 single exchanges).") #[span_10](end_span)
    [span_11](start_span)pdf.text(16, y_pos + 23, "  Lock in 'Toes to the Nose'.") #[span_11](end_span)
    pdf.set_font("Helvetica", "B", 9.5)
    [span_12](start_span)pdf.text(16, y_pos + 29, "The Technical Tool: Wicket Runs (5-6 high-quality runs).") #[span_12](end_span)
    pdf.set_font("Helvetica", "", 9.5)
    [span_13](start_span)pdf.text(16, y_pos + 34, "• Setup & Spacing: Set up at a 5.0 ft base. First marker 11-12m from start line, followed by 6 to 8 wickets.") #[span_13](end_span)
    [span_14](start_span)pdf.text(16, y_pos + 39, "• Coaching Cue: 'Step down over the opposite knee.' Focus on maximal hip height. Do not reach.") #[span_14](end_span)

    # 2. JUEVES BLOCK
    y_pos += 49
    pdf.set_fill_color(*BG_LIGHT)
    pdf.rect(12, y_pos, 186, 38, 'F')
    pdf.set_text_color(*PRIMARY_DARK)
    pdf.set_font("Helvetica", "B", 11)
    [span_15](start_span)pdf.text(16, y_pos + 6, "JUEVES: STRENGTH & ELASTICITY") #[span_15](end_span)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(*TEXT_MUTED)
    [span_16](start_span)pdf.text(16, y_pos + 11, "Focus: Building the structural armor and ankle stiffness needed to support high-velocity impacts.") #[span_16](end_span)
    
    pdf.set_font("Helvetica", "", 9.5)
    pdf.set_text_color(*TEXT_DARK)
    [span_17](start_span)pdf.text(16, y_pos + 18, "• Ankle Stiffness: Pogo Jumps - 3 sets of 15 seconds (Stiff springs, zero knee bend).") #[span_17](end_span)
    [span_18](start_span)pdf.text(16, y_pos + 23, "• Explosive Power: Broad Jumps - 3 sets of 3 max-effort reps (Focus on landing stability).") #[span_18](end_span)
    [span_19](start_span)pdf.text(16, y_pos + 28, "• Speed Lift Foundation: Bodyweight Single-Leg RDLs - 3 sets of 8 reps per leg.") #[span_19](end_span)
    [span_20](start_span)pdf.text(16, y_pos + 33, "• Garage Gym: Light Barbell Quarter-Squat Jumps - 3 sets of 3 reps (explosive upward drive).") #[span_20](end_span)

    # 3. VIERNES BLOCK
    y_pos += 43
    pdf.set_fill_color(*BG_LIGHT)
    pdf.rect(12, y_pos, 186, 38, 'F')
    pdf.set_text_color(*PRIMARY_DARK)
    pdf.set_font("Helvetica", "B", 11)
    [span_21](start_span)pdf.text(16, y_pos + 6, "VIERNES: SPEED ENDURANCE & RELAXATION") #[span_21](end_span)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(*TEXT_MUTED)
    [span_22](start_span)pdf.text(16, y_pos + 11, "Focus: Maintaining high top-end velocities without tightening up late in the race.") #[span_22](end_span)
    
    pdf.set_font("Helvetica", "", 9.5)
    pdf.set_text_color(*TEXT_DARK)
    [span_23](start_span)pdf.text(16, y_pos + 18, "• Warm-Up: Standard full dynamic track protocol.") #[span_23](end_span)
    [span_24](start_span)pdf.text(16, y_pos + 23, "• The Workout: Ins & Outs (Float Sprints) - 60 meters total distance.") #[span_24](end_span)
    [span_25](start_span)pdf.text(16, y_pos + 28, "• Execution: 20m acceleration zone -> 20m 'Float' phase (relax jaw/face/shoulders) -> 20m re-acceleration.") #[span_25](end_span)
    [span_26](start_span)pdf.text(16, y_pos + 33, "• Volume & Rest: 3 high-quality reps. 5 full minutes rest between reps.") #[span_26](end_span)

    # 4. SÁBADO & DOMINGO BLOCK
    y_pos += 43
    pdf.set_fill_color(*BG_LIGHT)
    pdf.rect(12, y_pos, 186, 22, 'F')
    pdf.set_text_color(*PRIMARY_DARK)
    pdf.set_font("Helvetica", "B", 11)
    [span_27](start_span)pdf.text(16, y_pos + 6, "SABADO & DOMINGO: COMPLETE CNS RECOVERY") #[span_27](end_span)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(*TEXT_MUTED)
    [span_28](start_span)pdf.text(16, y_pos + 11, "Focus: Complete structural and neural compensation.") #[span_28](end_span)
    pdf.set_font("Helvetica", "", 9.5)
    pdf.set_text_color(*TEXT_DARK)
    [span_29](start_span)pdf.text(16, y_pos + 17, "• Zero running or lifting. Allow the central nervous system to super-compensate for Week 2.") #[span_29](end_span)

    # --- FOOTER SECTION (OPERATIONAL NOTE) ---
    y_pos += 29
    pdf.set_draw_color(210, 215, 225)
    pdf.line(12, y_pos, 198, y_pos)
    
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*PRIMARY_DARK)
    [span_30](start_span)pdf.text(12, y_pos + 5, "Coach Dad's Operational Note:") #[span_30](end_span)
    
    pdf.set_font("Helvetica", "", 8.5)
    pdf.set_text_color(*TEXT_DARK)
    [span_31](start_span)note_line1 = "Quality Over Quantity. Speed training is neural, not metabolic. If posture degrades or mechanics look" #[span_31](end_span)
    note_line2 = "sluggish during any rep, terminate the session immediately. Log wicket metrics to adjust base if necessary." [span_32](start_span)#
    pdf.text(12, y_pos + 10, note_line1)
    pdf.text(12, y_pos + 14, note_line2)

    return pdf.output(dest='S').encode('latin-1')

# 2. LOGIN LOGIC (The Foyer)
if "logged_in" not in st.session_state:
    st.title("Welcome to RDZ Speed Lab")
    coach_name = st.selectbox("Select Coach", ["He Rod", "She Rod"])
    if st.button("Login"):
        st.session_state.coach_id = coach_name
        st.session_state.logged_in = True
        st.rerun()
    st.stop() # This forces the app to wait here until login

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
# ==========================================
# 2. DATA PERSISTENCE (Corrected)
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
   
    # 4. Meet Results
    if not os.path.exists("meet_results.csv"):
        pd.DataFrame(columns=["name", "race", "time", "meet_name", "date"]).to_csv("meet_results.csv", index=False)
    if "meet_results" not in st.session_state:
        st.session_state.meet_results = pd.read_csv("meet_results.csv")
        
    # 5. Combined Sessions
    if 'combined_sessions' not in st.session_state:
        st.session_state.combined_sessions = pd.DataFrame(columns=["name", "fly_time", "block_time", "projection", "date"])

# --- Save Functions ---
def save_data():
    st.session_state.roster.to_csv("roster.csv", index=False)

def save_fly_data():
    st.session_state.fly_sessions.to_csv("fly_sessions.csv", index=False)

def save_block_data():
    st.session_state.block_sessions.to_csv("block_sessions.csv", index=False)

def save_meet_data():
    st.session_state.meet_results.to_csv("meet_results.csv", index=False)

def save_combined_data():
    st.session_state.combined_sessions.to_csv("combined_sessions.csv", index=False)

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
            # Pass 5 arguments so it matches the function definition:
            proj = get_unified_projection("Fly", None, 0, fly_time, gender)
 
            
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
    st.header("📈 Athlete PRs")
    
    if st.session_state.roster.empty:
        st.warning("No athletes in roster.")
        return

    athlete = st.selectbox("Select Athlete", st.session_state.roster["name"].unique())
    gender = st.session_state.roster[st.session_state.roster["name"] == athlete]["gender"].iloc[0]
    
    # --- PR CALCULATION ---
    fly_pr = st.session_state.fly_sessions[st.session_state.fly_sessions["name"] == athlete]["fly_time"].min()
    block_pr = st.session_state.block_sessions[st.session_state.block_sessions["name"] == athlete]["block_time"].min()
    
    meet_data = st.session_state.meet_results[st.session_state.meet_results["name"] == athlete]
    pr_100 = meet_data[meet_data["race"] == "100m"]["time"].min()
    pr_200 = meet_data[meet_data["race"] == "200m"]["time"].min()
    pr_400 = meet_data[meet_data["race"] == "400m"]["time"].min()

    # --- DISPLAY PRs ---
    col1, col2 = st.columns(2)
    col1.metric("20m Fly PR", f"{fly_pr}s" if pd.notnull(fly_pr) else "N/A")
    col2.metric("30m Block PR", f"{block_pr}s" if pd.notnull(block_pr) else "N/A")
    
    st.markdown("---")
    
    col3, col4, col5 = st.columns(3)
    col3.metric("100m PR", f"{pr_100}s" if pd.notnull(pr_100) else "N/A")
    col4.metric("200m PR", f"{pr_200}s" if pd.notnull(pr_200) else "N/A")
    col5.metric("400m PR", f"{pr_400}s" if pd.notnull(pr_400) else "N/A")
    
    # --- CURRENT PROJECTION ---
    st.markdown("---")
    proj_100 = get_unified_projection("Combined", None, block_pr if pd.notnull(block_pr) else 0, fly_pr if pd.notnull(fly_pr) else 0, gender)
    st.metric("Precise 100m Projection", f"{proj_100}s")
      
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
                proj = get_unified_projection("Combined", 0, b.iloc[-1]["block_time"], f.iloc[-1]["fly_time"], "gender")
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
        df = pd.DataFrame(all_metrics)
        if len(df) >= 4:
            s1 = df.sort_values("block").iloc[0]
            pool = df[df["name"] != s1["name"]].sort_values("fly")
            s2, s3, s4 = pool.iloc[0], pool.iloc[1], pool.iloc[2]
            
            legs = [("1st (Starter)", s1), ("2nd (Backstretch)", s2), ("3rd (Curve)", s3), ("4th (Anchor)", s4)]
            
            for leg_name, athlete in legs:
                with st.container(border=True):
                    st.markdown(f"**{leg_name}**: {athlete['name']}")
                    st.write(f"{athlete['fly']:.2f}s")
        else:
            st.info("Log at least 4 athletes with both Fly and Block times to see the suggested relay order.")

    st.markdown("---")
    
    # 2. Manual Override
    st.subheader("Manual Lineup Override")
    selected_runners = st.multiselect("Select 4 runners:", st.session_state.roster["name"].unique(), max_selections=4)
    
    if len(selected_runners) == 4:
        cols = st.columns(4)
        order_list = [cols[i].selectbox(f"Leg {i+1}", selected_runners, key=f"leg_{i}") for i in range(4)]
        
        if "exchanges_data" not in st.session_state:
            st.session_state.exchanges_data = None
            st.session_state.order_list = None

        if st.button("Calculate Exchanges"):
            exchanges = []
            for i in range(3):
                name_in = order_list[i]
                name_out = order_list[i+1]
                
                f = st.session_state.fly_sessions[st.session_state.fly_sessions["name"]==name_in]["fly_time"].iloc[-1]
                b = st.session_state.block_sessions[st.session_state.block_sessions["name"]==name_out]["block_time"].iloc[-1]
                gen = st.session_state.roster[st.session_state.roster["name"]==name_out]["gender"].iloc[0]
                
                raw, _ = get_go_mark_logic(f, b, gen)
                exchanges.append((name_in, name_out, raw))
            
            st.session_state.exchanges_data = exchanges
            st.session_state.order_list = order_list
            st.rerun()

        if st.session_state.exchanges_data:
            for i, (n1, n2, mark) in enumerate(st.session_state.exchanges_data):
                with st.container(border=True):
                    st.write(f"🔄 Exchange {i+1}: {n1} → {n2}")
                    st.metric("Recommended Mark", f"{mark} feet")
            
            # PATCH: Map list to dict for PDF generator
            order_dict = {
                "1st": st.session_state.order_list[0],
                "2nd": st.session_state.order_list[1],
                "3rd": st.session_state.order_list[2],
                "4th": st.session_state.order_list[3]
            }
            
            if st.button("Generate & Download PDF"):
                generate_relay_pdf(order_dict, {n: m for n, _, m in st.session_state.exchanges_data})
                with open("relay_report.pdf", "rb") as f:
                    st.download_button("Download Relay Report (PDF)", f, "relay_report.pdf")
                    
def workout_module():
    st.header("🏋️ Workout Planner")
    st.write("Click below to download your structured training plan template.")
    
    # Prepares the clean, styled data bytes seamlessly
    pdf_bytes = generate_training_pdf()
    
    st.download_button(
        label="📥 Download Week 1 Training PDF",
        data=pdf_bytes,
        file_name="aisa_training_plan_week1.pdf",
        mime="application/pdf"
    )
                  
# ==========================================
# 4. MAIN EXECUTION
# ==========================================
init_app()
st.title("RDZ Speed Lab ⚡ 🧪")

tabs = st.tabs(["👤 Roster", "🪰 Fly", "🚀 Block", "🔗 Combined", "📅 Meets", "📈 Progress", "🏆 Leaderboard", "⚡ Relay", "🏋️ Workout"])

with tabs[0]: roster_module()
with tabs[1]: fly_module()
with tabs[2]: block_module()
with tabs[3]: combined_module()
with tabs[4]: meet_module()
with tabs[5]: progress_module()
with tabs[6]: leaderboard_module()
with tabs[7]: relay_optimizer_module()
with tabs[8]: workout_module()
   

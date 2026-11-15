import streamlit as st
st.header('Work in Progres 🚧🛠️')
st.title('Ultimate Squad Builder')
st.header('This is where you can build your fpl squad, think about your strategies, without worrying about silly mistakes(Like mistaking your transfer)')
formation=st.selectbox(
    "Choose your formation:",['3-4-3','3-5-2','4-4-2','4-3-3','5-3-2','5-4-1']
)
st.markdown("""
<style>
/* Make the cards vertical, compact, and centered! */
.fpl-card {
    background: linear-gradient(135deg, rgba(55, 0, 60, 0.95), rgba(26, 0, 28, 0.95));
    border: 2px solid #04f5ff;
    border-radius: 12px;
    padding: 15px 5px;
    text-align: center;
    color: white;
    box-shadow: 0px 8px 15px rgba(0,0,0,0.5);
    margin: 5px auto;
    width: 100%; /* Adjusts nicely to the column */
    max-width: 130px; /* Stops it from getting too wide! */
    transition: transform 0.2s;
}

.fpl-card:hover {
    transform: scale(1.05);
    border-color: #00ff85;
}

/* Make the player name bold and neat */
.player-name {
    font-size: 14px;
    font-weight: 800;
    margin-top: 5px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
</style>
""", unsafe_allow_html=True)
def_count,midf_count,fw_count=[int(x) for x in formation.split('-')]
st.divider()
st.markdown(f"<h3 style='text-align: center;'>Your Starting XI ({formation})</h3>", unsafe_allow_html=True)
st.write("")
spacer_1,gk_col,spacer2=st.columns([1,2,1])
def draw_card(slot_name, icon="👕"):
    player_name = st.session_state['squad'][slot_name]
    
    # Draw the premium HTML card
    st.markdown(f"""
        <div class="fpl-card">
            <div style="font-size: 24px;">{icon}</div>
            <div style="font-size: 10px; color: #00ff85;">{slot_name}</div>
            <div class="player-name">{player_name}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Add the tiny remove button underneath
    if player_name != "Empty":
        if st.button("✖ Remove", type="tertiary", key=f"btn_rem_{slot_name}", use_container_width=True):
            st.session_state['squad'][slot_name] = "Empty"
            st.rerun()

st.write("") # Spacer

# --- ROW 1: GOALKEEPER ---
# 1.5 ratio on the outside squeezes the GK perfectly into the center box
col_l, gk_col, col_r = st.columns([1.5, 1, 1.5])
with gk_col:
    draw_card("GK", "🧤")

st.write("") 

# --- ROW 2: DEFENDERS ---
# Create empty layout list: e.g. [1, 2, 2, 2, 1]
layout = [1] + [1.5]*def_count + [1] 
def_cols = st.columns(layout)
for i in range(def_count):
    with def_cols[i+1]: # i+1 skips the first spacer column
        draw_card(f"DEF{i+1}", "🛡️")

st.write("")

# --- ROW 3: MIDFIELDERS ---
layout = [0.5] + [1.5]*midf_count + [0.5] 
mid_cols = st.columns(layout)
for i in range(midf_count):
    with mid_cols[i+1]:
        draw_card(f"MID{i+1}", "🪄")

st.write("")

# --- ROW 4: FORWARDS ---
layout = [1] + [1.5]*fw_count + [1] 
fw_cols = st.columns(layout)
for i in range(fw_count):
    with fw_cols[i+1]:
        draw_card(f"FWD{i+1}", "⚽")



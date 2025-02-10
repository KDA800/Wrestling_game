import pandas as pd
import streamlit as st
import random

users = ["Todd", "Hurley", "Beau", "Kyle", "Tony"]

# Initialize session state
if "match_results" not in st.session_state:
    st.session_state.match_results = {}
if "df" not in st.session_state:
    st.session_state.df = None
if "user_assignments" not in st.session_state:
    st.session_state.user_assignments = {}

data = {
    "125 lbs": [
        (1, "Matt Ramos", "Purdue"), (2, "Drake Ayala", "Iowa"),
        (3, "Eric Barnett", "Wisconsin"), (4, "Patrick McKee", "Minnesota"),
        (5, "Caleb Smith", "Nebraska"), (6, "Braeden Davis", "Penn State"),
        (7, "Michael DeAugustino", "Michigan"), (8, "Brendan McCrone", "Ohio State"),
        (9, "Dean Peterson", "Rutgers"), (10, "Tristan Lujan", "Michigan State"),
        (11, "Justin Cardani", "Illinois"), (12, "Massey Odiotti", "Northwestern"),
        (13, "Tommy Capul", "Maryland"), (14, "Blaine Fraizer", "Maryland"),
        (15, "Bye", "TBD"), (16, "Bye", "TBD")
    ]
}

def create_dataframe(data):
    records = []
    for weight, wrestlers in data.items():
        for seed, name, school in wrestlers:
            records.append({"Weight Class": weight, "Seed": seed, "Original Seed": seed, "Name": name, "School": school, "Points": 0, "User": ""})
    return pd.DataFrame(records)

st.title("Big Ten Wrestling Score Tracker")

selected_page = st.sidebar.radio("Navigation", ["Team Selection", "Tournament"])

if selected_page == "Team Selection":
    st.write("### Pick Teams")
    for name in data["125 lbs"]:
        if name[1] == "Bye":
            continue
        wrestler_name = name[1]
        st.session_state.user_assignments[wrestler_name] = st.selectbox(f"Assign {wrestler_name}", ["Unassigned"] + users, key=f"assign_{wrestler_name}")
    
    if st.button("Confirm Teams"):
        st.session_state.df = create_dataframe(data)
        for wrestler, assigned_user in st.session_state.user_assignments.items():
            if assigned_user != "Unassigned":
                st.session_state.df.loc[st.session_state.df["Name"] == wrestler, "User"] = assigned_user
    st.stop()

def generate_matchups(df, weight_class, round_num):
    df = df.sort_values(by="Seed")
    match_orders = {
        1: [(1, 16), (8, 9), (5, 12), (4, 13), (3, 14), (6, 11), (7, 10), (2, 15)],
        2: [(1, 8), (4, 5), (3, 6), (2, 7)],
        2.5: [(9, 16), (12, 13), (11, 14), (10, 15)],
        3: [(1, 4), (3, 2)],
        3.5: [(9, 7), (12, 6), (11, 5), (10, 8)],
        4: [(6, 4), (5, 3)],
        3.75: [(6, 7), (5,8)],
        78: [(7,8)],
        5: [(5,6)],
        6: [(3,4)],
        7: [(1,2)]}
    return [(df.loc[df["Seed"] == high, "Name"].values[0], df.loc[df["Seed"] == low, "Name"].values[0])
            for high, low in match_orders.get(round_num, []) if high in df["Seed"].values and low in df["Seed"].values]

def update_scores(df, matchups, round_num):
    st.write(f"### Update Match Results - Round {round_num}")
    results = {"Decision": 0, "Major Decision": 1, "Tech Fall": 1.5, "Fall": 2}
    
    for i, match in enumerate(matchups):
        # Store Round 1 and Round 2.5 opponents for future reference
        if round_num in [1]:
            st.session_state[f'round_{round_num}_opponent_{match[0]}'] = match[1]
            st.session_state[f'round_{round_num}_opponent_{match[1]}'] = match[0]
        if round_num in [2.5]:
            st.session_state[f'round_{round_num}_opponent_{match[0]}'] = match[1]
            st.session_state[f'round_{round_num}_opponent_{match[1]}'] = match[0]
        winner_key = f"winner_{round_num}_{i}"
        win_type_key = f"win_type_{round_num}_{i}"
        submitted_key = f"submitted_{round_num}_{i}"

        if submitted_key not in st.session_state:
            st.session_state[submitted_key] = 0
        
        winner = st.radio(f"Winner: {match[0]} vs. {match[1]}", [None, match[0], match[1]], key=winner_key)
        win_type = st.radio(f"Win Type for {winner}", [None] + list(results.keys()), key=win_type_key) if winner else None
    
    if st.button(f"Submit Results for Round {round_num}"):
        for i, match in enumerate(matchups):
            winner = st.session_state.get(f"winner_{round_num}_{i}")
            win_type = st.session_state.get(f"win_type_{round_num}_{i}")
            submitted_key = f"submitted_{round_num}_{i}"
            
            if winner and win_type and st.session_state[submitted_key] == 0:
                round_base_points = {1: 1, 2: 4, 2.5: 0.5, 3: 10, 3.5: 0.5, 3.75: 3.5, 4: 4.5, 7: 4, 6: 3, 5:2, 78:1}  # Custom scoring per round
                base_points = round_base_points.get(round_num, 0)
                if round_num in [2] and st.session_state.get(f'round_1_opponent_{winner}', None) == 'Bye':
                  base_points += 1  # Extra point for winning after a Bye
                if round_num in [3.5] and st.session_state.get(f'round_2.5_opponent_{winner}', None) == 'Bye':
                  base_points += .5  # Extra point for winning after a Bye
                if 'Bye' in match:
                    total_points = 0  # No points for winning against Bye in Round 1 or 2.5
                else:
                  total_points = base_points + results[win_type]
                  df.loc[df["Name"] == winner, "Points"] += total_points
                  st.session_state[submitted_key] = 1
        st.session_state.df = df.copy()
    return df

if st.session_state.df is None:
    st.session_state.df = create_dataframe(data)
df = st.session_state.df

available_rounds = ["Round 1"]
round_order = ["Round 1", "Round 2", "Round 3", "Round 4", "Round 5", "7th/ 8th place match", "Championship Round"]

def is_round_complete(round_num):
    total_matches = len(generate_matchups(df, "125 lbs", round_num))
    completed_matches = sum(1 for i in range(total_matches) if st.session_state.get(f'winner_{round_num}_{i}') is not None)
    return completed_matches == total_matches

for i in range(1, len(round_order)):
    if is_round_complete(i):
        available_rounds.append(round_order[i])

selected_tab = st.radio("Select Round", available_rounds)
#df = update_scores(df, generate_matchups(df, int(selected_tab.split()[1])), int(selected_tab.split()[1]))

if selected_tab == "Round 1":
    st.write("### Round 1 Matchups")
    df = update_scores(df, generate_matchups(df, "125 lbs", 1), 1)

if selected_tab == "Round 2":
    st.write("### Round 2 Matchups")
    df = update_scores(df, generate_matchups(df, "125 lbs", 2), 2)
    st.write("### Round 2 Losers Bracket Matchups")
    df = update_scores(df, generate_matchups(df, "125 lbs", 2.5), 2.5)

if selected_tab == "Round 3":
    st.write("### Round 3 Matchups")
    df = update_scores(df, generate_matchups(df, "125 lbs", 3), 3)
    st.write("### Round 3 Losers Bracket Matchups")
    df = update_scores(df, generate_matchups(df, "125 lbs", 3.5), 3.5)

if selected_tab == "Round 4":
    st.write("### Round 4 Matchups")
    df = update_scores(df, generate_matchups(df, "125 lbs", 3.75), 3.75)

if selected_tab == "Round 5":
    st.write("### Round 5 Matchups")
    df = update_scores(df, generate_matchups(df, "125 lbs", 4), 4)

if selected_tab == "7th/ 8th place match":
    st.write("### Round 5 Matchups")
    df = update_scores(df, generate_matchups(df, "125 lbs", 78), 78)
  
if selected_tab == "Championship Round":
    st.write("### 1st/ 2nd place match")
    df = update_scores(df, generate_matchups(df, "125 lbs", 7), 7)
    st.write("### 3rd/ 4th place match")
    df = update_scores(df, generate_matchups(df, "125 lbs", 6), 6)
    st.write("### 5th/ 6th place match")
    df = update_scores(df, generate_matchups(df, "125 lbs", 5), 5)



st.sidebar.write("### Competitor Scores")
st.sidebar.dataframe(df[["Name", "Points"]].sort_values(by="Points", ascending=False))

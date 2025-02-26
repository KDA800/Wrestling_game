import firebase_admin
from firebase_admin import credentials, db
import streamlit as st
import pandas as pd
import re
import numpy as np
import os
import json

# --- Constants ---
DATA = {
    "125 lbs": [
        (1, "Matt Ramos", "Purdue"), (2, "Drake Ayala", "Iowa"),
        (3, "Braeden Davis", "Penn State"), (4, "Patrick McKee", "Minnesota"),
        (5, "Dean Peterson", "Rutgers"), (6, "Michael DeAugustino", "Michigan"),
        (7, "Eric Barnett", "Wisconsin"), (8, "Brendan McCrone", "Ohio State"),
        (9, "Tristan Lujan", "Michigan State"), (10, "Massey Odiotti", "Northwestern"),
        (11, "Justin Cardani", "Illinois"), (12, "Tommy Capul", "Maryland"),
        (13, "Blaine Fraizer", "Indiana"), (14, "Jacob Moran", "Nebraska"),
        (15, "Bye", "TBD"), (16, "Bye", "TBD")
    ],
    "133 lbs": [
        (1, "Dylan Ragusin", "Michigan"), (2, "Aaron Nagao", "Penn State"),
        (3, "Nicolar Rivera", "Wisconsin"), (4, "Jacob Van Dee", "Nebraska"),
        (5, "Cody Chittum", "Iowa"), (6, "Tony Madrigal", "Illinois"),
        (7, "Braxton Brown", "Maryland"), (8, "Dustin Norris", "Purdue"),
        (9, "Andrew Hampton", "Michigan State"), (10, "Dominic Zaccone", "Ohio State"),
        (11, "Jake Gliva", "Minnesota"), (12, "Jordan Hamdan", "Indiana"),
        (13, "Zeno Moore", "Northwestern"), (14, "Santana Serrano", "Rutgers"),
        (15, "Bye", "TBD"), (16, "Bye", "TBD")
    ],
    "141 lbs": [
        (1, "Real Woods", "Iowa"), (2, "Beau Bartlett", "Penn State"),
        (3, "Jesse Mendez", "Ohio State"), (4, "Mitch Moore", "Rutgers"),
        (5, "Danny Pucino", "Illinois"), (6, "Vince Santaniello", "Maryland"),
        (7, "Jordan Titus", "Minnesota"), (8, "Cole Mattin", "Michigan"),
        (9, "Felix Salas", "Wisconsin"), (10, "Greyson Clark", "Purdue"),
        (11, "Kal Miller", "Indiana"), (12, "Sammy Alvarez", "Nebraska"),
        (13, "Joseph Olivieri", "Northwestern"), (14, "Andrew Chambal", "Michigan State"),
        (15, "Bye", "TBD"), (16, "Bye", "TBD")
    ],
    "149 lbs": [
        (1, "Ridge Lovett", "Nebraska"), (2, "Caleb Rathjen", "Iowa"),
        (3, "Tyler Kasak", "Penn State"), (4, "Austin Gomez", "Michigan"),
        (5, "Ethen Miller", "Maryland"), (6, "Graham Rooks", "Indiana"),
        (7, "Joseph Zargo", "Wisconsin"), (8, "Drew Roberts", "Minnesota"),
        (9, "Aiden Vandenbush", "Northwestern"), (10, "Jake Harrier", "Illinois"),
        (11, "Cayden Rooks", "Purdue"), (12, "Dylan D`Emilio", "Ohio State"),
        (13, "Marcos Polanco", "Michigan State"), (14, "Jake Hockaday", "Rutgers"),
        (15, "Bye", "TBD"), (16, "Bye", "TBD")
    ],
    "157 lbs": [
        (1, "Levi Haines", "Penn State"), (2, "Jared Franek", "Iowa"),
        (3, "Chase Saldate", "Michigan"), (4, "Will Lewan", "Michigan State"),
        (5, "Peyton Robb", "Nebraska"), (6, "Isaac Wilcox", "Ohio State"),
        (7, "Trevor Chumbley", "Northwestern"), (8, "Joey Blaze", "Purdue"),
        (9, "Tommy Askey", "Minnesota"), (10, "Michael Cetta", "Rutgers"),
        (11, "Clayton Ulrey", "Indiana"), (12, "Kaden Laster", "Illinois"),
        (13, "Luke Mechler", "Wisconsin"), (14, "Conor McGonigle", "Maryland"),
        (15, "Bye", "TBD"), (16, "Bye", "TBD")
    ],
    "165 lbs": [
        (1, "Mitchell Mesenbrink", "Penn State"), (2, "Dean Hamiti", "Wisconsin"),
        (3, "Cameron Amine", "Michigan"), (4, "Caleb Fish", "Michigan State"),
        (5, "Michael Caliendo", "Iowa"), (6, "Maxx Mayfield", "Northwestern"),
        (7, "Stoney Buell", "Purdue"), (8, "Andrew Sparks", "Minnesota"),
        (9, "Tyler Lillard", "Indiana"), (10, "Charlie Darracott", "Maryland"),
        (11, "Chris Moore", "Illinois"), (12, "Gaven Bell", "Ohio State"),
        (13, "AJ Rodrigues", "Nebraska"), (14, "Luke Gayer", "Rutgers"),
        (15, "Bye", "TBD"), (16, "Bye", "TBD")
    ],
    "174 lbs": [
        (1, "Carter Starocci", "Penn State"), (2, "Edmond Ruth", "Illinois"),
        (3, "Shane Griffith", "Michigan"), (4, "Rocco Welsh", "Ohio State"),
        (5, "Jackson Turley", "Rutgers"), (6, "Max Maylor", "Wisconsin"),
        (7, "DJ Shannon", "Iowa"), (8, "Ceasar Garza", "Michigan State"),
        (9, "Andrew Salazar", "Minnesota"), (10, "Bubba Wilson", "Nebraska"),
        (11, "James Conway", "Indiana"), (12, "Josh Ogunsanya", "Maryland"),
        (13, "Dominic Solis", "Purdue"), (14, "Evan Bates", "Northwestern"),
        (15, "Bye", "TBD"), (16, "Bye", "TBD")
    ],
    "184 lbs": [
        (1, "Isaiah Salazar", "Minnesota"), (2, "Lenny Pinto", "Nebraska"),
        (3, "Bernie Truax", "Penn State"), (4, "Jaden Bullock", "Michigan"),
        (5, "Brian Soldano", "Rutgers"), (6, "Layton Bull", "Ohio State"),
        (7, "James Rowley", "Purdue"), (8, "Dylan Connell", "Illinois"),
        (9, "Troy Fisher", "Northwestern"), (10, "Chase Mielnik", "Maryland"),
        (11, "Roman Rogotzke", "Indiana"), (12, "Guiseppe Hoose", "Wisconsin"),
        (13, "Gabe Sollars", "Michigan State"), (14, "Bye", "TBD"),
        (15, "Bye", "TBD"), (16, "Bye", "TBD")
    ],
    "197 lbs": [
        (1, "Aaron Brooks", "Penn State"), (2, "Zach Glazier", "Iowa"),
        (3, "Silas Allred", "Nebraska"), (4, "Jaxon Smith", "Maryland"),
        (5, "Evan Bates", "Northwestern"), (6, "Gabe Sollars", "Indiana"),
        (7, "Ben Vanadia", "Purdue"), (8, "John Crawford", "Michigan"),
        (9, "Kael Wisler", "Michigan State"), (10, "Brad Wilton", "Illinois"),
        (11, "Seth Shigg", "Minnesota"), (12, "Luke Geog", "Ohio State"),
        (13, "Josh Otto", "Wisconsin"), (14, "Evan Herriman", "Rutgers"),
        (15, "Bye", "TBD"), (16, "Bye", "TBD")
    ],
    "HWT": [
        (1, "Greg Kerkvliet", "Penn State"), (2, "Nick Feldman", "Ohio State"),
        (3, "Lucas Davison", "Michigan"), (4, "Yarok Slavikouski", "Rutgers"),
        (5, "Boone McDermott", "Nebraska"), (6, "Seth Nevills", "Maryland"),
        (7, "Bennett Tice", "Indiana"), (8, "Gannon Gremmel", "Iowa"),
        (9, "Hunter Catka", "Purdue"), (10, "Bradley Hill", "Wisconsin"),
        (11, "Tyler Emery", "Illinois"), (12, "Nick Willham", "Minnesota"),
        (13, "Nash Hutmacher", "Nebraska"), (14, "Peter Marinopoulos", "Michigan State"),
        (15, "Bye", "TBD"), (16, "Bye", "TBD")
    ]
}

WEIGHT_CLASSES = ["125 lbs", "133 lbs", "141 lbs", "149 lbs", "157 lbs", "165 lbs", "174 lbs", "184 lbs", "197 lbs", "HWT"]

ROUND_ORDER_MAP = {
    "Round 1": 1,
    "Round 2": 2,
    "Round 3": 3,
    "Round 4": 4,
    "Round 5": 5,
    "7th/8th place match": 6,
    "Championship Round": 7,
    "3rd/4th place match": 8,
    "5th/6th place match": 9
}

ROUND_BASE_POINTS = {
    1: 1,
    2: 7,
    2.5: 0.5,
    3: 7,
    3.5: 3.5,
    4: 3.5,
    5: 3.5,
    6: 1,
    7: 4,
    8: 1,
    9: 1
}

RESULTS_POINTS = {"Decision": 0, "Major Decision": 1, "Tech Fall": 1.5, "Fall": 2}

NEXT_ROUNDS = {
    1: "Round 2",
    2: "Round 3",
    3: "Round 4",
    4: "Round 5",
    5: "7th/8th place match",
    6: "Championship Round",
    7: "3rd/4th place match",
    8: "5th/6th place match"
}

ALL_ROUNDS = [1, 2, 2.5, 3, 3.5, 4, 5, 6, 7, 8, 9]

# --- Custom CSS for Appearance ---
def get_css(is_todd_and_easter_active):
    if is_todd_and_easter_active:
        return """
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@700&family=Roboto&display=swap');
            .stApp {
                background-color: #041E42;
                color: #FFFFFF;
                background-image: url('https://www.bigten.org/images/logos/Big_Ten_Championship_Logo.png');
                background-size: 50%;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
                opacity: 0.9;
            }
            h1, h2, h3, h4, h5, h6 {
                font-family: 'Oswald', sans-serif;
                color: #FFFFFF !important;
                text-transform: uppercase;
            }
            body, p, div {
                font-family: 'Roboto', sans-serif;
                color: #FFFFFF;
            }
            .sidebar .sidebar-content {
                background-color: #041E42 !important;
                border-right: 1px solid #FFFFFF;
            }
            .sidebar .sidebar-content, 
            .sidebar .sidebar-content p, 
            .sidebar .sidebar-content div, 
            .sidebar .sidebar-content h3 {
                color: #FFFFFF !important;
            }
            .sidebar .sidebar-content .stRadio > label {
                color: #FFFFFF !important;
                background-color: #2A4A8C;
                padding: 5px;
                border-radius: 5px;
            }
            .sidebar .sidebar-content .stButton > button {
                width: 100%;
            }
            .stSelectbox label {
                color: #041E42 !important;
            }
            .stSelectbox div[data-baseweb="select"] > div {
                background-color: #2A4A8C;
                color: #041E42 !important;
            }
            .stSelectbox [data-baseweb="menu"] li {
                color: #041E42 !important;
                background-color: #FFFFFF;
            }
            .stSelectbox [data-baseweb="menu"] li:hover {
                background-color: #FFFFFF !important;
                color: #041E42 !important;
            }
            .stButton > button {
                background-color: #FFFFFF;
                color: #041E42;
                font-family: 'Oswald', sans-serif;
                font-weight: bold;
                border-radius: 5px;
                border: 2px solid #FFFFFF;
            }
            .stButton > button:hover {
                background-color: #D3D3D3;
                color: #041E42;
            }
            .stButton > button:disabled {
                background-color: #666666;
                color: "gray";
            }
            .stTabs [data-baseweb="tab-list"] {
                background-color: #041E42;
            }
            .stTabs [data-baseweb="tab"] {
                font-family: 'Oswald', sans-serif;
                color: #FFFFFF;
                background-color: #041E42;
            }
            .stTabs [data-baseweb="tab"]:hover {
                color: #FFFFFF;
            }
            .stTabs [aria-selected="true"] {
                color: #FFFFFF;
                border-bottom: 3px solid #FFFFFF;
            }
            .excel-chart {
                background-color: #041E42;
                padding: 10px;
                border-radius: 5px;
            }
            .excel-header {
                font-family: 'Oswald', sans-serif;
                color: #FFFFFF;
                font-size: 16px;
                text-align: center;
                padding: 5px;
                background-color: #2A4A8C;
            }
            .excel-row {
                display: flex;
                justify-content: space-between;
                padding: 5px;
                background-color: #2A4A8C;
                font-family: 'Roboto', sans-serif;
                font-size: 14px;
            }
            .excel-row:nth-child(even) {
                background-color: #041E42;
            }
            .excel-row-top {
                display: flex;
                justify-content: space-between;
                padding: 5px;
                background-color: #2A4A8C;
                font-family: 'Roboto', sans-serif;
                font-size: 14px;
                border: 1px solid #FFFFFF;
            }
            .excel-cell {
                flex: 1;
                text-align: center;
                color: #FFFFFF;
            }
            .excel-cell.points, .excel-cell.bonus-points {
                color: #FFFFFF;
                font-weight: bold;
            }
            .leaderboard-row {
                background-color: #2A4A8C;
                border: 1px solid #FFFFFF;
                padding: 10px;
                margin: 5px 0;
                border-radius: 5px;
            }
            .leaderboard-top {
                background-color: #2A4A8C;
                border: 2px solid #FFFFFF;
                padding: 10px;
                margin: 5px 0;
                border-radius: 5px;
                animation: pulse 2s infinite;
            }
            @keyframes pulse {
                0% { box-shadow: 0 0 5px #FFFFFF; }
                50% { box-shadow: 0 0 15px #FFFFFF; }
                100% { box-shadow: 0 0 5px #FFFFFF; }
            }
            .mini-leaderboard table {
                width: 50%;
                background-color: #2A4A8C;
                color: #FFFFFF;
                font-size: 14px;
            }
            .mini-leaderboard th {
                background-color: #FFFFFF;
                color: #041E42;
                font-family: 'Oswald', sans-serif;
            }
            </style>
        """
    else:
        return """
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@700&family=Roboto&display=swap');
            .stApp {
                background-color: #1F2525;
                color: #FFFFFF;
                background-image: url('https://www.bigten.org/images/logos/Big_Ten_Championship_Logo.png');
                background-size: 50%;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
                opacity: 0.9;
            }
            h1, h2, h3, h4, h5, h6 {
                font-family: 'Oswald', sans-serif;
                color: #FFC107 !important;
                text-transform: uppercase;
            }
            body, p, div {
                font-family: 'Roboto', sans-serif;
                color: #FFFFFF;
            }
            .sidebar .sidebar-content {
                background-color: #1F2525 !important;
                border-right: 1px solid #000000;
            }
            .sidebar .sidebar-content, 
            .sidebar .sidebar-content p, 
            .sidebar .sidebar-content div, 
            .sidebar .sidebar-content h3 {
                color: #FFFFFF !important;
            }
            .sidebar .sidebar-content .stRadio > label {
                color: #FFFFFF !important;
                background-color: #2A3030;
                padding: 5px;
                border-radius: 5px;
            }
            .sidebar .sidebar-content .stButton > button {
                width: 100%;
            }
            .stSelectbox label {
                color: #000000 !important;
            }
            .stSelectbox div[data-baseweb="select"] > div {
                background-color: #2A3030;
                color: #000000 !important;
            }
            .stSelectbox [data-baseweb="menu"] li {
                color: #000000 !important;
                background-color: #FFFFFF;
            }
            .stSelectbox [data-baseweb="menu"] li:hover {
                background-color: #FFD54F !important;
                color: #000000 !important;
            }
            .stButton > button {
                background-color: #FFC107;
                color: #1F2525;
                font-family: 'Oswald', sans-serif;
                font-weight: bold;
                border-radius: 5px;
                border: 2px solid #000000;
            }
            .stButton > button:hover {
                background-color: #FFD54F;
                color: #000000;
            }
            .stButton > button:disabled {
                background-color: #666666;
                color: "gray";
            }
            .stTabs [data-baseweb="tab-list"] {
                background-color: #1F2525;
            }
            .stTabs [data-baseweb="tab"] {
                font-family: 'Oswald', sans-serif;
                color: #FFFFFF;
                background-color: #1F2525;
            }
            .stTabs [data-baseweb="tab"]:hover {
                color: #FFC107;
            }
            .stTabs [aria-selected="true"] {
                color: #FFC107;
                border-bottom: 3px solid #FFC107;
            }
            .excel-chart {
                background-color: #1F2525;
                padding: 10px;
                border-radius: 5px;
            }
            .excel-header {
                font-family: 'Oswald', sans-serif;
                color: #FFC107;
                font-size: 16px;
                text-align: center;
                padding: 5px;
                background-color: #2A3030;
            }
            .excel-row {
                display: flex;
                justify-content: space-between;
                padding: 5px;
                background-color: #2A3030;
                font-family: 'Roboto', sans-serif;
                font-size: 14px;
            }
            .excel-row:nth-child(even) {
                background-color: #1F2525;
            }
            .excel-row-top {
                display: flex;
                justify-content: space-between;
                padding: 5px;
                background-color: #2A3030;
                font-family: 'Roboto', sans-serif;
                font-size: 14px;
                border: 1px solid #FFD54F;
            }
            .excel-cell {
                flex: 1;
                text-align: center;
                color: #FFFFFF;
            }
            .excel-cell.points, .excel-cell.bonus-points {
                color: #FFC107;
                font-weight: bold;
            }
            .leaderboard-row {
                background-color: #2A3030;
                border: 1px solid #FFC107;
                padding: 10px;
                margin: 5px 0;
                border-radius: 5px;
            }
            .leaderboard-top {
                background-color: #2A3030;
                border: 2px solid #FFD54F;
                padding: 10px;
                margin: 5px 0;
                border-radius: 5px;
                animation: pulse 2s infinite;
            }
            @keyframes pulse {
                0% { box-shadow: 0 0 5px #FFD54F; }
                50% { box_shadow: 0 0 15px #FFD54F; }
                100% { box_shadow: 0 0 5px #FFD54F; }
            }
            .mini-leaderboard table {
                width: 50%;
                background-color: #2A3030;
                color: #FFFFFF;
                font-size: 14px;
            }
            .mini-leaderboard th {
                background-color: #FFC107;
                color: #1F2525;
                font-family: 'Oswald', sans-serif;
            }
            </style>
        """

# --- Database Functions ---
def initialize_firebase():
    try:
        if not firebase_admin._apps:
            cred_json = os.getenv("FIREBASE_CRED")
            cred_dict = json.loads(cred_json)
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred, {
                'databaseURL': "https://wrestlingpickem-default-rtdb.firebaseio.com/"
            })
        return db.reference("/")
    except ValueError as e:
        st.error(f"Firebase initialization failed: {e}. Check your credentials.")
        st.stop()

def save_state(db_ref):
    if st.session_state.user_name.endswith("Kyle"):
        try:
            df_dict = st.session_state.df.replace({np.nan: None}).to_dict(orient="records") if st.session_state.df is not None else []
            match_results_dict = st.session_state.match_results.replace({np.nan: None}).to_dict(orient="records") if st.session_state.match_results is not None else []
            state_data = {
                "df": df_dict,
                "match_results": match_results_dict,
                "user_assignments": st.session_state.get("user_assignments", {}),
                "available_rounds_by_weight": st.session_state.get("available_rounds_by_weight", {weight: ["Round 1"] for weight in WEIGHT_CLASSES}),
                "selected_tabs": st.session_state.get("selected_tabs", {weight: "Round 1" for weight in WEIGHT_CLASSES}),
                "selected_weight": st.session_state.get("selected_weight", "125 lbs"),
                "users": st.session_state.get("users", ["Todd", "Hurley", "Beau", "Kyle", "Tony"])
            }
            db_ref.child("state").set(state_data)
            st.success("State saved successfully!")
        except Exception as e:
            st.error(f"Failed to save state: {e}")

def load_state(db_ref):
    try:
        state = db_ref.child("state").get() or {}
        st.session_state.df = pd.DataFrame(state.get("df", [])) if state.get("df") else create_dataframe(DATA)
        st.session_state.match_results = pd.DataFrame(state.get("match_results", [])) if state.get("match_results") else pd.DataFrame(columns=["Weight Class", "Round", "Match Index", "W1", "W2", "Winner", "Loser", "Win Type", "Submitted"])
        st.session_state.user_assignments = state.get("user_assignments", {})
        st.session_state.available_rounds_by_weight = state.get("available_rounds_by_weight", {weight: ["Round 1"] for weight in WEIGHT_CLASSES})
        st.session_state.selected_tabs = state.get("selected_tabs", {weight: "Round 1" for weight in WEIGHT_CLASSES})
        st.session_state.selected_weight = state.get("selected_weight", "125 lbs")
        st.session_state.users = state.get("users", ["Todd", "Hurley", "Beau", "Kyle", "Tony"])
    except Exception as e:
        st.error(f"Failed to load state: {e}")
        if "df" not in st.session_state or st.session_state.df is None:
            st.session_state.df = create_dataframe(DATA)
        if "match_results" not in st.session_state:
            st.session_state.match_results = pd.DataFrame(columns=["Weight Class", "Round", "Match Index", "W1", "W2", "Winner", "Loser", "Win Type", "Submitted"])
        if "available_rounds_by_weight" not in st.session_state:
            st.session_state.available_rounds_by_weight = {weight: ["Round 1"] for weight in WEIGHT_CLASSES}
        if "selected_tabs" not in st.session_state:
            st.session_state.selected_tabs = {weight: "Round 1" for weight in WEIGHT_CLASSES}
        if "users" not in st.session_state:
            st.session_state.users = ["Todd", "Hurley", "Beau", "Kyle", "Tony"]

# --- Utility Functions ---
def create_dataframe(data):
    records = []
    for weight, wrestlers in data.items():
        for seed, name, school in wrestlers:
            record = {"Weight Class": weight, "Seed": seed, "Original Seed": seed, "Name": name, "School": school, "Points": 0, "User": ""}
            records.append(record)
    return pd.DataFrame(records)

def calculate_bonus_points(wrestler_name, match_results):
    wrestler_wins = match_results[match_results["Winner"] == wrestler_name]
    bonus_points = wrestler_wins["Win Type"].map(RESULTS_POINTS).sum()
    return bonus_points

def generate_matchups(df, weight_class, round_num):
    df = df[df["Weight Class"] == weight_class].sort_values(by="Seed")
    match_orders = {
        1: [(1, 16), (8, 9), (5, 12), (4, 13), (3, 14), (6, 11), (7, 10), (2, 15)],
        2: [(1, 8), (4, 5), (3, 6), (2, 7)],
        2.5: [(9, 16), (12, 13), (11, 14), (10, 15)],
        3: [(1, 4), (3, 2)],
        3.5: [(9, 7), (12, 6), (11, 5), (10, 8)],
        4: [(6, 7), (5, 8)],
        5: [(6, 4), (5, 3)],
        6: [(7, 8)],
        7: [(1, 2)],
        8: [(3, 4)],
        9: [(5, 6)]
    }
    return [(df.loc[df["Seed"] == high, "Name"].values[0], df.loc[df["Seed"] == low, "Name"].values[0])
            for high, low in match_orders.get(round_num, []) if high in df["Seed"].values and low in df["Seed"].values]

def is_round_complete(df, weight_class, round_num):
    matchups = generate_matchups(df, weight_class, round_num)
    return len(st.session_state.match_results[
        (st.session_state.match_results["Weight Class"] == weight_class) &
        (st.session_state.match_results["Round"] == round_num) &
        (st.session_state.match_results["Submitted"] == 1)
    ]) == len(matchups)

def update_available_rounds(df, weight_class, current_round):
    round_order = ["Round 1", "Round 2", "Round 3", "Round 4", "Round 5", "7th/8th place match", "Championship Round", "3rd/4th place match", "5th/6th place match"]
    available_rounds = st.session_state.available_rounds_by_weight[weight_class]
    if is_round_complete(df, weight_class, current_round):
        next_round_name = NEXT_ROUNDS.get(current_round)
        if next_round_name and next_round_name not in available_rounds:
            available_rounds.append(next_round_name)
    st.session_state.available_rounds_by_weight[weight_class] = available_rounds

def update_scores(df, matchups, round_num, weight_class):
    st.write(f"### Update Match Results - Round {round_num} ({weight_class})")
    round_str = str(round_num).replace('.', '_')

    for i, (w1, w2) in enumerate(matchups):
        match_data = st.session_state.match_results[
            (st.session_state.match_results["Weight Class"] == weight_class) &
            (st.session_state.match_results["Round"] == round_num) &
            (st.session_state.match_results["Match Index"] == i) &
            (st.session_state.match_results["Submitted"] == 1)
        ]
        if not match_data.empty:
            winner = match_data["Winner"].iloc[0]
            loser = match_data["Loser"].iloc[0]
            win_type = match_data["Win Type"].iloc[0]
            st.write(f"{w1} vs {w2}: {winner} beat {loser} by {win_type}")

    if st.session_state.user_name.endswith("Kyle"):
        for i, (w1, w2) in enumerate(matchups):
            match_exists = not st.session_state.match_results[
                (st.session_state.match_results["Weight Class"] == weight_class) &
                (st.session_state.match_results["Round"] == round_num) &
                (st.session_state.match_results["Match Index"] == i) &
                (st.session_state.match_results["Submitted"] == 1)
            ].empty
            if not match_exists:
                winner_key = f"winner_{round_str}_{i}_{weight_class}"
                win_type_key = f"win_type_{round_str}_{i}_{weight_class}"
                winner = st.radio(f"Winner: {w1} vs {w2}", [None, w1, w2], key=winner_key)
                if winner:
                    st.radio(f"Win Type for {winner}", list(RESULTS_POINTS.keys()), key=win_type_key, index=0)

        if st.button(f"Submit Results for Round {round_num} ({weight_class})"):
            for i, (w1, w2) in enumerate(matchups):
                winner_key = f"winner_{round_str}_{i}_{weight_class}"
                win_type_key = f"win_type_{round_str}_{i}_{weight_class}"
                winner = st.session_state.get(winner_key)
                win_type = st.session_state.get(win_type_key)
                if winner and win_type and not st.session_state.match_results[
                    (st.session_state.match_results["Weight Class"] == weight_class) &
                    (st.session_state.match_results["Round"] == round_num) &
                    (st.session_state.match_results["Match Index"] == i) &
                    (st.session_state.match_results["Submitted"] == 1)
                ].any().any():
                    loser = w2 if winner == w1 else w1
                    winner_idx = df.index[df["Name"] == winner].tolist()[0]
                    loser_idx = df.index[df["Name"] == loser].tolist()[0]
                    new_result = pd.DataFrame([{
                        "Weight Class": weight_class,
                        "Round": round_num,
                        "Match Index": i,
                        "W1": w1,
                        "W2": w2,
                        "Winner": winner,
                        "Loser": loser,
                        "Win Type": win_type,
                        "Submitted": 1
                    }])
                    st.session_state.match_results = pd.concat([st.session_state.match_results, new_result], ignore_index=True)
                    if "Bye" not in [w1, w2]:
                        base_points = ROUND_BASE_POINTS.get(round_num, 0)
                        prev_round = 1 if round_num == 2 else 2.5 if round_num == 3.5 else None
                        if prev_round:
                            prev_opponent = st.session_state.match_results[
                                (st.session_state.match_results["Weight Class"] == weight_class) &
                                (st.session_state.match_results["Round"] == prev_round) &
                                ((st.session_state.match_results["W1"] == winner) | (st.session_state.match_results["W2"] == winner))
                            ]
                            if not prev_opponent.empty and prev_opponent["Loser"].iloc[0] == "Bye":
                                base_points += 1 if round_num == 2 else 0.5
                        total_points = base_points + RESULTS_POINTS[win_type]
                        df.at[winner_idx, "Points"] += total_points
                    try:
                        winner_seed = df.at[winner_idx, "Seed"]
                        loser_seed = df.at[loser_idx, "Seed"]
                        if winner_seed > loser_seed:
                            df.at[winner_idx, "Seed"], df.at[loser_idx, "Seed"] = loser_seed, winner_seed
                    except IndexError as e:
                        st.error(f"Error updating seeds for {winner} vs {loser}: {e}")
            update_available_rounds(df, weight_class, round_num)
            save_state(db_ref)
            st.session_state.df = df
    return df

# Updated Display Match Results Function
def display_match_results(df, weight_class):
    st.write(f"### Match Results Recap - {weight_class}")
    user_wrestlers = set(df[df["User"] == st.session_state.user_name]["Name"].tolist())
    
    for round_num in ALL_ROUNDS:
        matchups = generate_matchups(df, weight_class, round_num)
        submitted_matches = []
        for i, (w1, w2) in enumerate(matchups):
            match_data = st.session_state.match_results[
                (st.session_state.match_results["Weight Class"] == weight_class) &
                (st.session_state.match_results["Round"] == round_num) &
                (st.session_state.match_results["Match Index"] == i) &
                (st.session_state.match_results["Submitted"] == 1)
            ]
            if not match_data.empty:
                winner = match_data["Winner"].iloc[0]
                loser = match_data["Loser"].iloc[0]
                win_type = match_data["Win Type"].iloc[0]
                # Validate loser against matchup
                expected_loser = w2 if winner == w1 else w1
                if loser != expected_loser:
                    loser = expected_loser  # Correct mismatch
                match_text = f"{w1} vs {w2}: {winner} defeated {loser} by {win_type}"
                
                style = ""
                if winner in user_wrestlers:
                    style = "background-color: #2ecc71; color: white; padding: 5px; border-radius: 5px;"
                elif loser in user_wrestlers:
                    style = "background-color: #e74c3c; color: white; padding: 5px; border-radius: 5px;"
                
                submitted_matches.append((match_text, style))
        
        if submitted_matches:
            round_name = next((name for name, num in ROUND_ORDER_MAP.items() if num == round_num), f"Round {round_num}")
            if round_num == 2.5:
                round_name = "Round 2 Losers Bracket"
            elif round_num == 3.5:
                round_name = "Round 3 Losers Bracket"
            elif round_num in [7, 8, 9]:
                round_name = {7: "Championship Round", 8: "3rd/4th place match", 9: "5th/6th place match"}[round_num]
            st.write(f"#### {round_name}")
            for match_text, style in submitted_matches:
                st.markdown(f'<div style="{style}">{match_text}</div>', unsafe_allow_html=True)

def calculate_points_race(df, match_results):
    user_points = {}
    school_points = {}
    rounds = sorted(match_results["Round"].unique())
    
    for round_num in rounds:
        round_matches = match_results[match_results["Round"] <= round_num]
        temp_df = df.copy()
        temp_df["Points"] = 0
        
        for _, match in round_matches.iterrows():
            if match["W1"] != "Bye" and match["W2"] != "Bye":
                winner_idx = temp_df.index[temp_df["Name"] == match["Winner"]].tolist()
                if winner_idx:
                    winner_idx = winner_idx[0]
                    base_points = ROUND_BASE_POINTS.get(match["Round"], 0)
                    total_points = base_points + RESULTS_POINTS[match["Win Type"]]
                    temp_df.at[winner_idx, "Points"] += total_points
        
        user_totals = temp_df[temp_df["User"] != ""].groupby("User")["Points"].sum()
        for user in st.session_state.users:
            if user not in user_points:
                user_points[user] = []
            user_points[user].append(user_totals.get(user, 0))
        
        school_totals = temp_df.groupby("School")["Points"].sum()
        for school in temp_df["School"].unique():
            if school not in school_points:
                school_points[school] = []
            school_points[school].append(school_totals.get(school, 0))
    
    user_df = pd.DataFrame(user_points, index=[f"Round {int(r) if r.is_integer() else r}" for r in rounds])
    school_df = pd.DataFrame(school_points, index=[f"Round {int(r) if r.is_integer() else r}" for r in rounds])
    
    return user_df, school_df

# New Function: Calculate Max Points Available per Wrestler
def calculate_max_points_available(wrestler_name, df, match_results):
    wrestler_matches = match_results[(match_results["Winner"] == wrestler_name) | (match_results["Loser"] == wrestler_name)]
    wins = len(wrestler_matches[wrestler_matches["Winner"] == wrestler_name])
    losses = len(wrestler_matches[wrestler_matches["Loser"] == wrestler_name])
    earned_points = df[df["Name"] == wrestler_name]["Points"].iloc[0] if not df[df["Name"] == wrestler_name].empty else 0

    if losses >= 2:
        return earned_points  # Eliminated, max = current points

    latest_round = wrestler_matches["Round"].max() if not wrestler_matches.empty else 0

    # Winners' Bracket
    if losses == 0:
        if latest_round < 7:
            remaining_wins = 4 - wins  # To 1st place
            remaining_base = 0
            if wins == 0:
                remaining_base = 1 + 7 + 7 + 4  # Round 1, 2, 3, 7
            elif wins == 1:
                remaining_base = 7 + 7 + 4  # Round 2, 3, 7
            elif wins == 2:
                remaining_base = 7 + 4  # Round 3, 7
            elif wins == 3:
                remaining_base = 4  # Round 7
            remaining_bonus = remaining_wins * 2
            # Check for bye in Round 1
            if "Bye" in wrestler_matches[wrestler_matches["Round"] == 1]["Loser"].values and wins == 0:
                remaining_base = 0 + 8 + 7 + 4  # Adjust Round 1 to 0, Round 2 to 8
            return earned_points + remaining_base + remaining_bonus
        elif latest_round == 7:
            return earned_points + (4 + 2 if wins == 3 else 0)  # Win Round 7 or done

    # Losers' Bracket (1 Loss)
    if losses == 1:
        if latest_round < 8:
            # Max 3rd place
            total_wins_needed = 6 if wins > 0 else 5  # 6 if lost Round 2+, 5 if Round 1
            remaining_wins = total_wins_needed - wins
            remaining_base = 0
            if wins == 0:  # Lost Round 1
                remaining_base = 0.5 + 3.5 + 3.5 + 3.5 + 1  # 2.5 → 8
            elif wins == 1:
                remaining_base = 3.5 + 3.5 + 3.5 + 1  # 3.5 → 8
            elif wins == 2:
                remaining_base = 3.5 + 3.5 + 1  # 4 → 8
            elif wins == 3:
                remaining_base = 3.5 + 1  # 5 → 8
            elif wins == 4:
                remaining_base = 1  # Round 8
            remaining_bonus = remaining_wins * 2
            # Adjust for bye if Round 1 was a bye
            if "Bye" in wrestler_matches[wrestler_matches["Round"] == 1]["Loser"].values and wins <= 1:
                remaining_base += 0.5 if wins < 2 else 0  # Add to Round 3.5 if not yet earned
            return earned_points + remaining_base + remaining_bonus
        elif latest_round == 8:
            return earned_points + (1 + 2 if wins == 5 else 0)  # Win Round 8 or done
        elif latest_round == 9:
            return earned_points + (1 + 2 if wins == 4 else 0)  # Win Round 9 or done
        elif latest_round == 6:
            return earned_points + (1 + 2 if wins == 2 else 0)  # Win Round 6 or done

    return earned_points  # Default to current if position unclear

def initialize_session_state():
    defaults = {
        "user_name": "",
        "users": ["Todd", "Hurley", "Beau", "Kyle", "Tony"],
        "df": None,
        "match_results": pd.DataFrame(columns=["Weight Class", "Round", "Match Index", "W1", "W2", "Winner", "Loser", "Win Type", "Submitted"]),
        "user_assignments": {},
        "available_rounds_by_weight": {weight: ["Round 1"] for weight in WEIGHT_CLASSES},
        "selected_tabs": {weight: "Round 1" for weight in WEIGHT_CLASSES},
        "selected_weight": "125 lbs",
        "reset_tournament_confirm": 0,
        "reset_assignments_confirm": 0,
        "delete_state_confirm": 0
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
    if st.session_state.df is None:
        st.session_state.df = create_dataframe(DATA)

# --- Main App ---
# Initialize critical session state attributes at the top level
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "reset_tournament_confirm" not in st.session_state:
    st.session_state.reset_tournament_confirm = 0
if "reset_assignments_confirm" not in st.session_state:
    st.session_state.reset_assignments_confirm = 0
if "delete_state_confirm" not in st.session_state:
    st.session_state.delete_state_confirm = 0

db_ref = initialize_firebase()
firebase_state = db_ref.child("state").get()
if firebase_state:
    load_state(db_ref)
else:
    initialize_session_state()

st.title("Big Ten Wrestling Score Tracker")
if not st.session_state.user_name:
    st.write("### Welcome!")
    selected_user = st.selectbox("Select your name:", st.session_state.users, key="user_selection")
    if st.button("Continue"):
        st.session_state.user_name = selected_user
        st.rerun()
    st.stop()

df = st.session_state.df

user_scores = df[df["User"] != ""].groupby("User")["Points"].sum().sort_values(ascending=False)
if user_scores.empty:
    is_penn_state_todd_active = False
else:
    is_penn_state_todd_active = (user_scores.index[0] == "Todd" and len(user_scores) > 1 and user_scores.iloc[0] > user_scores.iloc[1])

is_todd_and_easter_active = st.session_state.user_name == "Todd" and is_penn_state_todd_active
st.markdown(get_css(is_todd_and_easter_active), unsafe_allow_html=True)

if st.session_state.user_name.endswith("Kyle"):
    selected_page = st.sidebar.radio("Navigation", ["Team Selection", "Tournament", "User Assignments", "User Dashboard", "Individual Leaderboard", "Match Results"])
else:
    selected_page = st.sidebar.radio("Navigation", ["User Dashboard", "Individual Leaderboard", "Match Results"])

if st.sidebar.button("Refresh Data"):
    load_state(db_ref)
    df = st.session_state.df
    st.success("Data refreshed from latest state!")

if st.session_state.user_name.endswith("Kyle"):
    if st.sidebar.button("Restart Tournament"):
        st.session_state.reset_tournament_confirm = 1
    if st.session_state.reset_tournament_confirm == 1:
        st.sidebar.write("Are you sure you want to reset the tournament?")
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("Yes, I’m sure", key="reset_tournament_sure"):
                st.session_state.reset_tournament_confirm = 2
        with col2:
            if st.button("No", key="reset_tournament_no"):
                st.session_state.reset_tournament_confirm = 0
    if st.session_state.reset_tournament_confirm == 2:
        st.sidebar.write("Are you double sure? This will reset all tournament data!")
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("Yes, I’m double sure", key="reset_tournament_double_sure"):
                st.session_state.df = create_dataframe(DATA)
                st.session_state.match_results = pd.DataFrame(columns=["Weight Class", "Round", "Match Index", "W1", "W2", "Winner", "Loser", "Win Type", "Submitted"])
                st.session_state.user_assignments = {}
                st.session_state.available_rounds_by_weight = {weight: ["Round 1"] for weight in WEIGHT_CLASSES}
                st.session_state.selected_tabs = {weight: "Round 1" for weight in WEIGHT_CLASSES}
                st.session_state.selected_weight = "125 lbs"
                save_state(db_ref)
                st.session_state.reset_tournament_confirm = 0
                st.rerun()
        with col2:
            if st.button("No", key="reset_tournament_double_no"):
                st.session_state.reset_tournament_confirm = 0

    if st.sidebar.button("Reset User Assignments"):
        st.session_state.reset_assignments_confirm = 1
    if st.session_state.reset_assignments_confirm == 1:
        st.sidebar.write("Are you sure you want to reset all user assignments?")
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("Yes, I’m sure", key="reset_assignments_sure"):
                st.session_state.reset_assignments_confirm = 2
        with col2:
            if st.button("No", key="reset_assignments_no"):
                st.session_state.reset_assignments_confirm = 0
    if st.session_state.reset_assignments_confirm == 2:
        st.sidebar.write("Are you double sure? This will clear all user assignments!")
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("Yes, I’m double sure", key="reset_assignments_double_sure"):
                st.session_state.df["User"] = ""
                st.session_state.user_assignments = {}
                save_state(db_ref)
                st.session_state.reset_assignments_confirm = 0
                st.rerun()
        with col2:
            if st.button("No", key="reset_assignments_double_no"):
                st.session_state.reset_assignments_confirm = 0

    if st.sidebar.button("Delete State"):
        st.session_state.delete_state_confirm = 1
    if st.session_state.delete_state_confirm == 1:
        st.sidebar.write("Are you sure you want to delete the entire state?")
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("Yes, I’m sure", key="delete_state_sure"):
                st.session_state.delete_state_confirm = 2
        with col2:
            if st.button("No", key="delete_state_no"):
                st.session_state.delete_state_confirm = 0
    if st.session_state.delete_state_confirm == 2:
        st.sidebar.write("Are you double sure? This will wipe everything!")
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("Yes, I’m double sure", key="delete_state_double_sure"):
                delete_state(db_ref)
                st.session_state.delete_state_confirm = 0
        with col2:
            if st.button("No", key="delete_state_double_no"):
                st.session_state.delete_state_confirm = 0

st.sidebar.write("### User Scores")
user_scores_display = user_scores.reset_index()
user_scores_display["User"] = user_scores_display["User"].replace("Todd", "Penn State Todd" if is_penn_state_todd_active else "Todd")
st.sidebar.dataframe(user_scores_display)

st.sidebar.write("### NCAA Team Scores")
st.sidebar.dataframe(df.groupby("School")["Points"].sum().reset_index().sort_values(by="Points", ascending=False))

# Pages
if selected_page == "User Dashboard":
    display_name = "Penn State Todd" if st.session_state.user_name == "Todd" and is_penn_state_todd_active else st.session_state.user_name
    st.write(f"### Welcome, {display_name}!")

    st.write("#### Your Wrestlers")
    user_wrestlers = df[df["User"] == st.session_state.user_name].sort_values(by="Points", ascending=False)
    if not user_wrestlers.empty:
        st.markdown('<div class="excel-chart">', unsafe_allow_html=True)
        st.markdown("""
            <div class="excel-row">
                <div class="excel-header">Rank</div>
                <div class="excel-header">Name</div>
                <div class="excel-header">Weight Class</div>
                <div class="excel-header">Points</div>
                <div class="excel-header">Bonus Points</div>
                <div class="excel-header">School</div>
            </div>
        """, unsafe_allow_html=True)
        for idx, (_, wrestler) in enumerate(user_wrestlers.iterrows()):
            rank = idx + 1
            bonus_points = calculate_bonus_points(wrestler["Name"], st.session_state.match_results)
            row_class = "excel-row-top" if rank == 1 else "excel-row"
            st.markdown(f"""
                <div class="{row_class}">
                    <div class="excel-cell">{rank}</div>
                    <div class="excel-cell">{wrestler["Name"]}</div>
                    <div class="excel-cell">{wrestler["Weight Class"]}</div>
                    <div class="excel-cell points">{int(wrestler["Points"])}</div>
                    <div class="excel-cell bonus-points">{bonus_points:.1f}</div>
                    <div class="excel-cell">{wrestler["School"]}</div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.write("No wrestlers assigned yet!")

    # Updated User Scores with Max Points Available
    st.write("#### User Scores")
    user_totals = df[df["User"] != ""].groupby("User")["Points"].sum().sort_values(ascending=False).reset_index()
    if not user_totals.empty:
        user_bonus_points = {}
        user_max_points = {}
        for user in user_totals["User"]:
            user_wrestlers = df[df["User"] == user]["Name"].tolist()
            bonus_total = sum(calculate_bonus_points(wrestler, st.session_state.match_results) for wrestler in user_wrestlers)
            max_points_total = sum(calculate_max_points_available(wrestler, df, st.session_state.match_results) for wrestler in user_wrestlers)
            user_bonus_points[user] = bonus_total
            user_max_points[user] = max_points_total

        st.markdown('<div class="excel-chart">', unsafe_allow_html=True)
        st.markdown("""
            <div class="excel-row">
                <div class="excel-header">Rank</div>
                <div class="excel-header">User</div>
                <div class="excel-header">Points</div>
                <div class="excel-header">Bonus Points</div>
                <div class="excel-header">Max Points</div>
            </div>
        """, unsafe_allow_html=True)
        for idx, row in user_totals.iterrows():
            rank = idx + 1
            user = row["User"]
            display_user = "Penn State Todd" if user == "Todd" and is_penn_state_todd_active else user
            bonus_points = user_bonus_points[user]
            max_points = user_max_points[user]
            row_class = "excel-row-top" if rank == 1 else "excel-row"
            st.markdown(f"""
                <div class="{row_class}">
                    <div class="excel-cell">{rank}</div>
                    <div class="excel-cell">{display_user}</div>
                    <div class="excel-cell points">{int(row["Points"])}</div>
                    <div class="excel-cell bonus-points">{bonus_points:.1f}</div>
                    <div class="excel-cell">{max_points:.1f}</div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.write("No user scores available yet!")

    if not st.session_state.match_results.empty:
        user_points_race, school_points_race = calculate_points_race(df, st.session_state.match_results)
        user_points_race = user_points_race.rename(columns={"Todd": "Penn State Todd" if is_penn_state_todd_active else "Todd"})
        
        st.write("#### User Points Race")
        st.line_chart(user_points_race)
        
        st.write("#### School Points Race")
        st.line_chart(school_points_race)
    else:
        st.write("No match results available yet for points race!")

    if not st.session_state.user_name.endswith("Kyle"):
        st.info("Refresh to see Kyle's latest updates!")

elif selected_page == "Individual Leaderboard":
    st.write("### Individual Leaderboard")
    leaderboard = df.sort_values(by="Points", ascending=False)
    if not leaderboard.empty:
        st.markdown('<div class="excel-chart">', unsafe_allow_html=True)
        st.markdown("""
            <div class="excel-row">
                <div class="excel-header">Rank</div>
                <div class="excel-header">Name</div>
                <div class="excel-header">Weight Class</div>
                <div class="excel-header">Points</div>
                <div class="excel-header">Bonus Points</div>
                <div class="excel-header">School</div>
                <div class="excel-header">User</div>
            </div>
        """, unsafe_allow_html=True)
        for idx, (_, wrestler) in enumerate(leaderboard.iterrows()):
            rank = idx + 1
            bonus_points = calculate_bonus_points(wrestler["Name"], st.session_state.match_results)
            display_user = "Penn State Todd" if wrestler["User"] == "Todd" and is_penn_state_todd_active else wrestler["User"] or ""
            row_class = "excel-row-top" if rank == 1 else "excel-row"
            st.markdown(f"""
                <div class="{row_class}">
                    <div class="excel-cell">{rank}</div>
                    <div class="excel-cell">{wrestler["Name"]}</div>
                    <div class="excel-cell">{wrestler["Weight Class"]}</div>
                    <div class="excel-cell points">{int(wrestler["Points"])}</div>
                    <div class="excel-cell bonus-points">{bonus_points:.1f}</div>
                    <div class="excel-cell">{wrestler["School"]}</div>
                    <div class="excel-cell">{display_user}</div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.write("No leaderboard data available yet!")

elif selected_page == "User Assignments" and st.session_state.user_name.endswith("Kyle"):
    st.write("### User Assignments")
    
    user_display_names = [
        "Penn State Todd" if user == "Todd" and is_penn_state_todd_active else user
        for user in st.session_state.users
    ]
    user_tabs = st.tabs(user_display_names)
    
    for user, tab in zip(st.session_state.users, user_tabs):
        with tab:
            st.write(f"#### {user}'s Wrestlers")
            user_wrestlers = df[df["User"] == user].sort_values(by="Points", ascending=False)
            if not user_wrestlers.empty:
                st.markdown('<div class="excel-chart">', unsafe_allow_html=True)
                st.markdown("""
                    <div class="excel-row">
                        <div class="excel-header">Rank</div>
                        <div class="excel-header">Name</div>
                        <div class="excel-header">Weight Class</div>
                        <div class="excel-header">Points</div>
                        <div class="excel-header">Bonus Points</div>
                        <div class="excel-header">School</div>
                    </div>
                """, unsafe_allow_html=True)
                for idx, (_, wrestler) in enumerate(user_wrestlers.iterrows()):
                    rank = idx + 1
                    bonus_points = calculate_bonus_points(wrestler["Name"], st.session_state.match_results)
                    row_class = "excel-row-top" if rank == 1 else "excel-row"
                    st.markdown(f"""
                        <div class="{row_class}">
                            <div class="excel-cell">{rank}</div>
                            <div class="excel-cell">{wrestler["Name"]}</div>
                            <div class="excel-cell">{wrestler["Weight Class"]}</div>
                            <div class="excel-cell points">{int(wrestler["Points"])}</div>
                            <div class="excel-cell bonus-points">{bonus_points:.1f}</div>
                            <div class="excel-cell">{wrestler["School"]}</div>
                        </div>
                    """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.write(f"No wrestlers assigned to {user} yet!")

elif selected_page == "Team Selection" and st.session_state.user_name.endswith("Kyle"):
    st.write("### Pick Teams")
    weight_tabs = st.tabs(WEIGHT_CLASSES)
    for weight, tab in zip(WEIGHT_CLASSES, weight_tabs):
        with tab:
            wrestlers = df[df["Weight Class"] == weight]["Name"].tolist()
            for name in wrestlers:
                if name == "Bye":
                    continue
                options = ["Unassigned"] + [user if user != "Todd" or not is_penn_state_todd_active else "Penn State Todd" for user in st.session_state.users]
                st.session_state.user_assignments[name] = st.selectbox(
                    f"Assign {name}", options, key=f"assign_{name}_{weight}"
                )
    if st.button("Confirm Teams"):
        for wrestler, user in st.session_state.user_assignments.items():
            if user != "Unassigned":
                df.loc[df["Name"] == wrestler, "User"] = "Todd" if user == "Penn State Todd" else user
        save_state(db_ref)
        st.session_state.selected_tabs = {weight: "Round 1" for weight in WEIGHT_CLASSES}
        st.rerun()

elif selected_page == "Tournament" and st.session_state.user_name.endswith("Kyle"):
    weight_tabs = st.tabs(WEIGHT_CLASSES)
    for weight, tab in zip(WEIGHT_CLASSES, weight_tabs):
        with tab:
            update_available_rounds(df, weight, ROUND_ORDER_MAP.get(st.session_state.selected_tabs[weight], 1))
            available_rounds = st.session_state.available_rounds_by_weight[weight]
            default_index = available_rounds.index(st.session_state.selected_tabs[weight]) if st.session_state.selected_tabs[weight] in available_rounds else 0 if f"tournament_tab_{weight}" in st.session_state else 0
            
            selected_tab = st.radio(
                f"Select Round ({weight})",
                available_rounds,
                index=default_index,
                key=f"tournament_tab_{weight}"
            )
            st.session_state.selected_tabs[weight] = selected_tab
            round_num = ROUND_ORDER_MAP.get(selected_tab, 1)
            
            if selected_tab == "Round 2":
                st.write("### Winners Bracket")
                df = update_scores(df, generate_matchups(df, weight, 2), 2, weight)
                st.write("### Losers Bracket")
                df = update_scores(df, generate_matchups(df, weight, 2.5), 2.5, weight)
            elif selected_tab == "Round 3":
                st.write("### Winners Bracket")
                df = update_scores(df, generate_matchups(df, weight, 3), 3, weight)
                st.write("### Losers Bracket")
                df = update_scores(df, generate_matchups(df, weight, 3.5), 3.5, weight)
            else:
                df = update_scores(df, generate_matchups(df, weight, round_num), round_num, weight)

elif selected_page == "Match Results":
    weight_tabs = st.tabs(WEIGHT_CLASSES)
    for weight, tab in zip(WEIGHT_CLASSES, weight_tabs):
        with tab:
            display_match_results(df, weight)

def delete_state(db_ref):
    if st.session_state.user_name.endswith("Kyle"):
        try:
            db_ref.child("state").delete()
            st.session_state.clear()
            st.session_state.user_name = ""
            st.session_state.reset_tournament_confirm = 0
            st.session_state.reset_assignments_confirm = 0
            st.session_state.delete_state_confirm = 0
            st.success("State deleted successfully! Returning to user selection...")
            st.rerun()
        except Exception as e:
            st.error(f"Failed to delete state: {e}")

# --- Main App Execution ---
db_ref = initialize_firebase()
firebase_state = db_ref.child("state").get()
if firebase_state:
    load_state(db_ref)
else:
    initialize_session_state()

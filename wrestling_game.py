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
        (1, "Matt Ramos", "Purdue"), (2, "Caleb Smith", "Nebraska"),
        (3, "Dean Peterson", "Rutgers"), (4, "Luke Lilledahl", "Penn State"),
        (5, "Joey Cruz", "Iowa"), (6, "Jacob Moran", "Indiana"),
        (7, "Brendan McCrone", "Ohio State"), (8, "Nicolar Rivera", "Wisconsin"),
        (9, "Cooper Flynn", "Minnesota"), (10, "Dedrick Navarro", "Northwestern"),
        (11, "Caleb Weiand", "Michigan State"), (12, "Christian Tanefu", "Michigan"),
        (13, "Caelan Riley", "Illinois"), (14, "Tyler Garvin", "Maryland"),
        (15, "Bye", "TBD"), (16, "Bye", "TBD")
    ],
    "133 lbs": [
        (1, "Drake Ayala", "Iowa"), (2, "Lucas Byrd", "Illinois"),
        (3, "Braxton Brown", "Maryland"), (4, "Braeden Davis", "Penn State"),
        (5, "Dylan Shawver", "Rutgers"), (6, "Jacob Van Dee", "Nebraska"),
        (7, "Zan Fugitt", "Wisconsin"), (8, "Angelo Rini", "Indiana"),
        (9, "Nic Bouzakis", "Ohio State"), (10, "Tyler Wells", "Minnesota"),
        (11, "Dustin Norris", "Purdue"), (12, "Massey Odiotti", "Northwestern"),
        (13, "Andrew Hampton", "Michigan State"), (14, "Nolan Wertanen", "Michigan"),
        (15, "Bye", "TBD"), (16, "Bye", "TBD")
    ],
    "141 lbs": [
        (1, "Beau Bartlett", "Penn State"), (2, "Jesse Mendez", "Ohio State"),
        (3, "Brock Hardy", "Nebraska"), (4, "Vance Vombaur", "Minnesota"),
        (5, "Sergio Lemley", "Michigan"), (6, "Joseph Olivieri", "Rutgers"),
        (7, "Danny Pucino", "Illinois"), (8, "Henry Porter", "Indiana"),
        (9, "Greyson Clark", "Purdue"), (10, "Christopher Cannon", "Northwestern"),
        (11, "Cullan Schriever", "Iowa"), (12, "Dario Lemus", "Maryland"),
        (13, "Brock Bobzien", "Wisconsin"), (14, "Jaden Crumpler", "Michigan State"),
        (15, "Bye", "TBD"), (16, "Bye", "TBD")
    ],
    "149 lbs": [
        (1, "Shayne Van Ness", "Penn State"), (2, "Kyle Parco", "Iowa"),
        (3, "Ridge Lovett", "Nebraska"), (4, "Dylan D’Emilio", "Ohio State"),
        (5, "Kannon Webster", "Illinois"), (6, "Andrew Clark", "Rutgers"),
        (7, "Sam Cartella", "Northwestern"), (8, "Kal Miller", "Maryland"),
        (9, "Dylan Gilcher", "Michigan"), (10, "Drew Roberts", "Minnesota"),
        (11, "Isaac Ruble", "Purdue"), (12, "Clayton Jones", "Michigan State"),
        (13, "Joey Butler", "Indiana"), (14, "Royce Nilo", "Wisconsin"),
        (15, "Bye", "TBD"), (16, "Bye", "TBD")
    ],
    "157 lbs": [
        (1, "Ethen Miller", "Maryland"), (2, "Tyler Kasak", "Penn State"),
        (3, "Antrell Taylor", "Nebraska"), (4, "Jacori Teemer", "Iowa"),
        (5, "Tommy Askey", "Minnesota"), (6, "Joey Blaze", "Purdue"),
        (7, "Trevor Chumbley", "Northwestern"), (8, "Chase Saldate", "Michigan"),
        (9, "Brandon Cannon", "Ohio State"), (10, "Conner Harer", "Rutgers"),
        (11, "Jason Kraisser", "Illinois"), (12, "Ryan Garvick", "Indiana"),
        (13, "Luke Mechler", "Wisconsin"), (14, "Braden Stauffenberg", "Michigan State"),
        (15, "Bye", "TBD"), (16, "Bye", "TBD")
    ],
    "165 lbs": [
        (1, "Mitchell Mesenbrink", "Penn State"), (2, "Mike Caliendo", "Iowa"),
        (3, "Christopher Minto", "Nebraska"), (4, "Beau Mantanona", "Michigan"),
        (5, "Andrew Sparks", "Minnesota"), (6, "Braeden Scoles", "Illinois"),
        (7, "Tyler Lillard", "Indiana"), (8, "Maxx Mayfield", "Northwestern"),
        (9, "Paddy Gallagher", "Ohio State"), (10, "Anthony White", "Rutgers"),
        (11, "Stoney Buell", "Purdue"), (12, "Alex Uryniak", "Maryland"),
        (13, "Cody Goebel", "Wisconsin"), (14, "Jay Nivison", "Michigan State"),
        (15, "Bye", "TBD"), (16, "Bye", "TBD")
    ],
    "174 lbs": [
        (1, "Levi Haines", "Penn State"), (2, "Carson Kharchla", "Ohio State"),
        (3, "Lenny Pinto", "Nebraska"), (4, "Patrick Kennedy", "Iowa"),
        (5, "Clayton Whiting", "Minnesota"), (6, "Jackson Turley", "Rutgers"),
        (7, "Danny Braunagel", "Illinois"), (8, "Brody Baumann", "Purdue"),
        (9, "Lucas Condon", "Wisconsin"), (10, "Derek Gilcher", "Indiana"),
        (11, "Joseph Walker", "Michigan"), (12, "Branson John", "Maryland"),
        (13, "Ceasar Garza", "Michigan State"), (14, "Aiden Vandenbush", "Northwestern"),
        (15, "Bye", "TBD"), (16, "Bye", "TBD")
    ],
    "184 lbs": [
        (1, "Carter Starocci", "Penn State"), (2, "Max McEnelly", "Minnesota"),
        (3, "Silas Allred", "Nebraska"), (4, "Gabe Arnold", "Iowa"),
        (5, "Jaxon Smith", "Maryland"), (6, "Edmond Ruth", "Illinois"),
        (7, "Shane Cartagena-Walsh", "Rutgers"), (8, "Ryder Rogotzke", "Ohio State"),
        (9, "DJ Washington", "Indiana"), (10, "Jaden Bullock", "Michigan"),
        (11, "Jon Halvorsen", "Northwestern"), (12, "Lucas Daly", "Michigan State"),
        (13, "Orlando Cruz", "Purdue"), (14, "Dylan Russo", "Wisconsin"),
        (15, "Bye", "TBD"), (16, "Bye", "TBD")
    ],
    "197 lbs": [
        (1, "Stephen Buchanan", "Iowa"), (2, "Josh Barr", "Penn State"),
        (3, "Jacob Cardenas", "Michigan"), (4, "Isaiah Salazar", "Minnesota"),
        (5, "Zac Braunagel", "Illinois"), (6, "Evan Bates", "Northwestern"),
        (7, "Camden McDanel", "Nebraska"), (8, "Gabe Sollars", "Indiana"),
        (9, "Seth Shumate", "Ohio State"), (10, "Remy Cotton", "Michigan State"),
        (11, "Ben Vanadia", "Purdue"), (12, "Chase Mielnik", "Maryland"),
        (13, "PJ Casale", "Rutgers"), (14, "Niccolo Colluci", "Wisconsin"),
        (15, "Bye", "TBD"), (16, "Bye", "TBD")
    ],
    "HWT": [
        (1, "Gable Steveson", "Minnesota"), (2, "Greg Kerkvliet", "Penn State"),
        (3, "Joshua Heindselman", "Michigan"), (4, "Nick Feldman", "Ohio State"),
        (5, "Luke Luffman", "Illinois"), (6, "Yaraslau Slavikouski", "Rutgers"),
        (7, "Ben Kueter", "Iowa"), (8, "Jacob Bullock", "Indiana"),
        (9, "Seth Nevills", "Maryland"), (10, "Hayden Filipovich", "Purdue"),
        (11, "Harley Andrews", "Nebraska"), (12, "Max Vanadia", "Michigan State"),
        (13, "Dirk Morley", "Northwestern"), (14, "Gannon Rosenfeld", "Wisconsin"),
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
    "Round 6": 6,
    "Round 7": 7,
    "Round 8": 8,
    "Round 9": 9
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
    5: "Round 6",
    6: "Round 7",
    7: "Round 8",
    8: "Round 9"
}

ALL_ROUNDS = [1, 2, 2.5, 3, 3.5, 4, 5, 6, 7, 8, 9]

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

# --- Local Cache Functions ---
CACHE_FILE = "wrestling_state.json"

def save_to_local_cache(state_data):
    """Save the app state to a local JSON file."""
    try:
        with open(CACHE_FILE, 'w') as f:
            json.dump(state_data, f, indent=2)
        print(f"State saved to local cache: {CACHE_FILE}")
    except Exception as e:
        st.error(f"Failed to save to local cache: {e}")

def load_from_local_cache():
    """Load the app state from a local JSON file if it exists."""
    try:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'r') as f:
                state_data = json.load(f)
            print(f"State loaded from local cache: {CACHE_FILE}")
            return state_data
        return None
    except Exception as e:
        st.error(f"Failed to load from local cache: {e}")
        return None

# --- Custom CSS ---
def get_css(is_todd_and_easter_active):
    if is_todd_and_easter_active:
        css = """
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
            .excel-row-eliminated {
                display: flex;
                justify-content: space-between;
                padding: 5px;
                background-color: #e74c3c;
                font-family: 'Roboto', sans-serif;
                font-size: 14px;
            }
            .excel-cell {
                flex: 1;
                text-align: center;
                color: #FFFFFF;
            }
            .excel-cell.points {
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
            .centered-title {
                text-align: center;
                width: 100%;
            }
            .match-results-container {
                max-width: 100%;
                font-family: 'Roboto', sans-serif;
                font-size: 14px;
            }
            .match-card {
                border: 1px solid #ccc;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                margin: 2px 0;
            }
            .bracket-container {
                display: flex;
                flex-direction: row;
                overflow-x: auto;
                padding: 10px 0;
                gap: 20px;
            }
            .round-card {
                background-color: #041E42;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 10px;
                min-width: 200px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            .match-pair {
                margin-bottom: 20px;
            }
            @media (max-width: 600px) {
                h4 {
                    font-size: 16px;
                }
                .match-results-container, .bracket-container {
                    font-size: 12px;
                }
                .match-card {
                    padding: 8px;
                }
            }
            </style>
        """
    else:
        css = """
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
            .excel-row-eliminated {
                display: flex;
                justify-content: space-between;
                padding: 5px;
                background-color: #e74c3c;
                font-family: 'Roboto', sans-serif;
                font-size: 14px;
            }
            .excel-cell {
                flex: 1;
                text-align: center;
                color: #FFFFFF;
            }
            .excel-cell.points {
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
                50% { box-shadow: 0 0 15px #FFD54F; }
                100% { box-shadow: 0 0 5px #FFD54F; }
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
            .centered-title {
                text-align: center;
                width: 100%;
            }
            .match-results-container {
                max-width: 100%;
                font-family: 'Roboto', sans-serif;
                font-size: 14px;
            }
            .match-card {
                border: 1px solid #ccc;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                margin: 2px 0;
            }
            .bracket-container {
                display: flex;
                flex-direction: row;
                overflow-x: auto;
                padding: 10px 0;
                gap: 20px;
            }
            .round-card {
                background-color: #1F2525;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 10px;
                min-width: 200px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            .match-pair {
                margin-bottom: 20px;
            }
            @media (max-width: 600px) {
                h4 {
                    font-size: 16px;
                }
                .match-results-container, .bracket-container {
                    font-size: 12px;
                }
                .match-card {
                    padding: 8px;
                }
            }
            </style>
        """
    return css
	
	
	# --- Database Functions ---
def initialize_firebase():
    """Initialize Firebase with a fallback to local cache if unavailable."""
    try:
        if not firebase_admin._apps:
            cred_json = os.getenv("FIREBASE_CRED")
            if not cred_json:
                raise ValueError("FIREBASE_CRED environment variable not set")
            cred_dict = json.loads(cred_json)
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred, {
                'databaseURL': "https://wrestlingpickem-default-rtdb.firebaseio.com/"
            })
        db_ref = db.reference("/")
        st.session_state.is_offline = False
        return db_ref
    except Exception as e:
        st.warning(f"Firebase initialization failed: {e}. Switching to offline mode with local cache.")
        st.session_state.is_offline = True
        return None  # Return None to indicate offline mode

def save_state(db_ref):
    """Save the app state to Firebase (if online) and local cache."""
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
            
            # Save to local cache unconditionally
            save_to_local_cache(state_data)
            
            # Save to Firebase if online
            if db_ref and not st.session_state.get("is_offline", False):
                db_ref.child("state").set(state_data)
                st.success("State saved to Firebase and local cache successfully!")
            else:
                st.success("State saved to local cache (offline mode).")
        except Exception as e:
            st.error(f"Failed to save state: {e}")

def load_state(db_ref):
    """Load the app state from Firebase (if online) or local cache."""
    try:
        # Try loading from Firebase if available
        if db_ref and not st.session_state.get("is_offline", False):
            state = db_ref.child("state").get() or {}
            source = "Firebase"
        else:
            # Fallback to local cache
            state = load_from_local_cache() or {}
            source = "local cache"
            
        # Populate session state from loaded data
        st.session_state.df = pd.DataFrame(state.get("df", [])) if state.get("df") else create_dataframe(DATA)
        st.session_state.match_results = pd.DataFrame(state.get("match_results", [])) if state.get("match_results") else pd.DataFrame(columns=["Weight Class", "Round", "Match Index", "W1", "W2", "Winner", "Loser", "Win Type", "Submitted"])
        st.session_state.user_assignments = state.get("user_assignments", {})
        st.session_state.available_rounds_by_weight = state.get("available_rounds_by_weight", {weight: ["Round 1"] for weight in WEIGHT_CLASSES})
        st.session_state.selected_tabs = state.get("selected_tabs", {weight: "Round 1" for weight in WEIGHT_CLASSES})
        st.session_state.selected_weight = state.get("selected_weight", "125 lbs")
        st.session_state.users = state.get("users", ["Todd", "Hurley", "Beau", "Kyle", "Tony"])
        
        if source == "local cache" and not state:
            st.warning("No local cache found. Initializing with default state.")
        else:
            st.info(f"State loaded from {source}.")
    except Exception as e:
        st.error(f"Failed to load state: {e}")
        # Fallback to default initialization if both Firebase and cache fail
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

@st.cache_data
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
    round_order = ["Round 1", "Round 2", "Round 3", "Round 4", "Round 5", "Round 6", "Round 7", "Round 8", "Round 9"]
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

def display_match_results(df, weight_class):
    st.write(f"### Match Results Recap - {weight_class}")
    user_wrestlers = set(df[df["User"] == st.session_state.user_name]["Name"].tolist())
    
    if "match_results" not in st.session_state or st.session_state.match_results.empty:
        st.warning(f"No match results available for {weight_class}.")
        return
    
    weight_results = st.session_state.match_results[
        (st.session_state.match_results["Weight Class"] == weight_class) &
        (st.session_state.match_results["Submitted"] == 1)
    ]
    
    if weight_results.empty:
        st.info(f"No submitted match results for {weight_class} yet.")
        return
    
    st.markdown("<div class='match-results-container'>", unsafe_allow_html=True)
    
    for round_num in ALL_ROUNDS:
        round_results = weight_results[weight_results["Round"] == round_num]
        if not round_results.empty:
            round_display_names = {
                1: "Round of 16",
                2: "Quarterfinals",
                2.5: "Consolation Round 1",
                3: "Semifinals",
                3.5: "Consolation Quarterfinals",
                4: "Consolation Semifinals 1",
                5: "Consolation Semifinals 2",
                6: "7th/8th Place Match",
                7: "Championship Final",
                8: "3rd/4th Place Match",
                9: "5th/6th Place Match"
            }
            round_name = round_display_names.get(round_num, f"Round {round_num}")
            st.markdown(f"<h4>{round_name}</h4>", unsafe_allow_html=True)
            
            for _, match in round_results.iterrows():
                w1 = match["W1"]
                w2 = match["W2"]
                winner = match["Winner"]
                loser = match["Loser"]
                win_type = match["Win Type"]
                
                match_text = f"{winner} ({win_type}) over {loser}"
                bg_color = "#2A3030"
                if winner in user_wrestlers:
                    bg_color = "#2ecc71"
                elif loser in user_wrestlers:
                    bg_color = "#e74c3c"
                
                card_html = f"""
                    <div class='match-card' style='background-color: {bg_color}; padding: 10px; border-radius: 5px; margin: 5px 0; color: white;'>
                        {match_text}
                    </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

@st.cache_data
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
    
    final_school_totals = school_df.iloc[-1].sort_values(ascending=False)
    top_5_schools = final_school_totals.head(5).index
    school_df = school_df[top_5_schools]
    
    return user_df, school_df

def display_bracket(df, weight_class):
    # Debug: Print to verify HTML/CSS output and data
    print(f"Generating bracket for {weight_class}...")
    print(f"match_results shape: {st.session_state.match_results.shape}")
    print(f"match_results sample: {st.session_state.match_results.head().to_dict()}")

    # Get wrestlers and match results for the specific weight class
    wrestlers = df[df["Weight Class"] == weight_class].sort_values(by="Seed")
    match_results = st.session_state.match_results[
        (st.session_state.match_results["Weight Class"] == weight_class)
    ]  # Include all matches, not just submitted, for checking
    
    # Define bracket types and their rounds
    bracket_types = {
        "Winners’ Bracket": [1, 2, 3, 7],
        "Losers’ Bracket": [2.5, 3.5, 4, 5, 8],
        "Placement Matches": [6, 9]  # Includes 7th/8th (R6), 5th/6th (R9)
    }
    
    # Map numeric rounds to descriptive names
    round_names = {
        1: "Round of 16",
        2: "Quarterfinals",
        3: "Semifinals",
        7: "Championship Finals",
        2.5: "Consolation R1",
        3.5: "Consolation Quarters",
        4: "Consolation Semis 1",
        5: "Consolation Semis 2",
        6: "7th/8th Place",
        8: "3rd/4th Place",
        9: "5th/6th Place"
    }
    
    # Define round order for each bracket type
    round_order = {
        "Winners’ Bracket": [1, 2, 3, 7],
        "Losers’ Bracket": [2.5, 3.5, 4, 5, 8],
        "Placement Matches": [6, 9]
    }
    
    # Use tabs for bracket type selection
    bracket_tabs = st.tabs(list(bracket_types.keys()))
    
    for bracket_name, bracket_tab in zip(bracket_types.keys(), bracket_tabs):
        with bracket_tab:
            rounds_to_show = bracket_types[bracket_name]
            st.write(f"#### {bracket_name}")
            
            # Container for horizontal scrolling with dark grey background
            html = "<div class='bracket-container' style='background-color: #2A3030;'>"
            
            for round_num in rounds_to_show:
                # Determine the number of matches for this round based on match_results or max possible
                round_matches = match_results[match_results["Round"] == round_num]
                max_matches = len(match_orders.get(round_num, []))  # Fallback to match_orders for structure
                
                # Manual positioning for each match in each round
                manual_positions = {
                    1: [10, 60, 110, 160, 210, 260, 310, 360],  # Round 1 (8 matches)
                    2: [90, 310, 525, 740],  # Round 2 (4 matches)
                    3: [240, 480],  # Round 3 (2 matches)
                    7: [390],  # Round 7 (1 match)
                    2.5: [10, 60, 110, 160],  # Round 2.5 (4 matches)
                    3.5: [10, 60, 110, 160],  # Round 3.5 (4 matches)
                    4: [90, 310],  # Round 4 (2 matches)
                    5: [90, 310],  # Round 5 (2 matches)
                    6: [10],  # Round 6 (1 match)
                    8: [250],  # Round 8 (1 match)
                    9: [10]   # Round 9 (1 match)
                }
                
                # Determine if this round should be displayed based on completion of previous round
                show_round = True
                if round_num in round_order[bracket_name]:
                    round_index = round_order[bracket_name].index(round_num)
                    if round_index > 0:
                        prev_round = round_order[bracket_name][round_index - 1]
                        prev_matches = match_results[
                            (match_results["Round"] == prev_round) &
                            (match_results["Submitted"] == 1)
                        ]
                        show_round = len(prev_matches) == len(match_orders.get(prev_round, []))  # Check if all previous matches are submitted
                
                if show_round:
                    # Round container (without box styling, wider columns, dark grey background, stretched vertically)
                    html += f"<div class='round-container' style='background-color: #2A3030;'><h4>{round_names[round_num]}</h4>"
                    
                    for i in range(max_matches):  # Loop through all possible matches in this round
                        # Fetch match data from match_results if available
                        match_data = match_results[
                            (match_results["Round"] == round_num) &
                            (match_results["Match Index"] == i) &
                            (match_results["Submitted"] == 1)
                        ]
                        
                        w1 = ""
                        w2 = ""
                        w1_text = ""
                        w2_text = ""
                        w1_bg = "#2A3030"  # Default grey
                        w2_bg = "#2A3030"
                        
                        if not match_data.empty:
                            # Use match_results for historical matches
                            w1 = match_data["W1"].iloc[0]
                            w2 = match_data["W2"].iloc[0]
                            winner = match_data["Winner"].iloc[0]
                            win_type = match_data["Win Type"].iloc[0]
                            loser = match_data["Loser"].iloc[0]
                            
                            # Fetch original seed and school from DATA, using Original Seed from df
                            w1_seed = wrestlers[wrestlers["Name"] == w1]["Original Seed"].iloc[0] if w1 in wrestlers["Name"].values else "N/A"
                            w2_seed = wrestlers[wrestlers["Name"] == w2]["Original Seed"].iloc[0] if w2 in wrestlers["Name"].values else "N/A"
                            w1_school = next((sch for _, n, sch in DATA[weight_class] if n == w1), "TBD")
                            w2_school = next((sch for _, n, sch in DATA[weight_class] if n == w2), "TBD")
                            
                            # Format wrestler text with Original Seed
                            w1_text = f"({w1_seed}) {w1} - {w1_school}"
                            w2_text = f"({w2_seed}) {w2} - {w2_school}"
                            
                            if winner == w1:
                                w1_text += f" ({win_type})"
                                w1_bg = "#2ecc71"  # Green for winner
                                if round_num == 7:  # Add crown for Championship Finals winner
                                    w1_text = f"{w1_text} <span class='crown'>♚</span>"  # Black chess king (crown-like)
                            elif winner == w2:
                                w2_text += f" ({win_type})"
                                w2_bg = "#2ecc71"  # Green for winner
                                if round_num == 7:  # Add crown for Championship Finals winner
                                    w2_text = f"{w2_text} <span class='crown'>♚</span>"  # Black chess king (crown-like)
                        else:
                            # For upcoming (unsubmitted) matches, use generate_matchups, but only if previous round is complete
                            if show_round:
                                matchups = generate_matchups(df, weight_class, round_num)
                                if i < len(matchups):
                                    w1, w2 = matchups[i]
                                    # Fetch seeds and schools for upcoming wrestlers
                                    w1_seed = wrestlers[wrestlers["Name"] == w1]["Original Seed"].iloc[0] if w1 in wrestlers["Name"].values else "N/A"
                                    w2_seed = wrestlers[wrestlers["Name"] == w2]["Original Seed"].iloc[0] if w2 in wrestlers["Name"].values else "N/A"
                                    w1_school = next((sch for _, n, sch in DATA[weight_class] if n == w1), "TBD")
                                    w2_school = next((sch for _, n, sch in DATA[weight_class] if n == w2), "TBD")
                                    
                                    # Format wrestler text with Original Seed
                                    w1_text = f"({w1_seed}) {w1} - {w1_school}"
                                    w2_text = f"({w2_seed}) {w2} - {w2_school}"
                                    w1_bg = "#2A3030"  # Grey for upcoming match
                                    w2_bg = "#2A3030"
                                else:
                                    w1_text = "TBD"
                                    w2_text = "TBD"
                                    w1_bg = "#2A3030"
                                    w2_bg = "#2A3030"
                            else:
                                # If previous round isn’t complete, show blank cards
                                w1_text = ""
                                w2_text = ""
                                w1_bg = "#2A3030"
                                w2_bg = "#2A3030"
                        
                        # Use manual positioning from manual_positions
                        position = manual_positions.get(round_num, [0])[i] if i < len(manual_positions.get(round_num, [])) else 0
                        position_style = f"position: relative; top: {position}px;"
                        
                        # Match pair container with manual positioning (blank, TBD, or upcoming match)
                        html += f"<div class='match-pair' style='{position_style}'>"
                        html += f"""
                            <div class='match-card' style='background-color: {w1_bg}; padding: 20px; border-radius: 5px; color: white; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;'>
                                {w1_text}
                            </div>
                            <div class='match-card' style='background-color: {w2_bg}; padding: 20px; border-radius: 5px; color: white; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;'>
                                {w2_text}
                            </div>
                        """
                        html += "</div>"
                
                html += "</div>"
            
            html += "</div>"
            
            # CSS for styling, with wider columns, no boxes, dark grey background, stretched columns, wider cards, larger crown
            css = """
                <style>
                .bracket-container {
                    display: flex;
                    flex-direction: row;
                    overflow-x: auto;
                    padding: 10px 0;
                    gap: 0;  /* Removed gap to eliminate black line, using dark grey background */
                    background-color: #2A3030;  /* Dark grey background for everything under headers */
                    min-height: 100vh;  /* Ensure container fills viewport height */
                    height: auto;  /* Allow content to determine height if exceeding viewport */
                }
                .round-container {
                    background-color: #2A3030;  /* Dark grey background for rounds, matching container */
                    padding: 10px;
                    min-width: 400px;  /* Increased width for longer text */
                    position: relative;  /* For absolute positioning of matches */
                    min-height: 100%;  /* Stretch to fill container height */
                    height: auto;  /* Allow content to determine height */
                    display: flex;
                    flex-direction: column;
                    justify-content: flex-start;  /* Align content to top */
                    flex-grow: 1;  /* Ensure columns grow to fill available vertical space */
                }
                .round-container h4 {
                    text-align: center;
                    color: #FFC107;
                    font-size: 16px;
                }
                .match-pair {
                    display: flex;
                    flex-direction: column;
                    gap: 5px;
                    margin-bottom: 0;  /* Removed default margin to allow manual positioning */
                }
                .match-card {
                    text-align: center;
                    min-height: 40px;  /* Ensure consistent card height for spacing */
                    padding: 20px;  /* Increased padding for wider cards */
                    border-radius: 5px;
                    color: white;
                    white-space: nowrap;
                    overflow: hidden;
                    text-overflow: ellipsis;
                    width: 100%;  /* Ensure cards fill the container width */
                }
                .crown {
                    font-size: 24px;  /* Larger crown size */
                    vertical-align: middle;  /* Align with text */
                }
                @media (max-width: 600px) {
                    .bracket-container {
                        background-color: #2A3030;  /* Maintain dark grey on mobile */
                    }
                    .round-container {
                        min-width: 300px;  /* Reduced width for mobile */
                    }
                    .round-container h4 {
                        font-size: 14px;
                    }
                    .match-card {
                        font-size: 12px;
                        padding: 15px;  /* Reduced padding for mobile */
                        min-height: 30px;
                    }
                    .crown {
                        font-size: 18px;  /* Smaller crown on mobile */
                    }
                }
                </style>
            """
            
            # Combine CSS and HTML, ensuring proper rendering
            full_html = f"{css}{html}"
            st.markdown(full_html, unsafe_allow_html=True)
		
def calculate_max_points_available(wrestler_name, df, match_results):
    wrestler_matches = match_results[(match_results["Winner"] == wrestler_name) | (match_results["Loser"] == wrestler_name)]
    wins = len(wrestler_matches[wrestler_matches["Winner"] == wrestler_name])
    losses = len(wrestler_matches[wrestler_matches["Loser"] == wrestler_name])
    earned_points = df[df["Name"] == wrestler_name]["Points"].iloc[0] if not df[df["Name"] == wrestler_name].empty else 0
    latest_round = wrestler_matches["Round"].max() if not wrestler_matches.empty else 0
    sorted_matches = wrestler_matches.sort_values(by="Round")

    # Check if wrestler is in an unsubmitted placement match (R6, R8, R9)
    placement_rounds = [6, 8, 9]
    in_placement = any(
        not match_results[
            (match_results["Round"] == r) &
            ((match_results["W1"] == wrestler_name) | (match_results["W2"] == wrestler_name)) &
            (match_results["Submitted"] != 1)
        ].empty
        for r in placement_rounds
    )

    def was_in_winners_bracket(round_num):
        prior_matches = sorted_matches[sorted_matches["Round"] < round_num]
        return len(prior_matches) == 0 or prior_matches["Loser"].iloc[-1] not in ["Bye", wrestler_name]

    if losses == 0:  # Still in winners' bracket
        if latest_round < 7:
            remaining_wins = 4 - wins
            remaining_base = 0
            if wins == 0:
                remaining_base = 1 + 7 + 7 + 4  # R1, R2, R3, R7
            elif wins == 1:
                remaining_base = 7 + 7 + 4      # R2, R3, R7
            elif wins == 2:
                remaining_base = 7 + 4          # R3, R7
            elif wins == 3:
                remaining_base = 4             # R7
            remaining_bonus = remaining_wins * 2
            if "Bye" in wrestler_matches[wrestler_matches["Round"] == 1]["Loser"].values and wins == 0:
                remaining_base = 0 + 8 + 7 + 4  # Bye adjustment
            return earned_points + remaining_base + remaining_bonus
        elif latest_round == 7:
            return earned_points  # Championship completed

    elif losses == 1:  # In losers' bracket
        if latest_round < 6:
            total_wins_needed = 6 if was_in_winners_bracket(latest_round) else 5
            remaining_wins = total_wins_needed - wins
            remaining_base = 0
            if wins == 0:
                remaining_base = 0.5 + 3.5 + 3.5 + 3.5 + 1
            elif wins == 1:
                remaining_base = (3.5 + 3.5 + 3.5 + 1) if was_in_winners_bracket(latest_round) else (3.5 + 3.5 + 3.5 + 1)
            elif wins == 2:
                remaining_base = 3.5 + 3.5 + 1
            elif wins == 3:
                remaining_base = 3.5 + 1
            elif wins == 4:
                remaining_base = 1
            remaining_bonus = remaining_wins * 2
            if "Bye" in wrestler_matches[wrestler_matches["Round"] == 1]["Loser"].values and wins <= 1:
                remaining_base += 0.5 if wins < 2 else 0
            return earned_points + remaining_base + remaining_bonus
        elif latest_round in [6, 8, 9] and in_placement:
            return earned_points + 1 + 2  # Active in R6, R8, or R9
        elif latest_round == 6:
            return earned_points  # 7th/8th completed
        elif latest_round == 8:
            return earned_points  # 3rd/4th completed
        elif latest_round == 9:
            return earned_points  # 5th/6th completed

    elif losses == 2:  # Double elimination
        if latest_round < 6:
            if wins >= 2 and sorted_matches[sorted_matches["Loser"] == wrestler_name]["Round"].iloc[1] <= 4:
                return earned_points + 1 + 2  # R6: 1 base + 2 bonus if win
            elif wins >= 1 and sorted_matches[sorted_matches["Loser"] == wrestler_name]["Round"].iloc[1] <= 3.5:
                return earned_points + 3.5 + 1 + 2  # R5 + R9: 3.5 + 1 base + 2 bonus if win
            else:
                return earned_points  # Truly eliminated
        elif latest_round < 9 and sorted_matches[sorted_matches["Loser"] == wrestler_name]["Round"].iloc[1] <= 5:
            return earned_points + 1 + 2  # R9: 1 base + 2 bonus if win
        elif in_placement:  # Still active in R6, R8, or R9
            return earned_points + 1 + 2  # Max possible from placement match
        elif latest_round in [6, 9]:  # 7th/8th or 5th/6th completed
            return earned_points  # No further points possible
        else:
            return earned_points  # Truly eliminated

    return earned_points

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
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "reset_tournament_confirm" not in st.session_state:
    st.session_state.reset_tournament_confirm = 0
if "reset_assignments_confirm" not in st.session_state:
    st.session_state.reset_assignments_confirm = 0
if "delete_state_confirm" not in st.session_state:
    st.session_state.delete_state_confirm = 0
if "is_offline" not in st.session_state:
    st.session_state.is_offline = False
if "prev_selected_page" not in st.session_state:
    st.session_state.prev_selected_page = None	

db_ref = initialize_firebase()
firebase_state = db_ref.child("state").get() if db_ref else None
if firebase_state:
    load_state(db_ref)
else:
    initialize_session_state()

st.markdown('<div class="centered-title"><h1>Big Ten Wrestling Score Tracker</h1></div>', unsafe_allow_html=True)

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
    selected_page = st.sidebar.radio("Navigation", ["Team Selection", "Tournament", "Drafted Teams", "My Team", "Individual Leaderboard", "NCAA Teams", "Match Results", "Bracket"])
else:
    selected_page = st.sidebar.radio("Navigation", ["Drafted Teams", "My Team", "Individual Leaderboard", "NCAA Teams", "Match Results", "Bracket"])

# Check if the selected page has changed
if st.session_state.prev_selected_page != selected_page:
    # Update the previous page
    st.session_state.prev_selected_page = selected_page
    # Force sidebar to collapse by rerunning with a query parameter
    st.query_params["sidebar_state"] = "collapsed"
    st.rerun()
	
if st.sidebar.button("Refresh Data"):
    load_state(db_ref)
    df = st.session_state.df
    st.success("Data refreshed from latest state!")

if st.session_state.is_offline:
    st.sidebar.warning("Running in offline mode. Changes will be saved locally.")

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

# Calculate overperformers and underperformers globally
expected_points_by_seed = {
    1:  [1, 8, 8, 15, 15, 15, 15, 15, 19, 19, 19],
    2:  [1, 8, 8, 15, 15, 15, 15, 15, 15, 15, 15],
    3:  [1, 8, 8, 8, 8, 8, 11.5, 11.5, 11.5, 12.5, 12.5],
    4:  [1, 8, 8, 8, 8, 8, 11.5, 11.5, 11.5, 11.5, 11.5],
    5:  [1, 1, 1.5, 1.5, 5, 8.5, 8.5, 8.5, 8.5, 8.5, 9.5],
    6:  [1, 1, 1.5, 1.5, 5, 8.5, 8.5, 8.5, 8.5, 8.5, 8.5],
    7:  [1, 1, 1.5, 1.5, 5, 5, 5, 6, 6, 6, 6],
    8:  [1, 1, 1.5, 1.5, 5, 5, 5, 5, 5, 5, 5],
    9:  [0, 0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
    10: [0, 0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
    11: [0, 0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
    12: [0, 0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
    13: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    14: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    15: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    16: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
}
round_index = {1: 0, 2: 1, 2.5: 2, 3: 3, 3.5: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 10}
latest_round = st.session_state.match_results[st.session_state.match_results["Submitted"] == 1]["Round"].max() if not st.session_state.match_results.empty else 0

if latest_round > 0:
    latest_idx = round_index.get(latest_round, 0)
    df_performance = df.copy()
    df_performance["Expected Points"] = df_performance["Original Seed"].apply(
        lambda seed: expected_points_by_seed.get(int(seed), [0])[min(latest_idx, len(expected_points_by_seed.get(int(seed), [0])) - 1)]
    )
    df_performance["Performance Delta"] = df_performance["Points"] - df_performance["Expected Points"]
    top_overperformers = df_performance[df_performance["Performance Delta"] > 0].sort_values(by="Performance Delta", ascending=False).head(20)["Name"].tolist()
    top_underperformers = df_performance[df_performance["Performance Delta"] < 0].sort_values(by="Performance Delta", ascending=True).head(20)["Name"].tolist()
else:
    top_overperformers = []
    top_underperformers = []

# Pages
if selected_page == "My Team":
    display_name = "Penn State Todd" if st.session_state.user_name == "Todd" and is_penn_state_todd_active else st.session_state.user_name
    st.write(f"### Welcome, {display_name}!")
    st.write("#### Your Wrestlers")
    user_wrestlers = df[df["User"] == st.session_state.user_name].sort_values(by="Points", ascending=False)
    if not user_wrestlers.empty:
        st.markdown('<div class="excel-chart">', unsafe_allow_html=True)
        st.markdown("""
            <div class="excel-row">
                <div class="excel-header">Seed</div>
                <div class="excel-header">Name</div>
                <div class="excel-header">Weight Class</div>
                <div class="excel-header">Points</div>
                <div class="excel-header">Bonus Points</div>
                <div class="excel-header">School</div>
            </div>
        """, unsafe_allow_html=True)
        total_points = 0
        total_bonus_points = 0
        for idx, (_, wrestler) in enumerate(user_wrestlers.iterrows()):
            seed = wrestler["Original Seed"]
            bonus_points = calculate_bonus_points(wrestler["Name"], st.session_state.match_results)
            total_points += wrestler["Points"]
            total_bonus_points += bonus_points
            max_points = calculate_max_points_available(wrestler["Name"], df, st.session_state.match_results)
            is_eliminated = max_points == wrestler["Points"]
            row_class = "excel-row-top" if seed == 1 else "excel-row-eliminated" if is_eliminated else "excel-row"
            seed_display = f"{seed}"
            if wrestler["Name"] in top_overperformers:
                seed_display = f'<span style="color: #00FF00;">▲</span> {seed}'
            elif wrestler["Name"] in top_underperformers:
                seed_display = f'<span style="color: #FF0000;">▼</span> {seed}'
            st.markdown(f"""
                <div class="{row_class}">
                    <div class="excel-cell">{seed_display}</div>
                    <div class="excel-cell">{wrestler["Name"]}</div>
                    <div class="excel-cell">{wrestler["Weight Class"]}</div>
                    <div class="excel-cell points">{wrestler["Points"]:.1f}</div>
                    <div class="excel-cell bonus-points" style="color: #FFC107;">{bonus_points:.1f}</div>
                    <div class="excel-cell">{wrestler["School"]}</div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown(f"""
            <div class="excel-row" style="font-weight: bold;">
                <div class="excel-cell">TOTAL</div>
                <div class="excel-cell"></div>
                <div class="excel-cell"></div>
                <div class="excel-cell points">{total_points:.1f}</div>
                <div class="excel-cell bonus-points" style="color: #FFC107;">{total_bonus_points:.1f}</div>
                <div class="excel-cell"></div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.write("No wrestlers assigned yet!")
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
            points_display = float(row["Points"]) if pd.notna(row["Points"]) else 0.0
            bonus_points = user_bonus_points[user]
            max_points = user_max_points[user]
            row_class = "excel-row-top" if rank == 1 else "excel-row"
            st.markdown(f"""
                <div class="{row_class}">
                    <div class="excel-cell">{rank}</div>
                    <div class="excel-cell">{display_user}</div>
                    <div class="excel-cell points">{points_display:.1f}</div>
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
    leaderboard_views = st.tabs(["Points Leaders", "Game Changers", "Underperformers"])
    
    with leaderboard_views[0]:
        leaderboard = df.sort_values(by="Points", ascending=False)
        if not leaderboard.empty:
            st.markdown('<div class="excel-chart">', unsafe_allow_html=True)
            st.markdown("""
                <div class="excel-row">
                    <div class="excel-header">Seed</div>
                    <div class="excel-header">Name</div>
                    <div class="excel-header">Weight Class</div>
                    <div class="excel-header">Points</div>
                    <div class="excel-header">School</div>
                    <div class="excel-header">User</div>
                </div>
            """, unsafe_allow_html=True)
            for _, wrestler in leaderboard.iterrows():
                seed = wrestler["Original Seed"]
                display_user = "Penn State Todd" if wrestler["User"] == "Todd" and is_penn_state_todd_active else wrestler["User"] or ""
                row_class = "excel-row-top" if seed == 1 else "excel-row"
                st.markdown(f"""
                    <div class="{row_class}">
                        <div class="excel-cell">{seed}</div>
                        <div class="excel-cell">{wrestler["Name"]}</div>
                        <div class="excel-cell">{wrestler["Weight Class"]}</div>
                        <div class="excel-cell points" style="color: #FFC107;">{wrestler["Points"]:.1f}</div>
                        <div class="excel-cell">{wrestler["School"]}</div>
                        <div class="excel-cell">{display_user}</div>
                    </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.write("No leaderboard data available yet!")

    with leaderboard_views[1]:
        if latest_round > 0:
            latest_idx = round_index.get(latest_round, 0)
            leaderboard = df.copy()
            leaderboard["Expected Points"] = leaderboard["Original Seed"].apply(
                lambda seed: expected_points_by_seed.get(int(seed), [0])[min(latest_idx, len(expected_points_by_seed.get(int(seed), [0])) - 1)]
            )
            leaderboard["Game Changer Score"] = leaderboard["Points"] - leaderboard["Expected Points"]
            leaderboard = leaderboard[leaderboard["Game Changer Score"] > 0].sort_values(by=["Game Changer Score", "Points"], ascending=[False, False])
        
        if not leaderboard.empty and latest_round > 0:
            st.markdown('<div class="excel-chart">', unsafe_allow_html=True)
            st.markdown("""
                <div class="excel-row">
                    <div class="excel-header">Seed</div>
                    <div class="excel-header">Name</div>
                    <div class="excel-header">Weight Class</div>
                    <div class="excel-header">Points</div>
                    <div class="excel-header">Over Expected</div>
                    <div class="excel-header">School</div>
                    <div class="excel-header">User</div>
                </div>
            """, unsafe_allow_html=True)
            for _, wrestler in leaderboard.iterrows():
                seed = wrestler["Original Seed"]
                over_expected = wrestler["Game Changer Score"]
                display_user = "Penn State Todd" if wrestler["User"] == "Todd" and is_penn_state_todd_active else wrestler["User"] or ""
                row_class = "excel-row-top" if wrestler["Game Changer Score"] == leaderboard["Game Changer Score"].max() else "excel-row"
                st.markdown(f"""
                    <div class="{row_class}">
                        <div class="excel-cell">{seed}</div>
                        <div class="excel-cell">{wrestler["Name"]}</div>
                        <div class="excel-cell">{wrestler["Weight Class"]}</div>
                        <div class="excel-cell points" style="color: #FFC107;">{wrestler["Points"]:.1f}</div>
                        <div class="excel-cell" style="color: #FFC107;">{over_expected:.1f}</div>
                        <div class="excel-cell">{wrestler["School"]}</div>
                        <div class="excel-cell">{display_user}</div>
                    </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.write("No game changers identified yet—submit more match results!")

    with leaderboard_views[2]:
        if latest_round > 0:
            latest_idx = round_index.get(latest_round, 0)
            leaderboard = df.copy()
            leaderboard["Expected Points"] = leaderboard["Original Seed"].apply(
                lambda seed: expected_points_by_seed.get(int(seed), [0])[min(latest_idx, len(expected_points_by_seed.get(int(seed), [0])) - 1)]
            )
            leaderboard["Under Expected"] = leaderboard["Points"] - leaderboard["Expected Points"]
            leaderboard = leaderboard[leaderboard["Under Expected"] < 0].sort_values(by="Under Expected", ascending=True)
        
        if not leaderboard.empty and latest_round > 0:
            st.markdown('<div class="excel-chart">', unsafe_allow_html=True)
            st.markdown("""
                <div class="excel-row">
                    <div class="excel-header">Seed</div>
                    <div class="excel-header">Name</div>
                    <div class="excel-header">Weight Class</div>
                    <div class="excel-header">Points</div>
                    <div class="excel-header">Under Expected</div>
                    <div class="excel-header">School</div>
                    <div class="excel-header">User</div>
                </div>
            """, unsafe_allow_html=True)
            for _, wrestler in leaderboard.iterrows():
                seed = wrestler["Original Seed"]
                under_expected = wrestler["Under Expected"]
                display_user = "Penn State Todd" if wrestler["User"] == "Todd" and is_penn_state_todd_active else wrestler["User"] or ""
                row_class = "excel-row-top" if wrestler["Under Expected"] == leaderboard["Under Expected"].min() else "excel-row"
                st.markdown(f"""
                    <div class="{row_class}">
                        <div class="excel-cell">{seed}</div>
                        <div class="excel-cell">{wrestler["Name"]}</div>
                        <div class="excel-cell">{wrestler["Weight Class"]}</div>
                        <div class="excel-cell points" style="color: #FFC107;">{wrestler["Points"]:.1f}</div>
                        <div class="excel-cell" style="color: #FFC107;">{under_expected:.1f}</div>
                        <div class="excel-cell">{wrestler["School"]}</div>
                        <div class="excel-cell">{display_user}</div>
                    </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.write("No underperformers identified yet—submit more match results!")

elif selected_page == "Drafted Teams":
    st.write("### Drafted Teams")
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
                        <div class="excel-header">Seed</div>
                        <div class="excel-header">Name</div>
                        <div class="excel-header">Weight Class</div>
                        <div class="excel-header">Points</div>
                        <div class="excel-header">Bonus Points</div>
                        <div class="excel-header">School</div>
                    </div>
                """, unsafe_allow_html=True)
                total_points = 0
                total_bonus_points = 0
                for idx, (_, wrestler) in enumerate(user_wrestlers.iterrows()):
                    seed = wrestler["Original Seed"]
                    bonus_points = calculate_bonus_points(wrestler["Name"], st.session_state.match_results)
                    total_points += wrestler["Points"]
                    total_bonus_points += bonus_points
                    max_points = calculate_max_points_available(wrestler["Name"], df, st.session_state.match_results)
                    is_eliminated = max_points == wrestler["Points"]
                    row_class = "excel-row-top" if seed == 1 else "excel-row-eliminated" if is_eliminated else "excel-row"
                    seed_display = f"{seed}"
                    if wrestler["Name"] in top_overperformers:
                        seed_display = f'<span style="color: #00FF00;">▲</span> {seed}'
                    elif wrestler["Name"] in top_underperformers:
                        seed_display = f'<span style="color: #FF0000;">▼</span> {seed}'
                    st.markdown(f"""
                        <div class="{row_class}">
                            <div class="excel-cell">{seed_display}</div>
                            <div class="excel-cell">{wrestler["Name"]}</div>
                            <div class="excel-cell">{wrestler["Weight Class"]}</div>
                            <div class="excel-cell points">{wrestler["Points"]:.1f}</div>
                            <div class="excel-cell bonus-points" style="color: #FFC107;">{bonus_points:.1f}</div>
                            <div class="excel-cell">{wrestler["School"]}</div>
                        </div>
                    """, unsafe_allow_html=True)
                st.markdown(f"""
                    <div class="excel-row" style="font-weight: bold;">
                        <div class="excel-cell">TOTAL</div>
                        <div class="excel-cell"></div>
                        <div class="excel-cell"></div>
                        <div class="excel-cell points">{total_points:.1f}</div>
                        <div class="excel-cell bonus-points" style="color: #FFC107;">{total_bonus_points:.1f}</div>
                        <div class="excel-cell"></div>
                    </div>
                """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.write(f"No wrestlers assigned to {user} yet!")

elif selected_page == "NCAA Teams":
    st.write("### Team Performance")
    schools = sorted(df["School"].unique())
    school_tabs = st.tabs(schools)
    weight_order = ["125 lbs", "133 lbs", "141 lbs", "149 lbs", "157 lbs", "165 lbs", "174 lbs", "184 lbs", "197 lbs", "HWT"]  # Custom sort order with HWT last
    
    for school, tab in zip(schools, school_tabs):
        with tab:
            st.write(f"#### {school} Wrestlers")
            school_wrestlers = df[df["School"] == school].copy()
            school_wrestlers["Weight Order"] = school_wrestlers["Weight Class"].apply(lambda x: weight_order.index(x))
            school_wrestlers = school_wrestlers.sort_values(by="Weight Order").drop(columns="Weight Order")
            
            if not school_wrestlers.empty:
                st.markdown('<div class="excel-chart">', unsafe_allow_html=True)
                st.markdown("""
                    <div class="excel-row">
                        <div class="excel-header">Seed</div>
                        <div class="excel-header">Name</div>
                        <div class="excel-header">Weight Class</div>
                        <div class="excel-header">Points</div>
                        <div class="excel-header">Bonus Points</div>
                        <div class="excel-header">School</div>
                    </div>
                """, unsafe_allow_html=True)
                total_points = 0
                total_bonus_points = 0
                for idx, (_, wrestler) in enumerate(school_wrestlers.iterrows()):
                    seed = wrestler["Original Seed"]
                    bonus_points = calculate_bonus_points(wrestler["Name"], st.session_state.match_results)
                    total_points += wrestler["Points"]
                    total_bonus_points += bonus_points
                    max_points = calculate_max_points_available(wrestler["Name"], df, st.session_state.match_results)
                    is_eliminated = max_points == wrestler["Points"]
                    row_class = "excel-row-top" if seed == 1 else "excel-row-eliminated" if is_eliminated else "excel-row"
                    seed_display = f"{seed}"
                    if wrestler["Name"] in top_overperformers:
                        seed_display = f'<span style="color: #00FF00;">▲</span> {seed}'
                    elif wrestler["Name"] in top_underperformers:
                        seed_display = f'<span style="color: #FF0000;">▼</span> {seed}'
                    st.markdown(f"""
                        <div class="{row_class}">
                            <div class="excel-cell">{seed_display}</div>
                            <div class="excel-cell">{wrestler["Name"]}</div>
                            <div class="excel-cell">{wrestler["Weight Class"]}</div>
                            <div class="excel-cell points">{wrestler["Points"]:.1f}</div>
                            <div class="excel-cell bonus-points" style="color: #FFC107;">{bonus_points:.1f}</div>
                            <div class="excel-cell">{wrestler["School"]}</div>
                        </div>
                    """, unsafe_allow_html=True)
                st.markdown(f"""
                    <div class="excel-row" style="font-weight: bold;">
                        <div class="excel-cell">TOTAL</div>
                        <div class="excel-cell"></div>
                        <div class="excel-cell"></div>
                        <div class="excel-cell points">{total_points:.1f}</div>
                        <div class="excel-cell bonus-points" style="color: #FFC107;">{total_bonus_points:.1f}</div>
                        <div class="excel-cell"></div>
                    </div>
                """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.write(f"No wrestlers found for {school}.")

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
            elif selected_tab == "Round 7":
                st.write("### 1st/2nd Place Match (Round 7)")
                df = update_scores(df, generate_matchups(df, weight, 7), 7, weight)
                st.write("### 3rd/4th Place Match (Round 8)")
                df = update_scores(df, generate_matchups(df, weight, 8), 8, weight)
                st.write("### 5th/6th Place Match (Round 9)")
                df = update_scores(df, generate_matchups(df, weight, 9), 9, weight)
            else:
                df = update_scores(df, generate_matchups(df, weight, round_num), round_num, weight)

elif selected_page == "Match Results":
    weight_tabs = st.tabs(WEIGHT_CLASSES)
    for weight, tab in zip(WEIGHT_CLASSES, weight_tabs):
        with tab:
            display_match_results(df, weight)

elif selected_page == "Bracket":
    weight_tabs = st.tabs(WEIGHT_CLASSES)
    for weight, tab in zip(WEIGHT_CLASSES, weight_tabs):
        with tab:
            display_bracket(df, weight)

def delete_state(db_ref):
    """Delete the app state from Firebase (if online) and local cache."""
    if st.session_state.user_name.endswith("Kyle"):
        try:
            # Delete from Firebase if online
            if db_ref and not st.session_state.get("is_offline", False):
                db_ref.child("state").delete()
                st.success("Firebase state deleted successfully!")
            
            # Delete local cache
            if os.path.exists(CACHE_FILE):
                os.remove(CACHE_FILE)
                st.success("Local cache deleted successfully!")
            
            # Reset session state
            st.session_state.clear()
            st.session_state.user_name = ""
            st.session_state.reset_tournament_confirm = 0
            st.session_state.reset_assignments_confirm = 0
            st.session_state.delete_state_confirm = 0
            st.success("State reset complete! Returning to user selection...")
            st.rerun()
        except Exception as e:
            st.error(f"Failed to delete state: {e}")

# --- Main App Execution ---
db_ref = initialize_firebase()
firebase_state = db_ref.child("state").get() if db_ref else None
if firebase_state:
    load_state(db_ref)
else:
    initialize_session_state()

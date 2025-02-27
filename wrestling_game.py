# ... (Everything above the navigation stays the same) ...

# Navigation
if st.session_state.user_name.endswith("Kyle"):
    selected_page = st.sidebar.radio("Navigation", ["Team Selection", "Tournament", "User Assignments", "User Dashboard", "Individual Leaderboard", "Match Results", "Bracket"])
else:
    selected_page = st.sidebar.radio("Navigation", ["User Assignments", "User Dashboard", "Individual Leaderboard", "Match Results", "Bracket"])

if st.sidebar.button("Refresh Data"):
    load_state(db_ref)
    df = st.session_state.df
    st.success("Data refreshed from latest state!")

# Kyle-only admin controls
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
        total_points = 0
        total_bonus_points = 0
        for idx, (_, wrestler) in enumerate(user_wrestlers.iterrows()):
            rank = idx + 1
            bonus_points = calculate_bonus_points(wrestler["Name"], st.session_state.match_results)
            total_points += wrestler["Points"]
            total_bonus_points += bonus_points
            max_points = calculate_max_points_available(wrestler["Name"], df, st.session_state.match_results)
            is_eliminated = max_points == wrestler["Points"]
            row_class = "excel-row-top" if rank == 1 else "excel-row-eliminated" if is_eliminated else "excel-row"
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
        st.markdown(f"""
            <div class="excel-row" style="font-weight: bold;">
                <div class="excel-cell">TOTAL</div>
                <div class="excel-cell"></div>
                <div class="excel-cell"></div>
                <div class="excel-cell points">{int(total_points)}</div>
                <div class="excel-cell bonus-points">{total_bonus_points:.1f}</div>
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

elif selected_page == "User Assignments":
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
                total_points = 0
                total_bonus_points = 0
                for idx, (_, wrestler) in enumerate(user_wrestlers.iterrows()):
                    rank = idx + 1
                    bonus_points = calculate_bonus_points(wrestler["Name"], st.session_state.match_results)
                    total_points += wrestler["Points"]
                    total_bonus_points += bonus_points
                    max_points = calculate_max_points_available(wrestler["Name"], df, st.session_state.match_results)
                    is_eliminated = max_points == wrestler["Points"]
                    row_class = "excel-row-top" if rank == 1 else "excel-row-eliminated" if is_eliminated else "excel-row"
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
                st.markdown(f"""
                    <div class="excel-row" style="font-weight: bold;">
                        <div class="excel-cell">TOTAL</div>
                        <div class="excel-cell"></div>
                        <div class="excel-cell"></div>
                        <div class="excel-cell points">{int(total_points)}</div>
                        <div class="excel-cell bonus-points">{total_bonus_points:.1f}</div>
                        <div class="excel-cell"></div>
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

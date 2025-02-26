elif selected_page == "User Assignments" and st.session_state.user_name.endswith("Kyle"):
    st.write("### User Assignments")
    
    # User selection buttons across the top
    if "selected_user" not in st.session_state:
        st.session_state.selected_user = st.session_state.users[0]  # Default to first user
    
    cols = st.columns(len(st.session_state.users))
    for col, user in zip(cols, st.session_state.users):
        display_user = "Penn State Todd" if user == "Todd" and is_penn_state_todd_active else user
        with col:
            if st.button(display_user, key=f"assign_select_{user}"):
                st.session_state.selected_user = user
    
    # Display selected user's wrestlers
    selected_user = st.session_state.selected_user
    st.write(f"#### {selected_user}'s Wrestlers")
    user_wrestlers = df[df["User"] == selected_user].sort_values(by="Points", ascending=False)
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
        st.write(f"No wrestlers assigned to {selected_user} yet!")

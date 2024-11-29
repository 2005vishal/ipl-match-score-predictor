import streamlit as st
import pandas as pd
import pickle
import math

# Load the pre-trained pipeline/model
pipe = pickle.load(open('pip.pkl', 'rb'))

# Define teams and cities
team = ['Chennai Super Kings', 'Mumbai Indians',
        'Sunrisers Hyderabad', 'Kolkata Knight Riders',
        'Rajasthan Royals', 'Lucknow Super Giants', 'Gujarat Titans',
        'Punjab Kings', 'Royal Challengers Bengaluru',
        'Delhi Capitals']

cities = ['Mumbai', 'Delhi', 'Kolkata', 'Chennai', 'Hyderabad', 'Chandigarh',
          'Jaipur', 'Pune', 'Dubai', 'Abu Dhabi', 'Ahmedabad',
          'Bengaluru', 'Sharjah', 'Durban', 'Visakhapatnam', 'Lucknow',
          'Dharamsala', 'Centurion', 'Rajkot', 'Navi Mumbai', 'Indore',
          'Johannesburg', 'Port Elizabeth', 'Cuttack', 'Raipur', 'Cape Town',
          'Ranchi', 'Mohali']

# Streamlit app title
st.title("🏏 IPL Score Predictor! 🏆")
st.header("⚡ Quick Predictions for Every Match!")
st.subheader("🔥 Develop And Deploy by Vishal Patwa....")


# Layout for selecting batting and bowling teams
col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox("Select batting team", sorted(team))
with col2:
    bowling_team = st.selectbox("Select bowling team", sorted(team))

# Validation to ensure batting and bowling teams are not the same
if batting_team == bowling_team:
    st.error("Batting and Bowling teams cannot be the same. Please select different teams.")

# Select match city
city = st.selectbox("Select city", sorted(cities))

# Input fields for current score, overs, and wickets
col3, col4, col5 = st.columns(3)

with col3:
    current_score = st.number_input("Current Score", min_value=0, step=1)

with col4:
    # Use a slider for overs to ensure proper fractional increments
    over = st.number_input(
        "Overs Done (works for overs > 5)",
        min_value=5.0,
        max_value=20.0,
        step=0.1,
        format="%.1f",
        help="Enter overs completed. Use decimals for partial overs (e.g., 5.3 means 3 balls into the 6th over)."
    )

    # Correct the overs to handle cricket rules (max 5 balls before next over)
    if over % 1 > 0.5:  # If fractional part exceeds 0.5 (6th ball in an over)
        over = math.floor(over) + 1.0  # Move to the next over
    else:
        over = round(over, 1)

with col5:
    wickets = st.number_input("Wickets Out", min_value=0, max_value=10, step=1)

# Input field for runs scored in the last 5 overs
last_five = st.number_input("Runs Scored in last 5 overs", min_value=0, step=1)

# Predict button
if st.button("Predict Score"):
    if batting_team != bowling_team:  # Ensure teams are valid
        try:
            balls_left = 120 - (int(over) * 6 + round((over % 1) * 10))
            wickets_left = 10 - wickets
            crr = current_score / over

            # Prepare the input for the model
            input_data = pd.DataFrame({
                'city': [city],
                'batting_team': [batting_team],
                'bowling_team': [bowling_team],
                'current run': [current_score],
                'balls_left': [balls_left],
                'wicket_left': [wickets_left],
                'crr': [crr],
                'last_five': [last_five]
            })

            # Make a prediction
            predicted_score = pipe.predict(input_data)[0]

            # Display the predicted score
            st.subheader(f"Predicted Final Score: {int(predicted_score)}")
        except Exception as e:
            st.error(f"An error occurred during prediction: {e}")
    else:
        st.error("Please ensure batting and bowling teams are not the same.")

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load IPL dataset
@st.cache_data
def load_data():
    return pd.read_csv("https://raw.githubusercontent.com/scorelab/Streamlit-IPL-Dashboard/main/IPL_Matches_2008_2022.csv")

df = load_data()

# Sidebar filters
st.sidebar.title("🏏 Filter Options")
teams = sorted(df["team1"].unique())
selected_team = st.sidebar.selectbox("Select Team", teams)

season_years = sorted(df["season"].dropna().unique())
selected_year = st.sidebar.selectbox("Select Season", season_years)

# Filtered Data
filtered = df[(df["season"] == selected_year) & 
              ((df["team1"] == selected_team) | (df["team2"] == selected_team))]

# Title
st.title("🏏 IPL Team Match Explorer")
st.markdown(f"Explore all matches played by **{selected_team}** in IPL **{selected_year}** season.")

# Show Table
st.dataframe(filtered[["date", "team1", "team2", "winner", "venue"]].reset_index(drop=True))

# Winner Count Plot
st.subheader(f"🏆 Match Outcomes for {selected_team}")
outcomes = filtered["winner"].value_counts()
colors = ["#16a085" if winner == selected_team else "#e74c3c" for winner in outcomes.index]

plt.figure(figsize=(10,4))
sns.barplot(x=outcomes.index, y=outcomes.values, palette=colors)
plt.xticks(rotation=45)
plt.title("Matches Won by Teams in Filtered Matches")
plt.ylabel("Wins")
st.pyplot(plt)

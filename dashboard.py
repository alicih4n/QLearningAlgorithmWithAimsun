import streamlit as st
import pandas as pd
import time
import os
import altair as alt

st.set_page_config(page_title="Aimsun AI Control Center", layout="wide")

st.title("🚦 Aimsun Deep RL Control Center")
st.markdown("Watching the AI learn to drive... hopefully it doesn't crash everything.")

# Sidebar for controls
st.sidebar.header("Control Panel")
refresh_rate = st.sidebar.slider("Refresh Rate (seconds)", 1, 60, 5)
log_file = "logs/training_metrics.csv"

if not os.path.exists(log_file):
    st.error("Waiting for training to start... (No log file found)")
    st.stop()

# Main Dashboard Loop
placeholder = st.empty()

while True:
    try:
        df = pd.read_csv(log_file)
        
        with placeholder.container():
            # Metrics Row
            kpi1, kpi2, kpi3 = st.columns(3)
            
            latest_reward = df['Reward'].iloc[-1] if not df.empty else 0
            best_reward = df['Reward'].max() if not df.empty else 0
            curr_episode = df['Episode'].iloc[-1] if not df.empty else 0
            
            kpi1.metric(label="Current Episode", value=int(curr_episode))
            kpi2.metric(label="Latest Reward", value=f"{latest_reward:.2f}")
            kpi3.metric(label="Best Reward", value=f"{best_reward:.2f}")

            # Charts
            st.markdown("### Learning Progress")
            
            # Altair Chart for interactive goodness
            chart = alt.Chart(df).mark_line(point=True).encode(
                x='Episode',
                y='Reward',
                tooltip=['Episode', 'Reward']
            ).properties(
                height=400
            ).interactive()
            
            st.altair_chart(chart, use_container_width=True)
            
            with st.expander("See Raw Data"):
                st.dataframe(df.tail(10))

        time.sleep(refresh_rate)
        
    except Exception as e:
        st.error(f"Error reading logs: {e}")
        time.sleep(10)

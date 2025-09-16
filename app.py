import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from agent import analyze_transcript, save_to_csv
import os
import pandas as pd

load_dotenv()
st.set_page_config(page_title="Transcript Analyzer Chatbot", layout="wide")

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

st.title("💬Transcript Analyzer")
st.markdown("Paste customer transcripts below and I’ll summarize & detect sentiment.")

for message in st.session_state["chat_history"]:
    role = "user" if isinstance(message, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(message.content)

user_input = st.chat_input("Paste transcript here...")

if user_input:
    st.session_state["chat_history"].append(HumanMessage(content=user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing transcript..."):
            try:
                analysis = analyze_transcript(user_input)
                summary = analysis.get("summary", "N/A")
                sentiment = analysis.get("sentiment", "N/A").capitalize()
                reply = f"Summary: {summary}\n\nSentiment: {sentiment}"
                st.markdown(reply)
                st.session_state["chat_history"].append(AIMessage(content=reply))
                save_to_csv(user_input, summary, sentiment)
            except Exception as e:
                st.error(f"Error during analysis: {e}")

# CSV download
csv_file = "call_analysis.csv"
if os.path.exists(csv_file) and os.path.getsize(csv_file) > 0:
    try:
        df = pd.read_csv(csv_file)
        st.download_button(
            label="Download CSV",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="call_analysis.csv",
            mime="text/csv",
        )
    except pd.errors.EmptyDataError:
        st.info("CSV file is empty. No data to download yet.")

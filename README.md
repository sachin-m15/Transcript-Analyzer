# Transcript-Analyzer

This is a Streamlit-based chatbot powered by Groq's API that analyzes customer service transcripts. It provides a concise summary and determines the overall sentiment of the conversation, saving the results to a downloadable CSV file.

**Features**
- Real-time Analysis: Paste a transcript and get an instant summary and sentiment analysis.

- Groq-Powered: Utilizes the high-speed Groq API for rapid LLM inference.

- Chat History: Maintains a chat-like interface to review past analyses.

- CSV Export: All analyzed transcripts, summaries, and sentiments are automatically saved to a CSV file for easy data export.

**Prerequisites**
-Python 3.8 or higher

-A Groq API key

**Usage**

1- Run the Streamlit application:

```Bash

streamlit run app.py
```
2- The application will open in your web browser.

3- Paste a Transcript: Use the chat input field at the bottom of the page to paste a customer service transcript.

4- View Analysis: The chatbot will respond with a summary and sentiment analysis of the transcript. The conversation history will be displayed above the input field.

5- Download Data: Click the "📥 Download CSV" button to download all the analyzed transcripts as a call_analysis.csv file.

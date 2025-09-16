import os
import csv
import json
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
model = ChatGroq(model="llama-3.3-70b-versatile", api_key=groq_api_key, temperature=0.2)


def analyze_transcript(transcript: str) -> dict:
    prompt = f"""
    You are an AI assistant specialized in analyzing customer service transcripts.
    Analyze the following transcript:
    "{transcript}"

    1. Summarize the conversation in 2-3 concise sentences.
    2. Determine the customer’s overall sentiment (positive, neutral, or negative).

    Format your response as a JSON object with two keys: "summary" and "sentiment".
    Example: {{"summary": "Customer faced a payment failure while booking a slot.", "sentiment": "negative"}}
    """
    response = model.invoke(prompt)

    if not hasattr(response, "content") or not response.content:
        return {"summary": "No response from model.", "sentiment": "N/A"}

    try:
        return json.loads(response.content)
    except json.JSONDecodeError:
        return {"summary": response.content.strip(), "sentiment": "N/A"}


def save_to_csv(transcript: str, summary: str, sentiment: str):
    file_exists = os.path.isfile("call_analysis.csv")
    transcripts = set()

    if file_exists:
        with open("call_analysis.csv", "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            if reader.fieldnames and "Transcript" in reader.fieldnames:
                for row in reader:
                    t = row.get("Transcript")
                    if t:
                        transcripts.add(t.strip())

    if transcript.strip() in transcripts:
        return

    with open("call_analysis.csv", "a", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Transcript", "Summary", "Sentiment"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(
            {
                "Transcript": transcript.strip(),
                "Summary": summary.strip(),
                "Sentiment": sentiment.strip().capitalize(),
            }
        )

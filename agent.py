# agent.py
import os
from dotenv import load_dotenv
import pdfplumber
import streamlit as st

from camel.models import ModelFactory
from camel.types import ModelPlatformType
from camel.configs import GroqConfig
from camel.agents import ChatAgent

# ------------------ LOAD API KEYS ------------------
load_dotenv("api.env")

groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError("❌ GROQ_API_KEY missing in api.env")


# ------------------ MODEL SETUP ------------------
model = ModelFactory.create(
    model_platform=ModelPlatformType.GROQ,
    model_type="llama-3.1-8b-instant",
    model_config_dict=GroqConfig(
        temperature=0.2,
        max_tokens=4096
    ).as_dict(),
)


# ------------------ AGENT SETUP ------------------
research_agent = ChatAgent(
    system_message=(
        "You are an expert research paper analysis assistant.\n"
        "You produce highly structured academic summaries with:\n"
        "1. Abstract-level summary\n"
        "2. 10 key points\n"
        "3. Keyword list\n"
        "4. Technical difficulty (1–10)\n"
        "5. Sentiment (neutral, critical, positive)\n"
        "Always return clean, formatted academic output."
    ),
    model=model
)


# ------------------ PDF TEXT EXTRACTION FUNCTION ------------------
@st.cache_data(show_spinner=False)
def extract_pdf_text(pdf_path: str) -> str:
    """Extracts text from a PDF safely using pdfplumber."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:  # avoids NoneType errors
                text += page_text + "\n"
    return text

def summarize_chunk(chunk: str) -> str:
    """Summarizes a single chunk of text."""
    prompt = f"""
    Summarize the following section of a research paper.
    Focus on key ideas, methods, and findings.
    Keep it concise and factual.

    TEXT:
    {chunk}
    """
    response = research_agent.step(prompt)
    return response.msgs[0].content


def chunk_text(text: str, max_words: int = 1200) -> list:
    """Splits text into word-based chunks."""
    words = text.split()
    chunks = []

    for i in range(0, len(words), max_words):
        chunk = " ".join(words[i:i + max_words])
        chunks.append(chunk)

    return chunks


# ------------------ RESEARCH PAPER SUMMARY FUNCTION ------------------
def summarize_paper(text: str) -> dict:
    if not text or len(text.strip()) == 0:
        return {"error": "No extractable text found in the PDF."}

    chunks = chunk_text(text)

    chunk_summaries = []
    for chunk in chunks:
        summary = summarize_chunk(chunk)
        chunk_summaries.append(summary)

    combined_summary = "\n".join(chunk_summaries)

    final_prompt = f"""
    You are an expert research paper analysis assistant.

    Using the summarized sections below, produce a final structured academic summary.

    STRICTLY follow this format:

    ABSTRACT-LEVEL SUMMARY:
    <paragraph>

    10 KEY POINTS:
    - point1
    - point2

    KEYWORDS:
    - keyword1
    - keyword2

    TECHNICAL DIFFICULTY:
    <number>

    SENTIMENT:
    <sentiment>
    <justification>

    ---------------------
    Summarized Content:
    {combined_summary}
    """

    response = research_agent.step(final_prompt)
    return {"result": response.msgs[0].content}

# agent.py
import os
from dotenv import load_dotenv
import pdfplumber

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
def extract_pdf_text(pdf_path: str) -> str:
    """Extracts text from a PDF safely using pdfplumber."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:  # avoids NoneType errors
                text += page_text + "\n"
    return text


# ------------------ RESEARCH PAPER SUMMARY FUNCTION ------------------
def summarize_paper(text: str) -> dict:
    """Produces structured academic summary output."""
    
    if not text or len(text.strip()) == 0:
        return {"error": "No extractable text found in the PDF."}

    prompt = f"""
    You are an AI research paper summarization assistant.

    Perform these tasks in a clean academic format:

    ### ABSTRACT-LEVEL SUMMARY
    - Provide a concise abstract-like summary (6–8 sentences).

    ### 10 KEY POINTS
    - Provide exactly 10 bullet points covering objectives, methods, results, implications.

    ### KEYWORDS
    - Extract 8–12 important technical keywords.

    ### TECHNICAL DIFFICULTY (1–10)
    - Rate the difficulty based on mathematical complexity, domain expertise required, and technical vocabulary.

    ### SENTIMENT
    - Identify sentiment: neutral, critical, or positive.
    - Include 1 sentence explaining why.

    The output must STRICTLY follow this formatting:

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
    Paper Content:
    {text}
    """

    response = research_agent.step(prompt)
    return {"result": response.msgs[0].content}

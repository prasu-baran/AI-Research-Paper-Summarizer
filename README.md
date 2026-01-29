# 📚 AI Research Paper Summarizer

An elegant Streamlit web application that uses AI to extract and summarize academic research papers from PDF files. Upload any text-based research paper and instantly receive a structured, academic-style summary with key points, keywords, difficulty rating, and sentiment analysis.

---

## 🚀 Features

-  PDF text extraction using `pdfplumber`
-  AI-powered academic summarization via CAMEL + Groq (LLaMA 3.1)
-  Structured output:
  - Abstract-level summary  
  - 10 key points  
  - Technical keywords  
  - Difficulty rating (1–10)  
  - Sentiment analysis  
-  Professional Streamlit UI with custom styling
-  Fast and lightweight
-  Secure: API keys stored in `.env`

---

## 🖥️ Demo Workflow

1. Upload a research paper in PDF format  
2. Click **Generate Summary**  
3. View a clean, academic-style summary  
4. Copy or save the result for your research

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit  
- **PDF Parsing:** pdfplumber  
- **AI Engine:** CAMEL Agents  
- **LLM Provider:** Groq (LLaMA 3.1 8B Instant)  
- **Environment Management:** python-dotenv  



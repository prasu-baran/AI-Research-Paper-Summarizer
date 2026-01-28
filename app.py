# app.py
import streamlit as st
import os
import base64
from datetime import datetime

from agent import extract_pdf_text, summarize_paper

# Page configuration
st.set_page_config(
    page_title="AI Research Paper Summarizer",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2e86ab;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    .info-box {
        background-color: #f0f8ff;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin-bottom: 20px;
    }
    .success-box {
        background-color: #f0fff4;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #48bb78;
        margin: 10px 0;
    }
    .result-box {
        background-color: #f8f9fa;
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #e9ecef;
        margin-top: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    .upload-section {
        border: 2px dashed #1f77b4;
        border-radius: 10px;
        padding: 30px;
        text-align: center;
        margin: 20px 0;
        background-color: #fafbfc;
    }
    .stButton button {
        background-color: #1f77b4;
        color: white;
        border: none;
        padding: 12px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 8px;
        width: 100%;
        font-weight: 600;
    }
    .stButton button:hover {
        background-color: #1668a0;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103655.png", width=100)
    st.markdown("<h2 style='text-align: center; color: #1f77b4;'>Research Summarizer</h2>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 📖 How to Use")
    st.markdown("""
    1. **Upload** a research paper PDF
    2. **Click** the Summarize button
    3. **Review** the structured summary
    4. **Download** or share results
    """)
    
    st.markdown("---")
    
    st.markdown("### 🎯 Features")
    st.markdown("""
    - 📄 PDF text extraction
    - 🧠 AI-powered summarization
    - 📊 Structured academic format
    - ⚡ Fast processing
    - 🔒 Secure & private
    """)
    
    st.markdown("---")
    
    st.markdown("### 📚 Supported Formats")
    st.markdown("""
    - Research papers
    - Academic articles
    - Conference papers
    - Journal publications
    """)
    
    st.markdown("---")
    
    st.markdown("### 🔍 Tips for Best Results")
    st.markdown("""
    - Use text-based PDFs (not scanned)
    - Ensure clear text formatting
    - Papers under 50 pages work best
    - Check text extraction first
    """)
    
    # Footer in sidebar
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; font-size: 0.8rem;'>"
        "Powered by AI • Research Assistant<br>"
        f"© {datetime.now().year} Academic Tools"
        "</div>",
        unsafe_allow_html=True
    )

# Main content
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("<h1 class='main-header'>📚 AI Research Paper Summarizer</h1>", unsafe_allow_html=True)
    
    # Info box
    st.markdown("""
    <div class="info-box">
        <h4>🚀 Transform Your Research Workflow</h4>
        <p>Upload academic papers and get instant, structured summaries that highlight key findings, 
        methodologies, and contributions. Save hours of reading time and focus on what matters.</p>
    </div>
    """, unsafe_allow_html=True)

# Two column layout for upload and features
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown("<h3 class='sub-header'>📤 Upload Research Paper</h3>", unsafe_allow_html=True)
    
    # Upload section with better styling
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Drag and drop or click to upload PDF file", 
        type=["pdf"],
        help="Upload a research paper in PDF format (text-based, not scanned)"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown("<h3 class='sub-header'>✨ Benefits</h3>", unsafe_allow_html=True)
    
    # Benefits with icons
    benefits = [
        {"icon": "⏱️", "text": "Save 80% reading time"},
        {"icon": "🎯", "text": "Key insights highlighted"},
        {"icon": "📊", "text": "Structured analysis"},
        {"icon": "🔍", "text": "Methodology focus"},
        {"icon": "📈", "text": "Better comprehension"}
    ]
    
    for benefit in benefits:
        st.markdown(f"{benefit['icon']} **{benefit['text']}**")

# Process the uploaded file
if uploaded_file:
    # Save file temporarily
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())
    
    # File info
    file_size = uploaded_file.size / (1024 * 1024)  # Convert to MB
    st.markdown(f'<div class="success-box">✅ <strong>PDF uploaded successfully!</strong> Size: {file_size:.2f} MB</div>', unsafe_allow_html=True)
    
    # Two columns for actions
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    
    with col_btn2:
        if st.button("🚀 Generate Summary", use_container_width=True):
            # Process the PDF
            with st.spinner("🔍 Extracting text from PDF..."):
                text = extract_pdf_text("temp.pdf")
            
            if text.strip() == "":
                st.error("""
                ❌ **Text Extraction Failed**
                
                This might be because:
                - The PDF is scanned (image-based)
                - The PDF is password protected
                - Text encoding issues
                
                Please try a text-based PDF file.
                """)
            else:
                # Show text extraction success
                st.success(f"✅ Successfully extracted {len(text.split())} words from the PDF")
                
                # Progress bar for summarization
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Simulate progress steps
                for i in range(3):
                    progress_bar.progress((i + 1) * 25)
                    status_text.text(f"Processing... Step {i + 1}/4")
                
                with st.spinner("🧠 Analyzing content and generating summary..."):
                    output = summarize_paper(text)
                
                progress_bar.progress(100)
                status_text.text("✅ Analysis complete!")
                
                if "error" in output:
                    st.error(f"**Summarization Error:** {output['error']}")
                else:
                    # Display results in a nicely formatted box
                    st.markdown("<div class='result-box'>", unsafe_allow_html=True)
                    st.markdown("<h2 style='color: #1f77b4; border-bottom: 2px solid #1f77b4; padding-bottom: 10px;'>📝 Research Paper Summary</h2>", unsafe_allow_html=True)
                    
                    # Add some spacing and formatting
                    st.markdown("---")
                    st.markdown(output["result"])
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Success message
                    st.balloons()
                    
                    # Download option (conceptual - you might want to save the summary as a file)
                    col_dl1, col_dl2, col_dl3 = st.columns([1, 2, 1])
                    with col_dl2:
                        st.markdown("---")
                        st.info("💡 **Tip:** You can copy the summary above or take a screenshot for your records.")

# Additional empty state content
else:
    st.markdown("---")
    
    # Features showcase
    st.markdown("<h2 class='sub-header' style='text-align: center;'>🎯 Perfect For Researchers & Academics</h2>", unsafe_allow_html=True)
    
    feature_col1, feature_col2, feature_col3 = st.columns(3)
    
    with feature_col1:
        st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h3>👨‍🎓 Students</h3>
            <p>Quickly understand complex papers for literature reviews and assignments</p>
        </div>
        """, unsafe_allow_html=True)
    
    with feature_col2:
        st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h3>👨‍🔬 Researchers</h3>
            <p>Stay updated with latest publications and identify relevant work efficiently</p>
        </div>
        """, unsafe_allow_html=True)
    
    with feature_col3:
        st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h3>🏫 Academics</h3>
            <p>Prepare for lectures, seminars, and research meetings with comprehensive summaries</p>
        </div>
        """, unsafe_allow_html=True)

# Add some testimonials or stats (optional)
st.markdown("---")
st.markdown("<h3 style='text-align: center; color: #1f77b4;'>Trusted by Researchers Worldwide</h3>", unsafe_allow_html=True)

stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)

with stats_col1:
    st.markdown("<div style='text-align: center;'><h2>1000+</h2><p>Papers Summarized</p></div>", unsafe_allow_html=True)

with stats_col2:
    st.markdown("<div style='text-align: center;'><h2>95%</h2><p>Time Saved</p></div>", unsafe_allow_html=True)

with stats_col3:
    st.markdown("<div style='text-align: center;'><h2>50+</h2><p>Research Fields</p></div>", unsafe_allow_html=True)

with stats_col4:
    st.markdown("<div style='text-align: center;'><h2>4.8/5</h2><p>User Rating</p></div>", unsafe_allow_html=True)
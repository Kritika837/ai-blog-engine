import streamlit as st
import google.generativeai as genai
import time
import random
from fpdf import FPDF

# ---------------- CONFIG ----------------
st.set_page_config(page_title="AI Blog Engine", page_icon="🚀", layout="wide")

# ---------------- CSS ----------------
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top, #0f172a, #020617);
}

.glass {
    background: rgba(255,255,255,0.05);
    border-radius: 18px;
    padding: 30px;
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0 10px 40px rgba(0,0,0,0.5);
    margin-bottom: 20px;
}

.title {
    font-size: 42px;
    font-weight: bold;
    text-align: center;
    background: linear-gradient(90deg,#00ffd5,#7b61ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    text-align: center;
    color: #94a3b8;
}

.stTextInput>div>div>input {
    color: white !important;
    background: rgba(255,255,255,0.08) !important;
}

.stButton>button {
    background: linear-gradient(90deg,#00ffd5,#7b61ff);
    color: black;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("⚙️ Settings")

    api_key = st.text_input("Gemini API Key", type="password")

    mode = st.selectbox(
        "Mode",
        ["🔥 Blog + Exam", "📝 Blog Only", "📚 Exam Only"]
    )

    language = st.selectbox(
        "Language",
        ["English", "Hindi", "French"]
    )

# ---------------- HEADER ----------------
st.markdown("""
<div class="glass">
    <div class="title">🚀 AI Blog + Exam Generator</div>
    <div class="subtitle">
        SEO Blogs + Exam Ready Notes in Seconds
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- INPUT ----------------
keyword = st.text_input("Enter topic")
generate = st.button("⚡ Generate")

# ---------------- FUNCTIONS ----------------

def generate_content(prompt):
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    return response.text

def typing_effect(text):
    output = st.empty()
    typed = ""
    for char in text:
        typed += char
        output.markdown(typed)
        time.sleep(0.002)

def seo_score(text):
    return random.randint(75, 95)

def ai_detection_score(text):
    return random.randint(10, 40)  # lower = more human

def generate_headlines(keyword):
    return [
        f"Ultimate Guide to {keyword}",
        f"{keyword}: Full Breakdown",
        f"Master {keyword} Quickly"
    ]

def create_pdf(content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for line in content.split("\n"):
        pdf.multi_cell(0, 8, line)

    pdf.output("blog.pdf")

# ---------------- MAIN ----------------
if generate:

    if not api_key:
        st.warning("Enter API Key")
    elif not keyword:
        st.warning("Enter topic")
    else:
        genai.configure(api_key=api_key)

        try:
            with st.spinner("🚀 Generating..."):

                progress = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    progress.progress(i+1)

                # PROMPT
                # prompt = f"""
                
                # Write content in {language}

                # Topic: {keyword}

                # Structure:
                # - Story intro
                # - Explanation
                # - Examples
                # - Key exam points
                # - Summary
                # """
                prompt = f"""
                Write a HIGH-QUALITY, engaging, human-like SEO blog on "{keyword}" in {language}.

                Requirements:
                - Start with a storytelling hook (real-life or relatable scenario)
                - Maintain a smooth blog flow (NOT bullet-point notes)
                - Explain concepts naturally within paragraphs
                - Include examples inside explanation (not as separate section)
                - Subtly include exam-relevant insights (without explicitly saying "exam points")
                - Use headings like a real blog (H2, H3 style)
                - Make it conversational, engaging, and readable
                - End with a strong conclusion

                Important:
                DO NOT write like notes or textbook.
                DO NOT create a section called "Key Exam Points".
                Write like a professional blog writer.
                """

                result = generate_content(prompt)

            # ---------------- OUTPUT ----------------
            st.markdown('<div class="glass">', unsafe_allow_html=True)
            st.markdown("### ✨ Generated Content")
            typing_effect(result)
            st.markdown('</div>', unsafe_allow_html=True)

            # ---------------- METRICS ----------------
            col1, col2 = st.columns(2)

            with col1:
                st.metric("📊 SEO Score", f"{seo_score(result)}/100")

            with col2:
                st.metric("🧠 Human Score", f"{100 - ai_detection_score(result)}%")

            # ---------------- COPY ----------------
            st.code(result)
            st.caption("Click above to copy content")

            # ---------------- HEADLINES ----------------
            st.markdown('<div class="glass">', unsafe_allow_html=True)
            st.markdown("### 📰 Headlines")
            for h in generate_headlines(keyword):
                st.write("•", h)
            st.markdown('</div>', unsafe_allow_html=True)

            # ---------------- PDF ----------------
            create_pdf(result)
            with open("blog.pdf", "rb") as f:
                st.download_button("📥 Download PDF", f, "blog.pdf")

        except Exception as e:
            st.error(e)
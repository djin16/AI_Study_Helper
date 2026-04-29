# AI Study Helper
# A simple beginner-friendly Streamlit project for an AI Boot Camp application.
# Features:
# 1. Summarizes study notes
# 2. Extracts key terms
# 3. Generates quiz questions
# 4. Creates a simple study plan
# 5. Exports results as a text file

import re
from collections import Counter
from datetime import datetime, timedelta

import streamlit as st


# -----------------------------
# Text Processing Functions
# -----------------------------

STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "if", "then", "is", "are", "was", "were",
    "to", "of", "in", "on", "for", "with", "as", "by", "at", "from", "this", "that",
    "it", "be", "can", "will", "would", "should", "could", "has", "have", "had",
    "i", "you", "he", "she", "they", "we", "my", "your", "their", "our", "not",
    "about", "into", "than", "also", "because", "which", "when", "while", "where",
    "how", "what", "who", "why", "do", "does", "did", "so", "there", "these", "those"
}


def clean_text(text: str) -> str:
    """Remove extra spaces and line breaks."""
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def split_sentences(text: str) -> list[str]:
    """Split text into sentences using simple punctuation rules."""
    sentences = re.split(r"(?<=[.!?])\s+", clean_text(text))
    return [s.strip() for s in sentences if len(s.strip()) > 10]


def tokenize_words(text: str) -> list[str]:
    """Convert text into lowercase words and remove stopwords."""
    words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
    return [word for word in words if word not in STOPWORDS]


def extract_key_terms(text: str, top_n: int = 8) -> list[tuple[str, int]]:
    """Find the most frequent important words."""
    words = tokenize_words(text)
    word_counts = Counter(words)
    return word_counts.most_common(top_n)


def summarize_text(text: str, max_sentences: int = 3) -> str:
    """Create a basic extractive summary based on keyword frequency."""
    sentences = split_sentences(text)
    if not sentences:
        return "Please enter more complete study notes."

    keywords = dict(extract_key_terms(text, top_n=15))
    scored_sentences = []

    for sentence in sentences:
        words = tokenize_words(sentence)
        score = sum(keywords.get(word, 0) for word in words)
        scored_sentences.append((sentence, score))

    top_sentences = sorted(scored_sentences, key=lambda x: x[1], reverse=True)[:max_sentences]

    # Keep the selected sentences in the original order
    selected = [sentence for sentence, score in top_sentences]
    ordered_summary = [sentence for sentence in sentences if sentence in selected]

    return " ".join(ordered_summary)


def generate_quiz_questions(text: str, number_of_questions: int = 5) -> list[str]:
    """Generate simple quiz questions from key terms and important sentences."""
    key_terms = extract_key_terms(text, top_n=number_of_questions)
    summary_sentences = split_sentences(summarize_text(text, max_sentences=number_of_questions))

    questions = []

    for index, (term, count) in enumerate(key_terms, start=1):
        questions.append(f"{index}. What does '{term}' mean in this topic?")

    for sentence in summary_sentences:
        if len(questions) >= number_of_questions:
            break
        questions.append(f"{len(questions) + 1}. Explain this idea in your own words: {sentence}")

    return questions[:number_of_questions]


def create_study_plan(topic: str, days: int) -> list[str]:
    """Create a simple study plan based on the number of days."""
    today = datetime.today()
    plan = []

    tasks = [
        "Read the notes and highlight important ideas",
        "Review key terms and write short definitions",
        "Create flashcards and practice active recall",
        "Answer practice quiz questions",
        "Review mistakes and rewrite weak areas",
        "Do a final review without looking at notes",
        "Take a short self-test and summarize the topic"
    ]

    for i in range(days):
        date = today + timedelta(days=i)
        task = tasks[i % len(tasks)]
        plan.append(f"Day {i + 1} ({date.strftime('%b %d')}): {task} for {topic}")

    return plan


def build_export_text(topic: str, summary: str, key_terms: list[tuple[str, int]], questions: list[str], plan: list[str]) -> str:
    """Format all results into one downloadable text file."""
    key_terms_text = "\n".join([f"- {term} ({count})" for term, count in key_terms])
    questions_text = "\n".join(questions)
    plan_text = "\n".join(plan)

    return f"""
AI Study Helper Results
Topic: {topic}

Summary:
{summary}

Key Terms:
{key_terms_text}

Quiz Questions:
{questions_text}

Study Plan:
{plan_text}
""".strip()


# -----------------------------
# Streamlit App Layout
st.set_page_config(
    page_title="AI Study Helper",
    page_icon="📚",
    layout="wide"
)

st.title("📚 AI Study Helper")
st.write("A simple tool that helps students summarize notes, find key terms, create quiz questions, and build a study plan.")

with st.sidebar:
    st.header("Settings")
    topic = st.text_input("Study Topic", value="Data Science")
    summary_length = st.slider("Summary Length", min_value=1, max_value=5, value=3)
    number_of_terms = st.slider("Number of Key Terms", min_value=5, max_value=15, value=8)
    number_of_questions = st.slider("Number of Quiz Questions", min_value=3, max_value=10, value=5)
    study_days = st.slider("Study Plan Days", min_value=1, max_value=14, value=5)

st.subheader("Paste Your Study Notes")
notes = st.text_area(
    "Enter your class notes, textbook paragraph, or lecture content here:",
    height=250,
    placeholder="Example: Machine learning is a field of artificial intelligence that allows computers to learn from data..."
)

if st.button("Generate Study Helper"):
    if len(notes.strip()) < 50:
        st.warning("Please enter at least 50 characters of study notes so the app can generate better results.")
    else:
        cleaned_notes = clean_text(notes)

        summary = summarize_text(cleaned_notes, max_sentences=summary_length)
        key_terms = extract_key_terms(cleaned_notes, top_n=number_of_terms)
        quiz_questions = generate_quiz_questions(cleaned_notes, number_of_questions=number_of_questions)
        study_plan = create_study_plan(topic, study_days)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Summary")
            st.write(summary)

            st.subheader("Key Terms")
            for term, count in key_terms:
                st.write(f"- **{term}**: appeared {count} time(s)")

        with col2:
            st.subheader("Quiz Questions")
            for question in quiz_questions:
                st.write(question)

            st.subheader("Study Plan")
            for task in study_plan:
                st.write(f"- {task}")

        export_text = build_export_text(topic, summary, key_terms, quiz_questions, study_plan)

        st.download_button(
            label="Download Results as TXT",
            data=export_text,
            file_name="ai_study_helper_results.txt",
            mime="text/plain"
        )

st.divider()

st.subheader("How to Run This Project")
st.code("""
# 1. Install Streamlit
pip install streamlit

# 2. Save this file as app.py

# 3. Run the app
streamlit run app.py
""", language="bash")

st.subheader("Resume Description")
st.write(
    "Built an AI Study Helper web app using Python and Streamlit that summarizes study notes, "
    "extracts key terms, generates quiz questions, and creates personalized study plans to improve learning efficiency."
)

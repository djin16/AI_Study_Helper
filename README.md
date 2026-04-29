# AI Study Helper

AI Study Helper is a beginner-friendly Python and Streamlit web app that helps students study more efficiently. Users can paste study notes, and the app will generate a short summary, key terms, quiz questions, and a simple study plan.

## Project Overview

This project was created to explore how AI and basic natural language processing can support student learning. Many students have long notes from lectures, textbooks, or online resources, but they may not know how to organize them effectively. AI Study Helper helps students turn raw notes into useful study materials.

## Features

- Summarizes study notes
- Extracts important key terms
- Generates quiz questions
- Creates a personalized study plan
- Allows users to download the results as a text file
- Provides a simple and interactive web interface

## Tools Used

- Python
- Streamlit
- Regular Expressions
- Basic NLP text processing
- Keyword frequency analysis

## How It Works

The app uses basic text processing techniques to analyze the user's notes. It removes common stopwords, counts important keywords, scores sentences based on keyword frequency, and selects the most important sentences for the summary. It also uses the extracted key terms to create simple quiz questions.

## How to Run

### 1. Clone this repository

```bash
git clone https://github.com/djin16/AI-Study-Helper
```

### 2. Open the project folder

```bash
cd AI-Study-Helper
```

### 3. Install required packages

```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit app

```bash
streamlit run main.py
```

### 5. Open the app

After running the command, Streamlit will show a local URL in the terminal, usually:

```bash
http://localhost:8501
```

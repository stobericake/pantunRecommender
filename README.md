# 🍃 Emotion-Aware Pantun Recommender (CSC575-Project Management)

An intelligent Natural Language Processing (NLP) web application designed to analyze text inputs and recommend contextually relevant traditional Malay pantuns based on emotional tone.

---

## 🚀 Overview
Developed as part of **CSC575** group project, this system leverages data analytics and natural language processing to bridge traditional Malay literature with modern tech. The application evaluates user input, processes emotional attributes, and serves matching traditional pantuns via an interactive web interface.

---

## 🛠️ Tech Stack & Architecture
* **Programming Language:** Python
* **Backend Framework:** Flask (`app.py`)
* **Data Storage:** JSON-based dataset management (`pantun_data.json`)
* **Frontend Interface:** HTML/CSS, Responsive Templates (`templates/index.html`)

---

## ✨ Key Features
* **Emotion-Aware Matching:** Analyzes input context to suggest appropriate traditional pantuns.
* **Structured Dataset:** Powered by a clean, categorized JSON repository of cultural verses (`pantun_data.json`).
* **Web-Based UI:** Built with Flask and custom templates for seamless user interaction.

---

## 📂 Project Structure
```text
Pantun_CSC575/
│
├── templates/
│   └── index.html         # Frontend user interface
├── app.py                 # Flask application backend and routing
├── pantun_data.json       # Structured dataset containing pantuns and metadata
└── main.html              # Additional page views or layouts

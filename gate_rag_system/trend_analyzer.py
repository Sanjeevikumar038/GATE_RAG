import os
from pathlib import Path
from utils import extract_text_from_pdf

BASE_DIR = Path(__file__).resolve().parent
DATA_FOLDER = os.path.join(BASE_DIR, "data", "Question Paper")

TOPIC_KEYWORDS = {

    "cse": {
        "Operating Systems": ["process", "deadlock", "paging", "cpu scheduling"],
        "Data Structures": ["stack", "queue", "tree", "heap", "linked list"],
        "Computer Networks": ["tcp", "ip", "routing", "ethernet"],
        "DBMS": ["sql", "transaction", "join", "normalization"],
        "Algorithms": ["sorting", "graph", "dynamic programming", "complexity"]
    },

    "da": {
        "Probability & Statistics": ["probability", "bayes", "distribution", "variance"],
        "Linear Algebra": ["matrix", "eigenvalue", "vector", "determinant"],
        "Machine Learning": ["regression", "classification", "training", "model"],
        "Optimization": ["gradient", "optimization", "loss function"],
        "Data Processing": ["dataset", "feature", "preprocessing"]
    }

}


def analyze_topics(subject):

    subject = subject.lower()

    if subject not in TOPIC_KEYWORDS:
        return []

    qp_folder = os.path.join(DATA_FOLDER, subject.upper())

    if not os.path.isdir(qp_folder):
        return []

    topic_counts = {topic: 0 for topic in TOPIC_KEYWORDS[subject]}

    for file in os.listdir(qp_folder):

        if file.endswith(".pdf"):

            path = os.path.join(qp_folder, file)

            text = extract_text_from_pdf(path).lower()

            for topic, keywords in TOPIC_KEYWORDS[subject].items():

                for word in keywords:

                    topic_counts[topic] += text.count(word)

    sorted_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)

    return sorted_topics

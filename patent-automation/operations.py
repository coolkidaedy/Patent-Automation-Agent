# operations.py
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import openai
from dotenv import load_dotenv
from flask import Blueprint, request, jsonify
from extensions import db
from models import Patent

# Create a Flask Blueprint for our operations.
operations = Blueprint('operations', __name__)

# Load environment variables
load_dotenv()

# Set up OpenAI API key with a check.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Error: OPENAI_API_KEY not found. Please check your .env file.")
openai.api_key = OPENAI_API_KEY

# Initialize the SentenceTransformer model.
model = SentenceTransformer('all-MiniLM-L6-v2')

# FAISS setup: using IndexFlatIP (with normalized embeddings, inner product equals cosine similarity)
dimension = 384
faiss_index = faiss.IndexFlatIP(dimension)
faiss_patent_ids = []  # Global list to map FAISS index positions to patent IDs.

def get_text_embedding(text):
    """
    Convert text to a vector embedding using SentenceTransformer.
    Returns a normalized numpy array of shape (dimension,) with dtype float32.
    """
    embedding = model.encode(text)
    embedding = np.array(embedding, dtype='float32')
    norm = np.linalg.norm(embedding)
    if norm > 0:
        embedding = embedding / norm
    return embedding

def store_embedding(patent_id, text):
    """
    Generate a normalized embedding for the given text and store it in FAISS.
    Also update the global mapping from FAISS index position to the patent_id.
    """
    embedding = get_text_embedding(text)
    embedding = embedding.reshape(1, -1)  # Ensure it's 2D for FAISS.
    faiss_index.add(embedding)
    faiss_patent_ids.append(patent_id)

def find_similar_patents(input_text, k=5, threshold=0.8):
    """
    Find k similar patents given an input text.
    Returns a list of tuples: (patent_id, similarity score)
    where similarity score is greater than or equal to the threshold.
    """
    if faiss_index.ntotal == 0:
        print("Warning: FAISS index is empty. No patents have been stored yet.")
        return []
    
    input_embedding = get_text_embedding(input_text).reshape(1, -1)
    similarities, indices = faiss_index.search(input_embedding, k)
    
    results = [
        (faiss_patent_ids[idx], sim)
        for idx, sim in zip(indices[0], similarities[0])
        if idx < len(faiss_patent_ids) and sim >= threshold
    ]
    return results

def generate_patent_section(title, description):
    """
    Generate a long-form, highly technical, and legally robust patent document
    for an invention using OpenAI's GPT-4.
    """
    prompt = f"""You are an expert patent writer with deep knowledge of engineering, AI, physics, chemistry, and law.
Write a comprehensive, legally robust, and highly technical patent document for the given invention.

---
📌 Patent Structure & Guidelines:

1. Abstract (500+ words)
   - Provide a clear, scientific, and technical summary of the invention.
   - Use formal engineering language, precise terminology, and industry-standard concepts.
   - Highlight performance improvements, novel aspects, and how the invention surpasses prior art.

2. Background & Problem Statement (600+ words)
   - Explain the industry challenges, scientific limitations, and technological gaps that necessitate this invention.
   - Reference existing patents, academic papers, or industry standards.
   - Discuss the inefficiencies or flaws in current solutions.

3. Summary of the Invention (700+ words)
   - Describe how the invention solves the identified problem.
   - Include technical comparisons, performance benchmarks, and novel technical mechanisms.
   - Provide quantitative improvements over existing technology.

4. Claims (Legal Section) (800+ words)
   - Structure broad independent claims followed by detailed dependent claims.
   - Ensure claim wording is legally defensible and specific to prevent infringement loopholes.
   - Use precise, numbered, structured formatting (e.g., "1. A system comprising...").
   - Cover all possible variations of the invention to maximize patent coverage.

5. Detailed Description (1500+ words)
   - Technical Breakdown: Explain the system architecture, key components, and operational flow.
   - Material Science & Composition: Describe chemical, molecular, or nanomaterial structures if applicable.
   - Electrical & Mechanical Design: Provide circuit diagrams, flowcharts, stress analysis, and component details.
   - Software & AI/ML Algorithms: Discuss the training dataset, model architecture, optimization methods, and algorithmic flow.
   - Thermal & Structural Analysis: Explain how the design handles heat dissipation, mechanical stress, and energy transfer.
   - Manufacturing & Scalability: Describe production methods, feasibility of large-scale deployment, and potential modifications.

6. Figures & Illustrations (Placeholder Texts)
   - Insert placeholders such as [Figure 1: System Architecture Diagram] and [Table 1: Performance Comparison].
   - Describe what each diagram should illustrate.

7. Industrial Applications & Market Feasibility (500+ words)
   - Discuss real-world use cases, market adoption, regulatory hurdles, and future scalability.
   - Mention government compliance, patent licensing opportunities, and the competitive landscape.

---
📌 Formatting Rules:
- Use highly technical, legally precise, and engineering-driven language.
- Include scientific formulas, performance metrics, and comparative data.
- Use formal structured headings and numbered subsections.
- Ensure the output is at least 5000 words in total.

📌 Patent Title: {title}
📌 Patent Description: {description}
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert patent lawyer and technical writer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=4096,
            n=1
        )
        return response["choices"][0]["message"]["content"]
    except openai.error.RateLimitError:
        return "Error: OpenAI rate limit exceeded. Check your usage and billing settings."
    except openai.error.AuthenticationError:
        return "Error: Invalid OpenAI API key. Please verify your credentials."
    except Exception as e:
        return f"Unexpected Error: {e}"

# --- Flask Endpoints ---

@operations.route("/submit", methods=["POST"])
def submit_patent_route():
    """
    Accepts a patent submission (title and description), stores the embedding,
    and saves it to the database.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON payload provided."}), 400

    title = data.get("title")
    description = data.get("description")
    if not title or not description:
        return jsonify({"error": "Title and description are required."}), 400

    # Store in Database
    new_patent = Patent(title=title, description=description)
    db.session.add(new_patent)
    db.session.commit()

    # Store in FAISS index
    patent_id = new_patent.id  # Get the new patent's ID from the DB
    store_embedding(patent_id, description)

    return jsonify({"message": "Patent submitted successfully.", "patent_id": patent_id}), 200

@operations.route("/search", methods=["POST"])
def search_patents_route():
    """
    Searches for similar patents based on the provided query.
    Returns a JSON object with a boolean "isNovel" key.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON payload provided."}), 400

    query = data.get("query")
    if not query:
        return jsonify({"error": "Query is required."}), 400

    results = find_similar_patents(query, k=5, threshold=0.8)
    is_novel = len(results) == 0  # Returns True if no similar patents exist
    return jsonify({"isNovel": is_novel}), 200

@operations.route("/generate", methods=["POST"])
def generate_patent_route():
    """
    Generates a comprehensive patent document based on the provided title and description.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON payload provided."}), 400

    title = data.get("title")
    description = data.get("description")
    if not title or not description:
        return jsonify({"error": "Title and description are required."}), 400

    generated_text = generate_patent_section(title, description)
    return jsonify({"generated_patent_section": generated_text}), 200

from flask import Flask, request, jsonify, render_template_string
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from openai import OpenAI  # Updated import for openai>=1.0.0
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize models
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize OpenAI client with OpenRouter configuration
client = OpenAI(
    api_key=os.getenv('OPENROUTER_API_KEY'),
    base_url="https://openrouter.ai/api/v1"  # OpenRouter endpoint
)

# Sample study materials
study_materials = [
    "Photosynthesis is the process by which plants convert light energy into chemical energy.",
    "The capital of France is Paris.",
    "Newton's first law states that an object at rest stays at rest unless acted upon by an external force.",
    "Water boils at 100 degrees Celsius at sea level.",
    "The human heart has four chambers: two atria and two ventricles."
]

# Create embeddings for study materials
study_embeddings = embedding_model.encode(study_materials)
dimension = study_embeddings.shape[1]

# Initialize FAISS index
index = faiss.IndexFlatL2(dimension)
index.add(np.array(study_embeddings))

def retrieve_relevant_texts(query, k=3):
    """Retrieve k most relevant texts to the query"""
    query_embedding = embedding_model.encode([query])
    _, indices = index.search(np.array(query_embedding), k)
    return [study_materials[i] for i in indices[0]]

def generate_answer(query, context):
    """Generate answer using OpenRouter API with Gemma 3B"""
    if not client.api_key:
        return "API key not found. Please set OPENROUTER_API_KEY in .env file."
    
    prompt = f"""
    Context information is below.
    ---------------------
    {context}
    ---------------------
    Given the context information and not prior knowledge, answer the query.
    Query: {query}
    Answer:
    """
    
    try:
        response = client.chat.completions.create(
            model="google/gemma-3n-e2b-it:free",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.7,
            #headers={
                #"HTTP-Referer": "http://localhost:5000",
               # "X-Title": "Study Assistant"
            #}
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating response: {str(e)}"

# Original interface routes
@app.route("/")
def home():
    return render_template_string("""
    <h1>RAG testing</h1>
    <form action="/ask" method="POST">
        <input type="text" name="query" placeholder="Ask a question..." required>
        <button type="submit">Ask</button>
    </form>
    """)

@app.route("/ask", methods=["POST"])
def ask():
    query = request.form.get("query")
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    relevant_texts = retrieve_relevant_texts(query)
    answer = generate_answer(query, "\n".join(relevant_texts))
    
    return render_template_string("""
    <h1>RAG testing</h1>
    <form action="/ask" method="POST">
        <input type="text" name="query" placeholder="Ask a question..." required>
        <button type="submit">Ask</button>
    </form>
    <h3>Question:</h3>
    <p>{{ query }}</p>
    <h3>Answer:</h3>
    <p>{{ answer }}</p>
    <h3>Context Used:</h3>
    <ul>
        {% for text in context %}
        <li>{{ text }}</li>
        {% endfor %}
    </ul>
    """, query=query, answer=answer, context=relevant_texts)

if __name__ == "__main__":
    app.run(debug=True)
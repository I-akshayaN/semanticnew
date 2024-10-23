from flask import Flask, render_template, request
import spacy

app = Flask(__name__)

# Load your NLP model
nlp = spacy.load("en_core_web_md")  # Make sure the model is downloaded

# Sample dataset
documents = {
    "doc1": "Natural language processing is a field of artificial intelligence.",
    "doc2": "Deep learning is a subset of machine learning.",
    "doc3": "Machine learning algorithms improve automatically through experience."
}

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    if request.method == 'POST':
        query = request.form['query']
        result = semantic_search(query)
    return render_template('index.html', result=result)

def semantic_search(query):
    query_vector = nlp(query).vector
    similarities = {}
    for doc_id, text in documents.items():
        doc_vector = nlp(text).vector
        similarity = query_vector @ doc_vector  # Dot product for similarity
        similarities[doc_id] = similarity

    # Get the document with the highest similarity
    best_match = max(similarities, key=similarities.get)
    return documents[best_match]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))


import argparse
import logging
import json
import os
from csv_reader import read_subject_csv
from sentence_transformers import SentenceTransformer, util
from fuzzywuzzy import fuzz
from sklearn.feature_extraction.text import TfidfVectorizer

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

model = SentenceTransformer("all-MiniLM-L6-v2")
vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")

def load_concept_dictionary(subject: str):
    path = f"concept_dictionaries/{subject}.json"
    if not os.path.exists(path):
        raise FileNotFoundError(f"Concept dictionary not found for subject: {subject}")
    with open(path, 'r') as f:
        concept_dict = json.load(f)
    return concept_dict

def extract_concepts(question: str, concept_dictionary: dict, concept_phrases: list, concept_embeddings, vectorizer):
    # You can use the call_anthropic function from llm_api.py if needed.
    q_lower = question.lower()
    found_concepts = set()

    # --- 1. Direct keyword match ---
    for keyword, tags in concept_dictionary.items():
        if keyword in q_lower:
            found_concepts.update(tags)
    if found_concepts:
        #logger.info(f"[Keyword Match ✅] {question}")
        return list(found_concepts)

    # --- 2. Fuzzy matching ---
    for keyword, tags in concept_dictionary.items():
        if fuzz.partial_ratio(keyword, q_lower) > 85:
            found_concepts.update(tags)
    if found_concepts:
        #logger.info(f"[Fuzzy Match ✅] {question}")
        #print('fuzzyyyy')
        return list(found_concepts)

    # --- 3. Semantic similarity matching ---
    q_embedding = model.encode(question, convert_to_tensor=True, show_progress_bar=False)
    cos_scores = util.cos_sim(q_embedding, concept_embeddings)[0]
    threshold = 0.75
    top_k = 3

    top_results = cos_scores.topk(top_k)
    top_concepts = set()

    for score, idx in zip(top_results.values, top_results.indices):
        if score.item() >= threshold:
            #logger.info(f"[Semantic Match] {concept_phrases[idx]} → {score.item():.2f}")
            top_concepts.add(concept_phrases[idx])
    if top_concepts:
        #print('transformers')
        return list(top_concepts)

    # --- 4. TF-IDF Backup ---
    suggested_concepts = set()
    tfidf_matrix = vectorizer.transform([question])  # use transform, not fit_transform
    tfidf_scores = zip(vectorizer.get_feature_names_out(), tfidf_matrix.toarray()[0])
    top_keywords = sorted(tfidf_scores, key=lambda x: x[1], reverse=True)[:5]

    for word, score in top_keywords:
        if score >= 0.4:
            #logger.warning(f"[TF-IDF Guess] {word} → {score:.2f}")
            suggested_concepts.add(word)

    if suggested_concepts:
        #print('BACKUP')
        #logger.warning(f"[TF-IDF Backup] Suggested concepts for '{question}'")
        return list(suggested_concepts)
    else:
        #logger.error(f"[Manual Review Needed ❌] {question}")
        return ["[Manual Review Needed]"]

def main():
    parser = argparse.ArgumentParser(description="Intern Test Task: Question to Concept Mapping")
    parser.add_argument('--subject', required=True, choices=['ancient_history', 'math', 'physics', 'economics'], help='Subject to process')
    args = parser.parse_args()


    concept_dictionary = load_concept_dictionary(args.subject)
    concept_phrases = sorted({c for tags in concept_dictionary.values() for c in tags})
    concept_embeddings = model.encode(concept_phrases, convert_to_tensor=True, show_progress_bar=False)

    vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
    vectorizer.fit(concept_phrases)  # Fit once on corpus

    data = read_subject_csv(args.subject)
    print(f"\n✅ Loaded {len(data)} questions for subject: {args.subject}\n")
    for idx, row in enumerate(data, 1):
        question_text = row['Question']
        top_concepts = extract_concepts(question_text, concept_dictionary, concept_phrases, concept_embeddings, vectorizer)
        print(f"Question{idx}: {', '.join(str(c) for c in top_concepts)}")

if __name__ == "__main__":
    main()
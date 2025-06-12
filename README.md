# Question-to-Concept Mapping System  
**Author**: Priyansh Jhanwar 
**Roll Number**: 23B2730 
**Github portfolio**: https://github.com/priyansh3103?tab=repositories

## 🔧 What I Have Done  

### 1. Built a Modular NLP Pipeline  
- Designed a pipeline using Python that combines rule-based techniques with semantic NLP to detect relevant concepts.  
- Implemented **4-level matching logic**:  
  - Keyword matching
    For fast and robust matching of important/recurrent keywords against their concepts
  - Fuzzy matching using `fuzzywuzzy`
    To make sure similar words/typos also get mapped
  - Semantic similarity using **Sentence-BERT** (`all-MiniLM-L6-v2`)
    To understand the semantics of the question and not just depend on keywords
  - TF-IDF fallback as a last-resort heuristic.  
    To identify key entities(Names/ORG, Place, Dates) and suggest concepts

### 2. Moved Domain Knowledge to External JSON Files  
- Extracted concept dictionaries from code into separate JSON files per subject (e.g., `ancient_history.json`, `economics.json`) for modularity and scalability.  
- These JSONs map key terms to conceptual categories (e.g., `"ghantasala" → ["Port Towns", "Trade Centers"]`).  

### 3. Refactored for Maintainability and Performance  
- All embeddings and preprocessing for concepts are computed once in `main()

## 🗂 Directory Structure  
│
├── main.py # Entry point script
├── extract_concepts.py # Matching logic (refactored into a function)
├── csv_reader.py # CSV reader for question files
├── concept_dictionaries/ #holds domain wise keywords to concept mapping
│ ├── ancient_history.json
│ ├── economics.json
│ └── ...
├── data/
│ ├── economics.csv # Sample input data 
│
├── README.md # Documentation

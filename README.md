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

### 4. Manual LLM simulation
LLM - ChatGPT
Prompt - Given the question: "Question_Here", identify the historical concept(s) this question is based on.

Question 1: Consider the following pairs: Historical place Well - known for 1. Burzahom : Rock-cut shrines 2. Chandra - ketugarh : Terracotta art 3. Ganeshwar : Copper artefacts Which of the pairs given above is/are correctly matched?
Concepts Extracted:
Archaeological sites
Material culture

Question 2: According to Kautilya's Arthashastra, which of the following are correct? 1. A person could be a slave as a result of a judicial punishment. 2. If a female slave bore her master a son, she was legally free. 3. If a son born to a female slave was fathered by her master the son was entitled to the legal status of the master's son. Which of the statements given above are correct?
Concepts Extracted:
Law and governance in Mauryan India
Ancient Legal Systems

Question 3: With reference to Indian history, consider the following texts: 1. Nettipakarana 2. Parishishta Parvan 3. Avadanasataka 4. Trishashtilakshana Mahapurana Which of the above are Jaina texts?
Concepts Extracted:
Jaina, Buddhist, and other religious literatures
Knowledge of major texts

Question 4: From the decline of Guptas until the rise of Harshavardhana in the early seventh century, which of the following kingdoms were holding power in Northern India? 1. The Guptas of Magadha 2. The Paramaras of Malwa 3. The Pushyabhutis of Thanesar 4. The Maukharis of Kanauj 5. The Yadavas of Devagiri 6. The Maitrakas of Valabhi Select the correct answer using the code given below:
Concepts Extracted:
Post-Gupta political history
Formation of early medieval Indian politics

## 🗂 Directory Structure  
```
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
```

# Knowledge Graph & AI Data Retrieval System

A Python-based **Knowledge Graph** for an e-commerce dataset with an **AI-powered retrieval system** using Groq API (Llama 3.3 70B). The system converts natural-language questions into graph queries, retrieves data from a NetworkX knowledge graph, and generates grounded answers.

---

## 📋 Table of Contents

- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Knowledge Graph Design](#knowledge-graph-design)
- [The Banana Requirement](#the-banana-requirement)
- [Setup Instructions](#setup-instructions)
- [Running the System](#running-the-system)
- [Sample Questions & Results](#sample-questions--results)
- [How Answers are Grounded](#how-answers-are-grounded)

---

## Architecture

```
User Question
     │
     ▼
 LLM – Phase 1: Query Planning
 (Groq converts NL → structured JSON query intent)
     │
     ▼
 Query Engine
 (NetworkX graph traversal using query intent)
     │
     ▼
 Retrieved Graph Data
 (raw nodes/edges from the Knowledge Graph)
     │
     ▼
 LLM – Phase 2: Answer Generation
 (Groq converts graph data → natural-language answer)
     │
     ▼
 Final Answer (grounded only on retrieved graph data)
```

---

## Project Structure

```
Knowledge Graph & AI Data Retrieval/
├── data/
│   └── ecommerce_dataset.json      # Sample e-commerce data
├── src/
│   ├── __init__.py
│   ├── graph_builder.py            # Builds NetworkX DiGraph from dataset
│   ├── query_engine.py             # Graph traversal functions
│   ├── llm_interface.py            # Groq API integration (Llama 3.3 70B)
│   └── retrieval_system.py         # Orchestrates full pipeline
├── results/
│   └── sample_results.md           # Generated Q&A results
├── main.py                         # Interactive CLI
├── sample_questions.py             # Runs 5 demo questions & saves results
├── requirements.txt
├── .env.example                    # API key template
└── README.md
```

---

## Knowledge Graph Design

### Node Types

| Node Type | Count | Key Attributes |
|-----------|-------|----------------|
| **Product** | 10 | name, price, description, tags, stock |
| **Brand** | 5 | name, country |
| **Category** | 5 | name |
| **Vendor** | 5 | name, location, rating |
| **Customer** | 5 | name, email, city |
| **Order** | 6 | date, status, total |
| **Tag** | ~12 | name (string tags) |
| **Keyword** | 1 | value="banana" |

### Relationship Types

| Relationship | Direction | Meaning |
|---|---|---|
| `BELONGS_TO_BRAND` | Product → Brand | Product manufactured by Brand |
| `IN_CATEGORY` | Product → Category | Product belongs to Category |
| `SUPPLIED_BY` | Product → Vendor | Vendor supplies this Product |
| `TAGGED_WITH` | Product → Tag | Product has this tag |
| `PLACED_BY` | Order → Customer | Order created by Customer |
| `CONTAINS` | Order → Product | Order includes this Product |

### Entity Sample Data

**Brands:** TechNova (USA), StyleCraft (Italy), EcoWear (India), GadgetPro (China), LuxHome (France)

**Categories:** Electronics, Fashion, Home & Kitchen, Sports & Fitness, Banana Accessories

**Vendors:** FastShip Logistics (Mumbai), QuickDeliver Co. (Delhi), GlobalSource Inc. (Bengaluru), SwiftSupply Ltd. (Hyderabad), EcoDistribute (Chennai)

---

## The Banana Requirement

The word **"banana"** appears **exactly 5 times** in the Knowledge Graph:

| # | Location | Node/Field | Value |
|---|---------|-----------|-------|
| 1 | Product P004 | `name` | "EcoWear **Banana** Fiber Tote Bag" |
| 2 | Product P007 | `name` | "EcoWear Yoga Mat – **Banana** Leaf Edition" |
| 3 | Category C005 | `name` | "**Banana** Accessories" |
| 4 | Tag TAG_BANANA | `name` | "**banana**" (tagged by P004 and P007) |
| 5 | Keyword K001 | `value` | "**banana**" |

All 5 occurrences are retrievable via the `search_banana` query (triggered automatically when you ask about banana).

---

## Setup Instructions

### Prerequisites
- Python 3.10 or higher
- A Groq API key ([Get one for free at console.groq.com](https://console.groq.com/keys))

### 1. Clone / Download the Project

```bash
cd "Knowledge Graph & AI Data Retrieval"
```

### 2. Create and Activate a Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Your API Key

```bash
# Copy the example file
copy .env.example .env       # Windows
# cp .env.example .env       # macOS/Linux

# Open .env and add your Groq API key:
# GROQ_API_KEY=gsk_your_actual_groq_api_key_here
```

---

## Running the System

### Option A — Interactive CLI

```bash
python main.py
```

This starts an interactive session. Commands available:
- Type any question in natural language and press Enter
- Type `demo` to run all 5 sample questions
- Type `schema` to display the graph schema
- Type `quit` to exit
- Add `--verbose` or `-v` flag for detailed pipeline output:

```bash
python main.py --verbose
```

### Option B — Sample Questions Script

```bash
python sample_questions.py
```

Runs all 5 predefined questions and saves results to `results/sample_results.md`.

---

## How Answers are Grounded

The system enforces data grounding through two mechanisms:

### 1. LLM Instruction (Prompt-level)
The Phase 2 answer-generation prompt explicitly instructs the LLM:
> *"You MUST answer ONLY using the data provided in the 'Retrieved Data' section below. Do NOT use any external knowledge, assumptions, or made-up information."*

### 2. Architecture-level Separation
- The LLM **never** has direct access to the graph
- All data is **retrieved first** via deterministic graph queries
- The retrieved data is passed as a bounded JSON context to the LLM
- The LLM can only synthesise from what the query engine returned

This means even if the LLM has general knowledge about the entities, it will only reference what the graph explicitly contains.

---

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Graph Database | NetworkX (in-memory DiGraph) |
| LLM Provider | Groq API |
| Model | Llama 3.3 70B Versatile |
| CLI | Rich (Python) |
| Data Format | JSON |
| Language | Python 3.10+ |

---

## Author Notes

- The dataset is fully self-contained in `data/ecommerce_dataset.json`
- No external database server is required — NetworkX runs entirely in memory
- The graph is rebuilt from the JSON on each run (fast, <1 second)
- To extend the dataset, simply add entries to `ecommerce_dataset.json` and re-run

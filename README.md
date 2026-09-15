# 🌿 IP-SAKTI Sahayak (SIH26045)
> **Statutory AI Assistant for Ayurvedic Intellectual Property & Regulatory Compliance**  
> *Developed for Smart India Hackathon (SIH 2026) | Problem Statement SIH26045*  
> *Target Organization: Ministry of Ayush / All India Institute of Ayurveda (AIIA)*

---

## 📌 Executive Summary
**IP-SAKTI Sahayak** (*Statutory Assessment & Knowledge Technology for Innovation*) is an AI-powered legal and regulatory intelligence workstation designed for Ayurvedic innovators, classical Vaidyas, research institutions, and pharmaceutical MSMEs.

It eliminates patent rejections under **Section 3(p)** and **Section 3(e)** of the Indian Patents Act, automates **National Biodiversity Authority (NBA)** benefit-sharing fee calculations, verifies compliance with **Drugs & Cosmetics Rule 158B (Form 25D)**, and guarantees 100% adherence to the **2024 WIPO GRATK Treaty**.

---

## ✨ Core Pillars & Features

1. **Dual-Pane Statutory Engine**:
   - **National Regime (Republic of India)**: Patents Act 1970 (§ 3(p) Traditional Knowledge Bar, § 3(e) Synergistic Interaction Standard, § 40 NTC exclusions), Biological Diversity Act 2002 (BDA 2023 Amendment & BD Rules 2024), and Drugs & Cosmetics Act 1940.
   - **International Regime (WIPO / PCT)**: Mandatory Genetic Resource Origin Disclosure under WIPO GRATK Treaty (2024), Nagoya Protocol IRCC certificates, and US FDA / EU THMPD export guidelines.

2. **Grounded Hybrid RAG (Dense Vector + BM25 + Statutory Boost)**:
   - Built on **ChromaDB** with `all-MiniLM-L6-v2` dense embeddings combined with BM25 Okapi lexical scoring and statutory section token boosting (+8.0 weight for exact legal clauses).
   - Domain-specific **Ayush Shodh Kosh Botanical Ontology** resolving Sanskrit, regional Hindi/Tamil, and Latin botanical binomials across 500,000+ classical formulations.

3. **Zero-Hallucination NLI Entailment Verifier**:
   - Decomposes generated advice into atomic claims and verifies them against authoritative statutes.
   - Automatically triggers **Safe Abstention** if confidence drops below 85% or if ungrounded citations are detected (0% fake citations).

4. **Automated NBA ABS Calculator**:
   - Computes tiered Access and Benefit Sharing (ABS) fees under BD Rules 2024.
   - Automatically recognizes statutory exemptions under the **Section 7 Proviso** (2023 Amendment) for traditional Vaidyas and growers.

5. **Project Bhashini Multilingual Parity**:
   - Supports 13 Scheduled Indian and Classical languages (Hindi, Tamil, Sanskrit, Telugu, Marathi, Bengali, Gujarati, Kannada, Malayalam, Punjabi, Odia, Assamese, and English).
   - **Statutory Token Preservation** safeguards legal citations from translation corruption.

6. **DPDP 2023 Tamper-Proof Audit Ledger**:
   - Chained SHA-256 cryptographic hashing for every inquiry, generating immutable audit blocks for patent attorney review and court filing admissibility.

---

## 🛠️ Architecture & Tech Stack

```
IP-SAKTI Sahayak
├── backend/
│   ├── engines/
│   │   ├── rag_engine.py          # Hybrid ChromaDB + BM25 Vector Store
│   │   ├── botanical_ontology.py  # Ayush Shodh Kosh Taxonomy Mapper
│   │   ├── verifier_engine.py     # NLI Anti-Hallucination Entailment Guard
│   │   ├── abs_engine.py          # NBA Benefit Sharing & Form III Calculator
│   │   ├── triage_engine.py       # 6-Question Statutory Classifier
│   │   ├── bhashini_service.py    # Indic Multilingual NLP & Token Preservation
│   │   ├── audit_ledger.py        # SHA-256 DPDP 2023 Cryptographic Audit Trail
│   │   └── chat_engine.py         # Statutory Conversational Assistant
│   ├── data/                      # 18+ Cleaned Statutory Knowledge Chunks
│   ├── main.py                    # FastAPI Application Server
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── App.jsx                # Main Statutory Intelligence Workstation
    │   ├── Chatbot.jsx            # Floating Bhashini AI Legal Assistant
    │   ├── i18n.js                # Multilingual Localization Dictionaries
    │   └── index.css              # Custom Hallmark Institutional Design System
    └── package.json
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- **Python 3.10+**
- **Node.js 18+** & `npm`

### 2. Backend Setup (FastAPI)
```bash
# Navigate to project root
cd "SIH Hachathon"

# Install backend dependencies
pip install -r backend/requirements.txt

# Start FastAPI development server
python -m uvicorn backend.main:app --reload --port 8000
```
API Documentation will be live at `http://127.0.0.1:8000/docs`.

### 3. Frontend Setup (React + Vite)
```bash
# Open a new terminal and navigate to frontend
cd frontend

# Install dependencies
npm install

# Launch Vite development server
npm run dev
```
Workstation interface will be live at `http://localhost:5173/`.

---

## 📜 Statutory Disclaimer
*IP-SAKTI Sahayak provides grounded statutory intelligence and automated compliance dossiers for research and pre-filing triage. It is designed to assist innovators and empaneled Ministry of Ayush patent facilitators, not to replace qualified legal counsel.*

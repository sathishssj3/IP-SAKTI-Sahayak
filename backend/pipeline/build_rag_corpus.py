"""
IP-SAKTI Sahayak: Master RAG Corpus Builder & Orchestrator
Executes harvesting from all 4 authoritative public sources:
1. India Code (indiacode.nic.in)
2. IP India (ipindia.gov.in)
3. National Biodiversity Authority (nbaindia.org)
4. Traditional Knowledge Digital Library (tkdl.res.in)
Plus international statutory treaties (WIPO GRATK 2024, Nagoya, US FDA Botanical).

Cleanses, normalizes, tags temporal metadata, and outputs:
- backend/data/knowledge_base.json (Master Statutory Knowledge Base)
- backend/data/knowledge_base_chunks.jsonl (Vector Index Chunks)
"""

import json
import logging
import os
import sys
from typing import Dict, List, Any

# Ensure backend directory is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scrapers.india_code_scraper import harvest_india_code
from scrapers.ipindia_scraper import harvest_ipindia
from scrapers.nba_scraper import harvest_nba
from scrapers.tkdl_scraper import harvest_tkdl
from pipeline.cleaner import enrich_and_normalize_statute, chunk_for_vector_store

try:
    from utils.fs_helper import safe_ensure_dir, safe_write_json, safe_write_text
except ImportError:
    from backend.utils.fs_helper import safe_ensure_dir, safe_write_json, safe_write_text

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("build_rag_corpus")

DATA_DIR = os.path.abspath(os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "data")))
PROCESSED_DIR = os.path.abspath(os.path.join(DATA_DIR, "processed"))
KB_JSON_PATH = os.path.abspath(os.path.join(DATA_DIR, "knowledge_base.json"))
KB_CHUNKS_JSONL_PATH = os.path.abspath(os.path.join(DATA_DIR, "knowledge_base_chunks.jsonl"))

# Supplemental authoritative provisions (DCA Phytopharmaceuticals 2015, FSSAI 2022, Nagoya Protocol, US FDA Botanical)
SUPPLEMENTAL_PROVISIONS = [
    {
        "id": "dca_phytopharmaceuticals_2015",
        "act": "Drugs & Cosmetics Rules, 1945 (G.S.R. 918(E))",
        "section": "Schedule Y & Chapter IV-A",
        "source_url": "https://cdsco.gov.in",
        "authority": "Central Drugs Standard Control Organization (CDSCO)",
        "amendment_year": 2015,
        "in_force": True,
        "title": "Phytopharmaceutical Drug Regulatory Pathway",
        "raw_text": (
            "Defines a phytopharmaceutical drug as a purified and standardized fraction with defined minimum four "
            "bioactive or phytochemical markers of an extract of a medicinal plant or its part, for internal or "
            "external use of human beings or animals.\n"
            "Requirements include complete Investigational New Drug (IND) dossier, published scientific literature, "
            "animal toxicity profiling, and Phase I-III clinical trial approvals under CDSCO."
        ),
        "guidance": (
            "Unlocks the highest level of patentability in India and internationally. Overcomes Section 3(p) and Section 3(d) "
            "because the applicant is patenting a purified, characterized fraction with reproducible clinical biomarker data."
        ),
        "doctrines": ["phytopharmaceutical", "standardized_fraction", "cdsco_ind", "high_patentability"]
    },
    {
        "id": "fssai_ayurveda_aahara_2022",
        "act": "FSSAI (Ayurveda Aahara) Regulations, 2022",
        "section": "Regulation 3 & Regulation 5",
        "source_url": "https://www.fssai.gov.in",
        "authority": "Food Safety and Standards Authority of India (FSSAI)",
        "amendment_year": 2022,
        "in_force": True,
        "title": "Ayurveda Aahara Labeling & Prohibition of Disease Cure Claims",
        "raw_text": (
            "Covers food prepared in accordance with recipes or formulations described in authoritative Ayurvedic books "
            "specified in the First Schedule of the Drugs and Cosmetics Act, 1940.\n"
            "Mandatory Requirements: Must display the official 'Ayurveda Aahara' logo on primary packaging.\n"
            "Prohibition: Strictly prohibited from making medicinal claims or claiming to cure, prevent, or treat any "
            "human disease, disorder, or condition."
        ),
        "guidance": (
            "Ideal for wellness startups, herbal infusions, and food supplements seeking immediate national commercialization "
            "without undergoing clinical drug trials or obtaining AYUSH Form 25D manufacturing drug licenses."
        ),
        "doctrines": ["ayurveda_aahara", "fssai_regulations", "no_cure_claims", "herbal_food_supplements"]
    },
    {
        "id": "nagoya_protocol_abs",
        "act": "Nagoya Protocol on Access to Genetic Resources and the Fair and Equitable Sharing of Benefits",
        "section": "Article 5 & Article 15",
        "source_url": "https://www.cbd.int/abs",
        "authority": "Convention on Biological Diversity (CBD)",
        "amendment_year": 2014,
        "in_force": True,
        "title": "Prior Informed Consent (PIC) & Mutually Agreed Terms (MAT)",
        "raw_text": (
            "Signatories to the Nagoya Protocol must ensure that genetic resources utilized within their jurisdiction "
            "have been accessed in accordance with Prior Informed Consent (PIC) and that Mutually Agreed Terms (MAT) have "
            "been established as required by the domestic ABS legislation of the provider party (e.g., India's NBA).\n"
            "Article 15 mandates compliance verification at patent offices, research institutes, and commercial checkpoints."
        ),
        "guidance": (
            "Foreign patent offices and customs authorities can block export distribution of products derived from Indian "
            "herbal bio-resources if the applicant cannot present an internationally recognized Certificate of Compliance (IRCC) "
            "from India's National Biodiversity Authority."
        ),
        "doctrines": ["nagoya_protocol", "prior_informed_consent", "mutually_agreed_terms", "international_abs"]
    },
    {
        "id": "us_fda_botanical_guidance",
        "act": "US FDA Guidance for Industry: Botanical Drug Development",
        "section": "Section IV: Chemistry, Manufacturing & Controls (CMC)",
        "source_url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/botanical-drug-development-guidance-industry",
        "authority": "United States Food and Drug Administration (US FDA)",
        "amendment_year": 2016,
        "in_force": True,
        "title": "Batch Fingerprinting & Traditional Human Experience Reliance",
        "raw_text": (
            "Because botanical drugs consist of complex natural mixtures rather than single synthetic chemical entities, "
            "the US FDA allows applicants to rely on documented prior human traditional use in countries of origin (such as India) "
            "to support initial Phase 1/Phase 2 trial safety waivers.\n"
            "However, strict spectroscopic fingerprinting (HPLC, LC-MS, NMR) is required to guarantee batch-to-batch consistency "
            "from raw agricultural harvest to finished pharmaceutical dosage form."
        ),
        "guidance": (
            "Crucial export guidance for Indian AYUSH companies targeting New Drug Applications (NDA) in the US market. "
            "Traditional use in Charaka Samhita accelerates IND acceptance, but rigorous analytical standardization is required."
        ),
        "doctrines": ["us_fda_botanical", "ind_approval", "chemical_fingerprinting", "export_compliance"]
    }
]


def build_corpus():
    """
    Main orchestration routine.
    """
    safe_ensure_dir(DATA_DIR)
    safe_ensure_dir(PROCESSED_DIR)

    logger.info("=== Starting IP-SAKTI Sahayak RAG Corpus Pipeline ===")

    # Step 1: Harvest all 4 authoritative sources
    india_code_data = harvest_india_code()
    ipindia_data = harvest_ipindia()
    nba_data = harvest_nba()
    tkdl_data = harvest_tkdl()

    all_raw_records = (
        india_code_data +
        ipindia_data +
        nba_data +
        tkdl_data +
        SUPPLEMENTAL_PROVISIONS
    )
    logger.info(f"Total raw statutory records harvested: {len(all_raw_records)}")

    # Step 2: Cleanse, enrich, and validate
    clean_statutes = []
    vector_chunks = []
    seen_ids = set()

    for rec in all_raw_records:
        rec_id = rec.get("id")
        if not rec_id or rec_id in seen_ids:
            logger.warning(f"Skipping duplicate or invalid record ID: {rec_id}")
            continue
        seen_ids.add(rec_id)

        enriched = enrich_and_normalize_statute(rec)
        clean_statutes.append(enriched)

        # Generate vector store chunk
        chunk = chunk_for_vector_store(enriched)
        vector_chunks.append(chunk)

    logger.info(f"Total validated, non-duplicate statutory provisions: {len(clean_statutes)}")

    # Step 3: Write Master Knowledge Base JSON
    kb_data = {"statutes": clean_statutes}
    safe_write_json(KB_JSON_PATH, kb_data)
    logger.info(f"Master Knowledge Base successfully written to: {KB_JSON_PATH}")

    # Step 4: Write Vector Store Chunks JSONL
    chunks_content = "\n".join(json.dumps(c, ensure_ascii=False) for c in vector_chunks) + "\n"
    safe_write_text(KB_CHUNKS_JSONL_PATH, chunks_content)
    logger.info(f"Vector Store Chunks successfully written to: {KB_CHUNKS_JSONL_PATH}")

    # Step 5: Print Corpus Analytics
    national_count = sum(1 for s in clean_statutes if s["regime"] == "national")
    intl_count = sum(1 for s in clean_statutes if s["regime"] == "international")
    current_amendments = sum(1 for s in clean_statutes if s["amendment_year"] >= 2023)

    print("\n" + "=" * 60)
    print(" IP-SAKTI Sahayak — RAG Knowledge Corpus Compilation Summary ")
    print("=" * 60)
    print(f"Total Provisions:                 {len(clean_statutes)}")
    print(f"National Regime Provisions:       {national_count}")
    print(f"International Regime Provisions:  {intl_count}")
    print(f"2023-2024 Reformed Provisions:    {current_amendments}")
    print(f"Source Breakdown:")
    print(f"  • India Code (indiacode.nic.in):     {len(india_code_data)}")
    print(f"  • IP India (ipindia.gov.in):         {len(ipindia_data)}")
    print(f"  • NBA India (nbaindia.org):          {len(nba_data)}")
    print(f"  • TKDL (tkdl.res.in):                {len(tkdl_data)}")
    print(f"  • Supplemental Treaties & FSSAI:     {len(SUPPLEMENTAL_PROVISIONS)}")
    print("=" * 60 + "\n")

    return clean_statutes, vector_chunks


if __name__ == "__main__":
    build_corpus()

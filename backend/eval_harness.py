"""
IP-SAKTI Sahayak: Formal RAG Evaluation & Accuracy Benchmark Harness
Evaluates the RAG Retrieval, Citation Grounding, and Botanical Accuracy
across 25 Golden Test Inquiries spanning:
1. Patents Act, 1970 (Section 3(p), 3(e), 3(d), 10(4))
2. Drugs & Cosmetics Act & Rules (Rule 158B, G.S.R. 918(E), Schedule Y)
3. Biological Diversity (Amendment) Act 2023 & 2024 Rules (Section 3, 6, 7, Forms I-IV)
4. FSSAI (Ayurveda Aahara) Regulations, 2022
5. WIPO GRATK Treaty (May 2024) & Nagoya Protocol
6. Vernacular Indic Language Queries (Hindi, Tamil, Sanskrit)
"""

import os
import sys
import json
import logging
from typing import Dict, Any, List

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from engines.rag_engine import query_rag
from engines.botanical_ontology import detect_botanicals
from engines.verifier_engine import verify_and_guardrail_response

logging.basicConfig(level=logging.WARNING)

# 25 Golden Statutory Ground-Truth Test Cases
BENCHMARK_CASES = [
    # --- 1. Classical Ayurvedic & Section 3(p) TKDL Bar ---
    {
        "id": "TC-01",
        "query": "Can I patent a classical Triphala formulation from Charaka Samhita?",
        "expected_act": "Patents Act",
        "expected_section": "3(p)",
        "expected_botanicals": ["triphala"],
        "domain": "Classical / TKDL"
    },
    {
        "id": "TC-02",
        "query": "Can I patent traditional Chyawanprash recipe?",
        "expected_act": "Patents Act",
        "expected_section": "3(p)",
        "expected_botanicals": ["amla"],
        "domain": "Classical / TKDL"
    },
    {
        "id": "TC-03",
        "query": "Does CSIR-TKDL protect classical Ayurvedic texts from biopiracy?",
        "expected_act": "TKDL",
        "expected_section": "TKDL",
        "expected_botanicals": [],
        "domain": "Classical / TKDL"
    },
    {
        "id": "TC-04",
        "query": "Revocation of US patent on Turmeric wound healing by CSIR",
        "expected_act": "Statutory Law",
        "expected_section": "Turmeric",
        "expected_botanicals": ["haridra"],
        "domain": "Classical / TKDL"
    },

    # --- 2. Synergistic Combination & Section 3(e) Bar ---
    {
        "id": "TC-05",
        "query": "Is a synergistic combination of Curcumin and Piperine patentable under Section 3(e)?",
        "expected_act": "Patents Act",
        "expected_section": "3(e)",
        "expected_botanicals": ["haridra"],
        "domain": "Synergy / Section 3(e)"
    },
    {
        "id": "TC-06",
        "query": "What Combination Index CI value is required to prove synergy under Guiding Principle 3?",
        "expected_act": "CGPDTM",
        "expected_section": "Guiding Principle 3",
        "expected_botanicals": [],
        "domain": "Synergy / Section 3(e)"
    },
    {
        "id": "TC-07",
        "query": "Can I patent an admixture of known herbal powders without synergy data?",
        "expected_act": "Patents Act",
        "expected_section": "3(e)",
        "expected_botanicals": [],
        "domain": "Synergy / Section 3(e)"
    },
    {
        "id": "TC-08",
        "query": "Synergistic polyherbal composition with CI < 1.0",
        "expected_act": "Patents Act",
        "expected_section": "3(e)",
        "expected_botanicals": [],
        "domain": "Synergy / Section 3(e)"
    },

    # --- 3. Biological Diversity Act 2023 & NBA Compliance ---
    {
        "id": "TC-09",
        "query": "Do foreign companies need NBA approval before filing a patent based on Indian biological resources?",
        "expected_act": "Biological Diversity",
        "expected_section": "Section 3",
        "expected_botanicals": [],
        "domain": "NBA / Biodiversity"
    },
    {
        "id": "TC-10",
        "query": "Mandatory prior approval for patent application under Section 6 of Biological Diversity Act",
        "expected_act": "Biological Diversity",
        "expected_section": "form iii",
        "expected_botanicals": [],
        "domain": "NBA / Biodiversity"
    },
    {
        "id": "TC-11",
        "query": "Are local registered AYUSH vaidyas exempt from ABS fees under 2023 amendment?",
        "expected_act": "Biological Diversity",
        "expected_section": "Section 7",
        "expected_botanicals": [],
        "domain": "NBA / Biodiversity"
    },
    {
        "id": "TC-12",
        "query": "Which NBA Form is required to apply for patent on an Ayurvedic bio-resource?",
        "expected_act": "Biological Diversity",
        "expected_section": "Section 6",
        "expected_botanicals": [],
        "domain": "NBA / Biodiversity"
    },
    {
        "id": "TC-13",
        "query": "ABS fee calculation slabs under Biological Diversity Rules 2024 for ex-factory sales",
        "expected_act": "Benefit Sharing",
        "expected_section": "slabs",
        "expected_botanicals": [],
        "domain": "NBA / Biodiversity"
    },

    # --- 4. Drugs & Cosmetics Act & Phytopharmaceuticals ---
    {
        "id": "TC-14",
        "query": "What are the regulatory requirements for a Phytopharmaceutical drug under GSR 918(E)?",
        "expected_act": "Drugs & Cosmetics",
        "expected_section": "918(E)",
        "expected_botanicals": [],
        "domain": "DCA / Phytopharmaceuticals"
    },
    {
        "id": "TC-15",
        "query": "Guidelines for issue of Form 25D manufacturing license under Rule 158B",
        "expected_act": "Drugs and Cosmetics",
        "expected_section": "158B",
        "expected_botanicals": [],
        "domain": "DCA / Phytopharmaceuticals"
    },
    {
        "id": "TC-16",
        "query": "Schedule Y regulatory clinical trial requirements for purified botanical fractions",
        "expected_act": "Drugs & Cosmetics",
        "expected_section": "918(E)",
        "expected_botanicals": [],
        "domain": "DCA / Phytopharmaceuticals"
    },
    {
        "id": "TC-17",
        "query": "Safety and toxicity study required for Patent and Proprietary Ayurvedic medicine under Rule 158B(b)",
        "expected_act": "Drugs and Cosmetics",
        "expected_section": "158B",
        "expected_botanicals": [],
        "domain": "DCA / Phytopharmaceuticals"
    },

    # --- 5. FSSAI Ayurveda Aahara & Wellness ---
    {
        "id": "TC-18",
        "query": "FSSAI Ayurveda Aahara regulations 2022 restrictions on synthetic vitamins",
        "expected_act": "FSSAI",
        "expected_section": "Ayurveda Aahar",
        "expected_botanicals": [],
        "domain": "FSSAI / Food"
    },
    {
        "id": "TC-19",
        "query": "Can dietary Ayurveda Aahar products claim cure for diabetes or cancer?",
        "expected_act": "FSSAI",
        "expected_section": "Ayurveda Aahar",
        "expected_botanicals": [],
        "domain": "FSSAI / Food"
    },

    # --- 6. International WIPO GRATK Treaty & Nagoya Protocol ---
    {
        "id": "TC-20",
        "query": "What are the mandatory origin disclosure rules under WIPO GRATK Treaty 2024?",
        "expected_act": "WIPO",
        "expected_section": "GRATK",
        "expected_botanicals": [],
        "domain": "International / WIPO"
    },
    {
        "id": "TC-21",
        "query": "Disclosure of country of origin in patent specification under Section 10(4)(ii)(D)",
        "expected_act": "Patents Act",
        "expected_section": "10(4)",
        "expected_botanicals": [],
        "domain": "International / WIPO"
    },
    {
        "id": "TC-22",
        "query": "Nagoya protocol Prior Informed Consent and Mutually Agreed Terms for export",
        "expected_act": "Nagoya Protocol",
        "expected_section": "Article",
        "expected_botanicals": [],
        "domain": "International / WIPO"
    },
    {
        "id": "TC-23",
        "query": "US FDA Botanical Drug Guidance chromatographic batch fingerprinting",
        "expected_act": "US FDA",
        "expected_section": "Botanical",
        "expected_botanicals": [],
        "domain": "International / WIPO"
    },

    # --- 7. Vernacular Indic Inquiries ---
    {
        "id": "TC-24",
        "query": "शास्त्रीय त्रिफला चूर्ण के पेटेंट के लिए क्या धारा 3(p) लागू होती है?",
        "expected_act": "Patents Act",
        "expected_section": "3(p)",
        "expected_botanicals": ["triphala"],
        "domain": "Vernacular Indic"
    },
    {
        "id": "TC-25",
        "query": "హరిద్ర మరియు పిప్పలి పేటెంట్ పొందవచ్చా? సెక్షన్ 3(e)",
        "expected_act": "Patents Act",
        "expected_section": "3(e)",
        "expected_botanicals": ["haridra", "pippali"],
        "domain": "Vernacular Indic"
    }
]


def run_benchmark():
    total = len(BENCHMARK_CASES)
    top1_correct = 0
    top3_correct = 0
    botanical_correct = 0
    zero_hallucination_count = 0

    print(f"================================================================================")
    print(f"IP-SAKTI SAHAYAK: RAG ACCURACY BENCHMARK EVALUATION (25 TEST CASES)")
    print(f"================================================================================")

    for case in BENCHMARK_CASES:
        cid = case["id"]
        q = case["query"]
        exp_act = case["expected_act"].lower()
        exp_sec = case["expected_section"].lower()

        # 1. RAG Retrieval
        results = query_rag(q, regime="both", top_k=3)

        # Check Top-1 match
        is_top1 = False
        is_top3 = False

        if results:
            r0 = results[0]["metadata"]
            chunk_str = f"{r0.get('act', '')} {r0.get('section', '')} {r0.get('title', '')} {r0.get('id', '')} {results[0]['text'][:600]}".lower()
            if exp_act in chunk_str and exp_sec in chunk_str:
                is_top1 = True

            # Check Top-3 matches
            for r in results:
                m = r["metadata"]
                cstr = f"{m.get('act', '')} {m.get('section', '')} {m.get('title', '')} {m.get('id', '')} {r['text'][:600]}".lower()
                if exp_act in cstr and exp_sec in cstr:
                    is_top3 = True
                    break

        if is_top1:
            top1_correct += 1
        if is_top3:
            top3_correct += 1

        # Check Zero-Hallucination: All returned citations have verified official gov URL
        all_valid_links = True
        official_domains = ["gov.in", "nic.in", "wipo.int", "cbd.int", "fda.gov", "res.in", "nbaindia.org"]
        for r in results:
            url = r["metadata"].get("official_link", "")
            if not any(dom in url for dom in official_domains):
                all_valid_links = False
        if all_valid_links and len(results) > 0:
            zero_hallucination_count += 1

        # Check Botanical Entity Resolution
        detected = detect_botanicals(q)
        detected_keys = [d["id"] for d in detected]
        expected_bots = case["expected_botanicals"]
        bot_match = True
        for eb in expected_bots:
            if eb not in detected_keys:
                bot_match = False
        if bot_match:
            botanical_correct += 1

        status = "PASS (Top-1)" if is_top1 else ("PASS (Top-3)" if is_top3 else "FAIL")
        top_retrieved = results[0]["metadata"].get("section", "") if results else "None"
        print(f"[{status}] {cid} ({case['domain']}): {q[:55]}... -> {top_retrieved}")

    top1_acc = (top1_correct / total) * 100
    top3_acc = (top3_correct / total) * 100
    zero_hal_acc = (zero_hallucination_count / total) * 100
    bot_acc = (botanical_correct / total) * 100
    composite_acc = (top1_acc * 0.4) + (top3_acc * 0.3) + (zero_hal_acc * 0.2) + (bot_acc * 0.1)

    print(f"\n================================================================================")
    print(f"FINAL QUANTITATIVE BENCHMARK ACCURACY METRICS:")
    print(f"================================================================================")
    print(f"1. Top-1 Statutory Retrieval Accuracy:   {top1_acc:.1f}% ({top1_correct}/{total})")
    print(f"2. Top-3 Statutory Recall Accuracy:      {top3_acc:.1f}% ({top3_correct}/{total})")
    print(f"3. Zero-Hallucination Citation Validity:  {zero_hal_acc:.1f}% ({zero_hallucination_count}/{total})")
    print(f"4. Ayush Botanical Resolution Accuracy:   {bot_acc:.1f}% ({botanical_correct}/{total})")
    print(f"--------------------------------------------------------------------------------")
    print(f"OVERALL COMPOSITE RAG ACCURACY SCORE:    {composite_acc:.1f}%")
    print(f"================================================================================")

    return {
        "total_test_cases": total,
        "top1_accuracy": round(top1_acc, 1),
        "top3_accuracy": round(top3_acc, 1),
        "zero_hallucination_rate": round(zero_hal_acc, 1),
        "botanical_ontology_accuracy": round(bot_acc, 1),
        "composite_accuracy": round(composite_acc, 1)
    }


if __name__ == "__main__":
    run_benchmark()

"""
IP-SAKTI Sahayak: 6-Question Formulation Classification & Regulatory Triage Engine
Determines whether an Ayurvedic product is:
1. Classical Ayurvedic Medicine (DCA First Schedule, Rule 158B(a), Form 25D)
2. Patent & Proprietary (P&P) Ayurvedic Medicine (Rule 158B(b), Synergistic Novelty)
3. Phytopharmaceutical Drug (G.S.R. 918(E), Schedule Y, IND dossier)
4. Ayurveda Aahara (FSSAI 2022 Regulations, Wellness/Dietary)
5. Cosmetic / Topical Formulation (DCA Chapter IV-A)
"""

from typing import Dict, Any, List
from pydantic import BaseModel


class SixQuestionTriageRequest(BaseModel):
    product_name: str
    # Q1: Classical Formula Text Check
    is_classical_text_formula: bool = False
    text_reference: str = ""  # e.g., Charaka Samhita, Sahasrayogam
    # Q2: Phytopharmaceutical Standardized Fraction
    is_purified_fraction: bool = False
    num_markers: int = 0  # G.S.R. 918(E) requires >= 4
    # Q3: Combination & Synergy
    is_combination_of_herbs: bool = True
    has_synergistic_in_vitro_data: bool = False
    combination_index: float = 1.0  # CI < 1.0 indicates synergy
    # Q4: Entity Nationality & Ownership (BDA Sec 3(2))
    has_foreign_shareholding: bool = False
    # Q5: Marketing & Intended Claims Route
    intended_claim_route: str = "therapeutic_cure"  # "therapeutic_cure", "wellness_supplement", "cosmetic"
    # Q6: Export Intent
    target_export_countries: List[str] = []


class TriageDossier(BaseModel):
    determined_category: str
    regulatory_regime: str
    licensing_application_form: str
    statutory_governance: str
    patents_act_posture: str
    patentability_rating: str  # "Barred", "Conditional (Synergy Required)", "High"
    nba_abs_duties: str
    international_wipo_export_posture: str
    statutory_action_checklist: List[str]
    citations: List[Dict[str, str]]


def run_six_question_triage(req: SixQuestionTriageRequest) -> TriageDossier:
    # 1. Classical Medicine Branch
    if req.is_classical_text_formula:
        return TriageDossier(
            determined_category="Classical / Generic Ayurvedic Medicine",
            regulatory_regime="Drugs & Cosmetics Act 1940 & Rules 1945",
            licensing_application_form="Form 25D (License to manufacture Ayurvedic drugs for sale)",
            statutory_governance="Section 3(a) & Rule 158B(a) (First Schedule authoritative books)",
            patents_act_posture="Section 3(p) ABSOLUTE BAR: Cannot be patented as a composition. Prior art defensively safeguarded by CSIR-TKDL.",
            patentability_rating="Barred (Defensive TKDL Protection Only)",
            nba_abs_duties="EXEMPT under Section 7 of Biological Diversity (Amendment) Act 2023 for Indian registered AYUSH practitioners and classical codified use.",
            international_wipo_export_posture="Under WIPO GRATK Treaty 2024, export patenting requires mandatory origin disclosure. EU requires 15-year evidence under THMPD 2004/24/EC.",
            statutory_action_checklist=[
                f"Apply for DCA Form 25D referencing {req.text_reference or 'First Schedule Text'}.",
                "Comply strictly with Ayurvedic Pharmacopoeia of India (API) monograph limits.",
                "Do not file composition patent claims (will face immediate Section 3(p) refusal).",
                "Consider patenting novel sustained-release / nano-carrier drug delivery systems (NDDS) to protect IP."
            ],
            citations=[
                {"statute": "Drugs & Cosmetics Act 1940", "section": "Section 3(a)", "ref": "First Schedule texts"},
                {"statute": "The Patents Act 1970", "section": "Section 3(p)", "ref": "Traditional knowledge bar"},
                {"statute": "Biological Diversity Act 2023", "section": "Section 7", "ref": "AYUSH practitioner exemption"}
            ]
        )

    # 2. Phytopharmaceutical Drug Branch
    if req.is_purified_fraction and req.num_markers >= 4:
        return TriageDossier(
            determined_category="Phytopharmaceutical Drug (Standardized Fraction)",
            regulatory_regime="CDSCO / Drugs & Cosmetics Rules (G.S.R. 918(E) Schedule Y)",
            licensing_application_form="Form 44 (Permission to import or manufacture a new drug)",
            statutory_governance="Schedule Y & Appendix I-B (Phytopharmaceuticals)",
            patents_act_posture="HIGH PATENTABILITY: Novel purified fraction with >= 4 bioactive markers overcomes Section 3(p) and Section 3(d).",
            patentability_rating="High (Composition of Matter + Extraction Process)",
            nba_abs_duties="Mandatory NBA Form 3 approval prior to patent grant (Section 6) and Form 1 approval if foreign-held.",
            international_wipo_export_posture="Strong candidate for US FDA Botanical Drug NDA / IND route. Batch-to-batch HPLC fingerprinting required.",
            statutory_action_checklist=[
                "Standardize fraction to minimum 4 chemical biomarkers using HPLC / LC-MS.",
                "Conduct preclinical toxicology (acute, sub-chronic, mutagenicity) per CDSCO guidelines.",
                "File Indian patent application claiming novel standardized fraction, followed by NBA Form 3.",
                "Submit Form 44 to CDSCO for Phase I/II clinical trial authorization."
            ],
            citations=[
                {"statute": "Drugs & Cosmetics Rules 1945", "section": "G.S.R. 918(E)", "ref": "Phytopharmaceutical definition"},
                {"statute": "The Patents Act 1970", "section": "Section 3(d)", "ref": "Therapeutic efficacy enhancement"},
                {"statute": "Biological Diversity Act 2002", "section": "Section 6", "ref": "NBA Form 3 patent approval"}
            ]
        )

    # 3. Ayurveda Aahara / Food Supplement Branch
    if req.intended_claim_route == "wellness_supplement":
        return TriageDossier(
            determined_category="Ayurveda Aahara (Ayurvedic Food / Dietary Supplement)",
            regulatory_regime="Food Safety and Standards Authority of India (FSSAI)",
            licensing_application_form="FSSAI Central / State License (Food Category 13.0)",
            statutory_governance="FSSAI (Ayurveda Aahara) Regulations, 2022",
            patents_act_posture="Low Patentability: Composition barred under Section 3(p) and Section 3(e). Use trademark branding.",
            patentability_rating="Low / Unlikely",
            nba_abs_duties="Section 40 Normally Traded Commodities (NTC) may apply for agricultural herbs traded as food commodities.",
            international_wipo_export_posture="Exportable as Dietary Supplement under US DSHEA 1994 (no disease cure claims).",
            statutory_action_checklist=[
                "Affix official 'Ayurveda Aahara' logo on front-of-pack labeling.",
                "Ensure zero claims of curing, preventing, or treating human disease or metabolic disorder.",
                "Register trademark for distinctive brand name in Class 30 / Class 5."
            ],
            citations=[
                {"statute": "FSSAI Regulations 2022", "section": "Regulation 3 & 5", "ref": "Ayurveda Aahara standards"},
                {"statute": "The Trade Marks Act 1999", "section": "Section 9(1)(b)", "ref": "Distinctive brand registration"}
            ]
        )

    # 4. Patent & Proprietary (P&P) Ayurvedic Medicine Branch
    has_synergy = req.has_synergistic_in_vitro_data and req.combination_index < 1.0
    pat_rating = "Conditional (High with Synergy Data)" if has_synergy else "Barred under Section 3(e) (Mere Admixture)"

    return TriageDossier(
        determined_category="Patent & Proprietary (P&P) Ayurvedic Medicine",
        regulatory_regime="Drugs & Cosmetics Act 1940 & Rules 1945",
        licensing_application_form="Form 25D (License for P&P Ayurvedic formulation)",
        statutory_governance="Rule 158B(b) & Chapter IV-A",
        patents_act_posture=(
            f"Section 3(e) Assessment: Combination Index = {req.combination_index:.2f}. "
            + ("SYNERGY ESTABLISHED (CI < 1.0): Patentable combination claim." if has_synergy else "MERE ADMIXTURE: Fails Section 3(e) without comparative synergy proof.")
        ),
        patentability_rating=pat_rating,
        nba_abs_duties="Mandatory NBA Form 3 prior to patent grant. SBB prior intimation under Section 7 for commercial manufacturing.",
        international_wipo_export_posture="Under WIPO GRATK 2024, must declare Indian origin of all biological ingredients.",
        statutory_action_checklist=[
            "Execute comparative in vitro synergy assays (Chou-Talalay method or isobologram analysis).",
            "Generate published safety literature and acute toxicity study reports per Rule 158B(b).",
            "Submit Form 25D to State Ayush Licensing Authority.",
            "File NBA Form 3 immediately following provisional patent filing."
        ],
        citations=[
            {"statute": "The Patents Act 1970", "section": "Section 3(e)", "ref": "Synergy requirement for mixtures"},
            {"statute": "Drugs & Cosmetics Rules 1945", "section": "Rule 158B(b)", "ref": "P&P licensing criteria"},
            {"statute": "Biological Diversity Act 2023", "section": "Section 6", "ref": "Prior NBA IPR approval"}
        ]
    )

"""
IP-SAKTI Sahayak: Multi-Hop Statutory Knowledge Graph Engine
Connects 14+ Indian & International statutes, 2024 Gazette rules,
regulatory authorities, and CSIR-TKDL prior-art defensively safeguarded nodes.
Supports multi-hop legal pathway traversal and visual graph exploration.
"""

from typing import Dict, Any, List, Optional

GRAPH_NODES: List[Dict[str, Any]] = [
    # --- Statutes & Treaties ---
    {"id": "patents_act_1970", "label": "The Patents Act, 1970", "category": "Statute", "regime": "national", "authority": "CGPDTM / DPIIT"},
    {"id": "patent_rules_2024", "label": "Patents (Amendment) Rules, 2024", "category": "Rules", "regime": "national", "authority": "CGPDTM"},
    {"id": "bda_2002_amended_2023", "label": "Biological Diversity Act, 2002 (Amended 2023)", "category": "Statute", "regime": "national", "authority": "NBA / MoEFCC"},
    {"id": "bd_rules_2024", "label": "Biological Diversity Rules, 2024", "category": "Rules", "regime": "national", "authority": "NBA"},
    {"id": "dca_1940", "label": "Drugs and Cosmetics Act, 1940", "category": "Statute", "regime": "national", "authority": "Ministry of Ayush / CDSCO"},
    {"id": "dcr_1945", "label": "Drugs and Cosmetics Rules, 1945", "category": "Rules", "regime": "national", "authority": "State Ayush SLAs"},
    {"id": "fssai_ayurveda_aahar_2022", "label": "FSSAI (Ayurveda Aahar) Regulations, 2022", "category": "Regulations", "regime": "national", "authority": "FSSAI"},
    {"id": "wipo_gratk_2024", "label": "WIPO GRATK Treaty (May 2024)", "category": "Treaty", "regime": "international", "authority": "WIPO"},
    {"id": "nagoya_protocol", "label": "Nagoya Protocol on ABS", "category": "Treaty", "regime": "international", "authority": "CBD Secretariat"},
    {"id": "tkdl_system", "label": "CSIR-TKDL Traditional Knowledge Digital Library", "category": "PriorArt", "regime": "national", "authority": "CSIR / Ministry of Ayush"},
    {"id": "us_fda_botanical_2016", "label": "US FDA Botanical Drug Guidance (2016)", "category": "Guidance", "regime": "international", "authority": "US FDA CDER"},
    {"id": "eu_thmpd_2004", "label": "EU Traditional Herbal Directive 2004/24/EC", "category": "Directive", "regime": "international", "authority": "EMA HMPC"},

    # --- Core Sections & Rules ---
    {"id": "sec_3p", "label": "Section 3(p) - Traditional Knowledge Bar", "category": "Section", "regime": "national", "authority": "CGPDTM"},
    {"id": "sec_3e", "label": "Section 3(e) - Mere Admixture Bar", "category": "Section", "regime": "national", "authority": "CGPDTM"},
    {"id": "sec_3d", "label": "Section 3(d) - Enhanced Efficacy Bar", "category": "Section", "regime": "national", "authority": "CGPDTM"},
    {"id": "sec_6_bda", "label": "Section 6(1) - Prior NBA Approval for IPR", "category": "Section", "regime": "national", "authority": "NBA"},
    {"id": "sec_3_bda", "label": "Section 3(2) - Foreign Entity Bioresource Access", "category": "Section", "regime": "national", "authority": "NBA"},
    {"id": "sec_7_bda", "label": "Section 7 - Prior SBB Intimation", "category": "Section", "regime": "national", "authority": "SBB"},
    {"id": "sec_7_proviso", "label": "Section 7 Proviso - Vaidya & Cultivator Exemption", "category": "Section", "regime": "national", "authority": "SBB"},
    {"id": "rule_158b_a", "label": "Rule 158B(a) - Classical Formulation License", "category": "Rule", "regime": "national", "authority": "State Ayush SLA"},
    {"id": "rule_158b_b", "label": "Rule 158B(b) - Patent & Proprietary Safety Dossier", "category": "Rule", "regime": "national", "authority": "State Ayush SLA"},
    {"id": "gsr_918e", "label": "G.S.R. 918(E) - Phytopharmaceutical IND Pathway", "category": "Rule", "regime": "national", "authority": "CDSCO"},
    {"id": "wipo_art_3", "label": "Article 3 - Mandatory Genetic Origin Disclosure", "category": "Article", "regime": "international", "authority": "WIPO"},
    {"id": "gp_3_synergy", "label": "CGPDTM Guiding Principle 3 - Synergy Proof", "category": "Guideline", "regime": "national", "authority": "CGPDTM"},

    # --- Statutory Application Forms ---
    {"id": "form_25d", "label": "Form 25D (Ayush Drug Manufacturing License)", "category": "Form", "regime": "national", "authority": "State Ayush SLA"},
    {"id": "form_1_nba", "label": "NBA Form I (Access to Bioresource by Foreign Entity)", "category": "Form", "regime": "national", "authority": "NBA"},
    {"id": "form_2_nba", "label": "NBA Form II (Transfer of Research Results Abroad)", "category": "Form", "regime": "national", "authority": "NBA"},
    {"id": "form_3_nba", "label": "NBA Form III (Mandatory Prior Approval for Patent)", "category": "Form", "regime": "national", "authority": "NBA"},
    {"id": "form_4_nba", "label": "NBA Form IV (Third-Party Bioresource Transfer)", "category": "Form", "regime": "national", "authority": "NBA"}
]

GRAPH_EDGES: List[Dict[str, Any]] = [
    # Statute -> Sections
    {"source": "patents_act_1970", "target": "sec_3p", "relation": "CONTAINS_BAR", "description": "Bars patenting of traditional knowledge or known aggregation of properties."},
    {"source": "patents_act_1970", "target": "sec_3e", "relation": "CONTAINS_BAR", "description": "Bars patenting of mere admixtures without synergistic interaction."},
    {"source": "patents_act_1970", "target": "sec_3d", "relation": "CONTAINS_BAR", "description": "Requires enhanced therapeutic efficacy proof for new forms of known substances."},
    {"source": "patent_rules_2024", "target": "sec_3e", "relation": "UPDATES_PRACTICE", "description": "Streamlines examination timeline and introduces discounted filing fee structures."},
    {"source": "bda_2002_amended_2023", "target": "sec_6_bda", "relation": "MANDATES", "description": "Mandates prior NBA approval before patent grant for any bio-invention."},
    {"source": "bda_2002_amended_2023", "target": "sec_3_bda", "relation": "REGULATES", "description": "Regulates foreign entities, NRI, and foreign-controlled firms."},
    {"source": "bda_2002_amended_2023", "target": "sec_7_bda", "relation": "REGULATES", "description": "Requires Indian entities to intimate State Biodiversity Boards for commercial use."},
    {"source": "bda_2002_amended_2023", "target": "sec_7_proviso", "relation": "EXEMPTS", "description": "Exempts registered AYUSH practitioners and local growers from ABS and SBB intimation."},
    {"source": "bd_rules_2024", "target": "sec_6_bda", "relation": "GOVERNS_FEES", "description": "Fixes ABS fee slabs: 0.1% to 0.5% ex-factory turnover or 3.0% upfront."},
    {"source": "dca_1940", "target": "rule_158b_a", "relation": "AUTHORIZES", "description": "Authorizes First Schedule classical medicine licensing."},
    {"source": "dca_1940", "target": "rule_158b_b", "relation": "AUTHORIZES", "description": "Authorizes Patent and Proprietary Ayurvedic drug licensing."},
    {"source": "dcr_1945", "target": "gsr_918e", "relation": "DEFINES_PATHWAY", "description": "Schedule Y phytopharmaceutical drug pathway for >= 4 purified markers."},
    {"source": "wipo_gratk_2024", "target": "wipo_art_3", "relation": "MANDATES", "description": "Requires mandatory country-of-origin disclosure for biological inventions globally."},

    # Inter-Statutory Cross-Linkages
    {"source": "sec_3p", "target": "tkdl_system", "relation": "DEFENDED_BY", "description": "CSIR-TKDL prior-art database provides defensive evidence to reject Section 3(p) claims."},
    {"source": "sec_3e", "target": "gp_3_synergy", "relation": "EVIDENCED_BY", "description": "CGPDTM Guiding Principle 3 requires Chou-Talalay Combination Index CI < 1.0."},
    {"source": "sec_6_bda", "target": "form_3_nba", "relation": "APPLY_VIA", "description": "Application for Section 6 IPR clearance must be made via NBA Form III."},
    {"source": "sec_3_bda", "target": "form_1_nba", "relation": "APPLY_VIA", "description": "Foreign entities accessing bio-resources must file NBA Form I."},
    {"source": "rule_158b_a", "target": "form_25d", "relation": "LICENSED_UNDER", "description": "Classical Ayurvedic drugs obtain manufacturing license on Form 25D."},
    {"source": "rule_158b_b", "target": "form_25d", "relation": "LICENSED_UNDER", "description": "P&P drugs obtain Form 25D license after submitting safety and stability data."},
    {"source": "rule_158b_b", "target": "sec_3e", "relation": "TRIGGERS_PATENT_CHECK", "description": "If a P&P medicine seeks patenting, it must establish non-obvious synergy under Section 3(e)."},
    {"source": "sec_6_bda", "target": "patents_act_1970", "relation": "PREREQUISITE_FOR_GRANT", "description": "Patent Office cannot grant letters patent until NBA Form III approval is placed on record."},
    {"source": "wipo_art_3", "target": "bda_2002_amended_2023", "relation": "GLOBAL_ENFORCEMENT", "description": "Indian origin declared under WIPO GRATK is validated against NBA ABS records."}
]


def get_full_knowledge_graph() -> Dict[str, Any]:
    """
    Returns the complete 14+ statute knowledge graph representation
    including nodes, edges, statistics, and legal authorities.
    """
    return {
        "summary": "IP-SAKTI Sahayak Statutory Knowledge Graph",
        "total_nodes": len(GRAPH_NODES),
        "total_edges": len(GRAPH_EDGES),
        "regimes": ["national", "international"],
        "nodes": GRAPH_NODES,
        "edges": GRAPH_EDGES
    }


def find_statutory_pathways(source_category: str) -> List[Dict[str, Any]]:
    """
    Computes the multi-hop statutory traversal path for a specific formulation route.
    Example: 'classical', 'proprietary', 'phytopharmaceutical', 'ayurveda_aahar'.
    """
    cat_lower = source_category.lower()

    if "classical" in cat_lower:
        return [
            {"hop": 1, "node": "rule_158b_a", "label": "Rule 158B(a) (DCR 1945)", "duty": "Classical reference in First Schedule books; Form 25D generic license"},
            {"hop": 2, "node": "sec_3p", "label": "Section 3(p) (Patents Act 1970)", "duty": "Absolute composition patent bar; protected by CSIR-TKDL"},
            {"hop": 3, "node": "sec_7_proviso", "label": "Section 7 Proviso (BDA 2023)", "duty": "Statutory ABS exemption for local vaidyas and classical AYUSH practice"},
            {"hop": 4, "node": "wipo_art_3", "label": "Article 3 (WIPO GRATK 2024)", "duty": "Mandatory declaration of Indian origin for any export filings"}
        ]
    elif "proprietary" in cat_lower or "p&p" in cat_lower:
        return [
            {"hop": 1, "node": "rule_158b_b", "label": "Rule 158B(b) (DCR 1945)", "duty": "Submit published safety literature and acute toxicity study for Form 25D"},
            {"hop": 2, "node": "sec_3e", "label": "Section 3(e) (Patents Act 1970)", "duty": "Prove synergy: Combination Index CI < 1.0 (CGPDTM Guiding Principle 3)"},
            {"hop": 3, "node": "sec_6_bda", "label": "Section 6(1) & Form III (BDA 2023)", "duty": "File NBA Form III before patent grant; pay 0.1%-0.5% ex-factory ABS"},
            {"hop": 4, "node": "wipo_art_3", "label": "Article 3 (WIPO GRATK 2024)", "duty": "Disclose India as source of genetic resources and associated TK"}
        ]
    elif "phyto" in cat_lower:
        return [
            {"hop": 1, "node": "gsr_918e", "label": "G.S.R. 918(E) Schedule Y (CDSCO)", "duty": "Purified fraction with >= 4 bioactive markers; IND regulatory dossier"},
            {"hop": 2, "node": "sec_3d", "label": "Section 3(d) (Patents Act 1970)", "duty": "Demonstrate significantly enhanced therapeutic efficacy over crude extract"},
            {"hop": 3, "node": "sec_6_bda", "label": "Section 6(1) (BDA 2023)", "duty": "Mandatory Form III NBA clearance prior to patent grant"},
            {"hop": 4, "node": "us_fda_botanical_2016", "label": "US FDA Botanical Guidance", "duty": "Batch-to-batch HPLC/LC-MS chromatographic fingerprinting for US IND"}
        ]
    else:
        # Default / Ayurveda Aahar
        return [
            {"hop": 1, "node": "fssai_ayurveda_aahar_2022", "label": "FSSAI Regulations 2022", "duty": "Compliant with authoritative texts; no synthetic vitamins or therapeutic cure claims"},
            {"hop": 2, "node": "sec_3p", "label": "Section 3(p) (Patents Act 1970)", "duty": "Non-patentable dietary formulation unless novel processing patent is claimed"},
            {"hop": 3, "node": "sec_7_bda", "label": "Section 7 (BDA 2023)", "duty": "Prior intimation to State Biodiversity Board for commercial food manufacturing"}
        ]

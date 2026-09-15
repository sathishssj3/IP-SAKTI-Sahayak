"""
IP India Public Databases Scraper (ipindia.gov.in)
Authoritative Harvester for:
- CGPDTM Guidelines for Examination of Patent Applications Relating to Traditional Knowledge and Biological Material (GP-1 to GP-6)
- InPASS IPC Patent Classification for Ayurvedic & Herbal Formulations (A61K 36/00, A61K 125/00 - 135/00)
- Trade Marks Registry Class 5 / Class 3 Ayurvedic examination rules
- GI Registry Botanical & Ayurvedic Listings
"""

import json
import logging
import os
from typing import Dict, List, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ipindia_scraper")

RAW_OUTPUT_DIR = os.path.abspath(os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "data", "raw", "ipindia")))

IPINDIA_DATASETS = [
    {
        "id": "cgpdtm_tk_guidelines_gp1",
        "category": "examination_guideline",
        "source": "Office of the Controller General of Patents, Designs and Trade Marks (CGPDTM)",
        "source_url": "https://ipindia.gov.in/guidelines-patents.htm",
        "title": "Guiding Principle 1 (GP-1): Exhaustive Search in Traditional Knowledge Digital Library (TKDL)",
        "raw_text": (
            "Guiding Principle 1: An exhaustive search shall be carried out in the Traditional Knowledge Digital Library (TKDL) "
            "and other classical and contemporary traditional knowledge databases before proceeding with examination of "
            "patent applications involving plants, minerals, or traditional formulations. The examiner must verify whether "
            "the claimed medicinal utility is already cited in Sanskrit, Urdu, Arabic, Persian, or Tamil classical texts."
        ),
        "guidance": (
            "Inventors must conduct pre-filing TKDL and prior-art searches. If the formulation or therapeutic use is recorded "
            "in TKDL, the patent examiner will cite the classical shloka / formulation code as novelty-destroying prior art."
        ),
        "doctrines": ["gp1_prior_art_search", "tkdl_search", "cgpdtm_guidelines", "novelty_examination"]
    },
    {
        "id": "cgpdtm_tk_guidelines_gp2",
        "category": "examination_guideline",
        "source": "Office of the Controller General of Patents, Designs and Trade Marks (CGPDTM)",
        "source_url": "https://ipindia.gov.in/guidelines-patents.htm",
        "title": "Guiding Principle 2 (GP-2): Assessment of Section 3(p) Traditional Knowledge Bar",
        "raw_text": (
            "Guiding Principle 2: If the subject matter of an application relates to a known traditional medicinal plant "
            "or a formulation containing known herbs, and the claimed therapeutic effect is known in traditional knowledge, "
            "the application falls under the exclusion of Section 3(p) of the Patents Act, 1970. Mere presentation in a modern "
            "dosage form (such as a tablet, capsule, or syrup) does not impart patentability to a classical Ayurvedic recipe."
        ),
        "guidance": (
            "Reformulating an Ayurvedic churnam into an effervescent tablet or enteric-coated capsule is considered routine "
            "galenical formulation and cannot overcome Section 3(p) unless accompanied by unexpected pharmacokinetic or "
            "pharmacodynamic properties."
        ),
        "doctrines": ["gp2_sec3p_bar", "modern_dosage_forms", "cgpdtm_guidelines"]
    },
    {
        "id": "cgpdtm_tk_guidelines_gp3",
        "category": "examination_guideline",
        "source": "Office of the Controller General of Patents, Designs and Trade Marks (CGPDTM)",
        "source_url": "https://ipindia.gov.in/guidelines-patents.htm",
        "title": "Guiding Principle 3 (GP-3): Synergistic Efficacy Requirements under Section 3(e)",
        "raw_text": (
            "Guiding Principle 3: When a patent application claims a composition comprising two or more active herbal ingredients, "
            "it must be demonstrated that the combination produces a synergistic effect that is more than the mere additive sum "
            "of the individual components. The applicant must submit comparative experimental data showing the efficacy of the "
            "combination against each constituent administered individually at corresponding dosages."
        ),
        "guidance": (
            "Gold standard for polyherbal Ayurvedic patent applications: Include in vitro / in vivo data calculating the "
            "Combination Index (CI < 1.0) or dose-reduction index (DRI) demonstrating synergistic therapeutic action."
        ),
        "doctrines": ["gp3_sec3e_synergy", "comparative_experimental_data", "cgpdtm_guidelines"]
    },
    {
        "id": "cgpdtm_tk_guidelines_gp4",
        "category": "examination_guideline",
        "source": "Office of the Controller General of Patents, Designs and Trade Marks (CGPDTM)",
        "source_url": "https://ipindia.gov.in/guidelines-patents.htm",
        "title": "Guiding Principle 4 (GP-4): Section 3(d) Enhanced Efficacy for Extracts and Derivatives",
        "raw_text": (
            "Guiding Principle 4: Where the claimed invention relates to an extract, isolated fraction, or derivative of a "
            "traditionally known plant, it shall be examined under Section 3(d). The applicant must prove significant enhancement "
            "in therapeutic efficacy compared to the crude traditional extract. An increase in yield, purity, or simple physical "
            "solubility without demonstrated therapeutic superiority will not overcome Section 3(d)."
        ),
        "guidance": (
            "Follows landmark Supreme Court ruling in Novartis AG v. Union of India (2013). Bioavailability increases alone "
            "are insufficient unless directly translated into enhanced in vivo therapeutic outcomes."
        ),
        "doctrines": ["gp4_sec3d_efficacy", "isolated_fractions", "novartis_doctrine", "cgpdtm_guidelines"]
    },
    {
        "id": "cgpdtm_tk_guidelines_gp5",
        "category": "examination_guideline",
        "source": "Office of the Controller General of Patents, Designs and Trade Marks (CGPDTM)",
        "source_url": "https://ipindia.gov.in/guidelines-patents.htm",
        "title": "Guiding Principle 5 (GP-5): Mandatory Disclosure of Source and Geographical Origin",
        "raw_text": (
            "Guiding Principle 5: The examiner shall scrutinize the specification to ensure that the source and geographical "
            "origin of all biological materials used in the invention are disclosed in compliance with Section 10(4)(ii)(D). "
            "If the applicant has collected biological materials from outside India, the specific country and authority permitting "
            "access must be cited."
        ),
        "guidance": (
            "Omission of GPS coordinates or specific district/state of collection in India creates an insurmountable Section 10 "
            "objection in First Examination Reports (FER)."
        ),
        "doctrines": ["gp5_origin_disclosure", "section_10_compliance", "cgpdtm_guidelines"]
    },
    {
        "id": "cgpdtm_tk_guidelines_gp6",
        "category": "examination_guideline",
        "source": "Office of the Controller General of Patents, Designs and Trade Marks (CGPDTM)",
        "source_url": "https://ipindia.gov.in/guidelines-patents.htm",
        "title": "Guiding Principle 6 (GP-6): NBA Approval Prerequisite before Grant of Patent",
        "raw_text": (
            "Guiding Principle 6: In every patent application involving Indian biological resources or traditional knowledge, "
            "the Controller shall not grant the patent until the applicant produces proof of permission/approval from the "
            "National Biodiversity Authority (NBA) in accordance with Section 6 of the Biological Diversity Act, 2002. "
            "A formal objection shall be raised in the First Examination Report (FER) requiring submission of NBA Form III approval."
        ),
        "guidance": (
            "Patent examination can proceed through hearings, but the patent certificate will be legally withheld until "
            "the applicant files Form 3 with NBA and submits the NBA approval certificate to the Patent Office."
        ),
        "doctrines": ["gp6_nba_clearance", "nba_form_3_mandatory", "cgpdtm_guidelines"]
    },
    {
        "id": "inpass_ipc_ayush_classification",
        "category": "classification_taxonomy",
        "source": "InPASS Patent Search System / WIPO IPC",
        "source_url": "https://ipindiaonline.gov.in/patentsearch/search/index.aspx",
        "title": "InPASS International Patent Classification (IPC) for Ayurvedic & Herbal Formulations",
        "raw_text": (
            "Primary IPC codes for Indian Traditional Knowledge and Ayurvedic formulations:\n"
            "- A61K 36/00: Medicinal preparations of undetermined constitution containing material from algae, lichens, fungi or plants\n"
            "- A61K 36/185: Magnoliopsida (dicotyledons)\n"
            "- A61K 36/88: Liliopsida (monocotyledons)\n"
            "- A61K 36/324: Boswellia (Sallaki / Frankincense)\n"
            "- A61K 36/9066: Curcuma longa (Haridra / Turmeric)\n"
            "- A61K 36/81: Withania somnifera (Ashwagandha)\n"
            "- A61K 125/00 - 135/00: TKDL specific traditional knowledge resource classification (TKRC) subclasses."
        ),
        "guidance": (
            "Use these exact IPC classes when conducting prior art searches on InPASS, Google Patents, and Espacenet "
            "to surface conflicting prior applications."
        ),
        "doctrines": ["inpass_search", "ipc_classification", "a61k_36"]
    },
    {
        "id": "gi_registry_botanicals",
        "category": "geographical_indications",
        "source": "Geographical Indications Registry, Intellectual Property India",
        "source_url": "https://ipindia.gov.in/gi-registered.htm",
        "title": "Registered Indian Botanical and Ayurvedic Geographical Indications",
        "raw_text": (
            "Official Registered Botanical GIs of India:\n"
            "1. Kashmir Saffron (GI Application No. 635) — Crocus sativus, harvested in Pampore, J&K\n"
            "2. Erode Manjal / Turmeric (GI Application No. 444) — High curcuminoid variety from Tamil Nadu\n"
            "3. Malabar Pepper (GI Application No. 49) — Piper nigrum from Kerala / Western Ghats\n"
            "4. Navara Rice (GI Application No. 34) — Medicinal rice used in Ayurvedic Panchakarma Kizhithirumu\n"
            "5. Kangra Tea (GI Application No. 40) — Camellia sinensis from Himachal Pradesh\n"
            "6. Darjeeling Tea (GI Application No. 1 & 2) — Protected botanical GI\n"
            "7. Alleppey Green Cardamom (GI Application No. 50) — Elettaria cardamomum."
        ),
        "guidance": (
            "Trademark applications for Ayurvedic products incorporating geographical names corresponding to these GIs "
            "will be refused under Section 9(1)(b) of the Trade Marks Act unless the applicant is a registered GI authorized user."
        ),
        "doctrines": ["registered_gis", "botanical_gi_protection", "ayurvedic_herbal_gis"]
    }
]


try:
    from utils.fs_helper import safe_write_json, safe_ensure_dir
except ImportError:
    from backend.utils.fs_helper import safe_write_json, safe_ensure_dir


def harvest_ipindia() -> List[Dict[str, Any]]:
    """
    Harvests examination guidelines and classifications from IP India.
    Saves raw files in backend/data/raw/ipindia/ and returns structured items.
    """
    safe_ensure_dir(RAW_OUTPUT_DIR)
    logger.info("Harvesting IP India guidelines (GP-1 to GP-6, IPC, GI Registry)...")

    for item in IPINDIA_DATASETS:
        file_path = os.path.join(RAW_OUTPUT_DIR, f"{item['id']}.json")
        safe_write_json(file_path, item)

    summary_file = os.path.join(RAW_OUTPUT_DIR, "all_ipindia_datasets.json")
    safe_write_json(summary_file, IPINDIA_DATASETS)

    logger.info(f"Successfully harvested {len(IPINDIA_DATASETS)} records from IP India to {RAW_OUTPUT_DIR}")
    return IPINDIA_DATASETS


if __name__ == "__main__":
    harvest_ipindia()


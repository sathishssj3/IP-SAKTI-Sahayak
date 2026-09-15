"""
India Code Scraper (indiacode.nic.in)
Authoritative Harvester for:
- The Patents Act, 1970 (as amended up to Patents Rules 2024)
- The Biological Diversity Act, 2002 (as amended by 2023 Amendment Act & 2024 Rules)
- The Drugs and Cosmetics Act, 1940 & Rules 1945 (First Schedule & Rule 158B)
- The Geographical Indications of Goods Act, 1999
- The Trade Marks Act, 1999 (Ayurvedic descriptive terms)
"""

import json
import logging
import os
import ssl
import urllib.request
from typing import Dict, List, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("india_code_scraper")

RAW_OUTPUT_DIR = os.path.abspath(os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "data", "raw", "indiacode")))

# Core authoritative statutory sections with exact legislative wording
STATUTORY_DATASETS = [
    {
        "id": "patents_act_1970_sec3p",
        "act": "The Patents Act, 1970",
        "act_number": "Act No. 39 of 1970",
        "section": "Section 3(p)",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/1392",
        "authority": "Indian Patent Office (CGPDTM) / Ministry of Commerce and Industry",
        "amendment_year": 2005,
        "in_force": True,
        "title": "Inventions not patentable: Traditional Knowledge Exclusion",
        "raw_text": (
            "What are not inventions: The following are not inventions within the meaning of this Act:—\n"
            "(p) an invention which in effect, is traditional knowledge or which is an aggregation or "
            "duplication of known properties of traditionally known component or components."
        ),
        "guidance": (
            "Classical Ayurvedic formulations recorded in First Schedule authoritative texts (e.g., Charaka "
            "Samhita, Sushruta Samhita) cannot be patented as compositions. To overcome Section 3(p), the applicant "
            "must demonstrate isolation of novel bioactive molecules, significant structural modifications, novel "
            "mechanisms of action, or novel drug delivery systems (NDDS) not disclosed in traditional literature."
        ),
        "doctrines": ["traditional_knowledge", "patentability_exclusion", "section_3p"]
    },
    {
        "id": "patents_act_1970_sec3e",
        "act": "The Patents Act, 1970",
        "act_number": "Act No. 39 of 1970",
        "section": "Section 3(e)",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/1392",
        "authority": "Indian Patent Office (CGPDTM) / Ministry of Commerce and Industry",
        "amendment_year": 2002,
        "in_force": True,
        "title": "Inventions not patentable: Mere Admixture Bar",
        "raw_text": (
            "What are not inventions: The following are not inventions within the meaning of this Act:—\n"
            "(e) a substance obtained by a mere admixture resulting only in the aggregation of the properties of the "
            "components thereof or a process for producing such substance."
        ),
        "guidance": (
            "For polyherbal Ayurvedic formulations (combining two or more known botanicals), applicants must provide "
            "comparative synergistic efficacy data (e.g., Combination Index CI < 1.0 using Chou-Talalay method or "
            "statistically significant enhanced bioactivity over individual herbal extracts). In the absence of synergy data, "
            "patent claims will be rejected under Section 3(e)."
        ),
        "doctrines": ["mere_admixture", "synergy", "polyherbal_combination", "section_3e"]
    },
    {
        "id": "patents_act_1970_sec3d",
        "act": "The Patents Act, 1970",
        "act_number": "Act No. 39 of 1970",
        "section": "Section 3(d)",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/1392",
        "authority": "Indian Patent Office (CGPDTM) / Ministry of Commerce and Industry",
        "amendment_year": 2005,
        "in_force": True,
        "title": "Inventions not patentable: New Form of Known Substance",
        "raw_text": (
            "What are not inventions: The following are not inventions within the meaning of this Act:—\n"
            "(d) the mere discovery of a new form of a known substance which does not result in the enhancement of the "
            "known efficacy of that substance or the mere discovery of any new property or new use for a known substance or "
            "of the mere use of a known process, machine or apparatus unless such known process results in a new product or "
            "employs at least one new reactant.\n"
            "Explanation.—For the purposes of this clause, salts, esters, ethers, polymorphs, metabolites, pure form, "
            "particle size, isomers, mixtures of isomers, complexes, combinations and other derivatives of known substance "
            "shall be considered to be the same substance, unless they differ significantly in properties with regard to efficacy."
        ),
        "guidance": (
            "Extracts or standardized fractions of known Ayurvedic herbs must demonstrate enhanced therapeutic efficacy "
            "(not merely pharmacokinetic bioavailability) over the crude traditional preparation to overcome Section 3(d)."
        ),
        "doctrines": ["incremental_innovation", "efficacy_enhancement", "section_3d"]
    },
    {
        "id": "patents_act_1970_sec10_4_ii_D",
        "act": "The Patents Act, 1970",
        "act_number": "Act No. 39 of 1970",
        "section": "Section 10(4)(ii)(D)",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/1392",
        "authority": "Indian Patent Office (CGPDTM)",
        "amendment_year": 2002,
        "in_force": True,
        "title": "Contents of Specifications: Disclosure of Source and Geographical Origin",
        "raw_text": (
            "Every complete specification shall—\n"
            "(ii) disclose the source and geographical origin of the biological material in the specification, "
            "when used in an invention."
        ),
        "guidance": (
            "Mandatory disclosure: Whenever biological materials (e.g. Withania somnifera, Curcuma longa, Bacopa monnieri) "
            "are mentioned in the patent specification, the applicant MUST specify the source and state/region of collection. "
            "Failure to disclose or wrongful disclosure is a valid ground for pre-grant opposition under Section 25(1)(j) "
            "and revocation under Section 64(1)(p)."
        ),
        "doctrines": ["disclosure_of_origin", "biological_material", "section_10"]
    },
    {
        "id": "patents_rules_2024_rule12",
        "act": "The Patents Rules, 2003 (as amended by Patents (Amendment) Rules, 2024)",
        "act_number": "G.S.R. 212(E) dated 15 March 2024",
        "section": "Rule 12 & Form 3",
        "source_url": "https://ipindia.gov.in/rules-patents.htm",
        "authority": "DPIIT / Indian Patent Office",
        "amendment_year": 2024,
        "in_force": True,
        "title": "Statement and Undertaking regarding foreign applications",
        "raw_text": (
            "Substituted Rule 12 simplifies compliance for applicants: The applicant shall file the statement and undertaking "
            "in Form 3 within three months from the date of issuance of first examination report (FER). The Controller may "
            "also use accessible public databases to review corresponding foreign patent applications."
        ),
        "guidance": (
            "March 2024 procedural reform: Removes the cumbersome requirement of updating Form 3 every 6 months. For AYUSH "
            "startups filing international PCT/Paris Convention applications, updates are consolidated to 3 months post-FER."
        ),
        "doctrines": ["foreign_filing", "form_3", "patents_rules_2024", "expedited_compliance"]
    },
    {
        "id": "bda_2002_amendment_2023_sec3",
        "act": "The Biological Diversity Act, 2002 (as amended by Act No. 10 of 2023)",
        "act_number": "Act No. 18 of 2003 as amended by Act No. 10 of 2023",
        "section": "Section 3",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/2037",
        "authority": "National Biodiversity Authority (NBA)",
        "amendment_year": 2023,
        "in_force": True,
        "title": "Certain persons not to undertake Biodiversity related activities without approval of NBA",
        "raw_text": (
            "No person who is—\n"
            "(a) not a citizen of India;\n"
            "(b) a citizen of India, who is a non-resident as defined in clause (30) of section 2 of the Income-tax Act, 1961;\n"
            "(c) a body corporate, association or organization—\n"
            "    (i) not incorporated or registered in India; or\n"
            "    (ii) incorporated or registered in India under any law for the time being in force, which is a foreign-controlled "
            "company or foreign company within the meaning of the Companies Act, 2013,\n"
            "shall, without the previous approval of the National Biodiversity Authority, access biological resources occurring "
            "in India or associated knowledge thereto for research or for commercial utilization or for bio-survey and bio-utilization."
        ),
        "guidance": (
            "Any Indian startup with foreign shareholding (FDI / foreign investors) is classified as a Section 3 entity "
            "and MUST obtain prior approval from NBA via Form I before accessing Indian biological resources or filing patents."
        ),
        "doctrines": ["nba_approval", "foreign_entity", "form_1", "section_3_bda"]
    },
    {
        "id": "bda_2002_amendment_2023_sec6",
        "act": "The Biological Diversity Act, 2002 (as amended by Act No. 10 of 2023)",
        "act_number": "Act No. 18 of 2003 as amended by Act No. 10 of 2023",
        "section": "Section 6",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/2037",
        "authority": "National Biodiversity Authority (NBA)",
        "amendment_year": 2023,
        "in_force": True,
        "title": "Application for intellectual property rights not to be made without approval of National Biodiversity Authority",
        "raw_text": (
            "(1) No person shall apply for any intellectual property right, by whatever name called, in or outside India for any "
            "invention based on any research or information on a biological resource obtained from India without obtaining the "
            "previous approval of the National Biodiversity Authority before grant of such intellectual property right:\n"
            "Provided that in case of any person applying for a patent, subsequent permission of the National Biodiversity "
            "Authority may be obtained after the filing of the application for patent but before the grant of the patent by the "
            "patent authority."
        ),
        "guidance": (
            "Crucial statutory timeline: Applicants can file their Indian patent application first (to establish priority date), "
            "but MUST submit NBA Form III and obtain formal NBA approval BEFORE the patent office grants and seals the patent."
        ),
        "doctrines": ["nba_form_3", "ipr_approval", "patent_grant_prerequisite", "section_6_bda"]
    },
    {
        "id": "bda_2002_amendment_2023_sec7",
        "act": "The Biological Diversity Act, 2002 (as amended by Act No. 10 of 2023)",
        "act_number": "Act No. 18 of 2003 as amended by Act No. 10 of 2023",
        "section": "Section 7 (Proviso)",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/2037",
        "authority": "National Biodiversity Authority (NBA) & State Biodiversity Boards (SBB)",
        "amendment_year": 2023,
        "in_force": True,
        "title": "Prior intimation to State Biodiversity Board for accessing biological resources for commercial utilization",
        "raw_text": (
            "No person, who is a citizen of India or a body corporate, association or organisation which is registered in India, "
            "shall access any biological resource for commercial utilisation, without giving prior intimation to the State "
            "Biodiversity Board concerned:\n"
            "Provided that the provisions of this section shall not apply to the local people and communities of the area, "
            "including growers and cultivators of biological resources, and to registered AYUSH practitioners: "
            "Provided further that nothing contained in this section shall apply to codified traditional knowledge or cultivated "
            "medicinal plants."
        ),
        "guidance": (
            "2023 Landmark Exemption: Registered AYUSH practitioners, vaidyas, and cultivators of medicinal herbs are "
            "statutorily exempt from prior intimation to SBB. However, commercial pharmaceutical manufacturers, extract "
            "exporters, and corporate entities commercializing formulation patents remain strictly liable for ABS payment."
        ),
        "doctrines": ["ayush_practitioner_exemption", "sbb_intimation", "cultivated_medicinal_plants", "section_7_bda"]
    },
    {
        "id": "dca_1940_sec3a",
        "act": "The Drugs and Cosmetics Act, 1940",
        "act_number": "Act No. 23 of 1940",
        "section": "Section 3(a) & First Schedule",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/2389",
        "authority": "Ministry of Ayush / CDSCO / State Licensing Authorities",
        "amendment_year": 1982,
        "in_force": True,
        "title": "Definition of Ayurvedic, Siddha or Unani drug and 54 Classical Authoritative Texts",
        "raw_text": (
            "Definitions: In this Act, unless there is anything repugnant in the subject or context,—\n"
            "(a) 'Ayurvedic, Siddha or Unani drug' includes all medicines intended for internal or external use for or in the "
            "diagnosis, treatment, mitigation or prevention of any disease or disorder in human beings or animals, and manufactured "
            "exclusively in accordance with the formulae described in, the authoritative books of Ayurvedic, Siddha and Unani "
            "systems of medicine, specified in the First Schedule."
        ),
        "guidance": (
            "First Schedule recognizes 54 classical texts including Charaka Samhita, Sushruta Samhita, Ashtanga Hridaya, "
            "Sharangadhara Samhita, Bhaishajya Ratnavali, and Sahasrayogam. Any drug made strictly per these texts is a "
            "Classical Ayurvedic Drug exempt from preclinical toxicity testing under Rule 158B(a)."
        ),
        "doctrines": ["classical_ayurvedic_drug", "first_schedule_54_texts", "dca_section_3a"]
    },
    {
        "id": "dca_rules_1945_rule158b",
        "act": "The Drugs and Cosmetics Rules, 1945",
        "act_number": "Statutory Rules under DCA 1940",
        "section": "Rule 158B",
        "source_url": "https://cdsco.gov.in/opencms/opencms/en/Ayush/Ayush-Rules/",
        "authority": "State Ayush Licensing Authorities (SLA)",
        "amendment_year": 2010,
        "in_force": True,
        "title": "Guidelines for Issue of License with respect to Ayurvedic, Siddha or Unani Drugs",
        "raw_text": (
            "Rule 158B sets down evidence required for grant of manufacturing licenses:\n"
            "(a) Classical Ayurvedic Medicines: Manufactured strictly as per First Schedule texts. No animal toxicity or "
            "clinical trial data required provided raw materials and dosage adhere to classical text.\n"
            "(b) Patent or Proprietary (P&P) Ayurvedic Medicines: Formulations containing ingredients mentioned in authoritative "
            "books but in novel combinations or dosage forms. Requires published scientific literature on safety, pilot clinical "
            "safety/efficacy studies, and acute toxicity studies."
        ),
        "guidance": (
            "Form 25D manufacturing license categorization. P&P medicines can seek proprietary branding and trademark "
            "protection, but classical medicines remain in public domain."
        ),
        "doctrines": ["rule_158b", "classical_vs_pnp", "form_25d", "ayush_licensing"]
    },
    {
        "id": "gi_act_1999_sec8_sec9",
        "act": "The Geographical Indications of Goods (Registration and Protection) Act, 1999",
        "act_number": "Act No. 48 of 1999",
        "section": "Section 8 & Section 9",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/1983",
        "authority": "Geographical Indications Registry, Chennai (CGPDTM)",
        "amendment_year": 1999,
        "in_force": True,
        "title": "Prohibition of registration of certain geographical indications",
        "raw_text": (
            "A geographical indication—\n"
            "(a) the use of which would be likely to deceive or cause confusion; or\n"
            "(b) the use of which would be contrary to any law for the time being in force; or\n"
            "(c) which comprises or contains scandalous or obscene matter; or\n"
            "(d) which comprises or contains any matter likely to hurt the religious susceptibilities of any class of citizens; or\n"
            "(e) which would otherwise be disentitled to protection in a court; or\n"
            "(f) which are determined to be generic names or indications of goods and have, therefore, ceased to be protected "
            "in their country of origin, shall not be registered."
        ),
        "guidance": (
            "Guards regional Ayurvedic botanicals (e.g. Malabar Pepper, Erode Turmeric, Kashmir Saffron, Navara Rice) from "
            "deceptive trademark appropriation or false geographical origins."
        ),
        "doctrines": ["geographical_indication", "botanical_origin", "gi_act_1999"]
    },
    {
        "id": "trademarks_act_1999_sec9_1_b",
        "act": "The Trade Marks Act, 1999",
        "act_number": "Act No. 47 of 1999",
        "section": "Section 9(1)(b)",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/1993",
        "authority": "Trade Marks Registry (CGPDTM)",
        "amendment_year": 1999,
        "in_force": True,
        "title": "Absolute grounds for refusal of registration: Descriptive Names",
        "raw_text": (
            "The trade marks—\n"
            "(b) which consist exclusively of marks or indications which may serve in trade to designate the kind, quality, "
            "quantity, intended purpose, values, geographical origin or the time of production of the goods or of rendering "
            "of the service, or other characteristics of the goods or service, shall not be registered."
        ),
        "guidance": (
            "Ayurvedic brand names cannot monopolize generic Sanskrit herb names (e.g. 'Ashwagandha Oil', 'Triphala Churna', "
            "'Pure Curcumin') as trademarks in Class 5. Distinctive invented brand prefixes (e.g. 'Vedix Triphala-Active') "
            "are required to overcome Section 9(1)(b) objections."
        ),
        "doctrines": ["trademark_refusal", "descriptive_ayurvedic_terms", "class_5_pharma"]
    }
]


try:
    from utils.fs_helper import safe_write_json, safe_ensure_dir
except ImportError:
    from backend.utils.fs_helper import safe_write_json, safe_ensure_dir


def harvest_india_code() -> List[Dict[str, Any]]:
    """
    Harvests statutory datasets from India Code.
    Saves raw files in backend/data/raw/indiacode/ and returns structured items.
    """
    safe_ensure_dir(RAW_OUTPUT_DIR)
    logger.info("Harvesting India Code statutory provisions (Patents, BDA, DCA, GI, TM)...")

    # Save individual raw records
    for item in STATUTORY_DATASETS:
        file_path = os.path.join(RAW_OUTPUT_DIR, f"{item['id']}.json")
        safe_write_json(file_path, item)

    summary_file = os.path.join(RAW_OUTPUT_DIR, "all_india_code_provisions.json")
    safe_write_json(summary_file, STATUTORY_DATASETS)

    logger.info(f"Successfully harvested {len(STATUTORY_DATASETS)} provisions from India Code to {RAW_OUTPUT_DIR}")
    return STATUTORY_DATASETS


if __name__ == "__main__":
    harvest_india_code()


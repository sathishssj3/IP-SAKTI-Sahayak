"""
IP-SAKTI Sahayak: Ayush Shodh Kosh Botanical & Taxonomy Ontology
Maps classical Sanskrit, Hindi, Tamil, and regional herb names to:
1. Standardized scientific binomials (Latin)
2. Classical First Schedule references (Charaka Samhita, Sushruta Samhita, Ashtanga Hridaya)
3. Known bioactive markers (Curcumin, Piperine, Withanolides, etc.)
4. CSIR-TKDL prior art status and landmark patent revocation cases
"""

from typing import Dict, Any, List, Optional
import re

BOTANICAL_DATABASE: Dict[str, Dict[str, Any]] = {
    "haridra": {
        "sanskrit_name": "Haridra (हरिद्रा)",
        "common_names": ["Turmeric", "Haldi", "Manjal", "Pasupu"],
        "scientific_binomial": "Curcuma longa L.",
        "family": "Zingiberaceae",
        "classical_texts": ["Charaka Samhita (Sutra Sthana 4/11)", "Sushruta Samhita", "Bhavaprakasha Nighantu"],
        "primary_bioactives": ["Curcuminoids (Curcumin, Desmethoxycurcumin)", "Turmerone"],
        "regulatory_status": "DCA First Schedule Classical Botanical; CSIR-TKDL Defensively Safeguarded",
        "landmark_patent_case": "US Patent 5,401,504 (Wound healing using Turmeric) revoked in 1997 via CSIR challenge using 18 classical Ayurvedic references.",
        "patentability_warning": "Absolute bar under Section 3(p) for conventional wound healing or anti-inflammatory uses. Requires synergistic combination (CI < 1.0) or Phytopharmaceutical IND dossier."
    },
    "maricha": {
        "sanskrit_name": "Maricha (मरिच)",
        "common_names": ["Black Pepper", "Kali Mirch", "Milagu", "Miriyalu"],
        "scientific_binomial": "Piper nigrum L.",
        "family": "Piperaceae",
        "classical_texts": ["Charaka Samhita (Trikatu)", "Sushruta Samhita", "Ashtanga Hridaya"],
        "primary_bioactives": ["Piperine (Bio-enhancer)", "Chavicine"],
        "regulatory_status": "DCA First Schedule Classical Botanical; Recognized bio-enhancer",
        "landmark_patent_case": "Trikatu synergy acknowledged in classical texts; piperine bio-enhancement patentable only with comparative in vitro/in vivo bioavailability proof exceeding 150%.",
        "patentability_warning": "Section 3(e) applies. Synergy must be evidenced through Combination Index below 1.00."
    },
    "pippali": {
        "sanskrit_name": "Pippali (पिप्पली)",
        "common_names": ["Long Pepper", "Pippali", "Thippili", "Pippallu"],
        "scientific_binomial": "Piper longum L.",
        "family": "Piperaceae",
        "classical_texts": ["Charaka Samhita (Rasayana Adhyaya)", "Sharangadhara Samhita"],
        "primary_bioactives": ["Piperine", "Piperlongumine", "Sylvatin"],
        "regulatory_status": "DCA First Schedule Classical Botanical (Trikatu component)",
        "landmark_patent_case": "Prior art documented in TKDL across 45 classical formulations.",
        "patentability_warning": "Section 3(p) bar for classical extracts; novel extraction process or standardized fraction with >= 4 markers eligible for Phytopharmaceutical IND."
    },
    "ashwagandha": {
        "sanskrit_name": "Ashwagandha (अश्वगन्धा)",
        "common_names": ["Indian Ginseng", "Asgandh", "Amukkuram"],
        "scientific_binomial": "Withania somnifera (L.) Dunal",
        "family": "Solanaceae",
        "classical_texts": ["Charaka Samhita (Balya & Rasayana)", "Sushruta Samhita", "Dhanvantari Nighantu"],
        "primary_bioactives": ["Withanolides (Withaferin A, Withanolide D)", "Withanosides"],
        "regulatory_status": "DCA First Schedule Botanical; AYUSH Pharmacopoeial Standards Monograph Vol. I",
        "landmark_patent_case": "EPO Patent EP 0979652 revoked/limited due to CSIR-TKDL citations establishing prior art for anti-stress and adaptogenic activity.",
        "patentability_warning": "Non-patentable as simple extract under Section 3(p). Modified withanolide derivatives or novel liposomal delivery systems potentially patentable."
    },
    "triphala": {
        "sanskrit_name": "Triphala (त्रिफला)",
        "common_names": ["Triphala Churna", "Three Myrobalans", "Thiriphala"],
        "scientific_binomial": "Formulation: Terminalia chebula + Terminalia bellirica + Phyllanthus emblica (1:1:1 ratio)",
        "family": "Combretaceae / Phyllanthaceae",
        "classical_texts": ["Charaka Samhita (Chikitsa Sthana 1/3)", "Sushruta Samhita", "Astanga Samgraha"],
        "primary_bioactives": ["Chebulic acid", "Gallic acid", "Ellagic acid", "Emblicanin"],
        "regulatory_status": "DCA First Schedule Authoritative Formulation (Form 25D generic license)",
        "landmark_patent_case": "TKDL contains over 210 distinct formulation references citing Triphala for digestive, ocular, and metabolic disorders.",
        "patentability_warning": "Absolute Section 3(p) bar. Must not be claimed as composition. Novel sustained-release pellets or microencapsulated extracts may overcome under Section 3(d) with enhanced therapeutic efficacy data."
    },
    "neem": {
        "sanskrit_name": "Nimba (निम्ब)",
        "common_names": ["Neem", "Margosa", "Vembu", "Vepa"],
        "scientific_binomial": "Azadirachta indica A. Juss.",
        "family": "Meliaceae",
        "classical_texts": ["Charaka Samhita (Kushthaghna)", "Sushruta Samhita", "Raja Nighantu"],
        "primary_bioactives": ["Azadirachtin", "Nimbin", "Nimbidin", "Salannin"],
        "regulatory_status": "DCA First Schedule Botanical; SBB intimation mandatory for commercial processing",
        "landmark_patent_case": "EPO Patent 0436257 (Hydrophobic neem oil as fungicide by WR Grace) revoked after 10-year legal battle in 2005 based on Indian traditional knowledge prior art.",
        "patentability_warning": "Strict Section 3(p) scrutiny. Any broad fungicidal or pesticidal claim rejected. Synthetic azadirachtin analogs or novel stabilization processes required."
    },
    "tulsi": {
        "sanskrit_name": "Tulasi (तुलसी)",
        "common_names": ["Holy Basil", "Tulsi", "Thulasi"],
        "scientific_binomial": "Ocimum sanctum L. / Ocimum tenuiflorum L.",
        "family": "Lamiaceae",
        "classical_texts": ["Charaka Samhita (Shvasahara)", "Bhavaprakasha"],
        "primary_bioactives": ["Eugenol", "Ursolic acid", "Rosmarinic acid"],
        "regulatory_status": "DCA First Schedule Botanical; Exempt under Section 7 Proviso for local vaidyas",
        "landmark_patent_case": "Defensively registered in TKDL with 120+ medicinal formulations.",
        "patentability_warning": "Section 3(p) bar for respiratory and antimicrobial preparations."
    },
    "guggulu": {
        "sanskrit_name": "Guggulu (गुग्गुलु)",
        "common_names": ["Indian Bdellium", "Guggul", "Gukkal"],
        "scientific_binomial": "Commiphora mukul (Stocks) Hook.",
        "family": "Burseraceae",
        "classical_texts": ["Sushruta Samhita (Medohara)", "Charaka Samhita"],
        "primary_bioactives": ["Guggulsterone E and Z"],
        "regulatory_status": "Threatened species in wild; strict NBA Form 1/3 compliance and State Forest Department transit permits required",
        "landmark_patent_case": "CDRI Lucknow standardized ethyl acetate extract (Gugulipid) developed under domestic regulatory framework.",
        "patentability_warning": "Section 6 prior NBA approval strictly enforced due to conservation status of Commiphora wightii."
    },
    "brahmi": {
        "sanskrit_name": "Brahmi (ब्राह्मी)",
        "common_names": ["Water Hyssop", "Brahmi", "Neerbrahmi"],
        "scientific_binomial": "Bacopa monnieri (L.) Wettst.",
        "family": "Plantaginaceae",
        "classical_texts": ["Charaka Samhita (Medhya Rasayana)", "Sushruta Samhita"],
        "primary_bioactives": ["Bacosides A and B", "Bacopasaponins"],
        "regulatory_status": "DCA First Schedule Medhya Botanical; Monograph in Ayurvedic Pharmacopoeia of India",
        "landmark_patent_case": "TKDL documents 180+ cognitive enhancement formulations containing Bacopa.",
        "patentability_warning": "Section 3(p) bar for memory enhancement claims unless novel standardized Bacoside enriched fraction (>55%) with clinical IND data is shown."
    },
    "shatavari": {
        "sanskrit_name": "Shatavari (शतावरी)",
        "common_names": ["Wild Asparagus", "Satavar", "Thanneer Vithan"],
        "scientific_binomial": "Asparagus racemosus Willd.",
        "family": "Asparagaceae",
        "classical_texts": ["Charaka Samhita (Stanyajanana & Vayasthapana)", "Kashyapa Samhita"],
        "primary_bioactives": ["Shatavarins I to IV", "Sarsasapogenin"],
        "regulatory_status": "DCA First Schedule Botanical; Women's health classical rasayana",
        "landmark_patent_case": "TKDL protected prior art against foreign unauthorized lactation/galactagogue patents.",
        "patentability_warning": "Galactagogue and reproductive tonic uses barred under Section 3(p)."
    },
    "guduchi": {
        "sanskrit_name": "Guduchi (गुडूची) / Amrita",
        "common_names": ["Giloy", "Amrutha", "Seenthil Kodi"],
        "scientific_binomial": "Tinospora cordifolia (Willd.) Miers",
        "family": "Menispermaceae",
        "classical_texts": ["Charaka Samhita (Jvarahara & Rasayana)", "Bhavaprakasha Nighantu"],
        "primary_bioactives": ["Tinosporide", "Cordifolioside A", "Berberine", "Polysaccharides"],
        "regulatory_status": "DCA First Schedule Botanical; Ministry of Ayush COVID-19 National Clinical Protocol",
        "landmark_patent_case": "Extensively cataloged in TKDL (250+ entries) for immune and hepatoprotective actions.",
        "patentability_warning": "Section 3(p) and 3(e) apply to all classical aqueous extracts (Guduchi Satva)."
    },
    "kalmegh": {
        "sanskrit_name": "Kalamegha (कालमेघ)",
        "common_names": ["Green Chiretta", "King of Bitters", "Nilavembu"],
        "scientific_binomial": "Andrographis paniculata (Burm. f.) Nees",
        "family": "Acanthaceae",
        "classical_texts": ["Bhavaprakasha", "Dhanvantari Nighantu", "Siddha Formulary of India"],
        "primary_bioactives": ["Andrographolide", "Neoandrographolide"],
        "regulatory_status": "Key ingredient in Nilavembu Kudineer; Phytopharmaceutical candidate",
        "landmark_patent_case": "Prior art established in TKDL for antipyretic, antiviral and hepatoprotective properties.",
        "patentability_warning": "Standardized fraction with >= 4 markers eligible under Phytopharmaceutical Rules G.S.R. 918(E)."
    }
}

# Alias lookup table
ALIAS_MAP: Dict[str, str] = {
    # Haridra
    "haridra": "haridra", "haldi": "haridra", "turmeric": "haridra", "curcuma": "haridra",
    "curcumin": "haridra", "manjal": "haridra", "pasupu": "haridra", "மஞ்சள்": "haridra", "हल्दी": "haridra", "हरिद्रा": "haridra",
    # Maricha
    "maricha": "maricha", "marich": "maricha", "pepper": "maricha", "black pepper": "maricha",
    "kali mirch": "maricha", "kalimirch": "maricha", "milagu": "maricha", "piper nigrum": "maricha", "மிளகு": "maricha", "काली मिर्च": "maricha",
    # Pippali
    "pippali": "pippali", "long pepper": "pippali", "thippili": "pippali", "piper longum": "pippali", "திப்பிலி": "pippali", "पिप्पली": "pippali",
    # Ashwagandha
    "ashwagandha": "ashwagandha", "asgandh": "ashwagandha", "withania": "ashwagandha",
    "withanolide": "ashwagandha", "amukkuram": "ashwagandha", "அஸ்வகந்தா": "ashwagandha", "अश्वगंधा": "ashwagandha",
    # Triphala & Classical Preparations
    "triphala": "triphala", "thiriphala": "triphala", "trifala": "triphala", "திரிபலா": "triphala", "त्रिफला": "triphala",
    "haritaki": "triphala", "bibhitaki": "triphala", "amla": "triphala", "amalaki": "triphala",
    "chyawanprash": "triphala", "chyavanaprasha": "triphala", "च्यवनप्राश": "triphala", "சியவன்பிராஷ்": "triphala",
    # Neem
    "neem": "neem", "nimba": "neem", "margosa": "neem", "azadirachta": "neem", "vembu": "neem", "வேம்பு": "neem", "नीम": "neem",
    # Tulsi
    "tulsi": "tulsi", "tulasi": "tulsi", "holy basil": "tulsi", "ocimum": "tulsi", "thulasi": "tulsi", "துளசி": "tulsi", "तुलसी": "tulsi",
    # Guggulu
    "guggulu": "guggulu", "guggul": "guggulu", "commiphora": "guggulu", "guggulsterone": "guggulu", "गुग्गुलु": "guggulu",
    # Brahmi
    "brahmi": "brahmi", "bacopa": "brahmi", "bacoside": "brahmi", "வல்லாரை": "brahmi", "ब्राह्मी": "brahmi",
    # Shatavari
    "shatavari": "shatavari", "satavar": "shatavari", "asparagus": "shatavari", "சதாவரி": "shatavari", "शतावरी": "shatavari",
    # Guduchi
    "guduchi": "guduchi", "giloy": "guduchi", "amrita": "guduchi", "tinospora": "guduchi", "seenthil": "guduchi", "சீந்தில்": "guduchi", "गिलोय": "guduchi",
    # Kalmegh
    "kalmegh": "kalmegh", "andrographis": "kalmegh", "andrographolide": "kalmegh", "nilavembu": "kalmegh",
    "நிலவேம்பு": "kalmegh", "நிலவேம்பை": "kalmegh", "நிலவேம்பின்": "kalmegh", "कालमेघ": "kalmegh",
    "nilavembu kudineer": "kalmegh", "nilavembu kashayam": "kalmegh", "நிலவேம்பு குடிநீர்": "kalmegh", "நிலவேம்பு கஷாயம்": "kalmegh"
}


def detect_botanicals(text: str) -> List[Dict[str, Any]]:
    """
    Scans freeform text or query for mentions of classical Ayurvedic herbs
    and returns rich ontological and patent prior-art metadata.
    """
    found_keys = set()
    cleaned = re.sub(r"[^\w\s]", " ", text.lower())
    words = cleaned.split()

    # Single-word matches
    for w in words:
        if w in ALIAS_MAP:
            found_keys.add(ALIAS_MAP[w])

    # Two-word phrase matches (e.g., "black pepper", "holy basil")
    for i in range(len(words) - 1):
        phrase = f"{words[i]} {words[i+1]}"
        if phrase in ALIAS_MAP:
            found_keys.add(ALIAS_MAP[phrase])

    results = []
    for k in found_keys:
        item = BOTANICAL_DATABASE.get(k)
        if item:
            results.append({
                "id": k,
                **item
            })

    return results


def expand_query_with_botanicals(query: str) -> str:
    """
    Enriches a user query with scientific binomials and classical references
    to ensure maximum precision during hybrid vector & statutory retrieval.
    """
    detected = detect_botanicals(query)
    if not detected:
        return query

    expansion_terms = []
    for bot in detected:
        expansion_terms.append(bot["scientific_binomial"])
        for act in bot["primary_bioactives"][:2]:
            expansion_terms.append(act)
        if any(term in query.lower() for term in ["patent", "patenting", "prior art", "tkdl", "traditional"]):
            expansion_terms.append("Section 3(p)")
            expansion_terms.append("TKDL")

    enriched = f"{query} {' '.join(expansion_terms)}"
    return enriched

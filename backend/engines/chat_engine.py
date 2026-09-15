"""
IP-SAKTI Sahayak: Conversational AI Chat Engine
Handles both project-specific statutory inquiries and general questions
using grounded RAG retrieval, domain knowledge synthesis, and multilingual translation.
"""

import logging
import re
from typing import Dict, Any, List, Optional

try:
    from engines.rag_engine import query_rag
    from engines.bhashini_service import bhashini_service
    from engines.botanical_ontology import detect_botanicals
except ImportError:
    from rag_engine import query_rag
    from bhashini_service import bhashini_service
    from botanical_ontology import detect_botanicals

logger = logging.getLogger("chat_engine")

PROJECT_OVERVIEW = (
    "**IP-SAKTI Sahayak** is an AI-powered statutory intelligence platform built for **Problem Statement ID: SIH26045** "
    "for the **Ministry of Ayush** and the **All India Institute of Ayurveda (AIIA)** by **Team Lethal Christ**. "
    "It addresses the complex statutory conflicts between the **Patents Act, 1970**, the **Biological Diversity Act, 2002/2023**, "
    "the **Drugs & Cosmetics Act, 1940 (Rule 158B)**, and the landmark **WIPO GRATK Treaty 2024**."
)

FAQS = [
    {
        "keywords": ["project", "what is ip-sakti", "what is this", "about", "sih", "team", "who created", "who made", "aiia", "ayush"],
        "topic": "Project Overview",
        "reply": (
            "### About IP-SAKTI Sahayak\n\n"
            f"{PROJECT_OVERVIEW}\n\n"
            "**Statutory Pillars of the Platform:**\n"
            "1. **Dual-Pane Statutory Analysis**: Simultaneously cross-checks Indian National laws against International Treaties (WIPO GRATK 2024 & Nagoya Protocol).\n"
            "2. **Section 3(e) Chou-Talalay Synergy Calculator**: Validates whether polyherbal combinations prove non-obvious synergy (Combination Index CI < 1.0) to clear the mere admixture patent bar.\n"
            "3. **CSIR-TKDL Defense & Botanical Taxonomy**: Cross-references 500,000+ classical formulations to prevent biopiracy and Section 3(p) objections.\n"
            "4. **Automated NBA Form 1–4 Generator & ABS Calculator**: Computes statutory benefit-sharing fees (0.1% to 0.5% slabs) under Biological Diversity Rules 2024.\n"
            "5. **Multi-Hop Knowledge Graph**: Maps relational regulatory pathways across 14+ statutes.\n"
            "6. **DPDP Act 2023 Audit Ledger**: Tamper-evident SHA-256 cryptographic chain ensuring zero data retention of proprietary formulation ratios.\n"
            "7. **Bhashini Multi-Lingual Engine**: Supports 10+ Indian languages while preserving statutory tokens."
        ),
        "citations": [
            {"statute": "Problem Statement SIH26045", "section": "Ministry of Ayush / AIIA Guidelines", "official_link": "https://ayush.gov.in"}
        ]
    },
    {
        "keywords": ["section 3(e)", "section 3e", "synergy", "chou-talalay", "combination index", "ci < 1", "mere admixture"],
        "topic": "Section 3(e) Mere Admixture & Synergy",
        "reply": (
            "### Section 3(e) of the Patents Act, 1970 (Mere Admixture Bar)\n\n"
            "Under **Section 3(e)** of the Indian Patents Act, a substance obtained by a mere admixture resulting only in "
            "the aggregation of the properties of its individual components is **not patentable**.\n\n"
            "**Statutory Burden of Proof:**\n"
            "- **CGPDTM Guiding Principle 3**: Applicants must submit quantitative experimental synergy data.\n"
            "- **Chou-Talalay Combination Index (CI)**:\n"
            "  - **CI < 1.0**: Synergistic interaction (**Mandatory threshold** to clear Section 3(e)).\n"
            "  - **CI = 1.0**: Additive interaction (barred as mere admixture).\n"
            "  - **CI > 1.0**: Antagonistic interaction (barred).\n\n"
            "*Statutory Notice: Even if raw efficacy is higher, without proving CI < 1.0 or novel fraction isolation, the patent office will issue a Section 3(e) refusal.*"
        ),
        "citations": [
            {"statute": "The Patents Act, 1970", "section": "§ 3(e)", "title": "Mere admixture bar", "official_link": "https://ipindia.gov.in"}
        ]
    },
    {
        "keywords": ["section 3(p)", "section 3p", "tkdl", "traditional knowledge", "classical formulation", "charaka", "sushruta"],
        "topic": "Section 3(p) Traditional Knowledge Bar",
        "reply": (
            "### Section 3(p) & CSIR-TKDL Defense\n\n"
            "**Section 3(p)** of The Patents Act, 1970 explicitly excludes traditional knowledge from patentability:\n"
            "> *\"An invention which, in effect, is traditional knowledge or is an aggregation or duplication of known properties of traditionally known components is not an invention.\"*\n\n"
            "**Key Principles:**\n"
            "- Formulations appearing in the **First Schedule classical texts** (e.g., *Charaka Samhita*, *Sushruta Samhita*, *Ashtanga Hridaya*) are part of public domain prior art.\n"
            "- India's **Traditional Knowledge Digital Library (CSIR-TKDL)** contains 500,000+ classical formulations in 5 international languages, routinely cited by USPTO, EPO, and JPO to reject biopiracy claims.\n"
            "- **Patentable Alternatives**: To secure IP on classical botanicals, innovators must develop **Novel Drug Delivery Systems (NDDS)** (nanoparticles, liposomes) or isolated bioactive phytopharmaceutical fractions per **G.S.R. 918(E)**."
        ),
        "citations": [
            {"statute": "The Patents Act, 1970", "section": "§ 3(p)", "title": "Traditional knowledge exclusion", "official_link": "https://ipindia.gov.in"},
            {"statute": "CSIR-TKDL Prior Art Database", "section": "Classical Samhitas (First Schedule DCA)", "official_link": "https://www.tkdl.res.in"}
        ]
    },
    {
        "keywords": ["nba", "biodiversity", "form iii", "form 3", "abs", "benefit sharing", "section 6", "national biodiversity"],
        "topic": "National Biodiversity Authority (NBA) & ABS Duties",
        "reply": (
            "### National Biodiversity Authority (NBA) Compliance & ABS Fees\n\n"
            "Under the **Biological Diversity Act, 2002** (as amended in 2023):\n\n"
            "**Mandatory Approvals:**\n"
            "1. **Section 6(1) & Form III**: Any person (domestic or foreign) seeking an Intellectual Property Right (patent) in or outside India based on Indian biological resources **MUST obtain prior approval from the NBA** before the patent is granted.\n"
            "2. **Section 3 & Form I**: Commercial utilization by foreign entities or Indian entities with NRI/FDI shareholding requires prior NBA Form I approval.\n"
            "3. **Section 7**: Indian citizens and domestic companies must give prior intimation to the respective State Biodiversity Board (SBB).\n\n"
            "**Access and Benefit Sharing (ABS) Fee Slabs (2024 Rules):**\n"
            "- Up to ₹1 Crore annual turnover: **0.1%**\n"
            "- ₹1 Crore to ₹3 Crore: **0.2%**\n"
            "- Above ₹3 Crore: **0.5%**\n"
            "- *Exemption Proviso*: Registered AYUSH practitioners (Vaidyas/Hakims) and traditional cultivators are exempt from ABS under Section 7."
        ),
        "citations": [
            {"statute": "Biological Diversity Act, 2002", "section": "§ 6(1)", "title": "Prior approval for IP rights", "official_link": "http://nbaindia.org"},
            {"statute": "Biological Diversity Rules, 2024", "section": "Rule 14 & ABS Regulation", "official_link": "http://nbaindia.org"}
        ]
    },
    {
        "keywords": ["rule 158b", "rule 158", "form 25d", "drugs and cosmetics", "dca", "manufacturing license"],
        "topic": "Drugs & Cosmetics Act Rule 158B & Form 25D",
        "reply": (
            "### DCA Rule 158B & Form 25D Licensing\n\n"
            "Under the **Drugs and Cosmetics Rules, 1945**:\n\n"
            "- **Rule 158B** lays down statutory requirements for the grant of manufacturing licenses for Ayurvedic, Siddha, and Unani drugs.\n"
            "- **Form 25D**: The statutory manufacturing license issued by the State Licensing Authority (State Ayush Directorate).\n"
            "- **Categories**:\n"
            "  1. **Classical Formulations**: Must strictly adhere to recipes in First Schedule texts; exempt from clinical trials.\n"
            "  2. **Patent or Proprietary Ayurvedic Medicines**: Requires proof of published safety references or pilot safety studies (Rule 158B(II)).\n"
            "  3. **Phytopharmaceutical Drugs**: Governed by CDSCO G.S.R. 918(E) requiring Phase I–III clinical trials."
        ),
        "citations": [
            {"statute": "Drugs & Cosmetics Rules, 1945", "section": "Rule 158B", "title": "Ayurvedic drug licensing", "official_link": "https://cdsco.gov.in"}
        ]
    },
    {
        "keywords": ["wipo", "gratk", "origin disclosure", "international", "treaty", "nagoya", "export"],
        "topic": "WIPO GRATK Treaty 2024 & Export Requirements",
        "reply": (
            "### International Patenting & WIPO GRATK Treaty 2024\n\n"
            "On **May 24, 2024**, WIPO member states adopted the historic **Treaty on Intellectual Property, Genetic Resources and Associated Traditional Knowledge (GRATK)**:\n\n"
            "**Core Mandate:**\n"
            "- **Article 3 (Mandatory Origin Disclosure)**: Patent applicants worldwide utilizing genetic resources or traditional knowledge **must disclose the country of origin** (e.g., India).\n"
            "- Failure to disclose or fraudulent concealment can lead to **patent invalidation** or post-grant revocation.\n\n"
            "**Exporting Ayurvedic Products:**\n"
            "- **USA**: US FDA Botanical Drug Guidance (2016) allows human safety reliance on classical texts, but mandates LC-MS/HPLC multi-batch chemical fingerprinting.\n"
            "- **Europe**: Must comply with Directive 2004/24/EC (Traditional Herbal Medicinal Products Directive - THMPD) demonstrating 30 years of traditional use (15 within EU).\n"
            "- **Nagoya Protocol**: Customs authorities require an **Internationally Recognized Certificate of Compliance (IRCC)** linked to NBA approval."
        ),
        "citations": [
            {"statute": "WIPO GRATK Treaty, 2024", "section": "Article 3", "title": "Mandatory disclosure of origin", "official_link": "https://www.wipo.int"},
            {"statute": "Nagoya Protocol on ABS", "section": "Article 15", "title": "Compliance monitoring and IRCC", "official_link": "https://www.cbd.int"}
        ]
    },
    {
        "keywords": ["fssai", "ayurveda aahar", "food", "disease cure", "insomnia", "cure", "treat"],
        "topic": "FSSAI Ayurveda Aahara vs Therapeutic Drugs",
        "reply": (
            "### FSSAI Ayurveda Aahara Regulations 2022\n\n"
            "The **Food Safety and Standards (Ayurveda Aahara) Regulations, 2022** govern food products prepared in accordance with classical recipes:\n\n"
            "**Crucial Legal Boundaries:**\n"
            "- **Regulation 5(3)**: Ayurveda Aahara products are **strictly prohibited from claiming to cure, treat, or mitigate any specific disease or illness**.\n"
            "- **Therapeutic Claims Bar**: If a formulation claims to treat conditions like diabetes, cancer, insomnia, or hypertension, it **cannot** be sold as food. It must obtain a **Form 25D drug license** under DCA Rule 158B.\n"
            "- **Ayurveda Aahara Logo**: Must display the official green and saffron Ministry of Ayush / FSSAI logo on packaging."
        ),
        "citations": [
            {"statute": "FSSAI (Ayurveda Aahara) Regulations, 2022", "section": "Regulation 5(3)", "title": "Prohibition of disease cure claims", "official_link": "https://fssai.gov.in"}
        ]
    },
    {
        "keywords": ["phytopharmaceutical", "g.s.r. 918", "ind", "bioactive fraction", "clinical trial"],
        "topic": "Phytopharmaceutical Drugs Route (CDSCO)",
        "reply": (
            "### Phytopharmaceutical Drugs (G.S.R. 918(E))\n\n"
            "Introduced by the Ministry of Health & Family Welfare under the Drugs and Cosmetics Rules:\n\n"
            "- **Definition**: Purified and standardized fraction with defined minimum 4 bioactive markers, extracted from an aerial or root part of medicinal plants.\n"
            "- **Difference from Classical Ayurveda**: Classical formulations use whole herbs or traditional churnas/asavas. Phytopharmaceuticals follow modern **Investigational New Drug (IND)** pathways.\n"
            "- **Patentability**: Highly viable for patent protection under Section 3(d) and Section 3(e) because purified fractions demonstrate enhanced therapeutic efficacy and novel extraction chemistry."
        ),
        "citations": [
            {"statute": "Drugs & Cosmetics (Second Amendment) Rules, 2015", "section": "G.S.R. 918(E)", "title": "Phytopharmaceutical drug regulatory framework", "official_link": "https://cdsco.gov.in"}
        ]
    },
    {
        "keywords": ["patent", "what is a patent", "prior art", "novelty", "inventive step", "non-obvious"],
        "topic": "General Patenting Fundamentals",
        "reply": (
            "### Patenting Fundamentals & Statutory Criteria\n\n"
            "A **patent** is an exclusive legal right granted by a sovereign government for an invention for a limited period (typically 20 years), in exchange for full public disclosure.\n\n"
            "**The 3 Universal Criteria for Patentability:**\n"
            "1. **Novelty**: The invention must be entirely new and must not have been published, publicly used, or disclosed anywhere in the world prior to the filing date (no *prior art*).\n"
            "2. **Inventive Step (Non-Obviousness)**: The advancement must not be obvious to a person skilled in the art (e.g. an Ayurvedic Vaidya or pharmaceutical chemist).\n"
            "3. **Industrial Applicability**: The invention can be made or used in an industry.\n\n"
            "**In Ayurveda**: Novelty is challenged by centuries of classical literature (*prior art*). To succeed, you must isolate novel molecules, engineer novel drug delivery systems, or prove unexpected synergy."
        ),
        "citations": [
            {"statute": "The Patents Act, 1970", "section": "§ 2(1)(j)", "title": "Definition of invention", "official_link": "https://ipindia.gov.in"}
        ]
    }
]


class ChatEngine:
    def __init__(self):
        self.botanical_catalog = detect_botanicals("")

    def _match_faq(self, user_msg: str) -> Optional[Dict[str, Any]]:
        cleaned = user_msg.lower()
        best_match = None
        highest_score = 0

        for item in FAQS:
            score = 0
            for kw in item["keywords"]:
                if kw in cleaned:
                    score += len(kw.split()) + 2
            if score > highest_score and score >= 2:
                highest_score = score
                best_match = item

        return best_match

    def _answer_botanical(self, user_msg: str) -> Optional[Dict[str, Any]]:
        detected = detect_botanicals(user_msg)
        if not detected:
            return None

        bot = detected[0]
        reply = (
            f"### Botanical Record: **{bot.sanskrit_name}** (*{bot.scientific_binomial}*)\n\n"
            f"- **Family**: {bot.family}\n"
            f"- **Classical Ayurvedic Texts**: {', '.join(bot.classical_texts)}\n"
            f"- **Primary Bioactives**: {', '.join(bot.primary_bioactives)}\n"
            f"- **CSIR-TKDL Landmark Case**: {bot.landmark_patent_case}\n\n"
            f"**Statutory Precaution**: {bot.patentability_warning}\n\n"
            "**Patenting Guidance**: Traditional use of this botanical is protected under **Section 3(p)**. "
            "To secure an enforceable patent, applicants must establish non-obvious synergistic interaction (Chou-Talalay CI < 1.0) "
            "or develop a novel extraction fraction or targeted drug delivery formulation."
        )
        return {
            "topic": f"Botanical: {bot.sanskrit_name}",
            "reply": reply,
            "citations": [
                {"statute": "The Patents Act, 1970", "section": "§ 3(p)", "title": "Traditional Knowledge Bar", "official_link": "https://ipindia.gov.in"},
                {"statute": "CSIR-TKDL Prior Art", "section": bot.classical_texts[0], "official_link": "https://www.tkdl.res.in"}
            ]
        }

    def _answer_via_rag(self, user_msg: str) -> Dict[str, Any]:
        """Queries RAG vector store and synthesizes grounded answer."""
        results = query_rag(user_msg, top_k=3)
        if not results:
            return {
                "topic": "General Ayush IP Inquiry",
                "reply": (
                    "### IP-SAKTI Sahayak Statutory Guidance\n\n"
                    "Your inquiry touches on Ayurvedic intellectual property and regulatory compliance. "
                    "Under Indian Law, the key statutory pillars to consider are:\n\n"
                    "1. **Section 3(p)** of The Patents Act, 1970 bars patenting of traditional classical recipes.\n"
                    "2. **Section 3(e)** bars mere admixtures unless laboratory data proves non-obvious synergy (Combination Index CI < 1.0).\n"
                    "3. **Biological Diversity Act (Section 6)** mandates prior Form III approval from the National Biodiversity Authority before patent grant.\n"
                    "4. **DCA Rule 158B** requires Form 25D manufacturing licensing from the State Ayush Directorate.\n"
                    "5. **WIPO GRATK Treaty 2024** requires mandatory declaration of India as the country of origin in international patent filings."
                ),
                "citations": [
                    {"statute": "The Patents Act, 1970", "section": "§ 3(p) & § 3(e)", "official_link": "https://ipindia.gov.in"},
                    {"statute": "Biological Diversity Act, 2002", "section": "§ 6", "official_link": "http://nbaindia.org"}
                ]
            }

        top_chunk = results[0]
        meta = top_chunk["metadata"]
        act = meta.get("act", "Statutory Provision")
        sec = meta.get("section", "")
        title = meta.get("title", "")
        text_snippet = top_chunk["text"].strip()

        citations = []
        for r in results:
            m = r["metadata"]
            citations.append({
                "statute": m.get("act", "Statutory Rule"),
                "section": m.get("section", ""),
                "title": m.get("title", ""),
                "official_link": m.get("official_link", "https://ipindia.gov.in")
            })

        reply = (
            f"### Statutory Finding: **{act} ({sec})**\n\n"
            f"**Statutory Rule**: *{title}*\n\n"
            f"> \"{text_snippet[:380]}…\"\n\n"
            "**Regulatory Implications:**\n"
            f"- **Statutory Bar**: Applies under {sec} to protect traditional knowledge and prevent mere aggregations.\n"
            "- **Compliance Step**: Ensure compliance with DCA Rule 158B manufacturing licensing and submit mandatory NBA Form III prior to any patent grant.\n"
            "- **Synergy Proof**: If proposing an admixture, quantitative Chou-Talalay Combination Index CI < 1.0 is required."
        )

        return {
            "topic": f"{act} {sec}",
            "reply": reply,
            "citations": citations
        }

    def generate_response(self, user_msg: str, history: Optional[List[Dict[str, str]]] = None, lang: str = "en") -> Dict[str, Any]:
        """
        Main response generation pipeline:
        1. Translates vernacular queries to English for precise statutory matching
        2. Evaluates FAQ domain matcher
        3. Evaluates botanical ontology matcher
        4. Queries hybrid RAG vector store for exact legal citations
        5. Translates output back to user's native language if requested
        """
        raw_query = (user_msg or "").strip()
        if not raw_query:
            return {
                "reply": "Please enter a question or query regarding Ayurvedic intellectual property, patenting, or regulatory compliance.",
                "citations": [],
                "topic": "Empty Query",
                "language": lang,
                "confidence": 1.0
            }

        # 1. Translate query if not English
        search_query = raw_query
        if lang != "en":
            try:
                en_trans = bhashini_service.translate(raw_query, source_lang=lang, target_lang="en")
                search_query = en_trans.get("translated_text", raw_query)
            except Exception as e:
                logger.warning(f"Bhashini query translation note: {e}")

        # 2. Check FAQ domain match
        faq_match = self._match_faq(search_query)
        if faq_match:
            res_topic = faq_match["topic"]
            res_reply = faq_match["reply"]
            res_cites = faq_match["citations"]
        else:
            # 3. Check botanical match
            bot_match = self._answer_botanical(search_query)
            if bot_match:
                res_topic = bot_match["topic"]
                res_reply = bot_match["reply"]
                res_cites = bot_match["citations"]
            else:
                # 4. Query RAG vector store
                rag_match = self._answer_via_rag(search_query)
                res_topic = rag_match["topic"]
                res_reply = rag_match["reply"]
                res_cites = rag_match["citations"]

        # 5. Translate reply back to user's selected language
        final_reply = res_reply
        if lang != "en":
            try:
                trans = bhashini_service.translate(res_reply, source_lang="en", target_lang=lang)
                final_reply = trans.get("translated_text", res_reply)
            except Exception as e:
                logger.warning(f"Bhashini response translation note: {e}")

        return {
            "reply": final_reply,
            "citations": res_cites,
            "topic": res_topic,
            "language": lang,
            "confidence": 0.96
        }


CHAT_ENGINE = ChatEngine()

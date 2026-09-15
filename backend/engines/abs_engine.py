"""
IP-SAKTI Sahayak: National Biodiversity Authority (NBA) & ABS Compliance Engine
Implements the 2023 Biological Diversity Amendment Act & 2024 Rules:
- Evaluates Section 3 vs Section 7 entity status
- Determines mandatory NBA Forms (Form I, II, III, IV)
- Calculates prospective ABS fees based on annual turnover slabs or purchase price
"""

from typing import Dict, Any, List
from pydantic import BaseModel


class ABSAssessmentInput(BaseModel):
    is_foreign_incorporated: bool = False
    has_foreign_shareholders: bool = False
    is_registered_ayush_practitioner: bool = False
    is_cultivator_or_grower: bool = False
    is_normally_traded_commodity: bool = False
    intended_activity: str = "commercial_utilization"  # "commercial_utilization", "apply_for_patent", "transfer_research", "third_party_transfer"
    annual_turnover_inr_lakhs: float = 50.0  # In Lakhs INR
    purchase_price_inr_lakhs: float = 10.0


class ABSAssessmentOutput(BaseModel):
    exemption_granted: bool
    exemption_statutory_basis: str
    nba_statutory_form: str
    governing_clause: str
    benefit_sharing_rate: str
    statutory_fee_amount_inr: float
    procedural_compliance_checklist: List[str]
    legal_liability_warning: str


def compute_nba_abs_posture(inp: ABSAssessmentInput) -> ABSAssessmentOutput:
    # 1. Statutory Exemption under Section 7 Proviso (2023 Amendment)
    if inp.is_registered_ayush_practitioner or inp.is_cultivator_or_grower:
        return ABSAssessmentOutput(
            exemption_granted=True,
            exemption_statutory_basis="Section 7 Proviso of Biological Diversity (Amendment) Act 2023: Registered AYUSH practitioners and local cultivators are exempt from SBB intimation and ABS fees.",
            nba_statutory_form="No Form Required (Statutory Exemption)",
            governing_clause="Section 7, Biological Diversity Act 2002 (as amended in 2023)",
            benefit_sharing_rate="0.0% (Statutorily Exempt)",
            statutory_fee_amount_inr=0.0,
            procedural_compliance_checklist=[
                "Maintain valid State Ayush Registration Council certificate.",
                "Ensure biological resources are sourced exclusively for bona fide traditional clinical practice.",
                "Do not export raw biological extracts without prior NBA approval."
            ],
            legal_liability_warning="Exemption is strictly limited to personal practice. Commercial mass-manufacturing entities owned by practitioners remain subject to SBB intimation."
        )

    # 2. Section 40 Normally Traded Commodities (NTC) Exemption
    if inp.is_normally_traded_commodity and inp.intended_activity != "apply_for_patent":
        return ABSAssessmentOutput(
            exemption_granted=True,
            exemption_statutory_basis="Section 40 Notification: 421 species declared as Normally Traded Commodities (NTC) exempt when traded as agricultural produce.",
            nba_statutory_form="NTC Exemption Declaratory Certificate",
            governing_clause="Section 40, Biological Diversity Act 2002",
            benefit_sharing_rate="0.0% (Exempt from ABS)",
            statutory_fee_amount_inr=0.0,
            procedural_compliance_checklist=[
                "Verify botanical species against MoEFCC 421 NTC Schedule.",
                "Retain agricultural Mandi cess receipts and GST invoices proving purchase as commodity produce.",
                "Ensure no novel pharmaceutical isolation patent is filed on the commodity."
            ],
            legal_liability_warning="If an NTC commodity (e.g. black pepper or turmeric) is subjected to novel patentable extraction, the exemption is legally extinguished."
        )

    # 3. Patent Application Trigger (Section 6 & Form 3)
    if inp.intended_activity == "apply_for_patent":
        # Fee calculation: 0.1% to 0.5% ex-factory sales or 2-5% royalty on IPR transfer
        turnover = inp.annual_turnover_inr_lakhs
        if turnover <= 100.0:
            rate_str = "0.1% of annual gross ex-factory sale"
            fee = (turnover * 100000) * 0.001
        elif turnover <= 300.0:
            rate_str = "0.2% of annual gross ex-factory sale"
            fee = (turnover * 100000) * 0.002
        else:
            rate_str = "0.5% of annual gross ex-factory sale"
            fee = (turnover * 100000) * 0.005

        return ABSAssessmentOutput(
            exemption_granted=False,
            exemption_statutory_basis="Mandatory NBA approval required before grant of any IPR based on Indian biological resources.",
            nba_statutory_form="Form III (Application for IPR on Biological Inventions)",
            governing_clause="Section 6(1) & Rule 18 of Biological Diversity Rules, 2024",
            benefit_sharing_rate=rate_str,
            statutory_fee_amount_inr=fee,
            procedural_compliance_checklist=[
                "File provisional or complete patent application with Indian Patent Office.",
                "Submit NBA Form III with application fee (₹500 for Indian individuals/startups; ₹10,000 for corporates).",
                "Execute Benefit Sharing Agreement with NBA before patent sealing.",
                "Submit NBA approval certificate to Patent Controller to satisfy Guiding Principle 6."
            ],
            legal_liability_warning="Failure to obtain NBA Form 3 approval before patent grant creates fatal grounds for pre-grant opposition and patent revocation under Section 64(1)(p)."
        )

    # 4. Foreign / Section 3 Entity Access (Form 1)
    if inp.is_foreign_incorporated or inp.has_foreign_shareholders:
        purchase_fee = (inp.purchase_price_inr_lakhs * 100000) * 0.03
        return ABSAssessmentOutput(
            exemption_granted=False,
            exemption_statutory_basis="Foreign entities or Indian entities with foreign shareholding are Section 3 entities requiring prior NBA clearance.",
            nba_statutory_form="Form I (Prior Approval for Access to Biological Resources)",
            governing_clause="Section 3(2) & Rule 14, Biological Diversity Rules, 2024",
            benefit_sharing_rate="3.0% to 5.0% of purchase price of biological resources",
            statutory_fee_amount_inr=purchase_fee,
            procedural_compliance_checklist=[
                "Submit NBA Form I with ₹10,000 application fee.",
                "Obtain Prior Informed Consent (PIC) from State Biodiversity Board and BMCs.",
                "Execute formal ABS Agreement with National Biodiversity Authority."
            ],
            legal_liability_warning="Accessing Indian biological resources without prior Form I approval violates Section 3 and is punishable under Section 55."
        )

    # 5. Domestic Commercial Entity (State SBB Intimation)
    turnover = inp.annual_turnover_inr_lakhs
    rate_str = "0.1% of turnover"
    fee = (turnover * 100000) * 0.001
    return ABSAssessmentOutput(
        exemption_granted=False,
        exemption_statutory_basis="Domestic Indian entities accessing bioresources for commercial utilization must give prior intimation to State Biodiversity Board.",
        nba_statutory_form="Form I (State Biodiversity Board Prior Intimation)",
        governing_clause="Section 7, Biological Diversity Act 2002",
        benefit_sharing_rate="0.1% to 0.5% of turnover as assessed by the concerned State SBB",
        statutory_fee_amount_inr=fee,
        procedural_compliance_checklist=[
            "Submit prior intimation to the concerned SBB (e.g. Kerala SBB, Uttarakhand SBB).",
            "Maintain traceability logs of raw material mandis and cultivator procurement.",
            "Deposit annual ABS contribution as assessed by the SBB."
        ],
        legal_liability_warning="Ensure all purchased raw materials possess GST invoices and Mandi permits."
    )


def generate_nba_form_dossier(inp: ABSAssessmentInput, applicant_name: str = "Ayush Innovator / Enterprise", product_name: str = "Ayurvedic Formulation", bio_resources: str = "Curcuma longa (Haridra), Piper nigrum (Maricha)") -> Dict[str, Any]:
    """
    Automated NBA Form 1-4 Generator per Biological Diversity Rules 2024.
    Generates structured, pre-filled application dossier for NBA / SBB portal filing.
    """
    posture = compute_nba_abs_posture(inp)

    # Determine exact Form designation
    if inp.intended_activity == "apply_for_patent":
        form_code = "FORM_III"
        form_title = "Form III: Application for Applying for Intellectual Property Rights (Rule 18)"
        governing_sec = "Section 6(1) of Biological Diversity Act, 2002 (as amended 2023)"
        official_fee = 500.0 if not inp.is_foreign_incorporated else 10000.0
    elif inp.intended_activity == "transfer_research":
        form_code = "FORM_II"
        form_title = "Form II: Application for Transferring Results of Research (Rule 17)"
        governing_sec = "Section 4 of Biological Diversity Act, 2002"
        official_fee = 5000.0
    elif inp.intended_activity == "third_party_transfer":
        form_code = "FORM_IV"
        form_title = "Form IV: Application for Third Party Transfer of Accessed Bio-Resource (Rule 19)"
        governing_sec = "Section 20 of Biological Diversity Act, 2002"
        official_fee = 10000.0
    elif inp.is_foreign_incorporated or inp.has_foreign_shareholders:
        form_code = "FORM_I"
        form_title = "Form I: Application for Access to Biological Resources by Foreign Entity (Rule 14)"
        governing_sec = "Section 3(2) of Biological Diversity Act, 2002"
        official_fee = 10000.0
    else:
        form_code = "FORM_I_SBB"
        form_title = "State Biodiversity Board Intimation Form for Commercial Utilization"
        governing_sec = "Section 7 of Biological Diversity Act, 2002"
        official_fee = 1000.0

    dossier_text = f"""================================================================================
NATIONAL BIODIVERSITY AUTHORITY (NBA), CHENNAI
GOVERNMENT OF INDIA
STATUTORY APPLICATION DOSSIER — {form_code}
{form_title}
Governing Statute: {governing_sec}
Framework: Biological Diversity (Amendment) Act, 2023 & BD Rules, 2024
================================================================================

1. APPLICANT DETAILS & STATUTORY CAPACITY:
   Full Name / Entity:   {applicant_name}
   Nationality / Status: {'Foreign Entity / FDI Co (Section 3 Entity)' if inp.is_foreign_incorporated or inp.has_foreign_shareholders else 'Indian Enterprise / Vaidya (Section 7 Entity)'}
   Registered Ayush:     {'Yes (Exempt under Section 7 Proviso)' if inp.is_registered_ayush_practitioner else 'No'}
   Cultivator / Grower:  {'Yes' if inp.is_cultivator_or_grower else 'No'}

2. SUBJECT INVENTIVE MATTER & BIOLOGICAL RESOURCES:
   Formulation / Title:  {product_name}
   Intended Activity:    {inp.intended_activity.replace('_', ' ').title()}
   Biological Resources: {bio_resources}
   Geographical Source:  Wild collection / Cultivated Mandi source across India
   Traditional Knowledge:Associated with Classical Ayurvedic Formulary (TKDL referenced)

3. BENEFIT SHARING (ABS) DETERMINATION (2024 RULES):
   Exemption Status:     {'STATUTORILY EXEMPT' if posture.exemption_granted else 'MANDATORY COMPLIANCE REQUIRED'}
   Statutory Form:       {posture.nba_statutory_form}
   Projected Turnover:   ₹ {inp.annual_turnover_inr_lakhs:,.2f} Lakhs per annum
   Applicable ABS Rate:  {posture.benefit_sharing_rate}
   Estimated Annual ABS: ₹ {posture.statutory_fee_amount_inr:,.2f} INR
   Application Fee:      ₹ {official_fee:,.2f} INR (to be paid via Bharatkosh)

4. MANDATORY STATUTORY DECLARATION:
   I/We hereby solemnly declare that:
   (a) The biological resources accessed will be utilized strictly for the bona fide purposes stated.
   (b) Prior Informed Consent (PIC) has been initiated with concerned State Biodiversity Boards / BMCs.
   (c) A legally binding Benefit Sharing Agreement shall be entered into with the NBA prior to patent grant / commercial utilization.
   (d) All information provided is true, correct, and traceable under DPDP Act 2023.

5. PROCEDURAL NEXT STEPS:
"""
    for idx, step in enumerate(posture.procedural_compliance_checklist, 1):
        dossier_text += f"   {idx}. {step}\n"

    dossier_text += f"\n6. STATUTORY WARNING:\n   {posture.legal_liability_warning}\n"
    dossier_text += "================================================================================\n"

    return {
        "form_code": form_code,
        "form_title": form_title,
        "governing_section": governing_sec,
        "applicant_name": applicant_name,
        "product_name": product_name,
        "exemption_granted": posture.exemption_granted,
        "annual_turnover_lakhs": inp.annual_turnover_inr_lakhs,
        "benefit_sharing_rate": posture.benefit_sharing_rate,
        "estimated_fee_inr": posture.statutory_fee_amount_inr,
        "application_fee_inr": official_fee,
        "dossier_text": dossier_text,
        "official_portal_url": "http://nbaindia.org"
    }


"""
Service to generate comprehensive Markdown research reports.
"""
from datetime import datetime
from typing import Any, Dict

def generate_markdown_report(analysis_data: Dict[str, Any]) -> str:
    project = analysis_data.get("project", {})
    papers = analysis_data.get("retrieved_papers", [])
    comparisons = analysis_data.get("comparisons", [])
    gaps = analysis_data.get("research_gaps", [])
    claims = analysis_data.get("claims_verification", [])
    uncertainty = analysis_data.get("uncertainty_report", {})
    improvements = analysis_data.get("suggested_improvements", {})
    mode = analysis_data.get("analysis_mode", "Evidence-First Verification Engine")

    lines = []
    lines.append("# ResearchEcho — Evidence-First Research Analysis Report")
    lines.append(f"**Generated:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    lines.append(f"**Analysis Engine Mode:** {mode}")
    lines.append("")
    lines.append("> **IMPORTANT NOTICE**  ")
    lines.append(f"> {uncertainty.get('mandatory_disclaimer', 'This analysis is based on the sources retrieved. It does not prove that a project idea is entirely novel.')}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 1. Submitted Project Idea")
    lines.append(f"- **Title:** {project.get('title')}")
    lines.append(f"- **Domain:** {project.get('domain')}")
    lines.append(f"- **Abstract / Description:**\n  > {project.get('abstract')}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 2. Retrieved Scholarly Literature (Live API)")
    lines.append(f"Total Papers Retrieved: {len(papers)} | Provider: OpenAlex Live Scholarly Graph")
    lines.append("")

    for i, p in enumerate(papers, 1):
        lines.append(f"### {i}. {p.get('title')}")
        lines.append(f"- **Authors:** {p.get('authors')}")
        lines.append(f"- **Year:** {p.get('year')} | **Citations:** {p.get('citation_count')} | **Venue:** {p.get('venue')}")
        lines.append(f"- **DOI:** [{p.get('doi')}]({p.get('doi') if p.get('doi') != 'No DOI available' else '#'})")
        lines.append(f"- **Source Link:** [{p.get('url')}]({p.get('url')})")
        if p.get("pdf_url"):
            lines.append(f"- **Open Access PDF:** [Direct PDF Link]({p.get('pdf_url')})")
        lines.append(f"- **Abstract Status:** {'Available' if p.get('has_accessible_abstract') else 'Not Publicly Indexed'}")
        lines.append(f"> {p.get('abstract')}")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## 3. Comparative Literature Matrix")
    lines.append("")
    lines.append("| Paper | Research Problem | Methodology | Dataset | Limitations Stated by Authors |")
    lines.append("| :--- | :--- | :--- | :--- | :--- |")
    for c in comparisons:
        short_title = c.get('paper_title', '')[:35] + "..." if len(c.get('paper_title', '')) > 35 else c.get('paper_title', '')
        prob = c.get('problem', '').replace('\n', ' ')[:60] + "..."
        meth = c.get('methodology', '').replace('\n', ' ')[:60] + "..."
        data = c.get('dataset', '').replace('\n', ' ')[:40]
        lims = c.get('limitations', '').replace('\n', ' ')[:60] + "..."
        lines.append(f"| **{short_title}** | {prob} | {meth} | {data} | {lims} |")
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## 4. Evidence-Backed Research Gap Analysis")
    lines.append("")
    for i, g in enumerate(gaps, 1):
        lines.append(f"### Gap {i}: {g.get('gap_title')}")
        lines.append(f"- **Origin Classification:** `{g.get('origin')}`")
        lines.append(f"- **Possible Gap Description:** {g.get('possible_gap')}")
        lines.append(f"- **Why It Matters:** {g.get('why_it_matters')}")
        lines.append(f"- **Supporting Paper:** [{g.get('supporting_paper')}]({g.get('supporting_paper_url')})")
        lines.append(f"- **Supporting Quotation:** *\"{g.get('supporting_quote')}\"*")
        lines.append(f"- **Suggested Investigation Direction:** {g.get('suggested_direction')}")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## 5. Evidence Verification Panel")
    lines.append("")
    for i, cl in enumerate(claims, 1):
        status = cl.get('status')
        badge = "✅ SUPPORTED" if status == "Supported" else ("⚠️ PARTIALLY SUPPORTED" if status == "Partially Supported" else ("❌ CONTRADICTED" if status == "Contradicted" else "🔍 MANUAL VERIFICATION NEEDED"))
        lines.append(f"### Claim {i} [{badge}]")
        lines.append(f"- **Claim:** {cl.get('claim_text')}")
        lines.append(f"- **Linked Source:** {cl.get('linked_paper_title')}")
        lines.append(f"- **Supporting Passage:** *\"{cl.get('supporting_passage')}\"*")
        lines.append(f"- **Verification Assessment:** {cl.get('status_explanation')}")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## 6. Uncertainty & Coverage Report")
    lines.append(f"- **Total Papers Retrieved:** {uncertainty.get('total_papers_retrieved')}")
    lines.append(f"- **Papers with Accessible Abstracts:** {uncertainty.get('papers_with_accessible_abstracts')} ({uncertainty.get('abstract_coverage_percent')}%)")
    lines.append(f"- **Publication Year Range:** {uncertainty.get('publication_year_coverage')}")
    lines.append(f"- **Directly Supported Claims:** {uncertainty.get('claims_with_direct_evidence')} of {uncertainty.get('total_claims_evaluated')}")
    lines.append(f"- **Heuristic Traceability Score:** {uncertainty.get('traceability_score')}/100")
    lines.append(f"  *(Note: {uncertainty.get('score_explanation')})*")
    lines.append("")
    lines.append("### Missing Information:")
    for item in uncertainty.get("missing_information", []):
        lines.append(f"- {item}")
    lines.append("")
    lines.append("### Conflicting Findings:")
    for item in uncertainty.get("conflicting_findings", []):
        lines.append(f"- {item}")
    lines.append("")
    lines.append("### Current Search Limitations:")
    for item in uncertainty.get("search_limitations", []):
        lines.append(f"- {item}")
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## 7. Actionable Suggested Improvements & Test Experiments")
    lines.append("")
    lines.append("### Evidence-Based Recommendations:")
    for item in improvements.get("evidence_based_improvements", []):
        lines.append(f"- {item}")
    lines.append("")
    lines.append("### AI-Generated Hypotheses:")
    for item in improvements.get("ai_generated_hypotheses", []):
        lines.append(f"- {item}")
    lines.append("")
    lines.append("### Proposed Empirical Experiments:")
    for item in improvements.get("proposed_test_experiments", []):
        lines.append(f"- {item}")
    lines.append("")
    lines.append("### Evidence Still Needed:")
    for item in improvements.get("evidence_still_needed", []):
        lines.append(f"- {item}")
    lines.append("")
    lines.append("---")
    lines.append("*Generated by ResearchEcho — Evidence-First AI Research Assistant*")

    return "\n".join(lines)

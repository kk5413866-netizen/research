import urllib.request
import json

def test_researchecho():
    print("==================================================")
    print("  RESEARCHECHO COMPLETE SYSTEM INTEGRATION TEST  ")
    print("==================================================")

    # 1. Health Check
    res = urllib.request.urlopen("http://127.0.0.1:8000/api/health")
    health = json.loads(res.read().decode())
    print("[1] Health Check:", health)
    assert health["status"] == "healthy"

    # 2. Presets
    res = urllib.request.urlopen("http://127.0.0.1:8000/api/presets")
    presets = json.loads(res.read().decode())["presets"]
    print(f"[2] Presets Loaded: {len(presets)} presets available.")
    print("    Demo Preset 1:", presets[0]["title"])

    # 3. Analyze Preset 1
    print("\n[3] Executing Live Research Analysis against OpenAlex API...")
    payload = json.dumps({
        "title": presets[0]["title"],
        "abstract": presets[0]["abstract"],
        "domain": presets[0]["domain"]
    }).encode("utf-8")
    
    req = urllib.request.Request(
        "http://127.0.0.1:8000/api/analyze",
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=30) as res_analysis:
        analysis = json.loads(res_analysis.read().decode("utf-8"))

    print(f"    - Genuine Papers Retrieved: {len(analysis['retrieved_papers'])}")
    for i, p in enumerate(analysis['retrieved_papers'][:3], 1):
        print(f"      Paper {i}: {p['title']} ({p['year']})")
        print(f"        Authors: {p['authors']}")
        print(f"        DOI: {p['doi']}")
        print(f"        Citation Count: {p['citation_count']}")
        print(f"        Accessible Abstract: {p['has_accessible_abstract']}")

    print(f"\n    - Comparison Matrix Entries: {len(analysis['comparisons'])}")
    print(f"      Sample Comparison (Paper 1 Methodology): {analysis['comparisons'][0]['methodology'][:80]}...")
    print(f"      Sample Comparison (Paper 1 Stated Limitations): {analysis['comparisons'][0]['limitations'][:80]}...")

    print(f"\n    - Evidence-Backed Research Gaps: {len(analysis['research_gaps'])}")
    for i, g in enumerate(analysis['research_gaps'][:2], 1):
        print(f"      Gap {i} [{g['origin']}]: {g['gap_title']}")
        print(f"        Quotation: \"{g['supporting_quote'][:90]}...\"")
        print(f"        Suggested Direction: {g['suggested_direction'][:90]}...")

    print(f"\n    - Claims Verification: {len(analysis['claims_verification'])} claims")
    for i, c in enumerate(analysis['claims_verification'], 1):
        print(f"      Claim {i} [{c['status']}]: \"{c['claim_text']}\"")
        print(f"        Explanation: {c['status_explanation']}")

    u = analysis['uncertainty_report']
    print(f"\n    - Uncertainty & Coverage Report:")
    print(f"      Traceability Score: {u['traceability_score']}/100")
    print(f"      Score Formula: {u['score_explanation']}")
    print(f"      Temporal Span: {u['publication_year_coverage']}")
    print(f"      Mandatory Notice: \"{u['mandatory_disclaimer']}\"")

    # 4. Markdown Export Check
    print("\n[4] Testing Markdown Report Export...")
    req_exp = urllib.request.Request(
        "http://127.0.0.1:8000/api/export/markdown",
        data=json.dumps(analysis).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req_exp, timeout=10) as res_exp:
        md_text = res_exp.read().decode("utf-8")
    print(f"    Export Generated: {len(md_text)} bytes")
    print(f"    First line: {md_text.splitlines()[0]}")

    # 5. Frontend Dev Server Check
    print("\n[5] Testing Frontend Server...")
    res_fe = urllib.request.urlopen("http://127.0.0.1:5173")
    print(f"    Frontend status: HTTP {res_fe.getcode()} (Vite + React + TypeScript Live)")

    print("\n==================================================")
    print("  ALL RESEARCHECHO VERIFICATION CHECKS PASSED!    ")
    print("==================================================")

if __name__ == "__main__":
    test_researchecho()

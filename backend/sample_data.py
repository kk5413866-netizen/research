"""
Pre-configured academic research proposals for 1-click hackathon demonstration.
These presets represent sample project ideas submitted by students.
"""

SAMPLE_PROJECTS = [
    {
        "id": "sample-1",
        "title": "Federated Learning with Differential Privacy for Edge Healthcare Diagnostics",
        "domain": "Artificial Intelligence & Healthcare",
        "abstract": (
            "We propose a decentralized federated learning framework integrated with local differential privacy (LDP) "
            "designed to train diagnostic models across distributed hospital edge devices without transmitting sensitive patient records. "
            "Prior approaches suffer from high gradient noise which severely degrades diagnostic accuracy, and they fail to account for "
            "heterogeneous non-IID data distributions across medical imaging centers. Our approach introduces an adaptive gradient clipping "
            "and client weighting mechanism based on local data volume and noise budget, aiming to preserve patient confidentiality while "
            "maintaining clinical-grade classification metrics on distributed chest X-ray modalities."
        ),
        "target_keywords": "federated learning differential privacy healthcare edge diagnostics"
    },
    {
        "id": "sample-2",
        "title": "Multimodal Hallucination Mitigation in Medical Vision-Language Models via Knowledge Graph Verification",
        "domain": "Natural Language Processing & Computer Vision",
        "abstract": (
            "Vision-Language Models (VLMs) deployed in radiological reporting frequently suffer from factual hallucinations, generating "
            "plausible but clinically incorrect pathology descriptions from chest radiographs and CT scans. We propose a neuro-symbolic "
            "verification pipeline that extracts biomedical entities and relational triples from generated draft reports, aligns them with "
            "a curated Unified Medical Language System (UMLS) knowledge graph, and flags contradictory clinical claims prior to final output. "
            "Unlike purely prompt-based techniques, this approach grounds generation in deterministic medical ontologies."
        ),
        "target_keywords": "hallucination multimodal vision language models medical knowledge graph verification"
    },
    {
        "id": "sample-3",
        "title": "Low-Resource Cross-Lingual Code Generation using Retrieval-Augmented Instruction Tuning",
        "domain": "Software Engineering & NLP",
        "abstract": (
            "Large language models exhibit significant performance disparities when generating source code from docstrings written in "
            "low-resource natural languages compared to English. We propose a retrieval-augmented instruction tuning framework that dynamically "
            "retrieves cross-lingual code-comment pairs from multilingual open-source repositories to prime the model context. We evaluate whether "
            "dense semantic alignment across linguistic representations can bridge syntactic discrepancies and reduce functional bugs "
            "without requiring parameter-heavy multilingual foundation models."
        ),
        "target_keywords": "cross-lingual code generation retrieval augmented instruction low resource"
    }
]

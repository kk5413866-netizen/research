import json
import logging
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional

logger = logging.getLogger("researchecho.scholarly")

def reconstruct_abstract(inverted_index: Optional[Dict[str, List[int]]]) -> Optional[str]:
    """Reconstruct human-readable abstract from OpenAlex inverted index."""
    if not inverted_index:
        return None
    try:
        pos_words: List[tuple[int, str]] = []
        for word, positions in inverted_index.items():
            for pos in positions:
                pos_words.append((pos, word))
        pos_words.sort(key=lambda x: x[0])
        return " ".join(word for _, word in pos_words)
    except Exception as e:
        logger.warning(f"Failed to reconstruct abstract: {e}")
        return None

def fetch_openalex_papers(query: str, domain: Optional[str] = None, limit: int = 6) -> List[Dict[str, Any]]:
    """
    Query OpenAlex Works API for genuine scholarly literature.
    Does not invent metadata. Returns real papers with real DOIs and citations.
    """
    clean_query = query.strip()
    if domain and domain.lower() != "general":
        search_term = f"{clean_query} {domain}"
    else:
        search_term = clean_query

    encoded = urllib.parse.quote(search_term)
    url = f"https://api.openalex.org/works?search={encoded}&per_page={limit}&sort=relevance_score:desc"

    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "ResearchEcho/1.0 (https://researchecho.local; mailto:academic-assistant@researchecho.org)",
            "Accept": "application/json"
        }
    )

    papers: List[Dict[str, Any]] = []
    try:
        with urllib.request.urlopen(req, timeout=12) as response:
            if response.status == 200:
                raw_data = json.loads(response.read().decode("utf-8"))
                results = raw_data.get("results", [])

                for item in results:
                    title = item.get("title")
                    if not title:
                        continue

                    # Authors
                    authors_list = []
                    for authorship in item.get("authorships", []):
                        author_name = authorship.get("author", {}).get("display_name")
                        if author_name:
                            authors_list.append(author_name)

                    authors_str = ", ".join(authors_list[:3])
                    if len(authors_list) > 3:
                        authors_str += " et al."
                    elif not authors_str:
                        authors_str = "Authors not indexed"

                    # Abstract
                    abstract_raw = reconstruct_abstract(item.get("abstract_inverted_index"))
                    has_abstract = bool(abstract_raw and len(abstract_raw.strip()) > 30)
                    abstract_text = abstract_raw if has_abstract else "Abstract not publicly indexed by publisher in OpenAlex."

                    # Links and identifiers
                    doi = item.get("doi")
                    landing_url = None
                    primary_loc = item.get("primary_location") or {}
                    if primary_loc:
                        landing_url = primary_loc.get("landing_page_url")

                    pdf_url = None
                    oa_info = item.get("open_access") or {}
                    if oa_info.get("oa_url"):
                        pdf_url = oa_info.get("oa_url")
                    elif primary_loc.get("pdf_url"):
                        pdf_url = primary_loc.get("pdf_url")

                    source_url = doi or landing_url or (f"https://openalex.org/{item.get('id')}" if item.get("id") else None)

                    # Venue
                    venue = "Scholarly Publication"
                    source_info = primary_loc.get("source") or {}
                    if source_info and source_info.get("display_name"):
                        venue = source_info.get("display_name")

                    papers.append({
                        "id": item.get("id", f"paper-{len(papers)+1}"),
                        "title": title.strip(),
                        "authors": authors_str,
                        "authors_full": authors_list,
                        "year": item.get("publication_year") or "Year not reported",
                        "abstract": abstract_text,
                        "has_accessible_abstract": has_abstract,
                        "doi": doi or "No DOI available",
                        "url": source_url or "No URL available",
                        "pdf_url": pdf_url,
                        "citation_count": item.get("cited_by_count", 0),
                        "venue": venue,
                        "is_open_access": bool(oa_info.get("is_oa")),
                        "provider": "OpenAlex Live API"
                    })
    except Exception as e:
        logger.error(f"Error fetching from OpenAlex: {e}")

    return papers

def fetch_semantic_scholar_papers(query: str, api_key: Optional[str] = None, limit: int = 5) -> List[Dict[str, Any]]:
    """Query Semantic Scholar Graph API if configured or as secondary provider."""
    encoded = urllib.parse.quote(query.strip())
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={encoded}&limit={limit}&fields=title,authors,year,abstract,citationCount,url,externalIds,openAccessPdf"

    headers = {"User-Agent": "ResearchEcho/1.0"}
    if api_key:
        headers["x-api-key"] = api_key

    req = urllib.request.Request(url, headers=headers)
    papers = []
    try:
        with urllib.request.urlopen(req, timeout=8) as response:
            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))
                for item in data.get("data", []):
                    title = item.get("title")
                    if not title:
                        continue
                    authors_list = [a.get("name") for a in item.get("authors", []) if a.get("name")]
                    authors_str = ", ".join(authors_list[:3])
                    if len(authors_list) > 3:
                        authors_str += " et al."
                    elif not authors_str:
                        authors_str = "Authors not indexed"

                    abstract = item.get("abstract")
                    has_abstract = bool(abstract and len(abstract.strip()) > 30)
                    ext_ids = item.get("externalIds") or {}
                    doi = f"https://doi.org/{ext_ids['DOI']}" if "DOI" in ext_ids else None
                    oa_pdf = (item.get("openAccessPdf") or {}).get("url")

                    papers.append({
                        "id": item.get("paperId", f"s2-{len(papers)+1}"),
                        "title": title.strip(),
                        "authors": authors_str,
                        "authors_full": authors_list,
                        "year": item.get("year") or "Year not reported",
                        "abstract": abstract or "Abstract not publicly indexed by Semantic Scholar.",
                        "has_accessible_abstract": has_abstract,
                        "doi": doi or "No DOI available",
                        "url": doi or item.get("url") or "No URL available",
                        "pdf_url": oa_pdf,
                        "citation_count": item.get("citationCount", 0),
                        "venue": "Semantic Scholar Record",
                        "is_open_access": bool(oa_pdf),
                        "provider": "Semantic Scholar API"
                    })
    except Exception as e:
        logger.warning(f"Semantic scholar search failed (expected if rate limited or unauthenticated): {e}")

    return papers

def search_scholarly_literature(query: str, domain: Optional[str] = None, semantic_scholar_key: Optional[str] = None, limit: int = 6) -> List[Dict[str, Any]]:
    """
    Search scholarly APIs with preference for OpenAlex (open, reliable) and Semantic Scholar fallback.
    Guarantees no fabricated papers or imaginary DOIs.
    """
    papers = fetch_openalex_papers(query, domain=domain, limit=limit)
    if not papers:
        # If openalex had network issue or empty result, try semantic scholar
        papers = fetch_semantic_scholar_papers(query, api_key=semantic_scholar_key, limit=limit)

    return papers

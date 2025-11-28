# wiki_qa.py
import requests
import re
from bs4 import BeautifulSoup

WIKI_API = "https://en.wikipedia.org/w/api.php"
WIKI_REST = "https://en.wikipedia.org/api/rest_v1"
HEADERS = {"User-Agent": "CUET-Hospital-Management/1.0 (ashrafdcc1502@gmail.com)"}

# simple sentence splitter
_sentence_split_re = re.compile(r'(?<=[.!?])\s+')

def search_wikipedia(query, limit=1):
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "srlimit": limit,
        "format": "json"
    }
    r = requests.get(WIKI_API, params=params, headers=HEADERS, timeout=10)
    r.raise_for_status()
    data = r.json()
    hits = data.get("query", {}).get("search", [])
    if not hits:
        return None
    # return the top title
    return hits[0]["title"]

def get_summary(title):
    # REST summary endpoint — returns short lead, description, canonical url
    url = f"{WIKI_REST}/page/summary/{requests.utils.requote_uri(title)}"
    r = requests.get(url, headers=HEADERS, timeout=10)
    r.raise_for_status()
    return r.json()  # contains 'extract' (lead), 'content_urls' etc.

def get_mobile_sections(title):
    # mobile-sections gives structured sections; fallback to action=parse if unavailable
    url = f"{WIKI_REST}/page/mobile-sections/{requests.utils.requote_uri(title)}"
    r = requests.get(url, headers=HEADERS, timeout=10)
    if r.status_code == 200:
        return r.json()
    # Fallback: get page HTML via action=parse
    params = {"action": "parse", "page": title, "prop": "text|sections", "format": "json"}
    r2 = requests.get(WIKI_API, params=params, headers=HEADERS, timeout=10)
    r2.raise_for_status()
    return r2.json()

def html_to_text(html):
    # very small helper to extract clean text from a fragment
    soup = BeautifulSoup(html, "html.parser")
    # remove tables, references
    for tag in soup(["sup", "table", "style", "script"]):
        tag.decompose()
    text = soup.get_text(separator=" ", strip=True)
    # collapse whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def first_n_sentences(text, n=5):
    parts = _sentence_split_re.split(text.strip())
    # filter empties
    parts = [p.strip() for p in parts if p.strip()]
    return " ".join(parts[:n])

def extract_section_text_mobile(mobile_json, desired_headings):
    """
    mobile_json: JSON from mobile-sections endpoint
    desired_headings: list of heading strings to match (case-insensitive)
    returns: dict heading->text (first paragraph)
    """
    results = {}
    if not mobile_json:
        return results
    sections = []

    # mobile-sections format: 'lead' and 'sections'
    if "lead" in mobile_json and "sections" in mobile_json:
        lead_html = mobile_json["lead"].get("sections", [])
        # also gather all sections
        sections = mobile_json.get("remaining", {}).get("sections", []) + mobile_json.get("lead", {}).get("sections", [])
        # but easier: the 'sections' top-level may exist:
        sections = mobile_json.get("sections", []) or mobile_json.get("remaining", {}).get("sections", []) or []
        # some mobile responses put section list in 'sections'
    # fallback: try 'mobile_json.get("sections", [])'
    if not sections:
        sections = mobile_json.get("sections", []) or []

    # Normalize: each section may have 'id','anchor','text'
    for sec in sections:
        heading = sec.get("line") or sec.get("anchor") or sec.get("section")
        html = sec.get("html") or sec.get("text") or sec.get("content")
        if not heading or not html:
            continue
        heading_norm = heading.lower().strip()
        for desired in desired_headings:
            if desired.lower() in heading_norm:
                text = html_to_text(html)
                # take first paragraph / sentence
                results[desired] = first_n_sentences(text, n=2)
    return results

def extract_sections_actionparse(parse_json, desired_headings):
    """Fallback parser when using action=parse output"""
    results = {}
    parse = parse_json.get("parse", {})
    html = parse.get("text", {}).get("*", "")
    if not html:
        return results
    soup = BeautifulSoup(html, "html.parser")
    for heading in desired_headings:
        # find header tags containing heading text
        found = soup.find(lambda tag: tag.name in ["h2","h3","h4"] and heading.lower() in (tag.get_text() or "").lower())
        if found:
            # get next sibling paragraphs
            text_parts = []
            for sib in found.next_siblings:
                if sib.name and sib.name.startswith("h"):
                    break
                if sib.name == "p":
                    text_parts.append(sib.get_text(strip=True))
            if text_parts:
                results[heading] = first_n_sentences(" ".join(text_parts), n=2)
    return results

def answer_question(question):
    """
    Main entry:
    - searches Wikipedia
    - fetches summary + sections
    - returns short answer dict
    """
    title = search_wikipedia(question)
    if not title:
        return {"error": "No article found for query."}
    summary_json = get_summary(title)
    lead_text = summary_json.get("extract", "")
    source_url = summary_json.get("content_urls", {}).get("desktop", {}).get("page", f"https://en.wikipedia.org/wiki/{requests.utils.requote_uri(title)}")

    # Try mobile-sections for structured content
    sections_json = None
    try:
        sections_json = get_mobile_sections(title)
    except Exception:
        sections_json = None

    desired = ["Symptoms", "Signs and symptoms", "Cause", "Causes", "Treatment", "Management", "Medication", "Medications"]
    sections_text = {}
    if sections_json:
        sections_text = extract_section_text_mobile(sections_json, desired)
        # if empty, maybe this is action=parse output - try parse extractor
        if not sections_text and "parse" in sections_json:
            sections_text = extract_sections_actionparse(sections_json, desired)
    else:
        # Try action=parse fallback
        params = {"action": "parse", "page": title, "prop": "text|sections", "format": "json"}
        r = requests.get(WIKI_API, params=params, headers=HEADERS, timeout=10)
        if r.status_code == 200:
            try:
                sections_text = extract_sections_actionparse(r.json(), desired)
            except Exception:
                sections_text = {}

    # Build final concise answer
    answer = first_n_sentences(lead_text, n=5) if lead_text else ""

    # Specific short answers if user asks particular words
    resp = {
        "title": title,
        "answer": answer,
        "symptoms": sections_text.get("Symptoms") or sections_text.get("Signs and symptoms") or "",
        "causes": sections_text.get("Cause") or sections_text.get("Causes") or "",
        "treatment": sections_text.get("Treatment") or sections_text.get("Medication") or sections_text.get("Medications") or "",
        "source": source_url,
    }
    return resp

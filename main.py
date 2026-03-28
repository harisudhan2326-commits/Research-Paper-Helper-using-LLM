import os
import json
import re
from utils import extract_text_from_pdf
from ocr import extract_text_with_glm_ocr
from llm import refine_text


# ---------------- TEXT EXTRACTION ----------------
def extract_text(Input_Path):
    text = extract_text_from_pdf(Input_Path)

    if not text or len(text.strip()) < 500:
        print("Using OCR...")
        text = extract_text_with_glm_ocr(Input_Path)
    else:
        print("Text extracted using PDF Parser")

    return text


# ---------------- CLEANING ----------------
def clean_text(text):
    if not text:
        return ""

    text = text.encode("utf-8", "ignore").decode("utf-8", "ignore")

    text = re.sub(r"-\s*\n\s*", "", text)
    text = re.sub(r"\r", "\n", text)

    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    text = re.sub(r'(\d)([A-Za-z])', r'\1 \2', text)
    text = re.sub(r'([A-Za-z])(\d)', r'\1 \2', text)

    text = re.sub(r'([.,;:!?])([A-Za-z])', r'\1 \2', text)

    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n+", ". ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def trim_text(text):
    match = re.search(r'abstract', text, re.I)
    if match:
        text = text[match.start():]

    text = re.split(r'references', text, flags=re.I)[0]
    return text


def normalize_headings(text):
    text = re.sub(r'\bABSTRACT\b', 'Abstract', text)
    text = re.sub(r'\bINTRODUCTION\b', 'Introduction', text)
    text = re.sub(r'\bCONCLUSION\b', 'Conclusion', text)
    text = re.sub(r'\bMETHODS?\b', 'Methodology', text)
    text = re.sub(r'\bPROPOSED METHOD\b', 'Methodology', text)
    text = re.sub(r'\bSYSTEM MODEL\b', 'Methodology', text)
    return text


# ---------------- SECTION EXTRACTION ----------------
def extract_section(text, start, end_list):
    pattern = rf'{start}(.*?)(?={"|".join(end_list)})'
    match = re.search(pattern, text, re.I | re.S)

    if match:
        return match.group(1).strip()

    # fallback
    return text[:1000]


def extract_sections(text):
    sections = {}

    sections["Abstract"] = extract_section(
        text,
        r'abstract[:\s]*',
        ['introduction', 'keywords', 'index terms']
    )

    sections["Introduction"] = extract_section(
        text,
        r'introduction[:\s]*',
        ['related work', 'method', 'proposed', 'system model']
    )

    sections["Methodology"] = extract_section(
        text,
        r'(methodology|proposed method|system model)[:\s]*',
        ['results', 'discussion', 'conclusion', 'evaluation']
    )

    sections["Conclusion"] = extract_section(
        text,
        r'(conclusion|results and discussion)[:\s]*',
        ['references', 'acknowledgement']
    )

    return sections


# ---------------- KEYWORD EXTRACTION ----------------
def extract_by_keywords(text, keywords):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    scored = []

    for sent in sentences:
        score = 0

        for kw in keywords:
            if kw in sent.lower():
                score += 1

        if any(x in sent.lower() for x in ["model", "system", "algorithm"]):
            score += 1

        if len(sent.split()) > 6:
            scored.append((score, sent.strip()))

    scored = sorted(scored, reverse=True)

    best = [s for score, s in scored if score > 0]

    return " ".join(best[:2]) if best else ""


# ---------------- KEYWORDS ----------------
CONTRIBUTION_KEYWORDS = [
    "we propose",
    "we present",
    "this paper proposes",
    "this work introduces",
    "the novel",
    "our contribution",
    "we develop",
    "we design",
    "framework"
]

PROPOSED_KEYWORDS = [
    "proposed method",
    "proposed system",
    "our approach",
    "framework",
    "model",
    "architecture",
    "algorithm"
]

LIMITATION_KEYWORDS = [
    "limitation",
    "however",
    "challenge",
    "drawback",
    "low accuracy",
    "false alarm",
    "issue"
]

FUTURE_KEYWORDS = [
    "future work",
    "in future",
    "further research",
    "can be extended",
    "next step"
]


# ---------------- BUILD OUTPUT ----------------
def build_output(sections):
    intro = sections.get("Introduction", "")
    method = sections.get("Methodology", "")
    conclusion = sections.get("Conclusion", "")

    core = extract_by_keywords(method, CONTRIBUTION_KEYWORDS)
    proposed = extract_by_keywords(method, PROPOSED_KEYWORDS)
    limitation = extract_by_keywords(conclusion, LIMITATION_KEYWORDS)
    future = extract_by_keywords(conclusion, FUTURE_KEYWORDS)

    return {
        "Abstract": sections.get("Abstract", "")[:800] or "Not found",
        "Problem Statement": intro[:400] or "Not found",
        "Core Contribution": core if core else "Not found",
        "Proposed Work": proposed if proposed else "Not found",
        "Limitations": limitation if limitation else "Not found",
        "Future Work": future if future else "Not found"
    }


# ---------------- MAIN PIPELINE ----------------
def process_paper(Input_Path):

    if not os.path.exists(Input_Path):
        return {"error": "Input file not found"}

    text = extract_text(Input_Path)

    if not text or len(text.strip()) < 300:
        return {"error": "Text extraction failed"}

    # CLEAN
    text = clean_text(text)
    text = trim_text(text)
    text = normalize_headings(text)


    # EXTRACT SECTIONS
    sections = extract_sections(text)

    # FALLBACKS
    if not sections["Methodology"]:
        sections["Methodology"] = sections["Introduction"]

    if not sections["Conclusion"]:
        sections["Conclusion"] = sections["Methodology"]

    # BUILD OUTPUT
    result = build_output(sections)

    # LLM REFINEMENT (SAFE)
    for key in result:
        if result[key] != "Not found" and len(result[key].split()) > 10:

            refined = refine_text(result[key])

            if refined and len(refined.split()) >= 5:
                result[key] = refined

    # WEAK OUTPUT FILTER
    for k, v in result.items():
        if not v or len(v.split()) < 5:
            result[k] = "Not found"

    return result


# ---------------- SAVE ----------------
def save_output(result):
    os.makedirs("outputs", exist_ok=True)
    path = os.path.join("outputs", "results.json")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)

    return path


# ---------------- MAIN ----------------
def main():
    path = input("Enter PDF Path: ")

    result = process_paper(path)

    print("\n-------- OUTPUT --------\n")
    print(result)

    save_output(result)


if __name__ == "__main__":
    main()
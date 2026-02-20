import os
import json
from utils import extract_text_from_pdf
from ocr import extract_text_with_glm_ocr
from llm import generate_research_summary


Input_Path = r"D:\Phd works\Proposal & Paper Works\Carbon Foot Print\FL soln.pdf"
Output_Path = "outputs/results.json"

def prompt_builder(text):
    return f"""
Consider yourself as an academic research assistant.

Extract and simplify the following sections of the research paper:
Return the output STRICTLY in this exact format:

Abstract:
<write here>

Problem Statement:
<write here>

Core Contribution:
<write here>

Proposed Work:
<write here>

Limitations:
<write here>

Future Work:
<write here>

Rules:
- Do NOT add extra commentary.
- Do NOT add introduction text.
- Do NOT explain anything outside the sections.
- Only output in the above format.

Research Paper:
{text}
"""
def main():

    # File exist or not
    if not os.path.exists(Input_Path):
        print("Input file not found.")
        return
    
    # PDF text extraction 
    text = extract_text_from_pdf(Input_Path)

    # GLM-OCR Fallback Mechanism if pdf is not text
    if not text or len(text.strip()) < 500:
        text = extract_text_with_glm_ocr(Input_Path)
    
    text = text[:6000]

    # Providing Extacted input to the model
    prompt = prompt_builder(text)
    result  = generate_research_summary(prompt)
    print(result)

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    Output_Path = os.path.join(BASE_DIR, "outputs", "results.json")

    with open(Output_Path, "w", encoding="utf-8") as f:
        json.dump({"summary": result}, f, indent=4)


if __name__ == "__main__":
    main()

   
   
    
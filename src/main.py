import os
import json
from utils import extract_text_from_pdf


Input_Path = "data/sample.pdf"
Output_Path = "outputs/results.json"

def prompt_builder(text):
    return f"""
Consider yourself as an academic research assistant.

Extract and simplify the following sections of the research paper:
1. Abstract
2. Problem Statement
3. Core Contribution
4. Proposed Work
5. Limitations
6. Future Work

Provide the output clealry in section wise.

Research Paper Text:
{text}
"""
def main():

    #File exist or not
    if not os.path.exists(Input_Path):
        print("Input file not found.")
        return
    
    # PDF text extraction
    text = extract_text_from_pdf(Input_Path)
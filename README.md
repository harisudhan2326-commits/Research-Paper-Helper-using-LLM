# Research Paper Helper using Large Language Models

## Overview
Reading and understanding research papers is challenging for beginner researchers due to complex language, dense technical content, and scattered information across sections. This project presents a **Research Paper Helper** that assists new readers by extracting and simplifying key sections of a research paper using a Large Language Model (LLM).

The system focuses on improving readability and comprehension without replacing manual reading or expert judgment.

---

## Problem Statement
Beginner researchers often struggle to quickly identify the core problem, contributions, limitations, and future research directions in academic papers. There is a need for a system that can automatically analyze research papers and present important sections in a simplified and structured format to reduce cognitive load for new readers.

---

## Objectives
- Simplify the reading process of research papers for beginners
- Extract and summarize important sections such as:
  - Abstract
  - Problem Statement
  - Contributions
  - Proposed Work
  - Limitations
  - Future Work
- Support both text-based and scanned research papers
- Demonstrate practical use of prompt engineering with LLMs

---

## System Overview
The system accepts a research paper in PDF format as input. If the document is image-based or scanned, GLM-OCR is used as a pre-processing step to extract machine-readable text. For text-based PDFs, OCR is skipped and the text is extracted directly. The extracted text is then processed by a Large Language Model deployed locally using Ollama named Phi-2: a 2.7B . Through carefully designed prompts, the LLM analyzes and simplifies key sections of the paper, presenting them in a structured and beginner-friendly format.

---

## Technology Stack

### Hardware
- Device: HP Pavilion Gaming Laptop 15-ec2xxx
- Processor: AMD Ryzen 5 5600H (3.30 GHz)
- RAM: 8 GB
- Graphics: 4 GB GPU
- Storage: 500 GB
- OS Type: 64-bit

### Software
- Operating System: Windows 11 Home (64-bit)
- Programming Language: Python
- OCR Model: GLM-OCR (used only for scanned/image-based documents)
- LLM Runtime: Ollama
- LLM Model: Phi-2 (2.7B parameters)
- Libraries: pdfplumber, os, subprocess
- Version Control: Git & GitHub

---

## Methodology
1. Input research paper is provided in PDF format.
2. If the document is scanned or image-based, GLM-OCR extracts the text.
3. If the document is text-based, text is extracted directly without OCR.
4. The extracted text is segmented section-wise.
5. Prompt-engineered instructions guide the LLM to extract and simplify each section.
6. Structured output is generated for easy understanding.

---

## Model Selection Rationale
Due to limited hardware resources, the system uses lightweight models for local inference. 
GLM-OCR is employed only for text extraction from scanned documents, while **Phi-2 (2.7B parameters)** is selected as the primary Large Language Model to balance performance and computational efficiency. 
The focus of this project is prompt engineering and system design rather than model scale.


## Limitations
- The system does not verify factual correctness.
- OCR accuracy depends on document quality.
- Simplification may be generic for highly technical papers.
- Outputs should be reviewed by the user for accuracy.

---

## Applications
- Academic learning assistance
- Research paper overview for students
- Literature review support
- Portfolio demonstration project

---

## Disclaimer
This tool is designed to assist research paper reading and does not replace expert analysis or peer review.


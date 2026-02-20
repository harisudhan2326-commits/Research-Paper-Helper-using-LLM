import os
from ollama import chat
from pdf2image import convert_from_path

def extract_text_with_glm_ocr(pdf_path):
    emp_text = ""
    pages = convert_from_path(pdf_path)
    for i,page in enumerate (pages):
        temp_path = f"temp_page{i}.png"
        page.save(temp_path)

        response = chat(
            model="glm-ocr",
            messages=[
                {
                    "role": "user",
                    "content": "Extract all readable text from this image",
                    "images": [temp_path]
                }
            ]
        )

        extracted  = response["message"]["content"]
        emp_text += extracted + "\n"
        os.remove(temp_path)
    return emp_text
    
        

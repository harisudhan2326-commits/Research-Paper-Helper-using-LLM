import subprocess

def refine_text(text):

    prompt = f"""
Simplify the following research text.

Rules:
- Keep same meaning
- Make it concise
- Do NOT add examples
- Do NOT explain

Text:
{text}

Answer:
"""

    try:
        result = subprocess.run(
            ["ollama", "run", "phi:2.7b"],  
            input=prompt,
            text=True,
            encoding="utf-8",
            errors="ignore",
            capture_output=True
        )

        output = result.stdout.strip()

        if not output:
            return text
        
        bad_words = ["in short", "simplified","example","#","imagine"]
        if any(w in output.lower() for w in bad_words):
            return text

        if len(output) > len(text) * 1.5:
            return text

        # Filtering the Garbage 
        if any(x in output.lower() for x in ["example", "conversation"]):
            return text

        return output

    except:
        return text
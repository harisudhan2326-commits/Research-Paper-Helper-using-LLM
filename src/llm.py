from ollama import chat

def generate_research_summary(prompt, model="phi:2.7b"):
    response = chat(
        model = model, 
        messages = [
            {
                "role" : "user",
                "content" : prompt
            }
        ]
    )
    return response["message"]["content"]
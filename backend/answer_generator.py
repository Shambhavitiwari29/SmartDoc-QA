import requests


def generate_answer(context, question):

    prompt = f"""
    Context:
    {context}

    Question:
    {question}

    Answer based only on the context above.
    """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]
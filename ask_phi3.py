from ollama import chat

print("Medical Assistant - Phi-3")
print("Type 'quit' to exit.\n")

while True:
    question = input("You: ")

    if question.lower() == "quit":
        break

    response = chat(
        model="phi3",
        messages=[
    {
        "role": "system",
        "content": (
            "You are a helpful assistant. "
            "Answer questions accurately and concisely. "
            "If you are uncertain about an answer, say that you are uncertain "
            "rather than inventing information."
        ),
    },
    {
        "role": "user",
        "content": question,
    },
]
    )

    print(f"Phi-3: {response['message']['content']}\n")

import os
from dotenv import load_dotenv
from hindsight_client import Hindsight
from groq import Groq

load_dotenv()

# Hindsight
client = Hindsight(
    base_url="http://localhost:8888"
)

BANK_ID = "deal-intelligence"

# Groq
groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

print("======================================")
print("       DEAL INTELLIGENCE AGENT")
print("======================================")

while True:

    question = input("\nAsk about the deal (or type 'exit'): ")

    if question.lower() == "exit":
        print("Goodbye!")
        break

    print("\n🔎 Searching deal memory...")

    response = client.recall(
        bank_id=BANK_ID,
        query=question,
        max_tokens=1500
    )

    memory_text = "\n".join(
        f"- {result.text}"
        for result in response.results
    )

    if not memory_text:
        print("No relevant deal information found.")
        continue

    prompt = f"""
You are a Deal Intelligence Agent.

Answer the user's question using ONLY the retrieved deal memory below.

Retrieved deal memory:
{memory_text}

User question:
{question}

Give a concise, useful sales intelligence answer.

If the memory does not contain enough information, say:
"Insufficient information in deal memory."

Do not invent facts.
"""

    print("\n🧠 DEAL INTELLIGENCE:\n")

    result = groq_client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=600
    )

    print(result.choices[0].message.content)
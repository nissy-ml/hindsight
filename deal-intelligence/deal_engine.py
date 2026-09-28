import os
from dotenv import load_dotenv
from hindsight_client import Hindsight
from groq import Groq

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

load_dotenv()

HINDSIGHT_URL = os.getenv(
    "HINDSIGHT_URL",
    "http://localhost:8888"
)

BANK_ID = "deal-intelligence"

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is missing. Check your .env file."
    )

hindsight = Hindsight(HINDSIGHT_URL)

groq = Groq(
    api_key=GROQ_API_KEY
)

MODEL = "openai/gpt-oss-20b"


# --------------------------------------------------
# SEARCH DEAL MEMORY
# --------------------------------------------------

def search_deal(company_name):
    """Retrieve relevant memories for a company/deal."""

    print(f"\n🔎 Searching deal memory for: {company_name}")

    try:
        results = hindsight.recall(
            bank_id=BANK_ID,
            query=company_name
        )

        if not results:
            print(
                f"\n❌ No deal information found for "
                f"'{company_name}'."
            )
            return []

        memories = []

        for result in results:

            if hasattr(result, "text") and result.text:
                text = result.text.strip()

                if text and text not in memories:
                    memories.append(text)

        if not memories:
            print("\n❌ No useful memory found.")
            return []

        print(
            f"\n✅ Retrieved {len(memories)} "
            "relevant memory records."
        )

        return memories

    except Exception as e:

        print(f"\n❌ Memory search failed:")
        print(e)

        return []


# --------------------------------------------------
# GENERATE DEAL REPORT
# --------------------------------------------------

def generate_report(company_name, memories):
    """Generate a professional deal intelligence report."""

    context = "\n".join(memories)

    prompt = f"""
You are an expert Deal Intelligence Assistant.

Company / Deal:
{company_name}

Use ONLY the information contained in DEAL MEMORY.

Do not invent facts.
Do not assume missing information.
If information is unavailable, write "Not available".

Your job is to analyze the deal and provide useful,
precise and practical information for a sales representative.

DEAL MEMORY:
{context}

Create the report using these sections:

## DEAL SUMMARY

Give a concise overview of the deal.

## DEAL DETAILS

- Deal value
- Industry
- Deal stage
- Decision maker

## CUSTOMER NEEDS

List the customer's important requirements.

## CUSTOMER CONCERNS

List pricing, implementation, technical,
business or other concerns.

## BUYING SIGNALS

List evidence showing customer interest.

## COMPETITORS

List known competitors.

## DEAL RISKS

List risks supported by the memory.

## COMMERCIAL INFORMATION

Include pricing, discounts, deadlines,
contract information and commercial conditions.

## KEY INSIGHTS

Give 3-5 important insights.

## DEAL READINESS

Give a factual assessment using:

- Ready to progress
- Needs clarification
- Significant risks

Choose the category ONLY from evidence
contained in the deal memory.

Explain the evidence briefly.

## RECOMMENDED NEXT ACTIONS

Give practical actions for the sales team.

## INFORMATION GAPS

List important information that is still missing.

Keep the response professional, concise and
easy for a salesperson to understand.
"""

    try:

        response = groq.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a precise enterprise "
                        "sales intelligence assistant."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_tokens=1800
        )

        return response.choices[0].message.content.strip()

    except Exception as e:

        print("\n❌ Report generation failed:")
        print(e)

        return None


# --------------------------------------------------
# LEARN NEW INFORMATION
# --------------------------------------------------

def learn_from_user(company_name, user_message):
    """
    Detect useful new deal information from the user
    and permanently store it in Hindsight.
    """

    prompt = f"""
You are the long-term memory system of a
Deal Intelligence Agent.

Company:
{company_name}

New message from the user:
{user_message}

Determine whether this message contains NEW,
USEFUL information about the company's deal.

Useful information includes:

- customer updates
- new requirements
- customer concerns
- decision makers
- competitors
- pricing
- discounts
- implementation timelines
- meetings
- customer commitments
- decisions
- deal-stage changes
- next actions
- important sales observations
- newly learned facts

If the message contains useful information,
extract ONLY the facts that should be remembered.

Do NOT invent information.

If there is nothing useful to remember,
return exactly:

NO_NEW_INFORMATION
"""

    try:

        response = groq.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You extract important long-term "
                        "deal memory accurately."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0,
            max_tokens=500
        )

        memory = response.choices[0].message.content.strip()

        if memory == "NO_NEW_INFORMATION":

            print(
                "\nℹ️ No new deal information "
                "was detected."
            )

            return False

        # Store new information in Hindsight
        hindsight.retain(
            bank_id=BANK_ID,
            content=f"""
Deal: {company_name}

New information learned from user:

{memory}
"""
        )

        print("\n🧠 NEW INFORMATION LEARNED")
        print("-" * 60)
        print(memory)
        print("-" * 60)

        print(
            "✅ Information permanently stored "
            "in deal memory."
        )

        return True

    except Exception as e:

        print("\n❌ Could not store new information:")
        print(e)

        return False


# --------------------------------------------------
# ANSWER USER'S QUESTION
# --------------------------------------------------

def answer_question(company_name, memories, question):
    """Answer a user's question using deal memory."""

    context = "\n".join(memories)

    prompt = f"""
You are a friendly Deal Intelligence Assistant.

Company:
{company_name}

DEAL MEMORY:
{context}

USER QUESTION:
{question}

Rules:

1. Answer using the available deal memory.
2. Do not invent facts.
3. If the information is unavailable,
   clearly say that it is not available.
4. Be concise but useful.
5. Give precise deal-related details.
6. If appropriate, mention the evidence supporting
   your answer.
7. If the user asks what should happen next,
   provide practical actions based on the evidence.
"""

    try:

        response = groq.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a friendly and precise "
                        "enterprise deal intelligence assistant."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_tokens=800
        )

        return response.choices[0].message.content.strip()

    except Exception as e:

        print("\n❌ Question answering failed:")
        print(e)

        return None


# --------------------------------------------------
# MAIN PROGRAM
# --------------------------------------------------

def main():

    print("\n" + "=" * 70)
    print("             🤖 DEAL INTELLIGENCE AGENT")
    print("=" * 70)

    company = input(
        "\nEnter company/deal name "
        "(example: Acme Corporation): "
    ).strip()

    if not company:

        print("\n❌ Please enter a company or deal name.")
        return

    # ----------------------------------------------
    # STEP 1: SEARCH MEMORY
    # ----------------------------------------------

    memories = search_deal(company)

    if not memories:
        return

    # ----------------------------------------------
    # STEP 2: GENERATE REPORT
    # ----------------------------------------------

    print("\n🧠 Generating Deal Intelligence Report...")

    report = generate_report(
        company,
        memories
    )

    if report:

        print("\n")
        print("=" * 70)
        print("              DEAL INTELLIGENCE REPORT")
        print("=" * 70)

        print(report)

        print("=" * 70)

    # ----------------------------------------------
    # STEP 3: CONTINUOUS CHAT
    # ----------------------------------------------

    print("\n")
    print("💬 You can now ask questions about this deal.")
    print(
        "Type 'exit' to leave the deal conversation."
    )

    while True:

        print("\n" + "-" * 70)

        question = input(
            "You: "
        ).strip()

        if not question:
            continue

        if question.lower() in [
            "exit",
            "quit",
            "bye"
        ]:

            print(
                "\n👋 Deal conversation ended."
            )

            break

        # ------------------------------------------
        # STEP 4: CHECK FOR NEW INFORMATION
        # ------------------------------------------

        learn_from_user(
            company,
            question
        )

        # ------------------------------------------
        # STEP 5: REFRESH MEMORY
        # ------------------------------------------

        updated_memories = search_deal(
            company
        )

        if updated_memories:
            memories = updated_memories

        # ------------------------------------------
        # STEP 6: ANSWER QUESTION
        # ------------------------------------------

        answer = answer_question(
            company,
            memories,
            question
        )

        if answer:

            print("\n🤖 Deal Intelligence Agent:")
            print(answer)

    print("\n")
    print("=" * 70)
    print("              SESSION COMPLETED")
    print("=" * 70)


# --------------------------------------------------
# START PROGRAM
# --------------------------------------------------

if __name__ == "__main__":
    main()
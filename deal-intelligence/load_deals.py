import json
import os
import time
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

HINDSIGHT_URL = os.getenv("HINDSIGHT_URL", "http://localhost:8888")
BANK_ID = "deal-intelligence"

client = Hindsight(HINDSIGHT_URL)


# Load realistic deal data
with open("deals.json", "r", encoding="utf-8") as file:
    deals = json.load(file)


for deal in deals[2:3]:
    customer = deal["customer"]

    deal_text = f"""
Deal ID: {deal["deal_id"]}
Customer: {deal["customer"]}
Industry: {deal["industry"]}
Deal Value: {deal["deal_value"]}
Stage: {deal["stage"]}
Decision Maker: {deal["decision_maker"]}

Customer Needs:
{", ".join(deal["customer_needs"])}

Customer Concerns:
{", ".join(deal["customer_concerns"])}

Competitors:
{", ".join(deal["competitors"])}

Buying Signals:
{", ".join(deal["buying_signals"])}

Risks:
{", ".join(deal["risks"])}

Last Interaction:
{deal["last_interaction"]}

Commercial Terms:
{deal["commercial_terms"]}
"""

    print(f"\nStoring {customer}...")

    try:
        client.retain(
            bank_id=BANK_ID,
            content=deal_text
        )

        print(f"✅ {customer} stored successfully")

    except Exception as e:
        print(f"❌ Failed to store {customer}")
        print(e)

    # Small delay between deals
    time.sleep(2)


print("\n🎉 Finished loading deal data!")
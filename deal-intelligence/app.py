import os
import json
from dotenv import load_dotenv
from hindsight_client import Hindsight

# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

HINDSIGHT_URL = os.getenv(
    "HINDSIGHT_URL",
    "http://localhost:8888"
)

BANK_ID = "deal-intelligence"

DEALS_FILE = "deals.json"

client = Hindsight(HINDSIGHT_URL)


# ============================================================
# LOAD DEALS
# ============================================================

def load_deals():

    print("\n" + "=" * 70)
    print("        DEAL INTELLIGENCE DATA LOADER")
    print("=" * 70)

    if not os.path.exists(DEALS_FILE):

        print(f"\n❌ {DEALS_FILE} not found.")

        return

    try:

        with open(
            DEALS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            deals = json.load(file)

    except Exception as e:

        print("\n❌ Could not read deals.json")
        print(e)

        return

    print(
        f"\n📦 Found {len(deals)} deals in {DEALS_FILE}"
    )

    successful = 0
    failed = 0

    # --------------------------------------------------------
    # STORE EVERY DEAL
    # --------------------------------------------------------

    for deal in deals:

        customer = deal.get(
            "customer",
            "Unknown Customer"
        )

        deal_id = deal.get(
            "deal_id",
            "Unknown ID"
        )

        print("\n" + "-" * 70)

        print(
            f"📥 Loading {deal_id} - {customer}"
        )

        # Convert JSON object into readable memory
        deal_text = f"""
Deal ID: {deal.get("deal_id")}

Customer: {deal.get("customer")}

Industry: {deal.get("industry")}

Deal Value: {deal.get("deal_value")}

Stage: {deal.get("stage")}

Decision Maker: {deal.get("decision_maker")}

Customer Needs:
{chr(10).join("- " + item for item in deal.get("customer_needs", []))}

Customer Concerns:
{chr(10).join("- " + item for item in deal.get("customer_concerns", []))}

Competitors:
{chr(10).join("- " + item for item in deal.get("competitors", []))}

Buying Signals:
{chr(10).join("- " + item for item in deal.get("buying_signals", []))}

Risks:
{chr(10).join("- " + item for item in deal.get("risks", []))}

Last Interaction:
{deal.get("last_interaction")}

Commercial Terms:
{deal.get("commercial_terms")}
"""

        try:

            client.retain(
                bank_id=BANK_ID,
                content=deal_text
            )

            print(
                f"✅ Successfully stored {customer}"
            )

            successful += 1

        except Exception as e:

            print(
                f"❌ Failed to store {customer}"
            )

            print(e)

            failed += 1

    # --------------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------------

    print("\n" + "=" * 70)

    print("              DATA LOADING COMPLETE")

    print("=" * 70)

    print(
        f"\n✅ Successfully stored: {successful}"
    )

    print(
        f"❌ Failed: {failed}"
    )

    print(
        f"📦 Total deals: {len(deals)}"
    )

    print("\n")


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    load_deals()
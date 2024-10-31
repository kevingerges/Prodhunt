from dotenv import load_dotenv
from datetime import datetime
import json
import os
from pathlib import Path

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from business_plan.core.business_plan_crew import BusinessPlanCrew


def setup_folders():
    """Create necessary folders for output"""
    folders = ['output', 'logs']
    for folder in folders:
        Path(folder).mkdir(exist_ok=True)


def get_non_empty_input(prompt_text):
    """Prompt the user for input until they provide a non-empty response."""
    while True:
        user_input = input(prompt_text).strip()
        if user_input:
            return user_input
        else:
            print("This field is required. Please enter a value.")



def get_business_input() -> dict:
    """Gather business plan input from user with validation."""
    print("\n=== Business Plan Generator ===\n")

    return {
        "input_data": {
            "business_idea": get_non_empty_input("Enter your business idea: "),
            "industry": get_non_empty_input("Enter the industry: "),
            "scale": get_non_empty_input("Enter business scale (Local/Regional/National/Global): "),
            "target_market": get_non_empty_input("Enter target market: "),
            "initial_investment": get_non_empty_input("Enter estimated initial investment: "),
            "timeline": get_non_empty_input("Enter expected timeline to launch: ")
        }
    }


def save_results(results: dict, timestamp: str):
    """Save results to files"""
    if results.get("document"):
        with open(f"output/business_plan_{timestamp}.md", 'w') as f:
            f.write(results["document"])

    with open(f"output/metrics_{timestamp}.json", 'w') as f:
        json.dump({
            "metrics": results.get("metrics", {}),
            "validation": results.get("validation", {}),
            "execution_time": results.get("execution_time", "")
        }, f, indent=2)


def run():
    """Main execution function"""
    try:
        # environment variables
        load_dotenv()

        setup_folders()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        print("\nGathering business information...")
        business_context = get_business_input()

        with open(f"output/input_{timestamp}.json", "w") as f:
            json.dump(business_context, f, indent=2)

        print("\nInitializing business plan generation...")
        crew = BusinessPlanCrew()

        print("\nGenerating business plan...")
        results = crew.execute_analysis(business_context)


        print("\nSaving results...")
        save_results(results, timestamp)

        if results["status"] == "success":
            print("\n=== Generation Complete ===")
            print(f"Business plan saved as: business_plan_{timestamp}.md")
            print(f"Metrics saved as: metrics_{timestamp}.json")

            if results.get("metrics", {}).get("warnings"):
                print("\nWarnings:")
                for warning in results["metrics"]["warnings"]:
                    print(f"- {warning}")
        else:
            print("\n=== Generation Failed ===")
            print(f"Error: {results.get('error_message', 'Unknown error')}")

    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user. Exiting gracefully...")
    except Exception as e:
        print(f"\nError: {str(e)}")
        raise


if __name__ == "__main__":
    run()
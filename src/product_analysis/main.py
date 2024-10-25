#!/usr/bin/env python
from crew import BusinessPlanCrew
from dotenv import load_dotenv
import os
import sys
from datetime import datetime


def format_crew_output(output):
    """Convert CrewOutput to formatted string."""
    if hasattr(output, 'raw_output'):
        return str(output.raw_output)
    return str(output)


def run():
    load_dotenv()
    print("\n=== Business Plan Analysis Tool ===")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Using Python: {sys.version.split()[0]}")
    print(f"OLLAMA_BASE_URL: {os.getenv('OLLAMA_BASE_URL')}")
    print(f"OPENAI_MODEL_NAME: {os.getenv('OPENAI_MODEL_NAME')}")
    print("\n" + "=" * 40 + "\n")

    try:
        business_idea = input("Enter your business idea: ")
        print(f"\nAnalyzing: {business_idea}\n")

        inputs = {"business_idea": business_idea}

        crew = BusinessPlanCrew().crew()

        print("\nStarting analysis...\n")
        result = crew.kickoff(inputs=inputs)

        # Convert result to string
        formatted_result = format_crew_output(result)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"business_plan_{timestamp}.txt"

        with open(filename, "w") as f:
            f.write(f"Business Plan Analysis for: {business_idea}\n")
            f.write("=" * 50 + "\n\n")
            f.write(formatted_result)

        print(f"\nAnalysis complete! Results saved to: {filename}")
        print("\n" + formatted_result)

    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user. Exiting gracefully...")
    except Exception as e:
        print("\nAn unexpected error occurred:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print("\nPlease check your configuration and try again.")
    finally:
        print("\n=== Analysis Session Complete ===\n")


if __name__ == "__main__":
    run()
from business_input import BusinessInputProcessor
from crew import BusinessPlanCrew
from dotenv import load_dotenv
from datetime import datetime
import json

def run():
    load_dotenv()
    # Initialize input processor
    input_processor = BusinessInputProcessor()

    try:
        # Get processed business context
        business_context = input_processor.process_business_idea()

        # Save raw input for reference
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(f"business_input_{timestamp}.json", "w") as f:
            json.dump(business_context, f, indent=2)

        # Initialize and run crew with enhanced context
        crew = BusinessPlanCrew()
        result = crew.execute_analysis(business_context)

        # Convert the output to a string representation to handle any non-serializable types
        result_output = json.dumps(result["result"], indent=2, default=str)

        # Write output to file
        with open(f"business_output_{timestamp}.json", "w") as f:
            f.write(result_output)

        print("\nOutput saved successfully.")

    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user. Exiting gracefully...")
    except Exception as e:
        print(f"\nError: {str(e)}")
        raise

if __name__ == "__main__":
    run()

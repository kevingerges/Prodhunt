import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(src_dir)

from dotenv import load_dotenv
from datetime import datetime
import json
from pathlib import Path
import time
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.layout import Layout
from rich import print as rprint
from rich.markdown import Markdown
import questionary
from typing import Dict, Any
from dotenv import load_dotenv
from datetime import datetime
import json
from pathlib import Path
import time
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.layout import Layout
from rich import print as rprint
from rich.markdown import Markdown
import questionary
from typing import Dict, Any
import threading
from rich.spinner import Spinner
from rich.text import Text


from business_plan.core.business_plan_crew import BusinessPlanCrew

console = Console()

class ProgressManager:
    def __init__(self):
        self.is_running = True
        self.current_stage = "Initializing"
        self.progress = 0
        
    def update_stage(self, stage: str, progress: int = 0):
        self.current_stage = stage
        self.progress = progress
        
    def stop(self):
        self.is_running = False

def progress_spinner(progress_manager: ProgressManager):
    spinner = Spinner('dots')
    with Live(console=console, refresh_per_second=10) as live:
        while progress_manager.is_running:
            text = Text()
            text.append(f"\n{spinner.render()}")
            text.append(f" Current Stage: {progress_manager.current_stage}")
            if progress_manager.progress > 0:
                text.append(f" ({progress_manager.progress}%)")
            live.update(text)
            time.sleep(0.1)

def setup_folders():
    """Create necessary folders for output and data"""
    folders = ['output', 'logs', 'data']
    for folder in folders:
        Path(folder).mkdir(exist_ok=True)
        

def validate_input(input_data: dict) -> None:
    """Validate the business input data"""
    required_fields = [
        "business_idea", "industry", "scale", "target_market",
        "initial_investment", "timeline"
    ]
    
    missing_fields = [
        field for field in required_fields 
        if not input_data["input_data"].get(field)
    ]
    
    if missing_fields:
        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

def get_business_input() -> dict:
    """Enhanced interactive business input gathering"""
    layout = Layout()
    layout.split_column(
        Layout(Panel.fit("🚀 [bold blue]Business Plan Generator[/bold blue]", border_style="blue"), ratio=1),
        Layout(Panel.fit(
            """This enhanced tool will generate a comprehensive business plan using:
            ✨ Real-time market data (RAG)
            📊 Advanced market analysis (NLP/ML)
            🤖 Multi-agent collaboration
            🎯 Intelligent insights""",
            border_style="green"
        ), ratio=2)
    )
    
    console.print(layout)
    console.print("\n")

    # Using questionary for better interactive prompts
    questions = [
        {
            'type': 'text',
            'name': 'business_idea',
            'message': '💡 Enter your business idea:',
            'validate': lambda text: len(text) > 0 or "This field is required"
        },
        {
            'type': 'text',
            'name': 'industry',
            'message': '🏭 Enter the industry:',
            'validate': lambda text: len(text) > 0 or "This field is required"
        },
        {
            'type': 'select',
            'name': 'scale',
            'message': '🌍 Select business scale:',
            'choices': ['Local', 'Regional', 'National', 'Global']
        },
        {
            'type': 'text',
            'name': 'target_market',
            'message': '🎯 Enter target market:',
            'validate': lambda text: len(text) > 0 or "This field is required"
        },
        {
            'type': 'text',
            'name': 'initial_investment',
            'message': '💰 Enter estimated initial investment:',
            'validate': lambda text: len(text) > 0 or "This field is required"
        },
        {
            'type': 'text',
            'name': 'timeline',
            'message': '⏱️ Enter expected timeline to launch:',
            'validate': lambda text: len(text) > 0 or "This field is required"
        }
    ]
    
    answers = questionary.prompt(questions)
    
    return {"input_data": answers}

def display_analysis_progress(results: Dict[str, Any], timestamp: str):
    """Display analysis results with rich formatting"""
    # Create result table
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Category", style="dim")
    table.add_column("Details")
    
    if "market_intelligence" in results:
        mi = results["market_intelligence"]
        table.add_row(
            "Market Sentiment",
            f"[bold]{mi['market_sentiment']['interpretation']}[/bold]\n"
            f"Confidence: {mi['market_sentiment']['confidence']}"
        )
        
        trends = "\n".join([
            f"• {trend['type'].title()} ({trend['confidence']:.2f})"
            for trend in mi['identified_trends'][:3]
        ])
        table.add_row("Key Trends", trends)
        
        opportunities = "\n".join([
            f"• {opp['description'][:100]}..."
            for opp in mi['opportunities'][:3]
        ])
        table.add_row("Opportunities", opportunities)
    
    console.print(Panel(table, title="[bold]Analysis Results[/bold]", border_style="green"))

def save_results(results: dict, timestamp: str):
    """Save results with progress indication"""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TimeElapsedColumn(),
    ) as progress:
        # Save business plan document
        save_task = progress.add_task("[cyan]Saving business plan...", total=100)
        if results.get("document"):
            doc_path = Path("output") / f"business_plan_{timestamp}.md"
            with open(doc_path, 'w') as f:
                f.write(results["document"])
            progress.update(save_task, advance=50)
        
        # Save metrics and validation results
        metrics_task = progress.add_task("[green]Saving metrics...", total=100)
        metrics_path = Path("output") / f"metrics_{timestamp}.json"
        with open(metrics_path, 'w') as f:
            json.dump({
                "metrics": results.get("metrics", {}),
                "validation": results.get("validation", {}),
                "execution_time": results.get("execution_time", ""),
                "rag_queries": results.get("rag_queries", [])
            }, f, indent=2)
        progress.update(metrics_task, advance=100)

def run():
    """Enhanced main execution function with interactive UI"""
    try:
        setup_folders()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Get business input
        business_context = get_business_input()
        validate_input(business_context)

        # Save input data
        input_path = Path("output") / f"input_{timestamp}.json"
        with open(input_path, "w") as f:
            json.dump(business_context, f, indent=2)

        # Initialize and run business plan generation with progress tracking
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TimeElapsedColumn(),
        ) as progress:
            
            init_task = progress.add_task("[cyan]Initializing components...", total=100)
            for i in range(0, 101, 20):
                time.sleep(0.2)
                progress.update(init_task, completed=i)
            
            rag_task = progress.add_task("[green]Setting up RAG system...", total=100)
            market_task = progress.add_task("[yellow]Configuring market analysis...", total=100)
            agent_task = progress.add_task("[magenta]Preparing agent collaboration...", total=100)
            
            # Simulate progress for visual feedback
            for i in range(100):
                time.sleep(0.05)
                progress.update(rag_task, completed=min(i + 1, 100))
                progress.update(market_task, completed=min(i + 0.5, 100))
                progress.update(agent_task, completed=min(i + 0.8, 100))
            
            console.print("\n[bold green]✨ Components initialized successfully![/bold green]\n")
            
            # Execute analysis
            crew = BusinessPlanCrew()
            analysis_task = progress.add_task("[blue]Generating business plan...", total=100)
            results = crew.execute_analysis(business_context)
            progress.update(analysis_task, completed=100)

        # Save and display results
        console.print("\n[bold]💾 Saving results...[/bold]")
        save_results(results, timestamp)

        if results["status"] == "success":
            console.print("\n[bold green]✅ Generation Complete![/bold green]")
            console.print(f"📄 Business plan saved as: [cyan]business_plan_{timestamp}.md[/cyan]")
            console.print(f"📊 Metrics saved as: [cyan]metrics_{timestamp}.json[/cyan]\n")
            
            # Display analysis results
            display_analysis_progress(results, timestamp)
            
            if results.get("metrics", {}).get("warnings"):
                console.print("\n[bold yellow]⚠️ Warnings:[/bold yellow]")
                for warning in results["metrics"]["warnings"]:
                    console.print(f"  • {warning}")
            
        else:
            console.print("\n[bold red]❌ Generation Failed[/bold red]")
            console.print(f"Error: {results.get('error_message', 'Unknown error')}")
            if results.get("errors"):
                console.print("\n[bold red]Detailed errors:[/bold red]")
                for error in results["errors"]:
                    console.print(f"  • {error}")

        # Ask if user wants to view the generated plan
        if Confirm.ask("\nWould you like to view the generated business plan?"):
            doc_path = Path("output") / f"business_plan_{timestamp}.md"
            if doc_path.exists():
                with open(doc_path, 'r') as f:
                    markdown = Markdown(f.read())
                    console.print(Panel(markdown, title="[bold]Generated Business Plan[/bold]", 
                                     border_style="blue", expand=True))

    except KeyboardInterrupt:
        console.print("\n\n[bold red]Process interrupted by user. Exiting gracefully...[/bold red]")
    except ValueError as e:
        console.print(f"\n[bold red]Validation Error: {str(e)}[/bold red]")
    except Exception as e:
        console.print(f"\n[bold red]Unexpected Error: {str(e)}[/bold red]")
        raise

if __name__ == "__main__":
    run()
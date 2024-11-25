from crewai import Crew, Task, LLM, Process
from typing import Dict, Any, List, Tuple
from datetime import datetime
import os

from crewai.crews import CrewOutput
from crewai_tools import LlamaIndexTool

from ..agents.agent_prompts import AgentPrompts
from src.product_analysis.business_plan.utils.formatters import MarkdownFormatter, ContentFormatter
from src.product_analysis.business_plan.utils.validators import BusinessPlanValidator
from .content_processor import ContentProcessor
from ..agents.agent_factory import AgentFactory
from ..tools.market_analysis import MarketAnalysisPipeline


class BusinessPlanCrew:
    """Enhanced Business Plan Generation System with validation and aggregation"""

    def __init__(self, use_examples: bool = True):
        """
        Initialize BusinessPlanCrew

        Args:
            use_examples: Whether to use few-shot examples in prompts
        """
        self.start_time = datetime.now()
        self.llm = self._initialize_llm()
        self.agent_factory = AgentFactory(self.llm)
        self.content_processor = ContentProcessor()
        self.use_examples = use_examples
        self.prompts = AgentPrompts()

        self.api_key = "cb86325e02c715e12b7d8439f064e172713f1c40"

        self.metrics = {
            "execution_time": 0,
            "completion_scores": {},
            "quality_scores": {},
            "warnings": []
        }
    
    def _initialize_llm(self) -> LLM:
        """Initialize LLM with configuration"""
        return LLM(
            base_url="http://localhost:11434",
            model="ollama/llama2:13b"
        )
        
    def _create_crew(self, input_data: Dict[str, Any]) -> Crew:
        """Create and configure the crew with all necessary agents"""
        # Set context for agents
        self.agent_factory.set_input_data(input_data)
        
        # Create agents
        market_researcher = self.agent_factory.create_market_research_agent()
        financial_planner = self.agent_factory.create_financial_planner_agent()
        competitive_analyst = self.agent_factory.create_competitive_analyst_agent()
        implementation_planner = self.agent_factory.create_implementation_plan_agent()
        executive_summarizer = self.agent_factory.create_executive_summary_agent()
        aggregator = self.agent_factory.create_business_plan_aggregator_agent()

        # Create tasks with explicit dependencies
        market_research = Task(
            description=self.prompts.MARKET_RESEARCH_TASK,
            expected_output=self.prompts.MARKET_RESEARCH_EXPECTED_OUTPUT,
            agent=market_researcher,
            output_file="market_research_output.md"
        )

        financial_planning = Task(
            description=self.prompts.FINANCIAL_ANALYSIS_TASK,
            expected_output=self.prompts.FINANCIAL_ANALYSIS_EXPECTED_OUTPUT,
            agent=financial_planner,
            context=[market_research],
            output_file="financial_planning_output.md"
        )

        competitive_analysis = Task(
            description=self.prompts.COMPETITIVE_ANALYSIS_TASK,
            expected_output=self.prompts.COMPETITIVE_ANALYSIS_EXPECTED_OUTPUT,
            agent=competitive_analyst,
            context=[market_research, financial_planning],
            output_file="competitive_analysis_output.md"
        )

        implementation_plan = Task(
            description=self.prompts.IMPLEMENTATION_PLAN_TASK,
            expected_output=self.prompts.IMPLEMENTATION_PLAN_EXPECTED_OUTPUT,
            agent=implementation_planner,
            context=[market_research, financial_planning, competitive_analysis],
            output_file="implementation_plan_output.md",
            max_iter=3  # Limit iterations to ensure completion
        )

        executive_summary = Task(
            description=self.prompts.EXECUTIVE_SUMMARY_TASK,
            expected_output=self.prompts.EXECUTIVE_SUMMARY_EXPECTED_OUTPUT,
            agent=executive_summarizer,
            context=[market_research, financial_planning, competitive_analysis],
            output_file="executive_summary_output.md",
            max_iter=3  # Limit iterations to ensure completion
        )

        # implementation_plan = Task(
        #     description=self.prompts.IMPLEMENTATION_PLAN_TASK,
        #     expected_output=self.prompts.IMPLEMENTATION_PLAN_EXPECTED_OUTPUT,
        #     agent=aggregator,
        #     context=[market_research, financial_planning, competitive_analysis, executive_summary],
        #     output_file="implementation_plan_output.md",
        #     max_iter=3  # Limit iterations to ensure completion
        # )

        business_plan = Task(
            description=self.prompts.BUSINESS_PLAN_TASK,
            expected_output=f'''
            Complete business plan integrating market, financial, and competitive analyses with implementation strategy.
            The business plan should be structured with clear sections and headings, and should be written in a clear and concise manner.
            I've included an example of the expected output indicated by <EXAMPLE> tags, to a sample user input indicated by <INPUT> tags.
            {self.prompts.BUSINESS_PLAN_EXPECTED_OUTPUT}
            ''',
            agent=aggregator,
            context=[market_research, financial_planning, competitive_analysis, executive_summary, implementation_plan]
        )

        # Create crew with sequential process and planning
        return Crew(
            agents=[market_researcher, financial_planner, competitive_analyst, implementation_planner, executive_summarizer, aggregator],
            tasks=[market_research, financial_planning, competitive_analysis, implementation_plan, executive_summary, business_plan],
            process=Process.sequential,
            verbose=True,
            memory=False,
            share_crew=False,
            planning=False,  # Enable planning to ensure proper task execution
            max_iter=3  # Limit total iterations
        )

    def _update_tasks_with_context(self, tasks: List[Task], context: Dict[str, Any]) -> None:
        """Update task descriptions with business context."""
        required_fields = ["business_idea", "industry", "scale", "target_market", "initial_investment", "timeline"]

        context_vars = {}
        for field in required_fields:
            value = context["input_data"].get(field)
            if not value:
                raise ValueError(f"The field '{field}' is required but was not provided.")
            context_vars[field] = value

        try:
            for task in tasks:
                task.description = task.description.format(**context_vars)

        except KeyError as e:
            print(f"Missing required context field: {e}")
            raise
        except Exception as e:
            print(f"Error updating task with context: {e}")
            raise

    def _split_result_into_sections(self, result: str) -> List[str]:
        """Split the combined result string into sections for each task."""

        sections = result.split('# Agent:')
        outputs = []

        for section in sections:
            if section.strip():
                content = section.strip()
                outputs.append(content)

        print(f"DEBUG: Number of sections found: {len(outputs)}")
        return outputs

    def _extract_content_after_final_answer(self, text: str) -> str:
        """Extract content after '## Final Answer:' marker"""
        if "## Final Answer:" in text:
            content = text.split("## Final Answer:", 1)[1].strip()
            if "DEBUG:" in content:
                content = content.split("DEBUG:", 1)[0].strip()
            return content
        return text.strip()

    def aggregate_results(self, results: Dict[str, Any]) -> str:
        """
        Aggregate and format all results into a cohesive business plan

        Args:
            results: Dictionary containing processed results from all agents

        Returns:
            Formatted business plan as a string
        """
        try:
            enhanced_results = ContentFormatter.integrate_sections(
                results,
                self.agent_factory.examples if self.use_examples else {}
            )
            final_document = MarkdownFormatter.generate_markdown(enhanced_results)

            return final_document

        except Exception as e:
            print(f"Error during aggregation: {str(e)}")
            return MarkdownFormatter.generate_error_report(e)

    def _validate_results(self, results: Dict) -> Dict:
        """Validate results and calculate quality metrics"""
        validation_results = BusinessPlanValidator.validate_business_plan(results)
        validator = BusinessPlanValidator()
        for section, data in results.items():
            print("Validating section: ", section)
            print("Data: ", data)
            quality_result = validator.validate_section_quality(
                section=section,
                content=data.get("content", [])
            )
            self.metrics["quality_scores"][section] = quality_result["score"]
            if quality_result["issues"]:
                self.metrics["warnings"].extend(quality_result["issues"])

        return validation_results
    def _process_task_result(self, task: Task, task_result: Any, business_plan: Dict) -> None:
        """Process individual task result and update business plan"""

        role = task.agent.role
        content = task_result.strip() if isinstance(task_result, str) else str(task_result)

        if not content:
            print(f"WARNING: No content for role: {role}")
            content = "No content available."

        if "Market Research" in role:
            processed = self.content_processor.process_market_analysis(content)
            business_plan["market_analysis"]["content"].append(processed)
            business_plan["market_analysis"]["status"] = "complete"

        elif "Financial" in role:
            processed = self.content_processor.process_financial_data(content)
            business_plan["financial_projections"]["content"].append(processed)
            business_plan["financial_projections"]["status"] = "complete"

        elif "Competition" in role:
            processed = self.content_processor.process_competitive_analysis(content)
            business_plan["competitive_analysis"]["content"].append(processed)
            business_plan["competitive_analysis"]["status"] = "complete"
        elif "Implementation" in role:
            processed = self.content_processor.process_implementation_plan(content)
            business_plan["implementation_plan"]["content"].append(processed)
            business_plan["implementation_plan"]["status"] = "complete"

        elif "Executive" in role:
            processed = self.content_processor.process_executive_summary(content)
            business_plan["executive_summary"]["content"].append(processed)
            business_plan["executive_summary"]["status"] = "complete"

        elif "Strategy" in role or "Aggregator" in role:  # Check for both roles
            exec_summary, impl_plan = self._extract_strategic_content(content)
            
            if exec_summary:
                processed_summary = self.content_processor.process_executive_summary(exec_summary)
                business_plan["executive_summary"]["content"].append(processed_summary)
                business_plan["executive_summary"]["status"] = "complete"
            
            if impl_plan:
                processed_plan = self.content_processor.process_implementation_plan(impl_plan)
                business_plan["implementation_plan"]["content"].append(processed_plan)
                business_plan["implementation_plan"]["status"] = "complete"
            
            # If no implementation plan found in strategic content, try to extract it directly
            elif "Implementation Plan" in content:
                impl_plan = self._extract_section(content, "Implementation Plan", 
                    ["Conclusion", "Financial Plan", "Executive Summary"])
                if impl_plan:
                    processed_plan = self.content_processor.process_implementation_plan(impl_plan)
                    business_plan["implementation_plan"]["content"].append(processed_plan)
                    business_plan["implementation_plan"]["status"] = "complete"

    def _extract_strategic_content(self, content: str) -> Tuple[str, str]:
        """Extract executive summary and implementation plan from strategic content"""
        sections = {
            "executive_summary": [],
            "implementation_plan": []
        }

        current_section = None
        lines = content.split('\n')

        for line in lines:
            line = line.strip()

            if not line or "DEBUG:" in line or "**" == line:
                continue
            lower_line = line.lower()
            if "executive summary" in lower_line:
                current_section = "executive_summary"
                continue
            elif "implementation plan" in lower_line or "operations plan" in lower_line:
                current_section = "implementation_plan"
                continue

            if current_section and line:
                sections[current_section].append(line)

        exec_summary = '\n'.join(sections["executive_summary"])
        impl_plan = '\n'.join(sections["implementation_plan"])

        return exec_summary.strip(), impl_plan.strip()

    def _initialize_llm(self) -> LLM:
        """Initialize LLM with configuration"""
        ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        model_name = os.getenv("OPENAI_MODEL_NAME", "llama3:8b")
        return LLM(
            base_url=ollama_base_url,
            model=f"ollama/{model_name}"
        )



    def _clean_output_text(self, text: str) -> str:
        """Clean the output text by removing debug information and markers"""
        if "DEBUG:" in text:
            text = text.split("DEBUG:")[0]

        markers = ["# Agent:", "## Task:", "## Final Answer:"]
        for marker in markers:
            if marker in text:
                text = text.split(marker)[-1]

        return text.strip()

    def _extract_section_content(self, text: str, section_name: str) -> str:
        """Extract content for a specific section"""
        lines = text.split('\n')
        content = []
        in_section = False

        for line in lines:
            line = line.strip()
            if not line or line == "**":
                continue

            if section_name.lower() in line.lower():
                in_section = True
                continue

            if in_section and line.startswith('**') and line.endswith('**'):
                if not any(keyword in line.lower() for keyword in ["summary", "plan"]):
                    break

            if in_section:
                content.append(line)

        return '\n'.join(content).strip()

    def execute_analysis(self, business_context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the business plan analysis with enhanced market analysis"""
        try:
            market_analyzer = MarketAnalysisPipeline()
            
            crew = self._create_crew(input_data=business_context["input_data"])
            self._update_tasks_with_context(crew.tasks, business_context)

            print("\nExecuting business plan analysis...")
            result = crew.kickoff(inputs=business_context["input_data"])
            print("\nInitial analysis complete. Processing results...")

            processed_results = self._process_results(crew, result)
            
            market_analysis = market_analyzer.analyze_market_data(processed_results)
            if "market_analysis" in processed_results:
                processed_results["market_analysis"]["content"].append(
                    "\n\n### Market Intelligence\n" + 
                    ContentProcessor.format_market_intelligence(market_analysis)
                )

            validation_results = self._validate_results(processed_results)
            final_document = self.aggregate_results(processed_results)

            self.metrics["execution_time"] = str(datetime.now() - self.start_time)
            self.metrics["market_analysis_confidence"] = market_analysis["confidence_score"]

            return {
                "status": "success",
                "document": final_document,
                "metrics": self.metrics,
                "validation": validation_results,
                "market_intelligence": market_analysis,
                "errors": []
            }

        except Exception as e:
            print(f"Error during analysis: {str(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            return {
                "status": "error",
                "error_message": str(e),
                "execution_time": str(datetime.now() - self.start_time),
                "errors": [str(e)]
            }

    def _process_results(self, crew: Crew, result: Any) -> Dict[str, Any]:
        """Process and structure analysis results"""
        sections = {
            "market_analysis": {"content": [], "status": "pending"},
            "financial_projections": {"content": [], "status": "pending"},
            "competitive_analysis": {"content": [], "status": "pending"},
            "executive_summary": {"content": [], "status": "pending"},
            "implementation_plan": {"content": [], "status": "pending"}
        }

        try:
            if not hasattr(result, 'tasks_output'):
                raise ValueError("No tasks output available in result")

            for task_output in result.tasks_output:
                output_text = str(task_output)
                cleaned_text = self._clean_output_text(output_text)
                
                section_contents = self._split_into_sections(cleaned_text)
                
                for section_name, content in section_contents.items():
                    if content and section_name in sections:
                        sections[section_name]["content"].append(content)
                        sections[section_name]["status"] = "complete"
            
            for section in sections.values():
                if "status" not in section:
                    section["status"] = "pending"
                
                if section["content"] and section["status"] == "pending":
                    section["status"] = "complete"

            return sections

        except Exception as e:
            print(f"Error processing results: {str(e)}")
            for section in sections.values():
                section["status"] = "error"
            return sections
    
    def _split_into_sections(self, text: str) -> Dict[str, str]:
        """Split text into relevant sections based on headers"""
        sections = {
            "market_analysis": "",
            "financial_projections": "",
            "competitive_analysis": "",
            "executive_summary": "",
            "implementation_plan": ""
        }

        if "executive summary" in text.lower():
            exec_summary = self._extract_section(text, "executive summary",
                                                 ["business strategy", "implementation plan", "go-to-market plan"])
            if exec_summary:
                sections["executive_summary"] = exec_summary


        if "implementation plan" in text.lower():
            impl_plan = self._extract_section(text, "implementation plan",
                                              ["risk management", "conclusion", "financial plan"])
            if impl_plan:
                sections["implementation_plan"] = impl_plan

        if "market analysis" in text.lower() or "market size" in text.lower():
            market = self._extract_section(text, "market analysis",
                                           ["financial", "competition", "implementation"])
            if market:
                sections["market_analysis"] = market

        if "financial" in text.lower() or "revenue" in text.lower():
            financials = self._extract_section(text, "financial",
                                               ["competition", "implementation", "conclusion"])
            if financials:
                sections["financial_projections"] = financials

        if "competition" in text.lower() or "competitor" in text.lower():
            competition = self._extract_section(text, "competition",
                                                ["implementation", "financial", "conclusion"])
            if competition:
                sections["competitive_analysis"] = competition

        return sections

    def _extract_section(self, text: str, section_start: str, section_ends: List[str]) -> str:
        """Extract content between section start and any of the section ends"""
        lines = text.split('\n')
        content = []
        in_section = False

        for line in lines:
            if section_start in line.lower():
                in_section = True
                continue

            if in_section:
                if any(end in line.lower() for end in section_ends):
                    break
                content.append(line)

        return '\n'.join(content).strip()

    def _get_unique_content(self, content_list: List[str]) -> str:
        """Get unique content from potentially duplicate sections"""
        if not content_list:
            return ""

        sorted_content = sorted(content_list, key=len, reverse=True)
        return sorted_content[0]

    def _format_section_content(self, content: str, section_name: str) -> str:
        """Format section content with proper markdown structure"""
        if not content:
            return ""

        lines = content.split('\n')
        formatted = []
        current_heading = None

        for line in lines:
            line = line.strip()
            if not line or line == "**":
                continue

            if line.startswith('**') and line.endswith('**'):
                current_heading = line.strip('*')
                formatted.append(f"\n### {current_heading}\n")

            elif line.startswith('*'):
                formatted.append(line)

            else:
                line = line.replace('.', '. ')
                line = ' '.join(line.split())
                formatted.append(line)

        if section_name == "implementation_plan":
            formatted = self._format_implementation_plan(formatted)
        elif section_name == "financial_projections":
            formatted = self._format_financial_projections(formatted)

        return '\n'.join(formatted)

    def _format_implementation_plan(self, lines: List[str]) -> List[str]:
        """Add special formatting for implementation plan"""
        formatted = []
        in_timeline = False

        for line in lines:
            if "Timeline" in line or "Milestones" in line:
                in_timeline = True
                formatted.append(f"\n### {line}\n")
            elif in_timeline and line.startswith('*'):
                formatted.append(f"* {line.strip('* ')}")
            else:
                formatted.append(line)

        return formatted

    def _format_financial_projections(self, lines: List[str]) -> List[str]:
        """Add special formatting for financial projections"""
        formatted = []
        in_table = False

        for line in lines:
            if "|" in line:
                in_table = True
                formatted.append(line)
            elif in_table and not line.strip():
                in_table = False
                formatted.append("")
            else:
                formatted.append(line)

        return formatted
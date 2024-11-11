from crewai import Agent, LLM
from typing import Dict, Any
import yaml
from pathlib import Path
from crewai_tools import SerperDevTool, ScrapeWebsiteTool


class AgentFactory:
    """Factory class for creating specialized business plan agents"""

    def __init__(self, llm: LLM):
        self.llm = llm
        self.examples = self._load_examples()
        self.input_data = None
        self.industry = None
        self.target_market = None
        self.scale = None
        self.initial_investment = None
        self.timeline = None
        self.business_idea = None
    def set_input_data(self, input_data: Dict[str, Any]):
        """Set the input data for the agents"""
        self.input_data = input_data
        self.industry = input_data.get('industry', None)
        self.target_market = input_data.get('target_market', None)
        self.scale = input_data.get('scale', None)
        self.initial_investment = input_data.get('initial_investment', None)
        self.timeline = input_data.get('timeline', None)
        self.business_idea = input_data.get('business_idea', None)
    def _load_examples(self) -> Dict[str, Any]:
        """Load few-shot examples from YAML file"""
        try:
            examples_path = Path(__file__).parent.parent / 'examples' / 'few_shot_examples.yaml'
            with open(examples_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Warning: Could not load examples: {e}")
            return {}

    def _format_examples(self, examples_list: list) -> str:
        """Format the examples into a string for the backstory"""
        if not examples_list:
            return "No examples available."
        example_texts = []
        for example in examples_list:
            context = example.get('context', 'No context provided.')
            analysis = example.get('analysis', 'No analysis provided.')
            key_points = example.get('key_points', [])
            key_points_text = '\n- '.join(key_points) if key_points else 'No key points provided.'
            example_text = f"Context: {context}\nAnalysis:\n{analysis}\nKey Points:\n- {key_points_text}"
            example_texts.append(example_text)
        return "\n\n".join(example_texts)

    def create_market_research_agent(self) -> Agent:
        """Create market research agent with examples"""
        examples_list = self.examples.get('market_research', [])
        formatted_examples = self._format_examples(examples_list)
        return Agent(
            role=f'Senior Market Research Analyst in {self.industry}',
            goal=f'Provide comprehensive market insights and detailed target audience analysis for {self.business_idea} in {self.industry} for {self.target_market} market in {self.scale} scale',
            backstory=f"""Experienced market researcher with deep expertise in {self.industry} industry.
            Known for accurate market size predictions for {self.target_market} market and identifying emerging trends.
            Specialized in identifying market opportunities and customer needs.

            Reference Examples:
            {formatted_examples}""",
            allow_delegation=False,
            llm=self.llm
        )

    def create_financial_planner_agent(self) -> Agent:
        """Create financial planner agent with examples"""
        examples_list = self.examples.get('financial_planning', [])
        formatted_examples = self._format_examples(examples_list)
        
        return Agent(
            role=f'Financial Strategist in {self.industry} industry',
            goal=f'Create detailed financial models and realistic projections in {self.industry} industry at {self.scale} scale with {self.initial_investment} initial investment in {self.timeline} timeline',
            backstory=f"""Experienced financial advisor who has worked with businesses of all sizes.
            Expert in financial modeling, cost analysis, and revenue projections.
            Deep understanding of various business models and revenue streams in {self.industry} industry.

            Reference Examples:
            {formatted_examples}""",
            allow_delegation=False,
            llm=self.llm
        )

    def create_competitive_analyst_agent(self) -> Agent:
        """Create competitive analysis agent with examples"""
        examples_list = self.examples.get('competitive_analysis', [])
        formatted_examples = self._format_examples(examples_list)
        return Agent(
            role=f'Competition and Market Specialist in {self.industry} industry',
            goal=f'Analyze competitive landscape and market positioning for {self.business_idea} in {self.industry} industry for {self.target_market} market in {self.scale} scale',
            backstory=f"""Competition analyst with in-depth experience across {self.industry} industry.
            Expert at identifying competitive advantages and market gaps for {self.target_market} market at {self.scale} scale.
            Specialized in developing differentiation strategies.

            Reference Examples:
            {formatted_examples}""",
            allow_delegation=False,
            llm=self.llm
        )

    def create_business_plan_aggregator_agent(self) -> Agent:
        """Create business plan aggregator agent with examples"""
        examples_list = self.examples.get('plan_aggregation', [])
        formatted_examples = self._format_examples(examples_list)
        return Agent(
            role='Business Plan Generator',
            goal=f'Create comprehensive and actionable business plans for {self.business_idea} by synthesizing expert analyses into a cohesive document. Ensure ALL sections are thoroughly completed with specific details.',
            backstory=f"""Seasoned business strategist who has helped launch diverse ventures.
            Expert at crafting actionable business plans across various industries.
            Skilled in identifying key success factors and risk mitigation.

            Reference Examples:
            {formatted_examples}""",
            allow_delegation=False,
            llm=self.llm
        )

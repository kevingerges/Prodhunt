from crewai import Agent, LLM
from typing import Dict, Any
import yaml
from pathlib import Path


class AgentFactory:
    """Factory class for creating specialized business plan agents"""

    def __init__(self, llm: LLM):
        self.llm = llm
        self.examples = self._load_examples()

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
            role='Senior Market Research Analyst',
            goal='Provide comprehensive market insights and detailed target audience analysis',
            backstory=f"""Experienced market researcher with deep expertise across multiple industries.
Known for accurate market size predictions and identifying emerging trends.
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
            role='Financial Strategist',
            goal='Create detailed financial models and realistic projections',
            backstory=f"""Experienced financial advisor who has worked with businesses of all sizes.
Expert in financial modeling, cost analysis, and revenue projections.
Deep understanding of various business models and revenue streams.

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
            role='Competition and Market Specialist',
            goal='Analyze competitive landscape and market positioning',
            backstory=f"""Industry-agnostic competition analyst with experience across markets.
Expert at identifying competitive advantages and market gaps.
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
            role='Business Strategy Director',
            goal='Create comprehensive and actionable business plans',
            backstory=f"""Seasoned business strategist who has helped launch diverse ventures.
Expert at crafting actionable business plans across various industries.
Skilled in identifying key success factors and risk mitigation.

Reference Examples:
{formatted_examples}""",
            allow_delegation=False,
            llm=self.llm
        )

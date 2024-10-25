# crew.py
from crewai import Crew, Task, Agent, LLM
import os

class BusinessPlanCrew:
    def crew(self):
        ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        model_name = os.getenv("OPENAI_MODEL_NAME", "llama3:8b")

        llm = LLM(
            base_url=ollama_base_url,
            model=f"ollama/{model_name}"
        )

        # Create agents with the LLM
        market_research_agent = Agent(
            role='Market Researcher',
            goal='Identify market opportunities and target audience',
            backstory='Expert in market research with a focus on identifying new opportunities.',
            allow_delegation=False,
            llm=llm
        )

        financial_planner_agent = Agent(
            role='Financial Planner',
            goal='Develop financial projections and budget plans',
            backstory='Experienced in financial planning and budgeting.',
            allow_delegation=False,
            llm=llm
        )

        competitive_analysis_agent = Agent(
            role='Competitive Analyst',
            goal='Analyze competitors and identify market positioning',
            backstory='Specialist in competitive analysis and market positioning strategies.',
            allow_delegation=False,
            llm=llm
        )

        business_plan_aggregator_agent = Agent(
            role='Business Plan Aggregator',
            goal='Compile and synthesize the business plan components',
            backstory='Responsible for creating a cohesive and comprehensive business plan.',
            allow_delegation=False,
            llm=llm
        )

        return Crew(
            agents=[
                market_research_agent,
                financial_planner_agent,
                competitive_analysis_agent,
                business_plan_aggregator_agent
            ],
            tasks=[
                Task(
                    description="Conduct market research to identify opportunities and target audience for {business_idea}",
                    expected_output="Detailed market analysis report including target audience and market opportunities",
                    agent=market_research_agent
                ),
                Task(
                    description="Develop financial projections and budget plans for {business_idea}",
                    expected_output="Financial projections and budget plan for the business",
                    agent=financial_planner_agent
                ),
                Task(
                    description="Analyze competitors and identify market positioning for {business_idea}",
                    expected_output="Competitive analysis report with market positioning strategy",
                    agent=competitive_analysis_agent
                ),
                Task(
                    description="Compile and synthesize the business plan components for {business_idea}",
                    expected_output="Comprehensive business plan document",
                    agent=business_plan_aggregator_agent
                )
            ],
            verbose=True
        )
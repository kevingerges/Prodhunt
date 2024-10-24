from crewai import Crew, Task
from langchain_community.llms import Ollama
from agents import BusinessPlanAgents

class BusinessPlanCrew:
    def crew(self):
        agents = BusinessPlanAgents()
        llm = agents.llm  # Use the same LLM instance from BusinessPlanAgents
        
        return Crew(
            agents=[
                agents.market_research_agent,
                agents.financial_planner_agent,
                agents.competitive_analysis_agent,
                agents.business_plan_aggregator_agent
            ],
            tasks=[
                Task(
                    description="Conduct market research to identify opportunities and target audience for {business_idea}",
                    expected_output="Detailed market analysis report including target audience and market opportunities",
                    agent=agents.market_research_agent
                ),
                Task(
                    description="Develop financial projections and budget plans for {business_idea}",
                    expected_output="Financial projections and budget plan for the business",
                    agent=agents.financial_planner_agent
                ),
                Task(
                    description="Analyze competitors and identify market positioning for {business_idea}",
                    expected_output="Competitive analysis report with market positioning strategy",
                    agent=agents.competitive_analysis_agent
                ),
                Task(
                    description="Compile and synthesize the business plan components for {business_idea}",
                    expected_output="Comprehensive business plan document",
                    agent=agents.business_plan_aggregator_agent
                )
            ],
            verbose=True,
            llm=llm
        )

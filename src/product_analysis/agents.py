from crewai import Agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

class BusinessPlanAgents:
    def __init__(self):
        
        self.llm = ChatOpenAI(
            model="ollama/llama3",
            base_url="http://localhost:11434/v1"
        )


        self.market_research_agent = Agent(
            role='Market Researcher',
            goal='Identify market opportunities and target audience',
            backstory='Expert in market research with a focus on identifying new opportunities.',
            llm=self.llm
        )

        self.financial_planner_agent = Agent(
            role='Financial Planner',
            goal='Develop financial projections and budget plans',
            backstory='Experienced in financial planning and budgeting.',
            llm=self.llm
        )

        self.competitive_analysis_agent = Agent(
            role='Competitive Analyst',
            goal='Analyze competitors and identify market positioning',
            backstory='Specialist in competitive analysis and market positioning strategies.',
            llm=self.llm
        )

        self.business_plan_aggregator_agent = Agent(
            role='Business Plan Aggregator',
            goal='Compile and synthesize the business plan components',
            backstory='Responsible for creating a cohesive and comprehensive business plan.',
            llm=self.llm
        )

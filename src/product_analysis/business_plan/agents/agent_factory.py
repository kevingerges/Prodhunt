from crewai import Agent, LLM
from typing import Dict, Any, List, Optional
from pathlib import Path
import yaml
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from ..tools.llama_rag_tool import DynamicRAGTool
from ..tools.market_analysis import MarketAnalysisPipeline

class AgentFactory:
    """Enhanced factory class for creating specialized business plan agents"""

    def __init__(self, llm: LLM):
        """Initialize the agent factory with enhanced capabilities"""
        self.llm = llm
        self.context = {}
        try:
            self.rag_tool = DynamicRAGTool()
            self.market_analyzer = MarketAnalysisPipeline()
            print("Enhanced research and market analysis tools initialized successfully")
        except Exception as e:
            print(f"Warning: Tool initialization failed: {str(e)}")
            self.rag_tool = None
            self.market_analyzer = None

    def set_input_data(self, input_data: Dict[str, Any]) -> None:
        """Set business context data with enhanced context handling"""
        self.context = {
            "business_idea": input_data.get("business_idea", ""),
            "industry": input_data.get("industry", ""),
            "scale": input_data.get("scale", ""),
            "target_market": input_data.get("target_market", ""),
            "initial_investment": input_data.get("initial_investment", ""),
            "timeline": input_data.get("timeline", "")
        }
    def create_market_research_agent(self) -> Agent:
        """Create enhanced market research agent with RAG and market analysis capabilities"""
        tools = []
        if self.rag_tool:
            tools.append(self.rag_tool)
        if self.market_analyzer:
            tools.append({
                "name": "Market Analysis Tool",
                "func": lambda q: self.market_analyzer.analyze_market_data({"query": q, "context": self.context}),
                "description": "Use this tool for deep market analysis and trend identification"
            })

        return Agent(
            role='Market Research Analyst',
            goal=f'''Analyze market potential and provide actionable insights for {self.context.get("business_idea")}.
                    Use real-time market data and trend analysis for validation.''',
            backstory='''You are an expert market researcher with access to advanced market analysis tools.
                    You provide data-driven insights using real-time market intelligence.''',
            tools=tools,
            allow_delegation=False,
            llm=self.llm,
            verbose=True
        )


    def create_financial_planner_agent(self) -> Agent:
        """Create enhanced financial planner agent with RAG capabilities"""
        tools = []
        if self.rag_tool:
            tools.append(self.rag_tool)

        return Agent(
            role='Financial Planning Strategist',
            goal=f'''Create data-driven financial projections for a {self.context.get("scale")} scale business 
                    with {self.context.get("initial_investment")} initial investment.
                    Validate all assumptions with real market data.''',
            backstory=f'''You are a financial expert specializing in {self.context.get("industry")} startups.
                    You create practical financial models based on real market data and industry benchmarks.
                    You have access to comprehensive financial intelligence tools.''',
            tools=tools,
            allow_delegation=False,
            llm=self.llm,
            verbose=True
        )

    def create_competitive_analyst_agent(self) -> Agent:
        """Create enhanced competitive analysis agent with RAG capabilities"""
        tools = []
        if self.rag_tool:
            tools.append(self.rag_tool)

        return Agent(
            role='Competition and Market Specialist',
            goal=f'''Analyze competitive landscape and develop positioning strategy.
                    Identify market opportunities and potential threats.
                    Focus on {self.context.get("target_market")} market with real-time data.''',
            backstory=f'''You are a competition analyst who tracks {self.context.get("industry")} market dynamics.
                    You use advanced market intelligence tools to analyze competitor strategies.
                    You provide insights based on real-time market data.''',
            tools=tools,
            allow_delegation=False,
            llm=self.llm,
            verbose=True
        )

    def create_business_plan_aggregator_agent(self) -> Agent:
        """Create enhanced business plan aggregator with RAG capabilities"""
        tools = []
        if self.rag_tool:
            tools.append(self.rag_tool)

        return Agent(
            role='Business Plan Integration Specialist',
            goal=f'''Create a comprehensive business plan for {self.context.get("business_idea")}.
                    Synthesize market research, financial projections, and competitive analysis.
                    Ensure all recommendations are validated with real market data.''',
            backstory='''You are a business strategist who excels at creating data-driven business plans.
                    You integrate multiple sources of information into coherent strategies.
                    You ensure all aspects of the plan are realistic and supported by market intelligence.''',
            tools=tools,
            allow_delegation=False,
            llm=self.llm,
            verbose=True
        )

    def _load_examples(self) -> Dict:
        """Load example business plans for reference"""
        try:
            examples_path = Path(__file__).parent / 'examples' / 'few_shot_examples.yaml'
            with open(examples_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Warning: Could not load examples: {e}")
            return {}
class SmartBusinessAnalyzer:
    """Research tool for gathering real-time business intelligence"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.search_tool = SerperDevTool()
        self.scrape_tool = ScrapeWebsiteTool()
    
    def research_market(self, query: str, context: Dict[str, Any]) -> str:
        """Conduct market research by searching and analyzing online data"""
        industry = context.get('industry', '')
        market = context.get('target_market', '')
        
        
        searches = [
            f"latest market size {industry} industry {market}",
            f"market growth rate {industry} {market} current year",
            f"major trends {industry} market analysis",
            f"{industry} industry statistics current year",
            f"competitor analysis {industry} {market}"
        ]
        
        results = []
        for search in searches:
            try:
                search_result = self.search_tool(search)
            
                if isinstance(search_result, dict):
                    for item in search_result.get('organic', [])[:3]:
                        url = item.get('link')
                        if url:
                            # Scrape content from the URL
                            content = self.scrape_tool(url)
                            results.append(content)
                
            except Exception as e:
                print(f"Error in research: {str(e)}")
                continue
        
        return "\n\n".join(results) if results else "No relevant data found."

class SmartAgentFactory:
    """Factory class for creating specialized business plan agents with real-time data capabilities"""

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
        self.analyzer = SmartBusinessAnalyzer()

    def _load_examples(self) -> Dict:
        """Load example business plans for reference"""
        try:
            examples_path = Path(__file__).parent / 'examples' / 'few_shot_examples.yaml'
            with open(examples_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Warning: Could not load examples: {e}")
            return {}

    def create_market_research_agent(self) -> Agent:
        """Create a market research agent with real-time research capabilities"""
        examples_list = self.examples.get('market_research', [])
        
        tools = [
            {
                "name": "Market Research Tool",
                "func": lambda q: self.analyzer.research_market(q, {
                    "industry": self.industry,
                    "target_market": self.target_market,
                    "scale": self.scale
                }),
                "description": "Use this tool to gather current market insights and data"
            },
            self.analyzer.search_tool,
            self.analyzer.scrape_tool
        ]
        
        return Agent(
            role=f'Senior Market Research Analyst specialized in {self.industry}',
            goal=f'''Analyze market potential and provide actionable insights for {self.business_idea}.
                    Focus on current market size, growth trends, and competitive landscape.
                    Use real-time data to validate assumptions and identify opportunities.''',
            backstory=f'''You are an expert market researcher with deep expertise in {self.industry}.
                    You use data-driven approaches to uncover market opportunities and validate business models.
                    You have access to real-time market data and know how to analyze industry trends.''',
            tools=tools,
            allow_delegation=False,
            llm=self.llm,
            verbose=True
        )

    def create_financial_planner_agent(self) -> Agent:
        """Create a financial planner agent with real-time market data access"""
        tools = [
            {
                "name": "Financial Research Tool",
                "func": lambda q: self.analyzer.research_market(q, {
                    "industry": self.industry,
                    "scale": self.scale,
                    "investment": self.initial_investment
                }),
                "description": "Use this tool to gather current financial benchmarks and metrics"
            },
            self.analyzer.search_tool
        ]
        
        return Agent(
            role=f'Financial Planning Strategist for {self.industry}',
            goal=f'''Create realistic financial projections and funding strategy for {self.business_idea}.
                    Design a viable financial model with {self.initial_investment} initial investment.
                    Use current market data to validate assumptions.''',
            backstory=f'''You are a financial expert who specializes in {self.industry} startups.
                    You understand current market conditions and funding landscapes.
                    You use real-world data to create practical financial models.''',
            tools=tools,
            allow_delegation=False,
            llm=self.llm,
            verbose=True
        )

    def create_competitive_analyst_agent(self) -> Agent:
        """Create a competitive analysis agent with real-time competitor tracking"""
        tools = [
            {
                "name": "Competitor Analysis Tool",
                "func": lambda q: self.analyzer.research_market(q, {
                    "industry": self.industry,
                    "target_market": self.target_market
                }),
                "description": "Use this tool to analyze current competitors and market positioning"
            },
            self.analyzer.search_tool,
            self.analyzer.scrape_tool
        ]
        
        return Agent(
            role=f'Competition and Market Specialist in {self.industry}',
            goal=f'''Analyze current competitive landscape for {self.business_idea}.
                    Identify market opportunities and potential threats.
                    Develop positioning strategy based on real market data.''',
            backstory=f'''You are a competition analyst who tracks {self.industry} market dynamics.
                    You understand how to analyze competitor strategies and market positions.
                    You use real-time data to identify market gaps and opportunities.''',
            tools=tools,
            allow_delegation=False,
            llm=self.llm,
            verbose=True
        )

    def create_business_plan_aggregator_agent(self) -> Agent:
        """Create a business plan aggregator that synthesizes real-time insights"""
        tools = [
            {
                "name": "Business Intelligence Tool",
                "func": lambda q: self.analyzer.research_market(q, self.input_data),
                "description": "Use this tool to validate business plan assumptions with current data"
            },
            self.analyzer.search_tool
        ]
        
        return Agent(
            role='Business Plan Integration Specialist',
            goal=f'''Create a comprehensive business plan for {self.business_idea}.
                    Synthesize market research, financial projections, and competitive analysis.
                    Ensure all recommendations are backed by current market data.''',
            backstory=f'''You are a business strategist who excels at creating actionable plans.
                    You know how to integrate multiple sources of information into coherent strategies.
                    You validate all assumptions with real-world data and market insights.''',
            tools=tools,
            allow_delegation=False,
            llm=self.llm,
            verbose=True
        )

    def set_input_data(self, input_data: Dict[str, Any]):
        """Set the business context data for agent creation"""
        self.input_data = input_data
        self.industry = input_data.get('industry', '')
        self.target_market = input_data.get('target_market', '')
        self.scale = input_data.get('scale', '')
        self.initial_investment = input_data.get('initial_investment', '')
        self.timeline = input_data.get('timeline', '')
        self.business_idea = input_data.get('business_idea', '')
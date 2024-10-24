from crewai import Agent, LLM
from langchain_openai import ChatOpenAI

class LLamaAgents:
    def __init__(self):
        self.llama_agent = ChatOpenAI(
            model="crewai-llama3:8b",
            base_url="http://localhost:11434/v1", # modify
            api_key="NA"
        )
    
    def product_manager(self):
        return self.llama_agent(
            role="Product Manager",
            # ...
            llm=self.llama_agent
        )
    

'''

    # variables
    model_name="llama3:8b"
    custom_model_name="crewai-llama3"

    # get the base model
    ollama pull $model_name

    # create the model file
    ollama create $custom_model_name -f ./Modelfile


'''

class BusinessAnalystAgents:
    def __init__(self):
        # Configure the LLM with Ollama
        llm = LLM(
            model="ollama/llama3.2",
            base_url="http://localhost:11434",  # Ollama's local endpoint
            api_key="NA"  # If authentication is required
        )

        # Define agents
        self.market_analysis_agent = Agent(
            role='Market Analyst',
            goal='Evaluate market potential and trends',
            backstory='Expert in market analysis with a focus on emerging trends.',
            llm=llm
        )

        self.financial_projection_agent = Agent(
            role='Financial Analyst',
            goal='Assess financial viability and projections',
            backstory='Experienced in financial modeling and projections.',
            llm=llm
        )

        self.operational_feasibility_agent = Agent(
            role='Operations Specialist',
            goal='Evaluate operational feasibility',
            backstory='Specialist in operational processes and efficiency.',
            llm=llm
        )

        self.legal_considerations_agent = Agent(
            role='Legal Advisor',
            goal='Review legal compliance and issues',
            backstory='Legal expert with a focus on business compliance.',
            llm=llm
        )

        self.central_aggregator_agent = Agent(
            role='Central Aggregator',
            goal='Compile and synthesize insights from all agents',
            backstory='Responsible for creating a comprehensive evaluation report.',
            llm=llm
        )

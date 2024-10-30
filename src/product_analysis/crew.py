from crewai import Crew, Task, Agent, LLM
import os
from typing import Dict, Any
from datetime import datetime

class BusinessPlanCrew:
    def __init__(self):
        self.start_time = datetime.now()

    def execute_analysis(self, business_context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the analysis with the provided business context"""
        try:
            # Create crew with context
            crew = self.crew()

            # Get business parameters
            business_idea = business_context["input_data"]["business_idea"]
            industry = business_context["input_data"]["industry"]
            scale = business_context["input_data"]["scale"]

            # Update task descriptions with context
            for task in crew.tasks:
                task.description = task.description.format(
                    business_idea=business_idea,
                    industry=industry,
                    scale=scale
                )

            # Execute analysis
            result = crew.kickoff(inputs=business_context)

            # Debugging Output for Result Structure
            print("\n--- Debugging CrewOutput Structure ---\n")
            print("Raw Crew Output:", result)
            print("\n--- End Debugging ---\n")

            # Attempt to parse `task_results` or use direct output if unavailable
            if hasattr(result, 'task_results'):
                task_outputs = result.task_results
            else:
                task_outputs = result  # Use the result directly if no `task_results`

            # Calculate execution time
            execution_time = datetime.now() - self.start_time
            return {
                "status": "success",
                "result": task_outputs,
                "execution_time": str(execution_time),
                "errors": []
            }

        except Exception as e:
            return {
                "status": "error",
                "error_message": str(e),
                "execution_time": str(datetime.now() - self.start_time),
                "errors": [str(e)]
            }

    def aggregate_results(self, results: Dict[str, Any]) -> str:
        """Aggregate results from each agent into a single cohesive document"""
        aggregated_content = "Business Plan Analysis:\n\n"

        for task_result in results["task_results"]:
            agent_role = task_result["agent"]["role"]
            agent_output = task_result["output"]

            # Add section heading and agent output
            aggregated_content += f"### {agent_role} ###\n"
            aggregated_content += f"{agent_output}\n\n"

        return aggregated_content

    def crew(self):
        ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        model_name = os.getenv("OPENAI_MODEL_NAME", "llama3:8b")
        llm = LLM(
            base_url=ollama_base_url,
            model=f"ollama/{model_name}"
        )

        # Generic Market Research Agent
        market_research_agent = Agent(
            role='Senior Market Research Analyst',
            goal='Provide comprehensive market insights and detailed target audience analysis',
            backstory="""Experienced market researcher with deep expertise across multiple industries.
            Known for accurate market size predictions and identifying emerging trends.
            Specialized in identifying market opportunities and customer needs.""",
            allow_delegation=False,
            llm=llm
        )

        # Generic Financial Planner Agent
        financial_planner_agent = Agent(
            role='Financial Strategist',
            goal='Create detailed financial models and realistic projections',
            backstory="""Experienced financial advisor who has worked with businesses of all sizes.
            Expert in financial modeling, cost analysis, and revenue projections.
            Deep understanding of various business models and revenue streams.""",
            allow_delegation=False,
            llm=llm
        )

        # Generic Competitive Analyst Agent
        competitive_analysis_agent = Agent(
            role='Competition and Market Specialist',
            goal='Analyze competitive landscape and market positioning',
            backstory="""Industry-agnostic competition analyst with experience across markets.
            Expert at identifying competitive advantages and market gaps.
            Specialized in developing differentiation strategies.""",
            allow_delegation=False,
            llm=llm
        )

        # Generic Business Plan Aggregator Agent
        business_plan_aggregator_agent = Agent(
            role='Business Strategy Director',
            goal='Create comprehensive and actionable business plans',
            backstory="""Seasoned business strategist who has helped launch diverse ventures.
            Expert at crafting actionable business plans across various industries.
            Skilled in identifying key success factors and risk mitigation.""",
            allow_delegation=False,
            llm=llm
        )

        tasks = [
            Task(
                description="""Conduct detailed market research for {business_idea} in the {industry} industry focusing on:
                1. Market Analysis:
                   - Total market size and growth potential
                   - Market segmentation and trends
                   - Geographic considerations for {scale} scale

                2. Customer Analysis:
                   - Primary target customers and their needs
                   - Customer behavior and preferences
                   - Market readiness and adoption factors

                3. Market Environment:
                   - Industry regulations and requirements
                   - Economic factors and market conditions
                   - Technology and innovation impact

                4. Opportunity Analysis:
                   - Market gaps and unmet needs
                   - Growth opportunities
                   - Potential market barriers

                5. Data-Driven Insights:
                   - Key market statistics
                   - Growth rate projections
                   - Market share potential

                Provide specific data points and justify all conclusions.""",
                expected_output="Comprehensive market analysis report with specific metrics and segment-wise breakdown",
                agent=market_research_agent
            ),
            Task(
                description="""Create detailed financial projections for {business_idea} considering {scale} scale operations:
                1. Setup and Operating Costs:
                   - Initial investment requirements
                   - Operating cost breakdown
                   - Resource allocation plan

                2. Revenue Model Design:
                   - Revenue streams identification
                   - Pricing strategy options
                   - Sales volume projections

                3. Financial Forecasting:
                   - Monthly projections (Year 1)
                   - Quarterly projections (Years 2-5)
                   - Cash flow analysis

                4. Key Metrics:
                   - Break-even analysis
                   - Profitability ratios
                   - Growth indicators

                5. Funding Requirements:
                   - Capital needs assessment
                   - Investment stages
                   - Return projections

                Include multiple scenarios and sensitivity analysis.""",
                expected_output="Detailed financial model with justified assumptions and clear growth metrics",
                agent=financial_planner_agent
            ),
            Task(
                description="""Analyze the competitive landscape for {business_idea} in the {industry} market:
                1. Competitor Analysis:
                   - Major players in {industry}
                   - Market share distribution
                   - Competitor strategies

                2. Competitive Positioning:
                   - Market positioning options
                   - Unique selling propositions
                   - Brand differentiation

                3. Market Dynamics:
                   - Entry barriers
                   - Supplier power
                   - Customer power

                4. Strategic Opportunities:
                   - Market gaps
                   - Partnership possibilities
                   - Growth vectors

                5. Threat Assessment:
                   - Emerging competitors
                   - Substitute products/services
                   - Market risks

                Provide specific examples and evidence-based analysis.""",
                expected_output="Strategic competitive analysis with actionable positioning recommendations",
                agent=competitive_analysis_agent
            ),
            Task(
                description="""Create a comprehensive business plan for {business_idea} targeting {scale} operations:
                1. Executive Summary:
                   - Business concept overview
                   - Market opportunity
                   - Value proposition

                2. Business Strategy:
                   - Operating model
                   - Revenue model
                   - Growth strategy

                3. Go-to-Market Plan:
                   - Market entry strategy
                   - Marketing approach
                   - Sales channels

                4. Implementation Plan:
                   - Key milestones
                   - Resource requirements
                   - Timeline and phases

                5. Risk Management:
                   - Key risks identification
                   - Mitigation strategies
                   - Success metrics

                Ensure all recommendations are specific to {industry} industry standards.""",
                expected_output="Detailed, actionable business plan with clear execution strategy",
                agent=business_plan_aggregator_agent
            )
        ]

        return Crew(
            agents=[
                market_research_agent,
                financial_planner_agent,
                competitive_analysis_agent,
                business_plan_aggregator_agent
            ],
            tasks=tasks,
            verbose=True
        )
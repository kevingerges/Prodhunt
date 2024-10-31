"""
Contains all prompts and templates for agent tasks
"""


class AgentPrompts:
    MARKET_RESEARCH_TASK = """Conduct detailed market research for {business_idea} in the {industry} industry focusing on:

    1. Market Analysis:
       - Total market size and growth potential
       - Market segmentation and trends
       - Geographic considerations for {scale} scale
       - Industry growth forecast
       - Market maturity assessment

    2. Customer Analysis:
       - Primary target customers and their needs
       - Customer behavior and preferences
       - Market readiness and adoption factors
       - Customer pain points
       - Buying patterns and decision factors

    3. Market Environment:
       - Industry regulations and requirements
       - Economic factors and market conditions
       - Technology and innovation impact
       - Political and legal considerations
       - Environmental factors

    4. Opportunity Analysis:
       - Market gaps and unmet needs
       - Growth opportunities
       - Potential market barriers
       - Entry timing considerations
       - Market accessibility

    5. Data-Driven Insights:
       - Key market statistics
       - Growth rate projections
       - Market share potential
       - Consumer trend data
       - Industry benchmark data

    Provide specific data points and justify all conclusions. Include market sizing calculations and growth projections.
    Use current industry data where available and note any assumptions made.

    Expected Output Format:
    - Use bullet points for key findings
    - Include numerical data with sources where possible
    - Organize insights by section
    - Highlight critical market factors
    - Include brief summaries for each major section"""

    FINANCIAL_ANALYSIS_TASK = """Create detailed financial projections for {business_idea} considering {scale} scale operations:

    1. Setup and Operating Costs:
       - Initial investment requirements
       - Operating cost breakdown
       - Resource allocation plan
       - Fixed vs variable costs
       - Infrastructure requirements

    2. Revenue Model Design:
       - Revenue streams identification
       - Pricing strategy options
       - Sales volume projections
       - Revenue growth models
       - Pricing sensitivity analysis

    3. Financial Forecasting:
       - Monthly projections (Year 1)
       - Quarterly projections (Years 2-5)
       - Cash flow analysis
       - Working capital requirements
       - Seasonal variations

    4. Key Metrics:
       - Break-even analysis
       - Profitability ratios
       - Growth indicators
       - Unit economics
       - Key performance indicators

    5. Funding Requirements:
       - Capital needs assessment
       - Investment stages
       - Return projections
       - Funding options analysis
       - Risk assessment

    Include multiple scenarios (conservative, moderate, aggressive) and sensitivity analysis.
    Provide detailed assumptions for all projections.

    Expected Output Format:
    - Use tables for numerical data
    - Include monthly/yearly breakdowns
    - Highlight key financial metrics
    - Show calculation methodologies
    - Include risk factors and mitigation strategies"""

    COMPETITIVE_ANALYSIS_TASK = """Analyze the competitive landscape for {business_idea} in the {industry} market:

    1. Competitor Analysis:
       - Major players in {industry}
       - Market share distribution
       - Competitor strategies
       - Competitor strengths and weaknesses
       - Historical performance

    2. Competitive Positioning:
       - Market positioning options
       - Unique selling propositions
       - Brand differentiation
       - Value proposition analysis
       - Target market alignment

    3. Market Dynamics:
       - Entry barriers
       - Supplier power
       - Customer power
       - Industry consolidation trends
       - Market maturity impact

    4. Strategic Opportunities:
       - Market gaps
       - Partnership possibilities
       - Growth vectors
       - Innovation opportunities
       - Market expansion potential

    5. Threat Assessment:
       - Emerging competitors
       - Substitute products/services
       - Market risks
       - Technology disruption potential
       - Regulatory challenges

    Provide specific examples and evidence-based analysis.
    Include competitive advantage analysis and market positioning strategy.

    Expected Output Format:
    - Use competitor comparison tables
    - Include market share charts
    - Highlight competitive advantages
    - Detail threat mitigation strategies
    - Provide actionable insights"""

    BUSINESS_PLAN_TASK = """Create a comprehensive business plan for {business_idea} targeting {scale} operations:

    1. Executive Summary:
       - Business concept overview
       - Market opportunity
       - Value proposition
       - Financial highlights
       - Implementation roadmap

    2. Business Strategy:
       - Operating model
       - Revenue model
       - Growth strategy
       - Scaling approach
       - Core competencies

    3. Go-to-Market Plan:
       - Market entry strategy
       - Marketing approach
       - Sales channels
       - Customer acquisition strategy
       - Partnership strategy

    4. Implementation Plan:
       - Key milestones
       - Resource requirements
       - Timeline and phases
       - Operational setup
       - Team structure

    5. Risk Management:
       - Key risks identification
       - Mitigation strategies
       - Success metrics
       - Contingency plans
       - Monitoring approach

    Ensure all recommendations are specific to {industry} industry standards.
    Integrate insights from market, financial, and competitive analyses.

    Expected Output Format:
    - Clear section organization
    - Executive summary highlights
    - Implementation timeline
    - Risk matrix
    - Success metrics dashboard"""
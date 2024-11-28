"""
Contains all prompts and templates for agent tasks
"""

class AgentPrompts:
    MARKET_RESEARCH_TASK = """
    Conduct detailed MARKET RESEARCH for {business_idea} in the {industry} industry focusing on the {target_market} market:
"""

    MARKET_RESEARCH_EXPECTED_OUTPUT = """
    Always prepend start the section with \"Market Research\"
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
    - Include brief summaries for each major section
    """

    FINANCIAL_ANALYSIS_TASK = """
    Conduct FINANCIAL ANALYSIS by creating detailed financial projections for {business_idea} considering {scale} scale operations in the {target_market} market with an initial investment of {initial_investment} and a timeline of {timeline}:
    """

    FINANCIAL_ANALYSIS_EXPECTED_OUTPUT = """
    Always prepend start the section with \"Financial Analysis\"
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
    - Include risk factors and mitigation strategies
    """

    COMPETITIVE_ANALYSIS_TASK = """
    Conduct COMPETITIVE ANALYSIS by analyzing the competitive landscape for {business_idea} in the {industry} market targeting the {target_market} market:
    """
    
    COMPETITIVE_ANALYSIS_EXPECTED_OUTPUT = """
    Always prepend start the section with \"Competitive Analysis\"
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
    - Provide actionable insights
    """

    BUSINESS_PLAN_TASK = """
    As the Business Plan Generator, your role is to create a comprehensive and cohesive business plan by synthesizing and harmonizing the analyses from the Market Research, Financial Analysis, and Competitive Analysis experts. 
    
    Business Context:
    - Business Idea: {business_idea}
    - Industry: {industry}
    - Scale: {scale}
    - Target Market: {target_market}
    - Initial Investment: {initial_investment}
    - Timeline: {timeline}

    Integration Guidelines:
    1. Cross-Reference Analysis:
       - Ensure market size data aligns across market and financial sections
       - Verify competitive positioning matches market opportunities
       - Confirm financial projections reflect market conditions
       - Link implementation timeline to market entry strategy

    2. Consistency Checks:
       - Use consistent terminology across all sections
       - Maintain aligned growth projections
       - Ensure compatible market assumptions
       - Verify matching timeline references

    3. Quality Standards:
       - Every section must include specific, actionable details
       - All claims must be supported by data or expert analysis
       - Financial projections must align with market potential
       - Risk assessments must cover all key areas

    4. Synthesis Requirements:
       - Identify and resolve any conflicts between expert analyses
       - Highlight synergies between different aspects of the plan
       - Create clear connections between sections
       - Ensure logical flow of information

    Generate a complete business plan with the following structure:

    1. Executive Summary (Integrate Executive Summary)
       - Compelling business concept overview
       - Clear value proposition
       - Key market opportunities
       - Financial highlights
       - Implementation roadmap

    2. Market Analysis (Integrate Market Research)
       - Market size and trends
       - Customer segmentation
       - Market drivers
       - Growth potential
       - Entry timing rationale

    3. Competitive Strategy (Integrate Competitive Analysis)
       - Competitive landscape
       - Positioning strategy
       - Competitive advantages
       - Market entry approach
       - Differentiation factors

    4. Financial Plan (Integrate Financial Analysis)
       - Startup costs
       - Revenue projections
       - Profitability analysis
       - Funding requirements
       - Key metrics and milestones

    5. Implementation Plan (Integrate Implementation Plan)
       - Detailed timeline
       - Resource requirements
       - Key partnerships
       - Risk mitigation
       - Success metrics

    Quality Control Requirements:
    - Each section must be complete with no placeholder content
    - All numerical data must be consistent across sections
    - Every strategy must be specific to {industry} industry
    - All projections must align with {scale} scale operations
    - Implementation must fit {timeline} timeline
    - Financial plans must reflect {initial_investment} investment

    Validation Checklist:
    □ All sections are thoroughly completed
    □ Numbers and projections are consistent
    □ Industry-specific strategies are included
    □ Timeline milestones are realistic
    □ Resource requirements are fully detailed
    □ Risks and mitigation strategies are addressed
    """

    BUSINESS_PLAN_EXPECTED_OUTPUT = """
    Your business plan should follow this structure with specific, actionable content in each section. Use the provided template and example as a reference for formatting and detail level expected.

    <INPUT>
      business_idea: "Offer biodegradable and eco-friendly packaging solutions tailored for e-commerce businesses."
      industry: "Packaging
      scale: "National"
      target_market: "Small to medium-sized e-commerce businesses in the U.S. seeking sustainable solutions."
      initial_investment: "$500,000"
      timeline: "6 months"
   </INPUT>
   <EXAMPLE>
      [Previous example content remains the same...]
   </EXAMPLE>
# Business Plan for Sustainable Pack Co.

## 1. Executive Summary
- **Business Concept Overview**: Sustainable Pack Co. provides biodegradable and eco-friendly packaging solutions tailored for e-commerce businesses. Our innovative products aim to reduce environmental impact while offering high-quality and cost-effective alternatives to traditional packaging.
- **Value Proposition**: By aligning with the growing demand for sustainability, our products enable e-commerce businesses to demonstrate environmental responsibility, attract eco-conscious customers, and comply with green regulations.
- **Key Market Opportunities**: The U.S. e-commerce packaging industry is valued at $15 billion and growing at 10% annually. Over 60% of businesses indicate a preference for sustainable options if cost-effective.
- **Financial Highlights**: Initial investment of $500,000 supports product development, production scale-up, and a marketing push, with projected profitability by year two and $3 million revenue by year three.
- **Implementation Roadmap**: Launch within six months with a phased rollout—initially targeting high-demand states like California and New York.

---

## 2. Market Analysis
- **Market Size and Trends**: The biodegradable packaging market is growing at 13% annually, fueled by increasing regulatory pressure and consumer demand for sustainable practices.
- **Customer Segmentation**: Focused on small to medium-sized e-commerce businesses with revenue between $1M–$20M, operating in eco-conscious sectors like food delivery and apparel.
- **Market Drivers**: Rising environmental regulations (e.g., California’s SB 54), consumer advocacy for sustainable brands, and increasing costs of waste disposal for businesses.
- **Growth Potential**: Sustainable Pack Co. aims to capture 5% of the $15B packaging market within five years.
- **Entry Timing Rationale**: Strategic entry during peak regulatory transitions offers first-mover advantage and market share growth.

---

## 3. Competitive Strategy
- **Competitive Landscape**: Competitors include large corporations like International Paper and small innovators like GreenWrap. Current gaps include affordable biodegradable packaging for SMEs.
- **Positioning Strategy**: Emphasize affordability and ease of adoption for SMEs, offering subscription models and bulk discounts.
- **Competitive Advantages**: Proprietary blend of biodegradable materials reduces production costs by 15% compared to competitors. High adaptability for branding and customization enhances value.
- **Market Entry Approach**: Start with regional campaigns targeting eco-conscious markets, then expand nationally.
- **Differentiation Factors**: Patented materials technology, integration with e-commerce platforms for automated packaging recommendations, and sustainable branding consultancy.

---

## 4. Financial Plan
- **Startup Costs**: $500,000 covers product development ($150,000), marketing ($100,000), equipment procurement ($200,000), and initial staffing ($50,000).
- **Revenue Projections**: $1M revenue in year one, scaling to $3M by year three through customer acquisition and product diversification.
- **Profitability Analysis**: Break-even projected within 18 months. Net profit margins of 20% achieved by year three.
- **Funding Requirements**: $500,000 investment split into equity (70%) and convertible debt (30%).
- **Key Metrics and Milestones**: 100 clients by month six; 10% month-over-month growth in revenue after launch.

---

## 5. Implementation Plan
- **Detailed Timeline**:
  - **Months 1–2**: Finalize product design, acquire equipment, hire staff.
  - **Month 3**: Pilot production and testing.
  - **Months 4–5**: Marketing launch, secure distribution channels.
  - **Month 6**: National rollout.
- **Resource Requirements**: Skilled labor, patented material supply chains, and advanced manufacturing facilities.
- **Key Partnerships**: Collaborations with logistics providers (e.g., FedEx, UPS) to integrate sustainable packaging in their services, and partnerships with e-commerce platforms like Shopify for product visibility.
- **Risk Mitigation**:
  - **Regulatory Risks**: Monitor evolving sustainability regulations to ensure compliance.
  - **Supply Chain Risks**: Establish multiple suppliers for key materials to reduce dependency.
  - **Market Adoption Risks**: Conduct market education campaigns to highlight the cost-benefit of sustainable packaging.
- **Success Metrics**: Customer retention rate of 90%, revenue milestone achievement within projected timelines, and reduction of production waste by 20% within the first year.

         </EXAMPLE>
"""

    EXECUTIVE_SUMMARY_TASK = """
    Create an EXECUTIVE SUMMARY for {business_idea} in the {industry} industry:
    - Synthesize key findings from market research, financial analysis, and competitive analysis
    - Highlight the unique value proposition and market opportunity
    - Summarize growth potential and financial projections
    - Outline key success factors and risk mitigation strategies
    - Output should start with header \"Executive Summary\"
    """

    EXECUTIVE_SUMMARY_EXPECTED_OUTPUT = """
    Always start the section with \"**Executive Summary**\"

    Expected structure:
    **Executive Summary**
    1. Business Overview
       - Core business concept
       - Target market and industry
       - Unique value proposition

    2. Market Opportunity
       - Market size and growth potential
       - Target customer segments
       - Key market trends

    3. Financial Highlights
       - Investment requirements
       - Revenue projections
       - Profitability timeline
       - Key financial metrics

    4. Competitive Advantage
       - Key differentiators
       - Market positioning
       - Barriers to entry

    5. Implementation Plan
       - Key milestones
       - Growth strategy
       - Risk management approach
    """

    IMPLEMENTATION_PLAN_TASK = """
    Create a DETAILED IMPLEMENTATION PLAN ONLY that includes:

    1. Implementation Timeline for {timeline}:
       - Specific milestones and deadlines
       - Key activities for each month
       - Resource requirements timing

    2. Detailed Action Steps:
       - Pre-launch activities (permits, equipment, hiring)
       - Launch phase activities
       - Post-launch operations
       - Each step should have specific time-frames

    3. Resource Deployment Schedule:
       - When to hire staff
       - When to purchase equipment
       - When to secure vendors
       - When to begin marketing activities

    4. Implementation Milestones:
       - Regulatory approvals
       - Facility setup
       - Staff training
       - Product testing
       - Marketing campaign launches
       - Sales targets by month

    Format the output as a detailed timeline with specific dates and actions.
    Focus ONLY on HOW and WHEN to implement the business.
    Start your answer with the EXACT header\"Implementation Plan\"
    """

    IMPLEMENTATION_PLAN_EXPECTED_OUTPUT = """
    Always start your answer with the EXACT header \"**Implementation Plan**\"
    Expected structure:
    **Implementation Plan**
    1. Implementation Timeline for {timeline}:
       - Specific milestones and deadlines
       - Key activities for each month
       - Resource requirements timing

    2. Detailed Action Steps:
       - Pre-launch activities (permits, equipment, hiring)
       - Launch phase activities
       - Post-launch operations
       - Each step should have specific time-frames

    3. Resource Deployment Schedule:
       - When to hire staff
       - When to purchase equipment
       - When to secure vendors
       - When to begin marketing activities

    4. Implementation Milestones:
       - Regulatory approvals
       - Facility setup
       - Staff training
       - Product testing
       - Marketing campaign launches
       - Sales targets by month
    """
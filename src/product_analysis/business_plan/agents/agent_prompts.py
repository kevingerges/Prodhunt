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

    1. Executive Summary
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

    5. Implementation Plan
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

---

## Executive Summary

**Business Concept Overview**  
Sustainable Pack Co. is a national B2B company providing fully compostable, biodegradable, and recyclable packaging solutions for e-commerce businesses. We aim to reduce plastic waste in e-commerce, offering customized, environmentally friendly packaging that supports brands in meeting regulatory and consumer demands for sustainability.

**Market Opportunity**  
The U.S. e-commerce packaging market is growing at an annual rate of 6.5%, with a significant increase in demand for sustainable alternatives. Studies show that 74% of consumers prefer to purchase from brands with eco-friendly practices. Our market analysis identifies a major gap in affordable, customizable sustainable packaging for small to medium-sized online retailers.

**Value Proposition**  
Sustainable Pack Co. offers eco-friendly packaging solutions tailored to each client’s branding needs, helping them reduce environmental impact, comply with emerging regulations, and attract eco-conscious customers. Our product range includes compostable mailers, recyclable boxes, and padded envelopes.

**Financial Projections**  
- Initial Investment: $500,000
- Projected Revenue (Year 1): $1.2 million
- Gross Profit Margin (Year 1): 45%
- Projected Break-Even: 12 months
- Year 2 Revenue Projection: $2.4 million

**Implementation Plan**  
- Phase 1: Product development and supplier partnerships (Months 1-3)
- Phase 2: Pilot launch with select e-commerce clients (Months 4-6)
- Phase 3: National rollout and brand partnerships (Months 7-12)

---

## Business Strategy

**Operating Model**  
Sustainable Pack Co. operates a B2B model, selling eco-friendly packaging solutions to e-commerce businesses across the U.S. Our structure includes sourcing biodegradable materials, customizing products for branding, and distributing via a streamlined logistics network. We will maintain high standards of quality control and compliance with environmental regulations.

**Revenue Model**  
- Subscription-Based Model: Monthly or quarterly packaging supply subscriptions based on order volume.
- Bulk Purchase Options: One-time bulk orders with discounts to encourage higher volumes.
- Custom Branding Add-ons: Additional charges for custom branding and design elements.

**Growth Strategy**  
We plan to achieve 40% year-over-year growth by expanding our product line, forming strategic partnerships with eco-focused brands, and leveraging digital marketing campaigns. Expansion will target diverse e-commerce industries, including fashion, beauty, and artisanal goods.

**Scaling Approach**  
Initial focus is on small and medium-sized businesses. After establishing a strong market presence, we will scale operations to serve larger retailers by automating production, expanding manufacturing capacity, and streamlining distribution.

**Core Competencies**  
Sustainable Pack Co.'s strengths include expertise in eco-material sourcing, robust supplier partnerships, and flexible customization capabilities, all of which set us apart in the packaging industry.

---

## Go-to-Market Plan

**Market Entry Strategy**  
Our initial entry focuses on eco-conscious small and medium-sized e-commerce brands, especially those in apparel and cosmetics. We will introduce the product through direct outreach, free samples, and partnerships with industry-specific platforms.

**Marketing Approach**  
We’ll use targeted social media campaigns, partnerships with environmental influencers, and a content marketing strategy that highlights our environmental impact. Additionally, we will leverage case studies and testimonials to build credibility.

**Sales Channels**  
Our main sales channel will be our website, featuring a user-friendly ordering and customization platform. We will also have a dedicated sales team for larger accounts and strategic partnerships with eco-focused online platforms.

**Customer Acquisition Strategy**  
To acquire new clients, we will offer first-order discounts and free samples for bulk orders. We’ll also participate in trade shows like the Sustainable Packaging Expo to reach high-quality leads.

**Partnership Strategy**  
Key partnerships will include eco-friendly organizations (e.g., 1% for the Planet), e-commerce platforms, and fulfillment centers. Collaborations with suppliers will enhance product consistency and cost-effectiveness.

---

## Implementation Plan

**Key Milestones**  
- Months 1-3: Finalize supplier contracts, complete product development, and build the initial product line.
- Months 4-6: Launch pilot program, gather client feedback, and optimize logistics.
- Months 7-12: National rollout, initiate marketing campaigns, and secure partnerships with five major sustainable brands.

**Resource Requirements**  
- Personnel: Sales team, marketing specialists, supply chain manager, and quality control.
- Facilities: 10,000 sq. ft. warehouse for distribution.
- Technology: E-commerce platform for managing subscriptions, orders, and customization.

**Timeline and Phases**  
The first year will focus on establishing product-market fit, followed by a phased rollout to scale operations nationally.

**Operational Setup**  
We will partner with certified suppliers for sustainable materials and reliable fulfillment centers. Quality assurance will be integral to our operational process, with regular checks to ensure material consistency.

**Team Structure**  
- CEO: Experienced in packaging and sustainability.
- VP of Sales: Oversee client acquisition and strategic partnerships.
- Marketing Director: Lead branding and awareness campaigns.
- Supply Chain Manager: Ensure product availability and quality standards.

---

## Risk Management

**Key Risks Identification**  
1. Supply Chain Disruptions: Shortages in biodegradable materials.
2. Regulatory Changes: Compliance challenges with evolving environmental standards.
3. Competitive Market: Increasing competition in sustainable packaging.

**Mitigation Strategies**  
- Supply Chain: Establish alternative suppliers to mitigate dependency.
- Regulations: Regularly consult legal advisors and stay updated on industry regulations.
- Competition: Differentiate with flexible customization and targeted marketing to build customer loyalty.

**Success Metrics**  
- Customer Acquisition: Target 50 new B2B clients by end of Year 1.
- Renewal Rate: 75% subscription renewal.
- Environmental Impact: Achieve 20,000 pounds of plastic reduction by end of Year 1.

**Contingency Plans**  
Activate secondary suppliers in case of disruptions. Pivot to alternative eco-materials if primary materials become scarce or costly.

**Monitoring Approach**  
Monthly KPI reviews with dashboards tracking client acquisition, production metrics, and environmental impact.
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
    Always start the section with \"Executive Summary\"

    Expected structure:
    Executive Summary
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
    Always start your answer with the EXACT header \"Implementation Plan\"
    Expected structure:
    Implementation Plan
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
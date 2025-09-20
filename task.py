## Importing libraries and files
from crewai import Task

from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from tools import search_tool, read_data_tool, investment_analysis_tool, risk_assessment_tool

## Creating a task to help solve user's query
analyze_financial_document = Task(
    description="""Conduct a comprehensive financial analysis based on the user's query: {query}
    
    Your analysis should include:
    1. Read and thoroughly analyze the financial document using the available tools
    2. Extract key financial metrics, trends, and performance indicators
    3. Provide data-driven insights based on the document content
    4. Address the specific aspects mentioned in the user's query
    5. Ensure all analysis is factual and based on the document data
    6. Use internet search if additional market context is needed
    
    Focus on providing accurate, professional financial analysis that would be suitable for investment decision-making.""",

    expected_output="""A comprehensive financial analysis report that includes:
    
    **Executive Summary**
    - Key findings from the financial document analysis
    - Direct response to the user's specific query
    
    **Financial Performance Analysis**
    - Revenue trends and growth patterns
    - Profitability metrics and margins
    - Cash flow analysis
    - Key financial ratios
    
    **Market Position & Outlook**
    - Competitive positioning
    - Market opportunities and challenges
    - Future growth prospects
    
    **Investment Considerations**
    - Strengths and opportunities
    - Risks and concerns
    - Overall investment thesis
    
    All analysis should be supported by specific data points from the financial document.""",

    agent=financial_analyst,
    tools=[read_data_tool, search_tool],
    async_execution=False,
)

## Creating an investment analysis task
investment_analysis = Task(
    description="""Provide professional investment analysis and recommendations based on the financial document analysis.
    
    Your task includes:
    1. Analyze the financial performance metrics from the document
    2. Evaluate the company's competitive position and market outlook
    3. Assess valuation metrics and compare to industry benchmarks
    4. Consider the user's specific query: {query}
    5. Provide balanced investment recommendations with clear rationale
    6. Include appropriate risk considerations and disclaimers
    
    Base all recommendations on factual analysis from the financial document and current market conditions.""",

    expected_output="""Professional Investment Analysis Report:
    
    **Investment Thesis**
    - Clear investment recommendation (Buy/Hold/Sell) with rationale
    - Target price range or valuation assessment
    - Investment time horizon considerations
    
    **Key Investment Drivers**
    - Primary factors supporting the investment case
    - Competitive advantages and market position
    - Growth catalysts and opportunities
    
    **Risk Factors**
    - Key risks that could impact investment performance
    - Market and company-specific risk considerations
    - Risk mitigation strategies
    
    **Financial Metrics Analysis**
    - Relevant valuation multiples (P/E, EV/EBITDA, etc.)
    - Growth rates and profitability trends
    - Balance sheet strength and financial health
    
    **Recommendation Summary**
    - Clear action items for investors
    - Portfolio allocation suggestions
    - Monitoring points for ongoing assessment""",

    agent=investment_advisor,
    tools=[read_data_tool, investment_analysis_tool, search_tool],
    async_execution=False,
)

## Creating a risk assessment task
risk_assessment = Task(
    description="""Conduct a comprehensive risk assessment based on the financial document analysis and user query: {query}
    
    Your risk assessment should include:
    1. Analyze financial stability and leverage metrics from the document
    2. Identify market risks and competitive threats
    3. Assess operational and business model risks
    4. Evaluate regulatory and compliance risks
    5. Consider macroeconomic factors affecting the investment
    6. Provide quantitative risk metrics where possible
    7. Suggest appropriate risk management strategies
    
    Ensure all risk analysis is based on factual data and professional risk management principles.""",

    expected_output="""Comprehensive Risk Assessment Report:
    
    **Executive Risk Summary**
    - Overall risk rating (Low/Medium/High) with justification
    - Key risk factors requiring immediate attention
    - Risk-adjusted return expectations
    
    **Financial Risks**
    - Credit and liquidity risks
    - Leverage and debt service coverage analysis
    - Cash flow volatility assessment
    - Working capital and operational efficiency risks
    
    **Market and Competitive Risks**
    - Industry and sector-specific risks
    - Competitive positioning vulnerabilities
    - Market share and pricing pressure risks
    - Regulatory and compliance risks
    
    **Operational Risks**
    - Business model sustainability
    - Management and governance risks
    - Technology and innovation risks
    - Supply chain and operational dependencies
    
    **Risk Management Recommendations**
    - Portfolio diversification strategies
    - Hedging and risk mitigation approaches
    - Monitoring and early warning indicators
    - Position sizing and risk limits
    
    **Stress Testing Scenarios**
    - Best case, base case, and worst case scenarios
    - Sensitivity analysis for key variables
    - Break-even and downside protection levels""",

    agent=risk_assessor,
    tools=[read_data_tool, risk_assessment_tool, search_tool],
    async_execution=False,
)

verification = Task(
    description="""Verify and validate that the uploaded document is a legitimate financial document suitable for analysis.
    
    Your verification process should:
    1. Read and examine the document content thoroughly
    2. Identify key financial document characteristics (financial statements, metrics, etc.)
    3. Verify the document contains analyzable financial data
    4. Check for document authenticity and completeness
    5. Assess data quality and reliability for analysis purposes
    6. Provide recommendations for analysis approach based on document type
    
    Only approve documents that contain genuine financial information suitable for investment analysis.""",

    expected_output="""Document Verification Report:
    
    **Document Classification**
    - Document type (10-K, 10-Q, Annual Report, Financial Statement, etc.)
    - Company and reporting period identified
    - Document completeness assessment
    
    **Financial Content Verification**
    - Key financial statements present (Income Statement, Balance Sheet, Cash Flow)
    - Financial metrics and KPIs availability
    - Data quality and consistency check
    
    **Analysis Readiness Assessment**
    - Suitability for financial analysis (Yes/No)
    - Recommended analysis approach
    - Any limitations or data gaps identified
    
    **Verification Conclusion**
    - Clear approval or rejection for analysis
    - Specific reasons for decision
    - Next steps for document processing""",

    agent=verifier,
    tools=[read_data_tool],
    async_execution=False
)
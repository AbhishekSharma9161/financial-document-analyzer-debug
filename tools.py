## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

from crewai_tools import SerperDevTool
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

## Creating search tool
search_tool = SerperDevTool()

## Creating custom pdf reader tool
class FinancialDocumentToolInput(BaseModel):
    """Input schema for FinancialDocumentTool."""
    path: str = Field(..., description="Path to the PDF file to read")

class FinancialDocumentTool(BaseTool):
    name: str = "read_financial_document"
    description: str = "Tool to read and extract content from financial PDF documents"
    args_schema: Type[BaseModel] = FinancialDocumentToolInput

    def _run(self, path: str = 'data/TSLA-Q2-2025-Update.pdf') -> str:
        """Tool to read data from a pdf file from a path

        Args:
            path (str, optional): Path of the pdf file. Defaults to 'data/TSLA-Q2-2025-Update.pdf'.

        Returns:
            str: Full Financial Document content
        """
        try:
            import PyPDF2
            import os
            
            # Check if file exists
            if not os.path.exists(path):
                return f"Error: PDF file not found at {path}"
            
            full_report = ""
            with open(path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    content = page.extract_text()
                    
                    # Clean and format the financial document data
                    while "\n\n" in content:
                        content = content.replace("\n\n", "\n")
                        
                    full_report += content + "\n"
            
            # Return a summary if the document is too long
            if len(full_report) > 10000:
                return full_report[:10000] + "\n\n[Document truncated for processing...]"
                    
            return full_report if full_report.strip() else "No readable content found in PDF"
            
        except Exception as e:
            return f"Error reading PDF file: {str(e)}"

# Create an instance of the tool
read_data_tool = FinancialDocumentTool()

## Creating Investment Analysis Tool
class InvestmentAnalysisToolInput(BaseModel):
    """Input schema for InvestmentAnalysisTool."""
    financial_data: str = Field(..., description="Financial document data to analyze")

class InvestmentAnalysisTool(BaseTool):
    name: str = "analyze_investment_opportunities"
    description: str = "Analyze financial data to identify investment opportunities and recommendations"
    args_schema: Type[BaseModel] = InvestmentAnalysisToolInput

    def _run(self, financial_data: str) -> str:
        """Analyze financial document data for investment insights"""
        try:
            # Process and analyze the financial document data
            processed_data = financial_data
            
            # Clean up the data format
            processed_data = processed_data.replace("  ", " ")  # Remove double spaces
            
            # Basic analysis framework
            analysis_points = []
            
            # Look for key financial indicators
            if "revenue" in processed_data.lower():
                analysis_points.append("Revenue data identified for trend analysis")
            if "profit" in processed_data.lower() or "earnings" in processed_data.lower():
                analysis_points.append("Profitability metrics available for evaluation")
            if "cash flow" in processed_data.lower():
                analysis_points.append("Cash flow information present for liquidity assessment")
                
            return f"Investment Analysis Summary:\n" + "\n".join([f"- {point}" for point in analysis_points])
            
        except Exception as e:
            return f"Error in investment analysis: {str(e)}"

## Creating Risk Assessment Tool
class RiskAssessmentToolInput(BaseModel):
    """Input schema for RiskAssessmentTool."""
    financial_data: str = Field(..., description="Financial document data to assess for risks")

class RiskAssessmentTool(BaseTool):
    name: str = "assess_financial_risks"
    description: str = "Assess financial risks based on document data and market conditions"
    args_schema: Type[BaseModel] = RiskAssessmentToolInput

    def _run(self, financial_data: str) -> str:
        """Create comprehensive risk assessment from financial data"""
        try:
            risk_factors = []
            
            # Analyze for common risk indicators
            if "debt" in financial_data.lower():
                risk_factors.append("Debt levels require monitoring for leverage risk")
            if "volatile" in financial_data.lower() or "uncertainty" in financial_data.lower():
                risk_factors.append("Market volatility factors identified")
            if "competition" in financial_data.lower():
                risk_factors.append("Competitive pressures noted in market analysis")
                
            return f"Risk Assessment Summary:\n" + "\n".join([f"- {point}" for point in risk_factors])
            
        except Exception as e:
            return f"Error in risk assessment: {str(e)}"

# Create tool instances
investment_analysis_tool = InvestmentAnalysisTool()
risk_assessment_tool = RiskAssessmentTool()
from typing import Dict, List, Any, Tuple
from datetime import datetime


class ContentProcessor:
    """Handles content processing and formatting for business plan sections"""

    @staticmethod
    def extract_section_content(raw_output: str, section_identifier: str) -> str:
        """Extract content for a specific section from the raw output"""
        # Split output into sections based on headers
        sections = raw_output.split("# Agent:")

        for section in sections:
            if section_identifier.lower() in section.lower():
                # Extract content after "Final Answer:" if present
                if "Final Answer:" in section:
                    content = section.split("Final Answer:")[1].strip()
                else:
                    content = section.strip()

                # Clean up the content
                lines = [line.strip() for line in content.split('\n') if line.strip()]
                return '\n'.join(lines)

        return ""

    @staticmethod
    def process_market_analysis(content: str) -> str:
        """Process and format market analysis content"""
        if not content:
            return ""

        formatted = []
        current_section = None

        for line in content.split('\n'):
            line = line.strip()
            if not line:
                continue

            # Handle section headers
            if line.startswith('**') and line.endswith('**'):
                current_section = line
                formatted.append(f"\n### {line.strip('*')}\n")
            # Handle bullet points
            elif line.startswith('*'):
                formatted.append(line)
            # Handle normal text
            else:
                formatted.append(line)

        return '\n'.join(formatted)

    @staticmethod
    def process_financial_data(content: str) -> str:
        """Process and format financial data"""
        if not content:
            return ""

        formatted = []
        in_table = False

        for line in content.split('\n'):
            line = line.strip()
            if not line:
                continue

            # Handle section headers
            if line.startswith('###'):
                formatted.append(f"\n{line}\n")
            # Handle tables
            elif '|' in line:
                in_table = True
                formatted.append(line)
            # Handle bullet points
            elif line.startswith('*'):
                if in_table:
                    formatted.append('\n')
                    in_table = False
                formatted.append(line)
            # Handle normal text
            else:
                if in_table:
                    formatted.append('\n')
                    in_table = False
                formatted.append(line)

        return '\n'.join(formatted)

    @staticmethod
    def process_competitive_analysis(content: str) -> str:
        """Process and format competitive analysis"""
        if not content:
            return ""

        formatted = []

        for line in content.split('\n'):
            line = line.strip()
            if not line:
                continue

            # Handle section headers
            if line.startswith('###'):
                formatted.append(f"\n{line}\n")
            # Handle subsection headers
            elif line.startswith('* **'):
                formatted.append(f"\n{line}\n")
            # Handle bullet points
            elif line.startswith('*'):
                formatted.append(line)
            # Handle normal text
            else:
                formatted.append(line)

        return '\n'.join(formatted)


class MarkdownFormatter:
    """Handles markdown formatting for business plan outputs"""

    @staticmethod
    def generate_markdown(business_plan: Dict) -> str:
        """Generate enhanced markdown with better formatting"""
        md_output = "# Comprehensive Business Plan\n\n"

        # Add table of contents
        md_output += MarkdownFormatter._generate_toc(business_plan)
        md_output += "\n---\n\n"

        # Add each section
        for section, data in business_plan.items():
            section_title = section.replace("_", " ").title()
            md_output += f"## {section_title}\n\n"

            if "status" in data and data["status"] == "complete" and "content" in data and data["content"]:
                md_output += data["content"][0]  # Content is now preprocessed
            else:
                if "status" not in data:
                    md_output += "*Section status is unknown*\n\n"
                else:
                    md_output += "*Section content may be incomplete*\n\n"
                if "content" in data and data["content"]:
                    md_output += data["content"][0]

            md_output += "\n\n---\n\n"

        return md_output

    @staticmethod
    def _generate_toc(business_plan: Dict) -> str:
        """Generate table of contents"""
        toc = "## Table of Contents\n\n"
        for section in business_plan.keys():
            section_title = section.replace("_", " ").title()
            toc += f"- [{section_title}](#{section.lower()})\n"
        return toc

    @staticmethod
    def generate_error_report(error: Exception) -> str:
        """Generate formatted error report"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"""# Error Report - {timestamp}

## Error Details
- **Type:** {type(error).__name__}
- **Message:** {str(error)}

## Business Plan Status
The business plan generation encountered an error during processing.

### Recommendations
1. Check the input data format
2. Verify all required sections are present
3. Review agent outputs for completeness
4. Try regenerating the business plan

### Technical Details
```python
{str(error.__class__.__name__)}: {str(error)}
```

---
*This error report was generated automatically. Please review the error details and try again.*
"""


class ContentFormatter:
    """Handles content formatting and integration"""

    @staticmethod
    def integrate_sections(business_plan: Dict, examples: Dict) -> Dict:
        """Integrate sections with better cohesion"""
        # Initialize structure if missing
        sections = [
            "market_analysis", 
            "financial_projections", 
            "competitive_analysis",
            "executive_summary",
            "implementation_plan"
        ]
        
        enhanced_plan = {}
        for section in sections:
            if section not in business_plan:
                print("Section not found: ", section)
                business_plan[section] = {"content": [], "status": "pending"}
            elif not isinstance(business_plan[section], dict):
                business_plan[section] = {"content": [business_plan[section]], "status": "complete"}
            elif "content" not in business_plan[section]:
                business_plan[section]["content"] = []
        
        enhanced_plan = business_plan.copy()

        for section, data in enhanced_plan.items():
            if "content" in data and data["content"]:
                data["content"] = [
                    ContentFormatter._enhance_section_cohesion(
                        data["content"], section, examples
                    )
                ]

        return enhanced_plan

    @staticmethod
    def _enhance_section_cohesion(content: List[str], section_type: str, examples: Dict) -> str:
        """Enhance section cohesion with transitions"""
        transitions = {
            "market_analysis": ["Building on these insights,", "Furthermore,", "Importantly,"],
            "financial_projections": ["These projections indicate", "Based on these figures,"],
            "competitive_analysis": ["In the competitive landscape,", "Given this position,"]
        }

        enhanced_content = []
        current_transition_idx = 0

        for content_piece in content:
            if section_type in transitions and current_transition_idx < len(transitions[section_type]):
                enhanced_content.append(f"\n{transitions[section_type][current_transition_idx]}")
                current_transition_idx += 1
            enhanced_content.append(content_piece)

        return "\n".join(enhanced_content)
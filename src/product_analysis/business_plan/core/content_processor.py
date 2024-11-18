from typing import Dict, List, Tuple
import re


class ContentProcessor:
    """Handles content processing and formatting for business plan sections"""

    @staticmethod
    def format_section(content: str) -> str:
        """Format a section's content with proper structure"""
        lines = content.split('\n')
        formatted = []
        current_section = None

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if line.endswith(':') or line.endswith('-'):
                current_section = line.rstrip(':-')
                formatted.append(f"\n**{current_section}**\n")
            elif line.startswith('-') or line.startswith('*'):
                formatted.append(line)
            elif ':' in line:
                key, value = line.split(':', 1)
                formatted.append(f"- **{key.strip()}**: {value.strip()}")
            else:
                formatted.append(line)

        return '\n'.join(formatted)

    @staticmethod
    def process_market_analysis(content: str) -> str:
        """Process market analysis content with highlighting"""
        try:
            formatted = ContentProcessor.format_section(content)
            return ContentProcessor.highlight_market_metrics(formatted)
        except Exception as e:
            return f"Error processing market analysis: {str(e)}\n{content}"

    @staticmethod
    def process_financial_data(content: str) -> str:
        """Process financial data with metric formatting"""
        try:
            formatted = ContentProcessor.format_section(content)
            return ContentProcessor.format_financial_metrics(formatted)
        except Exception as e:
            return f"Error processing financial data: {str(e)}\n{content}"

    @staticmethod
    def process_competitive_analysis(content: str) -> str:
        """Process competitive analysis with table formatting"""
        try:
            formatted = ContentProcessor.format_section(content)

            if "competitor" in formatted.lower():
                lines = formatted.split('\n')
                table_lines = []
                in_competitor_section = False

                for line in lines:
                    if "competitor" in line.lower() and line.endswith(':'):
                        in_competitor_section = True
                        table_lines.extend([
                            "\n| Competitor | Strengths | Weaknesses | Market Share |",
                            "|------------|-----------|------------|--------------|"
                        ])
                    elif in_competitor_section and line.startswith('-'):
                        parts = line.strip('- ').split(',')
                        if len(parts) >= 2:
                            competitor = parts[0].strip()
                            details = [p.strip() for p in parts[1:]]
                            table_lines.append(f"| {competitor} | {' | '.join(details)} |")
                    else:
                        table_lines.append(line)

                formatted = '\n'.join(table_lines)

            return formatted
        except Exception as e:
            return f"Error processing competitive analysis: {str(e)}\n{content}"

    @staticmethod
    def format_financial_metrics(content: str) -> str:
        """Format financial metrics with currency and number formatting"""
        try:
            lines = content.split('\n')
            formatted = []
            in_metrics = False

            for line in lines:
                if any(term in line.lower() for term in ['revenue', 'cost', 'profit', 'break-even']):
                    if not in_metrics:
                        in_metrics = True
                        formatted.append("\n**Financial Metrics:**\n")

                if ':' in line and any(c.isdigit() for c in line):
                    key, value = line.split(':', 1)
                    if '$' in value or any(term in key.lower() for term in ['cost', 'revenue', 'profit']):
                        try:
                            number = float(''.join(c for c in value if c.isdigit() or c == '.'))
                            formatted.append(f"- **{key.strip()}:** ${number:,.2f}")
                            continue
                        except ValueError:
                            pass

                formatted.append(line)

            return '\n'.join(formatted)
        except Exception as e:
            return f"Error formatting financial metrics: {str(e)}\n{content}"

    @staticmethod
    def highlight_market_metrics(content: str) -> str:
        """Add visual highlights to market metrics"""
        try:
            lines = content.split('\n')
            highlighted = []

            for line in lines:
                if any(term in line.lower() for term in ['market size', 'growth rate', 'cagr', 'market share']):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        highlighted.append(f"🔍 **{key.strip()}:**{value}")
                    else:
                        highlighted.append(f"🔍 {line}")
                elif any(term in line.lower() for term in ['demographic', 'age group', 'target audience']):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        highlighted.append(f"👥 **{key.strip()}:**{value}")
                    else:
                        highlighted.append(f"👥 {line}")
                elif 'trend' in line.lower():
                    if ':' in line:
                        key, value = line.split(':', 1)
                        highlighted.append(f"📈 **{key.strip()}:**{value}")
                    else:
                        highlighted.append(f"📈 {line}")
                else:
                    highlighted.append(line)

            return '\n'.join(highlighted)
        except Exception as e:
            return f"Error highlighting market metrics: {str(e)}\n{content}"
    
    @staticmethod
    def process_market_analysis(content: str, market_data: Dict = None) -> str:
        """Process market analysis content with enhanced insights"""
        try:
            formatted = ContentProcessor.format_section(content)
            
            if market_data:
                formatted += "\n\n### Market Intelligence Insights\n"
                
                if "market_sentiment" in market_data:
                    sentiment = market_data["market_sentiment"]
                    formatted += f"\n**Market Sentiment**: {sentiment['interpretation']}"
                    formatted += f"\n- Confidence Score: {sentiment['confidence']}\n"
                
                if "identified_trends" in market_data:
                    formatted += "\n**Key Market Trends**:\n"
                    for trend in market_data["identified_trends"]:
                        formatted += f"- {trend['type'].title()}: {', '.join(trend['keywords'])} "
                        formatted += f"(Confidence: {trend['confidence']})\n"
                

                if "opportunities" in market_data:
                    formatted += "\n**Market Opportunities**:\n"
                    for opp in market_data["opportunities"]:
                        formatted += f"- {opp['description']} "
                        formatted += f"(Confidence: {opp['confidence']})\n"
            
                if "risks" in market_data:
                    formatted += "\n**Market Risks**:\n"
                    for risk in market_data["risks"]:
                        formatted += f"- {risk['description']} "
                        formatted += f"(Type: {risk['risk_type']}, "
                        formatted += f"Confidence: {risk['confidence']})\n"
            
            return ContentProcessor.highlight_market_metrics(formatted)
        except Exception as e:
            return f"Error processing market analysis: {str(e)}\n{content}"

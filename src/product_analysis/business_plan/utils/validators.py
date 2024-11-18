from typing import Dict, List
from transformers import pipeline
import spacy
from collections import Counter

class BusinessPlanValidator:
    """Validates business plan content and structure with NLP analysis"""

    required_sections = {
        "executive_summary": ["overview", "opportunity", "value proposition"],
        "market_analysis": ["market size", "segmentation", "trends"],
        "financial_projections": ["costs", "revenue", "projections"],
        "competitive_analysis": ["competitors", "positioning", "advantages"],
        "implementation_plan": ["timeline", "milestones", "resources"]
    }

    def __init__(self):
        """Initialize NLP components"""
        try:
            self.nlp = spacy.load("en_core_web_sm")
            self.sentiment_analyzer = pipeline("sentiment-analysis")
            print("NLP components initialized successfully")
        except Exception as e:
            print(f"Warning: NLP initialization failed: {str(e)}")
            self.nlp = None
            self.sentiment_analyzer = None

    @staticmethod
    def validate_business_plan(business_plan: Dict) -> Dict:
        """Validate the completeness and quality of the business plan"""
        warnings = []

        for section, data in business_plan.items():
            if data["status"] != "complete":
                warnings.append(f"Section '{section}' may be incomplete")
            if not data["content"]:
                warnings.append(f"Section '{section}' has no content")

            if section in BusinessPlanValidator.required_sections:
                missing_keywords = BusinessPlanValidator._check_required_keywords(
                    data["content"],
                    BusinessPlanValidator.required_sections[section]
                )
                if missing_keywords:
                    warnings.append(
                        f"Section '{section}' missing key elements: {', '.join(missing_keywords)}"
                    )

        return {
            "is_valid": len(warnings) == 0,
            "warnings": warnings
        }

    @staticmethod
    def _check_required_keywords(content: List[str], required_keywords: List[str]) -> List[str]:
        """Check content for required keywords"""
        content_text = ' '.join(content).lower()
        return [
            keyword for keyword in required_keywords
            if keyword not in content_text
        ]

    def validate_section_quality(self, section: str, content: List[str]) -> Dict:
        """Validate the quality of a specific section with NLP analysis"""
        quality_score = 0
        issues = []

        # Check content length
        if not content or not any(content):
            issues.append("Section is empty")
            return {"score": 0, "issues": issues}

        content_text = ' '.join(content)

        if len(content_text.split()) < 100:
            issues.append("Content may be too brief")
        else:
            quality_score += 0.2

        if '**' in content_text:
            quality_score += 0.1
        else:
            issues.append("Lacks formatted elements")

        if any(line.startswith('-') for line in content):
            quality_score += 0.1
        else:
            issues.append("Lacks structured bullet points")

        if self.nlp:
            try:
                doc = self.nlp(content_text)
                
                avg_sent_length = sum(len(sent.text.split()) for sent in doc.sents) / len(list(doc.sents))
                if avg_sent_length > 25:
                    issues.append("Sentences may be too long for clarity")
                elif avg_sent_length < 10:
                    issues.append("Content may lack detail")
                else:
                    quality_score += 0.2

                key_phrases = [chunk.text for chunk in doc.noun_chunks]
                business_terms = ["market", "revenue", "growth", "strategy", "competitive", 
                                "financial", "investment", "opportunity", "risk"]
                term_usage = sum(1 for phrase in key_phrases if any(term in phrase.lower() for term in business_terms))
                
                if term_usage < 5:
                    issues.append("Limited use of business terminology")
                else:
                    quality_score += 0.2

                if self.sentiment_analyzer:
                    try:
                        sentiment = self.sentiment_analyzer(content_text[:512])[0]
                        if sentiment['label'] == 'NEGATIVE' and section not in ['risk_analysis', 'competitive_analysis']:
                            issues.append("Tone may be too negative for section type")
                        quality_score += 0.2
                    except Exception as e:
                        print(f"Sentiment analysis failed: {str(e)}")

            except Exception as e:
                print(f"NLP analysis failed: {str(e)}")

        return {
            "score": round(quality_score, 2),
            "issues": issues
        }
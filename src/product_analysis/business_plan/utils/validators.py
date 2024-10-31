from typing import Dict, List


class BusinessPlanValidator:
    """Validates business plan content and structure"""

    required_sections = {
        "executive_summary": ["overview", "opportunity", "value proposition"],
        "market_analysis": ["market size", "segmentation", "trends"],
        "financial_projections": ["costs", "revenue", "projections"],
        "competitive_analysis": ["competitors", "positioning", "advantages"],
        "implementation_plan": ["timeline", "milestones", "resources"]
    }

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

    @staticmethod
    def validate_section_quality(section: str, content: List[str]) -> Dict:
        """Validate the quality of a specific section"""
        quality_score = 0
        issues = []

        # Check content length
        if not content or not any(content):
            issues.append("Section is empty")
            return {"score": 0, "issues": issues}

        content_text = ' '.join(content)

        # Check length
        if len(content_text.split()) < 100:
            issues.append("Content may be too brief")
        else:
            quality_score += 0.3

        # Check formatting
        if '**' in content_text:
            quality_score += 0.2
        else:
            issues.append("Lacks formatted elements")

        # Check structure
        if any(line.startswith('-') for line in content):
            quality_score += 0.2
        else:
            issues.append("Lacks structured bullet points")

        # Check metrics
        if any(char.isdigit() for char in content_text):
            quality_score += 0.3
        else:
            issues.append("Lacks numerical data or metrics")

        return {
            "score": round(quality_score, 2),
            "issues": issues
        }
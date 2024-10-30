from typing import Dict, List, Optional, Any
import json
from datetime import datetime


class BusinessInputProcessor:
    def __init__(self):
        self.required_fields = {
            "business_idea": "Main business concept",
            "industry": "Primary industry sector",
            "target_market": "Target audience/market",
            "scale": "Business scale (Local/Regional/National/Global)",
            "initial_investment": "Estimated initial investment range",
            "timeline": "Expected timeline to launch"
        }

        self.clarifying_questions = {
            "industry": {
                "Tech": ["B2B or B2C?", "Software or Hardware?", "Cloud-based?"],
                "Retail": ["Online or Physical?", "Product categories?", "Price point?"],
                "Service": ["Professional or Consumer?", "Location-dependent?", "Subscription-based?"]
            },
            "scale": {
                "Local": ["Single or multiple locations?", "Service radius?"],
                "Regional": ["Which regions?", "Expansion timeline?"],
                "National": ["Starting regions?", "Distribution strategy?"],
                "Global": ["Initial target countries?", "International constraints?"]
            }
        }

    def get_basic_input(self) -> Dict[str, str]:
        """Gather initial business idea information"""
        inputs = {}
        print("\n=== Business Plan Input Collection ===")
        print("Please provide the following information:\n")

        for field, description in self.required_fields.items():
            value = input(f"{description}: ").strip()
            inputs[field] = value

        return inputs

    def get_clarifying_info(self, basic_input: Dict[str, str]) -> Dict[str, Any]:
        """Get additional context based on initial inputs"""
        context = basic_input.copy()

        # Get industry-specific details
        if basic_input["industry"] in self.clarifying_questions["industry"]:
            print(f"\nSpecific questions about your {basic_input['industry']} business:")
            industry_context = {}
            for question in self.clarifying_questions["industry"][basic_input["industry"]]:
                answer = input(f"{question} ").strip()
                industry_context[question] = answer
            context["industry_details"] = industry_context

        # Get scale-specific details
        if basic_input["scale"] in self.clarifying_questions["scale"]:
            print(f"\nQuestions about your {basic_input['scale']} scale:")
            scale_context = {}
            for question in self.clarifying_questions["scale"][basic_input["scale"]]:
                answer = input(f"{question} ").strip()
                scale_context[question] = answer
            context["scale_details"] = scale_context

        return context

    def preprocess_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Preprocess and validate the gathered information"""
        processed = {
            "timestamp": datetime.now().isoformat(),
            "input_data": context,
            "derived_context": {},
            "flags": []
        }

        # Derive additional context
        if "industry_details" in context:
            processed["derived_context"]["business_model"] = self._derive_business_model(context)
            processed["derived_context"]["complexity_level"] = self._assess_complexity(context)
            processed["derived_context"]["key_challenges"] = self._identify_challenges(context)

        # Add warning flags for missing or concerning information
        if not context.get("initial_investment"):
            processed["flags"].append("Missing investment information")
        if not context.get("timeline"):
            processed["flags"].append("Missing timeline information")

        return processed

    def _derive_business_model(self, context: Dict[str, Any]) -> str:
        """Derive likely business model based on inputs"""
        industry = context["industry"].lower()
        details = context.get("industry_details", {})

        if "B2B" in str(details):
            return "B2B"
        elif "B2C" in str(details):
            return "B2C"
        elif "subscription" in str(details).lower():
            return "Subscription"
        elif "service" in industry:
            return "Service-based"
        else:
            return "Traditional"

    def _assess_complexity(self, context: Dict[str, Any]) -> str:
        """Assess business complexity based on inputs"""
        scale = context["scale"].lower()
        if scale == "global":
            return "High"
        elif scale == "national":
            return "Medium-High"
        elif scale == "regional":
            return "Medium"
        else:
            return "Standard"

    def _identify_challenges(self, context: Dict[str, Any]) -> List[str]:
        """Identify potential challenges based on inputs"""
        challenges = []
        scale = context["scale"].lower()
        industry = context["industry"].lower()

        if scale in ["global", "national"]:
            challenges.append("Complex logistics and distribution")
        if "tech" in industry:
            challenges.append("Rapid technology changes")
        if context.get("timeline", "").lower() in ["immediate", "fast", "quick"]:
            challenges.append("Aggressive timeline")

        return challenges

    def process_business_idea(self) -> Dict[str, Any]:
        """Main method to gather and process all business information"""
        basic_input = self.get_basic_input()
        detailed_input = self.get_clarifying_info(basic_input)
        processed_context = self.preprocess_context(detailed_input)

        return processed_context
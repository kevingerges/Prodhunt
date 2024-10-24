#!/usr/bin/env python
import sys
import os
import logging
from crew import BusinessPlanCrew
from agents import BusinessPlanAgents

logging.basicConfig(level=logging.DEBUG)

def run():
    agents = BusinessPlanAgents()
    print(f"Using LLM: {agents.market_research_agent.llm}")
    print(f"LLM type: {type(agents.market_research_agent.llm)}")
    print(f"LLM attributes: {vars(agents.market_research_agent.llm)}")
    
    inputs = {"business_idea": input("Enter your business idea: ")}
    BusinessPlanCrew().crew().kickoff(inputs=inputs)

if __name__ == "__main__":
    run()

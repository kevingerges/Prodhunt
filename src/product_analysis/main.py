#!/usr/bin/env python
import sys
import os
from crew import BusinessPlanCrew
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from agents import BusinessPlanAgents

load_dotenv()


def run():

    
    inputs = {"business_idea": input("Enter your business idea: ")}
    crew = BusinessPlanCrew().crew()
    result = crew.kickoff(inputs=inputs)
    print(result)

if __name__ == "__main__":
    run()

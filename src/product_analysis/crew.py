from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class BusinessAnalystCrew():
		"""BusinessAnalyst crew"""
		agents_config = 'config/agents.yaml'
		tasks_config = 'config/tasks.yaml'

		@agent
		def market_analysis_agent(self) -> Agent:
				return Agent(config=self.agents_config['market_analysis_agent'])

		@agent
		def financial_projection_agent(self) -> Agent:
				return Agent(config=self.agents_config['financial_projection_agent'])

		@agent
		def operational_feasibility_agent(self) -> Agent:
				return Agent(config=self.agents_config['operational_feasibility_agent'])

		@agent
		def legal_considerations_agent(self) -> Agent:
				return Agent(config=self.agents_config['legal_considerations_agent'])

		@agent
		def central_aggregator_agent(self) -> Agent:
				return Agent(config=self.agents_config['central_aggregator_agent'])

		@task
		def market_analysis_task(self) -> Task:
				return Task(config=self.tasks_config['market_analysis_task'], agent=self.market_analysis_agent())

		@task
		def financial_projection_task(self) -> Task:
				return Task(config=self.tasks_config['financial_projection_task'], agent=self.financial_projection_agent())

		@task
		def operational_feasibility_task(self) -> Task:
				return Task(config=self.tasks_config['operational_feasibility_task'], agent=self.operational_feasibility_agent())

		@task
		def legal_considerations_task(self) -> Task:
				return Task(config=self.tasks_config['legal_considerations_task'], agent=self.legal_considerations_agent())

		@task
		def central_aggregation_task(self) -> Task:
				return Task(config=self.tasks_config['central_aggregation_task'], agent=self.central_aggregator_agent())

		@crew
		def crew(self) -> Crew:
				"""Creates the BusinessAnalyst crew"""
				return Crew(
						agents=self.agents,  # Automatically created by the @agent decorator
						tasks=self.tasks,  # Automatically created by the @task decorator
						process=Process.sequential,
						verbose=2
				)

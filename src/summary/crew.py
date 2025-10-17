from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from dotenv import dotenv_values

config = dotenv_values(".env")

llm = LLM(model="mistral/mistral-large-latest", api_key=config["MISTRAL_API_KEY"])


@CrewBase
class SummarizeCrew:
    """Research crew for comprehensive topic analysis and reporting"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def summarizer(self) -> Agent:
        return Agent(config=self.agents_config["summarizer"], verbose=True, llm=llm)

    @task
    def summarize_task(self) -> Task:
        return Task(config=self.tasks_config["summarize_task"], llm=llm)

    @crew
    def crew(self) -> Crew:
        """Creates the research crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )


def run_summary(topic: str, context: str) -> str:
    """
    Run the research crew.
    """
    inputs = {"topic": topic, "context": context}

    # Create and run the crew
    result = SummarizeCrew().crew().kickoff(inputs=inputs)

    return result.raw

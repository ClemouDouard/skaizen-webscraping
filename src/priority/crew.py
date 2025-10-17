from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from dotenv import dotenv_values


@CrewBase
class PrioritizeCrew:
    """Chose amongst a lot of search results"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def prioritizer(self) -> Agent:
        return Agent(config=self.agents_config["prioritizer"], verbose=True, llm=llm)

    @task
    def prioritizer_task(self) -> Task:
        return Task(config=self.tasks_config["prioritizer_task"], llm=llm)

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )


def run_prioritize(links, names):
    inputs = {"links": links, "names": names}

    result = PrioritizeCrew().crew().kickoff(inputs=inputs)

    return result.raw

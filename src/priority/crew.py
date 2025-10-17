from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from dotenv import dotenv_values

config = dotenv_values(".env")

llm = LLM(model="mistral/ministral-3b-latest", api_key=config["MISTRAL_API_KEY"],temperature=0.1)

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


def run_prioritize(search_results):
    inp = {"context" : search_results}

    result = PrioritizeCrew().crew().kickoff(inputs=inp)

    return result.raw

from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class SummarizeCrew:
    """Research crew for comprehensive topic analysis and reporting"""

    agents: List[BaseAgent]
    tasks: List[Task]

    llm = LLM(model="mistral/mistral-large-latest", api_key="")

    @agent
    def summarizer(self) -> Agent:
        return Agent(config=self.agents_config["summarizer"], verbose=True, llm=llm)

    @task
    def analysis_task(self) -> Task:
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


def run_crew(topic: str, context: str) -> str:
    """
    Run the research crew.
    """
    inputs = {"topic": topic}

    # Create and run the crew
    result = SummarizeCrew().crew().kickoff(inputs=inputs)

    return result.raw

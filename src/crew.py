from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class SummarizeCrew:
    """Research crew for comprehensive topic analysis and reporting"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def summarizer(self) -> Agent:
        return Agent(config=self.agents_config["summarizer"], verbose=True)

    @task
    def analysis_task(self) -> Task:
        return Task(config=self.tasks_config["summarize_task"])

    @crew
    def crew(self) -> Crew:
        """Creates the research crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )


def run_crew(topic: str):
    """
    Run the research crew.
    """
    inputs = {"topic": topic}

    # Create and run the crew
    result = SummarizeCrew().crew().kickoff(inputs=inputs)

    return result.raw

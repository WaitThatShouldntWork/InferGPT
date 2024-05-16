from .tool import tool_metadata
from .types import Parameter
from .agent import Agent, agent_metadata

@tool_metadata(
        name="create file",
        description="create a file with defined filename and Python list of strings for each line in file",
        parameters={
            "file_name": Parameter(
            type="string",
            description="the name of the file",
        ),
            "file_contents": Parameter(
            type="list[string]",
            description="A valid Python list of strings for each line in a file",
        )
    }
)
def create_file(file_name: str, file_contents: list[str]) -> str:
    f = open(f"{file_name}.txt", "a")
    f.writelines(file_contents)
    f.close()

    return f"I have create the file {file_name} with the passed contents"


@agent_metadata(
    name="CreateFileAgent",
    description="This agent is able to create new files of any type",
    tools=[create_file],
    prompt="You are a file writer. Make sure when assigning file_contents lines are split sensibly in the list[string]"
)
class CreateFileAgent(Agent):
    pass

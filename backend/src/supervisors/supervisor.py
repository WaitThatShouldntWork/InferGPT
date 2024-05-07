import logging
from src.prompts import PromptEngine
from src.router import pick_agent
from src.agents import DatastoreAgent, GoalAchievedAgent, UnresolvableTaskAgent, MathsAgent

unresolvable_task_agent = UnresolvableTaskAgent()
goal_achieved_agent = GoalAchievedAgent()
list_of_agents = [ DatastoreAgent(), MathsAgent(), goal_achieved_agent, unresolvable_task_agent ]

prompt_engine = PromptEngine()


def still_solving_tasks(current_agent, iter_count):
    agent_calling_unresolved = current_agent != "UnresolvableTaskAgent" and current_agent != "GoalAchievedAgent"
    count_not_exceeded = iter_count < 5
    return agent_calling_unresolved and count_not_exceeded


def onto_next_task(best_next_step_json):
    return best_next_step_json["current_or_next_task"].__contains__("next")


def find_agent_from_name(current_agent_name):
    return (agent for agent in list_of_agents if agent.name == current_agent_name)


def call_agent(next_step_dict, current_task, next_task, history):
    current_agent = next(find_agent_from_name(next_step_dict["agent"]), unresolvable_task_agent)
    task_to_send_to_agent = current_task if next_step_dict["current_or_next_task"] == "current" else next_task
    return current_agent.invoke(task_to_send_to_agent + "\n\nIn the past you found out the following:\n" + str(history))


def solve_all_tasks(tasks_dict):
    current_agent_name = "InitialAgent"
    history = []
    attempts_count = 0
    task_step = 0
    num_of_tasks = len(tasks_dict["tasks"])
    logging.info("Solving all (" + str(num_of_tasks) + ") tasks")

    # Check where we should keep iterating to call more agents
    while still_solving_tasks(current_agent_name, attempts_count):
        logging.info(f"attempts_count: {attempts_count}, task_step: {task_step}")
        logging.info(f"current_agent: {current_agent_name}, history: {history}")

        # Assign tasks
        current_task = str(tasks_dict["tasks"][task_step])

        # If on the last task don't iterate
        if (task_step == num_of_tasks-1):
            next_task = "There is no next task. Please solve the Current Task"
        else:
            next_task = str(tasks_dict["tasks"][task_step+1])

        # Call LLM to decide next best step
        next_step_dict = pick_agent(current_task, next_task, list_of_agents, history)

        # Check if we are done
        if next_step_dict["agent"] == "UnresolvableTaskAgent":
            logging.info("UnresolvableTaskAgent called :( returning fail case")
            return "I am sorry, but I was unable to find an answer to your question"
        if next_step_dict["agent"] == "GoalAchievedAgent":
            logging.info("goal achieved!")
            return next_step_dict["thoughts"]["speak"] # TODO: Properly return answer when problem is solved

        # Call agent
        agent_result = call_agent(next_step_dict, current_task, next_task, history)

        # Store the result in the prompt
        history.append(prompt_engine.load_prompt(
            "write-to-history",
            agent_name=current_agent_name,
            agent_result=agent_result
        ))

        # Are we solving the current or next task?
        task_progression_status = "We attempted to solve the current task"
        if onto_next_task(next_step_dict):
            if task_step == num_of_tasks:
                task_progression_status = "We attempted to solve the final task!"
            else:
                task_progression_status = "We attempted to solve the next task - will move next task to current task"
                task_step += 1
        logging.info("Did we just solve the current or next task? " + task_progression_status)
        attempts_count += 1

    return agent_result # TODO: Add summariser method

import logging
from prompts import PromptEngine
from router import pick_agent
from agents import DatastoreAgent, GoalAchievedAgent, UnresolvableTaskAgent

unresolvable_task_agent = UnresolvableTaskAgent()
goal_achieved_agent = GoalAchievedAgent()
list_of_agents = [ DatastoreAgent(), goal_achieved_agent, unresolvable_task_agent ]

prompt_engine = PromptEngine()


def still_solving_tasks(current_agent, iter_count):
    agent_calling_unresolved = current_agent != "UnresolvableTaskAgent" and current_agent != "GoalAchievedAgent"
    count_not_exceeded = iter_count < 5
    return agent_calling_unresolved and count_not_exceeded


def onto_next_task(best_next_step_json):
    return best_next_step_json["current_or_next_task"].__contains__("next")


def find_agent_from_name(current_agent_name):
    return (agent for agent in list_of_agents if agent.name == current_agent_name)


def solve_all_tasks(tasks_json):
    current_agent_name = "initial_agent"
    final_result = ""
    history = []
    attempts_count = 0
    task_step = 0
    task_total_count = len(tasks_json["tasks"])
    logging.info("Solving all (" + str(task_total_count) + ") tasks")

    # Check where we should keep iterating to call more agents
    while still_solving_tasks(current_agent_name, attempts_count):
        logging.info(f"attempts_count: {attempts_count}, task_step: {task_step}")
        logging.info(f"current_agent: {current_agent_name}, history: {history}")

        # Assign tasks
        current_task = str(tasks_json["tasks"][task_step])

        # Don't assign a next task if only 1 has been generated
        if (task_step >= task_total_count):
            next_task = "There is no next task - the Current Task is the final task"
        else:
            next_task = str(tasks_json["tasks"][task_step+1])

        # Call LLM to decide next best step
        best_next_step_json = pick_agent(current_task, next_task, list_of_agents, history)
        current_agent_name = best_next_step_json["agent"]

        # Check if we are done
        if current_agent_name == "UnresolvableTaskAgent":
            logging.info("UnresolvableTaskAgent called :( returning fail case")
            return "I am sorry, but I was unable to find an answer to your question"
        if current_agent_name == "GoalAchievedAgent":
            logging.info("goal achieved!")
            return best_next_step_json["thoughts"]["speak"] # TODO: Properly return answer when problem is solved

        # Call agent
        current_agent = next(find_agent_from_name(current_agent_name), unresolvable_task_agent)
        task_to_send_to_agent = current_task if best_next_step_json["current_or_next_task"] == "current" else next_task
        agent_result = current_agent.invoke(task_to_send_to_agent)

        # Store the result in the prompt
        history.append(prompt_engine.load_prompt(
            "write-to-history",
            agent_name=current_agent_name, agent_result=agent_result
            )
        )

        # Are we solving the current or next task?
        task_progression_status = "We attempted to solve the current task"
        if onto_next_task(best_next_step_json):
            task_progression_status = "We attempted to solve the next task - will move next task to current task for next iteration"
            task_step += 1
        logging.info("Did we just solve the current or next task? " + task_progression_status)
        attempts_count += 1

    return final_result

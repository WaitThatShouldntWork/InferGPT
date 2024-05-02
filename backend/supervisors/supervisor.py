import logging
from router import pick_agent


def still_solving_tasks(current_agent, iter_count):
    agent_calling_unresolved = current_agent != "UnresolvableTaskAgent" and current_agent != "GoalAchievedAgent"
    count_not_exceeded = iter_count < 5
    return agent_calling_unresolved and count_not_exceeded


def onto_next_task(best_next_step_json):
    return best_next_step_json["current_or_next_task"].__contains__("next")


# TODO: Adjust so the agent is _actually_ called
def call_agent_picked(agent_str):
    answer = ""
    match agent_str:
        case "database_agent":
            logging.info("Database agent called!")
            answer = "Last month you spend £6.99 on Spotify"
        case "financial_advisor_agent":
            logging.info("Financial advisor agent called!")
            answer = "you should invest in stocks and shares"
        case "web_search_agent":
            logging.info("Web search agent called!")
            answer = "The Labrador Retriever or simply Labrador is a British breed of retriever gun dog"
        case "UnresolvableTaskAgent":
            logging.info("UnresolvableTaskAgent called :( throwing exception")
            raise Exception("router could not find an agent to call for the task")
        case "GoalAchievedAgent":
            logging.info("goal achieved!")
            answer = "goal achieved"

    return answer


def solve_all_tasks(tasks_json):

    current_agent = "initial_agent"
    final_result = ""
    history = [""]
    attempts_count = 0
    task_step = 0
    task_total_count = len(tasks_json["tasks"])
    logging.info("Solving all (" + str(task_total_count) + ") tasks")

    # Check where we should keep iterating to call more agents
    while still_solving_tasks(current_agent, attempts_count):
        logging.info(f"attempts_count: {attempts_count}, task_step: {task_step}")
        logging.info(f"current_agent: {current_agent}, history: {history}")

        # Assign tasks
        current_task = str(tasks_json["tasks"][task_step])

        # Don't assign a next task if only 1 has been generated
        if (task_step >= task_total_count):
            next_task = "There is no next task - the Current Task is the final task"
        else:
            next_task = str(tasks_json["tasks"][task_step+1])

        # Call LLM to decide next best step
        best_next_step_json = pick_agent(current_task, next_task, history)
        current_agent = best_next_step_json["agent"]

        # Check if we are done
        if current_agent == "UnresolvableTaskAgent":
            logging.info("UnresolvableTaskAgent called :( returning fail case")
            return "I am sorry, but I was unable to find an answer to your question"
        if current_agent == "GoalAchievedAgent":
            logging.info("goal achieved!")
            return best_next_step_json["thoughts"]["speak"] # TODO: Properly return answer when problem is solved

        # Call agent
        agent_resolution = call_agent_picked(current_agent)

        # Store the result in the prompt
        history.append(agent_resolution)

        # Are we solving the current or next task?
        task_progression_status = "No - will retry with same current & next task"
        if onto_next_task(best_next_step_json):
            task_progression_status = "Yes! current_task = next_task & assign next task!"
            task_step += 1
        logging.info("Did we just solve the current or next task? " + task_progression_status)
        attempts_count += 1

    return final_result

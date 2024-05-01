import logging
from router import pick_agent


def still_solving_tasks(current_agent, iter_count):
    agent_calling_unresolved = current_agent != "unresolvable_agent" and current_agent != "goal_achieved_agent"
    count_not_exceeded = iter_count < 5
    logging.info("still solving?: " + str(agent_calling_unresolved or count_not_exceeded))
    return agent_calling_unresolved and count_not_exceeded


def onto_next_task(best_next_step_json):
    return best_next_step_json["current_or_next_task"].__contains__("next")


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
        case "unresolvable_agent":
            logging.info("unresolvable_agent called :( throwing exception")
            raise Exception("router could not find an agent to call for the task")
        case "goal_achieved_agent":
            logging.info("goal achieved!")
            answer = "goal achieved"

    return answer


def solve_all_tasks(tasks_json):

    current_agent = "initial_agent"
    history = [""]
    attempts_count = 0
    task_step = 0
    task_total_count = len(tasks_json["tasks"])
    logging.info("Task total count: " + str(task_total_count))

    # Check where we should keep iterating to call more agents
    while still_solving_tasks(current_agent, attempts_count):
        logging.info("attempts_count: " + str(attempts_count))

        # Assign tasks
        logging.info("Assign tasks")
        current_task = str(tasks_json["tasks"][task_step])

        # Don't assign a next task if only 1 has been generated
        if (task_step >= task_total_count):
            next_task = "There is no next task - the Current Task is the final task"
        else:
            next_task = str(tasks_json["tasks"][task_step+1])

        # Decide next best step
        logging.info("Decide next best step")
        best_next_step_json = pick_agent(current_task, next_task, history)
        current_agent = best_next_step_json["agent"]

        # Call agent
        logging.info("Call agent")
        agent_resolution = call_agent_picked(current_agent)

        # Store the result in the prompt
        logging.info("Store the result in the prompt")
        history.append(agent_resolution)

        # Are we solving the current or next task?
        logging.info("Are we solving the current or next task?")
        if onto_next_task(best_next_step_json):
            logging.info("Onto the next task!")
            task_step += 1

        attempts_count += 1


    logging.info("agent picked: " + best_next_step_json["agent"])

    return best_next_step_json["thoughts"]["speak"]

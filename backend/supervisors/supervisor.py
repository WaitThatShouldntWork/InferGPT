import logging
from router import pick_agent

def solve_all_tasks(tasks_json):

    first_task = tasks_json["tasks"][0]
    logging.info("solving first task: " + str(first_task))

    agent_for_first_task = pick_agent(str(first_task))
    logging.info("agent picked: " + agent_for_first_task)

    stub_final_answer = "Something went wrong. The agent picked was " + agent_for_first_task + " which does not exist"

    # TODO: adjust to call an agent's pick_method method
    if (agent_for_first_task == "database_agent"):
        # will call agent here
        stub_final_answer = "I have used database_agent to retrieve personal information about you"
    if (agent_for_first_task == "fiancial_advisor_agent"):
        # will call agent here
        stub_final_answer = "I have called the fiancial_advisor_agent to aid in the first task"
    if (agent_for_first_task == "web_search_agent"):
        # will call agent here
        stub_final_answer = "I have searched the web with web_search_agent to find data for the first task"
    if (agent_for_first_task == "unresolvable_agent"):
        # will call agent here
        stub_final_answer = "I was unable to find an agent to solve the specific task."

    return stub_final_answer

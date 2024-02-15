import streamlit as st
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolExecutor, ToolInvocation
from llm import llm
from langchain.tools.render import format_tool_to_openai_function
from typing import TypedDict, Annotated, Sequence
import operator
import json
from langchain_core.messages import FunctionMessage, HumanMessage, BaseMessage
from langgraph.graph import StateGraph, END

st.set_page_config(page_title="InferGPT - multiagent", page_icon=":globe_with_meridians:", layout="wide")

    
st.title("InferGPT 🧠 - multiagent")
    
input_text = st.text_area("Input Text", "Hello, how are you?")
    
if st.button("Run Agent"):

    tools = [TavilySearchResults(max_results=1)]

    tool_executor = ToolExecutor(tools)

    llm = llm


    functions = [format_tool_to_openai_function(t) for t in tools]
    model = llm.bind_functions(functions)

    class AgentState(TypedDict):
        messages: Annotated[Sequence[BaseMessage], operator.add]
        
        # Define the function that determines whether to continue or not
    def should_continue(state):
        messages = state['messages']
        last_message = messages[-1]
        # If there is no function call, then we finish
        if "function_call" not in last_message.additional_kwargs:
            return "end"
        # Otherwise if there is, we continue
        else:
            return "continue"

    # Define the function that calls the model
    def call_model(state):
        messages = state['messages']
        response = model.invoke(messages)
        # We return a list, because this will get added to the existing list
        return {"messages": [response]}

    # Define the function to execute tools
    def call_tool(state):
        messages = state['messages']
        # Based on the continue condition
        # we know the last message involves a function call
        last_message = messages[-1]
        # We construct an ToolInvocation from the function_call
        action = ToolInvocation(
            tool=last_message.additional_kwargs["function_call"]["name"],
            tool_input=json.loads(last_message.additional_kwargs["function_call"]["arguments"]),
        )
        # We call the tool_executor and get back a response
        response = tool_executor.invoke(action)
        # We use the response to create a FunctionMessage
        function_message = FunctionMessage(content=str(response), name=action.tool)
        # We return a list, because this will get added to the existing list
        return {"messages": [function_message]}



    # Define a new graph
    workflow = StateGraph(AgentState)

    # Define the two nodes we will cycle between
    workflow.add_node("agent", call_model)
    workflow.add_node("action", call_tool)

    # Set the entrypoint as `agent`
    # This means that this node is the first one called
    workflow.set_entry_point("agent")

    # We now add a conditional edge
    workflow.add_conditional_edges(
        # First, we define the start node. We use `agent`.
        # This means these are the edges taken after the `agent` node is called.
        "agent",
        # Next, we pass in the function that will determine which node is called next.
        should_continue,
        # Finally we pass in a mapping.
        # The keys are strings, and the values are other nodes.
        # END is a special node marking that the graph should finish.
        # What will happen is we will call `should_continue`, and then the output of that
        # will be matched against the keys in this mapping.
        # Based on which one it matches, that node will then be called.
        {
            # If `tools`, then we call the tool node.
            "continue": "action",
            # Otherwise we finish.
            "end": END
        }
    )

    # We now add a normal edge from `tools` to `agent`.
    # This means that after `tools` is called, `agent` node is called next.
    workflow.add_edge('action', 'agent')

    # Finally, we compile it!
    # This compiles it into a LangChain Runnable,
    # meaning you can use it as you would any other runnable
    app = workflow.compile()

    inputs = {"messages": [HumanMessage(content=input_text)]}
    app.invoke(inputs)

    result = []
    
    for s in app.stream(inputs):
        result.append(list(s.values())[0])

    st.write(result)
     
     
    for output in app.stream(inputs):
        # stream() yields dictionaries with output keyed by node name
        for key, value in output.items():
            st.write(f"Output from node '{key}':")
            st.write("---")
            st.write(value)
    st.write("\n---\n") 
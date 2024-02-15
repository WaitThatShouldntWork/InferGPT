from langchain import hub
from langchain.agents import tool, create_json_agent
import os
from typing import TypedDict, Annotated, Union
from langchain_core.agents import AgentAction, AgentFinish
import operator
from langchain_core.agents import AgentFinish
from langgraph.prebuilt import ToolExecutor
from langchain_core.agents import AgentFinish
from langchain_core.agents import AgentActionMessageLog
from langgraph.graph import END, StateGraph
import streamlit as st
from llm import llm
from langchain_core.messages import BaseMessage

st.set_page_config(page_title="LangChain", page_icon=":globe_with_meridians:", layout="wide")

def main():
    
    st.title("LangChain")
    
    input_text = st.text_area("Input Text", "Hello, how are you?")
    
    if st.button("Run Agent"):
        
        os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
        
        search = GoogleSerperAPIWrapper()
        
        def toggle_case(word):
            toggle_case = " "
            for char in word:
                if char.islower():
                    toggle_case += char.upper()
                elif char.isupper():
                    toggle_case += char.lower()
                else:
                    toggle_case += char
            return toggle_case
        def sort_string(string):
            return ''.join(sorted(string))
        
        tools = [
            Tool(
                name= "search",
                func=search.run,
                description= "useful for when you needto answer questions about current events",
            )
            Tool(
                name = "Toggle_Case",
                func = lambda word: toggle_case(word),
                description = "Use when you want to convert the letter to uppercase or lowercase",
            )
            Tool(
                name= "Sort_String",
                func= lambda string: sort_string(string),
                description= "Use when you want to sort the string alphabetically",
            )
        ]
        
        prompt = hub.pull("hwchase17/react")
        
        llm = llm

        class AgentState(TypedDict):
            input: str
            chat_history : list[BaseMessage]
            agent_outcome : Union[AgentFinish, AgentFinish, None]
            return_direct : bool
            intermediate_steps: Annotated[list[tuple[AgentAction, str]], operator.add]

        tool_extractor = ToolExecutor(tools)

        def run_agent(state):
            agent_outcome = agent_runnable.invoke(state)
            return {"agent_outcome": agent_outcome}
            
            def execute_tools(state):
                messages = [state['agent_outcome']]
                last_message = messages[-1]
                
                tool_name = last_message.tool
                arguments = last_message
                
                tool_name = last_message.tool
                argument = last_message
                
                if tool_name == "Search" or tool_name == "sort" or tool_name =="Toggle_Case":
                    if "return_direct" in arguments:
                        del arguments["return_direct"]
                    action = ToolInvocation(
                        tool_name, 
                        tool_input= last_message.tool_input,
                        )
                response = tool_extractor.invoke(action)
                return {"intermediate_steps":[(state['agent_outcome'], response)]}
                
            def should_continue(state):
                message = [state['agent_outcome']]
                last_message = message[-1]
                if "Action" not in last_message.log:
                    return "end"
                else:
                    arguments = state["return_direct"]
                    if arguments is True:
                        return "final"
                    else:
                        return "continue"
        def first_agent(inputs):
            action = AgentActionMessageLog(
                tool="search",
                tool_input=inputs["input"],
                log= "",
                message_log= [],
            )
            return {"agent_outcome": action}
        
        workflow = StateGraph(AgentAction)
        
        workflow.add_node("agent", run_agent)
        workflow.add_node("action",execute_tools)
        workflow.add_node("final", execute_tools)            
        workflow.set_entry_point("agent")        
        workflow.add_conditional_edges(
            "agent",
            should_continue,
            {
                "continue": "action",
                "final": "final",
                "end": END,
            }
        )
        
        workflow.add_edge("action", "agent")
        workflow.add_edge("final", END)
        
        app = workflow.compile    
        
        inputs = {"input": input_text , "chat_history": [], "return_direct": False,}   
        result = []
        
        for s in app.stream(inputs):
            result = list(s.value())[0]
            results.append(result)
            st.write(result)
from dotenv import load_dotenv

load_dotenv()

from langchain_core.agents import AgentFinish, AgentAction
from langgraph.graph import END, StateGraph

from nodes import reason_node, act_node
from react_state import AgentState

REASON_NODE = "reason_node"
ACT_NODE = "act_node"

def should_continue(state: AgentState) -> str:
    if isinstance(state["agent_outcome"], AgentFinish):
        return END
    else:
        return ACT_NODE


graph = StateGraph(AgentState)

graph.add_node(REASON_NODE, reason_node)
graph.set_entry_point(REASON_NODE)
graph.add_node(ACT_NODE, act_node)


graph.add_conditional_edges(
    REASON_NODE,
    should_continue,
)

graph.add_edge(ACT_NODE, REASON_NODE)

app = graph.compile()

result = app.invoke(
    {
        "input": "How many Starlink satellites has SpaceX launched so far and when is the next Starlink launch scheduled & how many days until then?",
        "agent_outcome": None, 
        "intermediate_steps": []
    }
)

print(result["agent_outcome"].return_values["output"], "final result")

'''
mermaid_code = app.get_graph().draw_mermaid()
# print(mermaid_code)
# app.get_graph().print_ascii()

with open("react_graph.mmd", "w") as f:
    f.write(mermaid_code)
# Open graph in Mermaid Live Editor https://mermaid.live/edit
# to preview and export as PNG/SVG.
'''
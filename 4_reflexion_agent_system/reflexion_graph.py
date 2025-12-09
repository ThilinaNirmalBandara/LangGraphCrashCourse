from typing import List

from langchain_core.messages import BaseMessage, ToolMessage
from langgraph.graph import END, MessageGraph

from chains import reviser_chain, first_responder_chain
from execute_tools import execute_tools

graph = MessageGraph()
MAX_ITERATIONS = 2

graph.add_node("first_responder", first_responder_chain)
graph.add_node("execute_tools", execute_tools)
graph.add_node("reviser", reviser_chain)

graph.add_edge("first_responder", "execute_tools")
graph.add_edge("execute_tools", "reviser")

def event_loop(state:List[BaseMessage]) -> str:
    count_tool_visits = sum(isinstance(item,ToolMessage) for item in state)
    num_iterations=count_tool_visits
    if num_iterations > MAX_ITERATIONS:
        return END
    return "execute_tools"

graph.add_conditional_edges("reviser",event_loop)
graph.set_entry_point("first_responder")

app = graph.compile()

mermaid_code = app.get_graph().draw_mermaid()
print(mermaid_code)
app.get_graph().print_ascii()

response = app.invoke("Write about how AI helps tech startups")

print(response[-1].tool_calls[0]["args"]["answer"])
'''
with open("graph.mmd", "w") as f:
    f.write(mermaid_code)
# Open graph in Mermaid Live Editor https://mermaid.live/edit
# to preview and export as PNG/SVG.
'''
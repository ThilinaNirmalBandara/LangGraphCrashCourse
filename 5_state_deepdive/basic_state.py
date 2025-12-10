from typing import TypedDict
from langgraph.graph import END, StateGraph


class SimpleState(TypedDict):
    count :  int

def increment(state: SimpleState) -> SimpleState:
    return {
        "count": state["count"] + 1
    }

def should_continue(state):
    if state["count"] < 5:
        return "continue"
    else:
        return "stop"

graph = StateGraph(SimpleState)

graph.add_node("increment", increment)
graph.add_conditional_edges(
    "increment",
    should_continue,
    {
        "continue":"increment",
        "stop":END
    }
)

graph.set_entry_point("increment")

app = graph.compile()

state ={
    "count": 0
}
response = app.invoke(state)
print(response)


'''
mermaid_code = app.get_graph().draw_mermaid()
# print(mermaid_code)
# app.get_graph().print_ascii()

with open("basic_graph.mmd", "w") as f:
    f.write(mermaid_code)
# Open graph in Mermaid Live Editor https://mermaid.live/edit
# to preview and export as PNG/SVG.
'''
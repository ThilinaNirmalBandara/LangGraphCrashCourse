from typing import TypedDict, List
from langgraph.graph import END, StateGraph


class SimpleState(TypedDict):
    count :  int
    sum : int
    history : list[int]

def increment(state: SimpleState) -> SimpleState:
    new_count = state["count"] + 1
    return {
        "count": new_count,
        "sum": state["sum"] + new_count,
        "history": state["history"]+[new_count]

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
    "count": 0,
    "sum": 0,
    "history": []
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
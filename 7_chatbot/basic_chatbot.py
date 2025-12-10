from typing import TypedDict, Annotated
from langgraph.graph import add_messages, StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model="llama-3.1-8b-instant")

class BasicChatState(TypedDict):
    messages: Annotated[list, add_messages ]

def chatbot(state: BasicChatState):
    return {
        "messages": [llm.invoke(state["messages"])]
    }

graph = StateGraph(BasicChatState)

graph.add_node("chatbot",chatbot)
graph.set_entry_point("chatbot")
graph.add_edge("chatbot",END)

app = graph.compile()

'''
mermaid_code = app.get_graph().draw_mermaid()
# print(mermaid_code)
# app.get_graph().print_ascii()

with open("basic_chatbot_graph.mmd", "w") as f:
    f.write(mermaid_code)
# Open graph in Mermaid Live Editor https://mermaid.live/edit
# to preview and export as PNG/SVG.
'''

while True:
    user_input = input("User: ")
    if user_input in ["exit","end","quit"]:
        break
    else:
        result = app.invoke({
            "messages": [HumanMessage(content=user_input)]
        })
        print(result["messages"][-1].content)
        #print(result)
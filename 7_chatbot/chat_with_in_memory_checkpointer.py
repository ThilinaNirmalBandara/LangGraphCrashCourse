from typing import TypedDict, Annotated
from langgraph.graph import add_messages, StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, HumanMessage
from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.runnables import RunnableConfig

load_dotenv()

memory_saver = MemorySaver()

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

app = graph.compile(checkpointer=memory_saver)

config: RunnableConfig = {
    "configurable": {
        "thread_id": "my-thread-1"
    }
}

'''
response1 = app.invoke({
    "messages": HumanMessage(content="Hello this is Thilina!")
},config=config)

response2 = app.invoke({
    "messages": HumanMessage(content="What's my name?")
},config=config)

print(response1)
print("\n")
print(response2)
'''
while True:
    user_input = input("User: ")
    if user_input in ["exit", "end", "quit"]:
        break
    else:
        result = app.invoke({
            "messages": [HumanMessage(content=user_input)]
        },config=config)

        #print(result)
        print("AI: " + result["messages"][-1].content)
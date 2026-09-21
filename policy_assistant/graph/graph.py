""" Assemble and compile the graph """

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import START, END, StateGraph

from policy_assistant.graph.nodes.condense import condense
from policy_assistant.graph.nodes.generate import generate
from policy_assistant.graph.nodes.intake import intake
from policy_assistant.graph.nodes.reframe import reframe
from policy_assistant.graph.nodes.refuse import refuse
from policy_assistant.graph.nodes.retrieve import retrieve
from policy_assistant.graph.state import AgentState
from policy_assistant.rules.routing import route_after_intake, route_after_retrieve


def build_graph(checkpointer=None):

    g = StateGraph(AgentState)

    g.add_node("intake", intake)
    g.add_node("condense", condense)
    g.add_node("retrieve", retrieve)
    g.add_node("reframe", reframe)
    g.add_node("generate", generate)
    g.add_node("refuse", refuse)

    g.add_edge(START, "intake")
    
    g.add_conditional_edges(
        "intake", 
        route_after_intake, 
        {"condense": "condense", "retrieve": "retrieve"}
    )
    
    g.add_edge("condense", "retrieve")
    
    g.add_conditional_edges(
        "retrieve",
        route_after_retrieve,
        {"generate": "generate", "reframe": "reframe", "refuse": "refuse"},
    )
    
    g.add_edge("reframe", "retrieve")
    
    g.add_edge("generate", END)
    g.add_edge("refuse", END)

    return g.compile(checkpointer=checkpointer)


def build_graph_with_memory():
    return build_graph(checkpointer=InMemorySaver())


if __name__ == "__main__":
    print(build_graph().get_graph().draw_mermaid())

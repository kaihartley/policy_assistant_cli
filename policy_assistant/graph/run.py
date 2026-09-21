""" Chat with the assistant in the terminal """

import uuid

from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig

from policy_assistant.graph.graph import build_graph_with_memory
from policy_assistant.models.index import get_local_store


def print_steps(app, graph_state: dict, config: RunnableConfig) -> None:
    for chunk in app.stream(graph_state, config, stream_mode="updates"):
        for node, update in chunk.items():
            fields = {k: v for k, v in update.items() if k in ("query", "attempts", "best_score")}
            if update.get("retrieved"):
                fields["found"] = [d.metadata["section"] for d in update["retrieved"] if "section" in d.metadata]
            print(f"  [{node}] {fields}" if fields else f"  [{node}]")


if __name__ == "__main__":

    print(f"Indexed {len(get_local_store().store)} chunks. Ask a policy question (Ctrl+C to quit).")

    app = build_graph_with_memory()

    config: RunnableConfig = {
        "configurable": {"thread_id": str(uuid.uuid4())},
        "recursion_limit": 25,
    }

    while True:
        try:
            question = input("\nyou > ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not question:
            continue

        print_steps(app, {"messages": [HumanMessage(content=question)]}, config)

        final_state = app.get_state(config).values
        print(f"\nassistant > {final_state['messages'][-1].content}")

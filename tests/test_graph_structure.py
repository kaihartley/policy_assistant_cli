from policy_assistant.graph.graph import build_graph


def _graph():
    return build_graph().get_graph()


def test_graph_has_expected_nodes():
    nodes = set(_graph().nodes)
    assert {"intake", "condense", "retrieve", "reframe", "generate", "refuse"} <= nodes


def test_graph_has_expected_edges():
    edges = {(e.source, e.target) for e in _graph().edges}
    assert edges >= {
        ("__start__", "intake"),
        ("intake", "condense"),
        ("intake", "retrieve"),
        ("condense", "retrieve"),
        ("retrieve", "generate"),
        ("retrieve", "reframe"),
        ("retrieve", "refuse"),
        ("reframe", "retrieve"),
        ("generate", "__end__"),
        ("refuse", "__end__"),
    }

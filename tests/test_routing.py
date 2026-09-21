from langchain_core.messages import AIMessage, HumanMessage

from policy_assistant.config import DEFAULT_RETRIEVER_THRESHOLD, MAX_ATTEMPTS
from policy_assistant.rules.routing import route_after_intake, route_after_retrieve


def make_state(**overrides) -> dict:
    state = {
        "messages": [HumanMessage(content="hi")],
        "question": "q",
        "query": "q",
        "queries": [],
        "retrieved": [],
        "attempts": 1,
        "best_score": 0.0,
    }
    return {**state, **overrides}


# --- the routing decision ---

def test_first_question_goes_straight_to_retrieve():
    assert route_after_intake(make_state()) == "retrieve"


def test_follow_up_is_condensed_first():
    messages = [HumanMessage(content="a"), AIMessage(content="b"), HumanMessage(content="c")]
    assert route_after_intake(make_state(messages=messages)) == "condense"


def test_good_score_goes_to_generate():
    assert route_after_retrieve(make_state(best_score=DEFAULT_RETRIEVER_THRESHOLD)) == "generate"


def test_weak_score_with_attempts_left_retries():
    assert route_after_retrieve(make_state(best_score=0.0, attempts=1)) == "reframe"


# --- the retry bound ---

def test_weak_score_with_no_attempts_left_refuses():
    assert route_after_retrieve(make_state(best_score=0.0, attempts=MAX_ATTEMPTS)) == "refuse"

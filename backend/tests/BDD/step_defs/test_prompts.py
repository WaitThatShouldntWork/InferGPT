from pytest_bdd import given, when, then, parsers, scenarios
from tests.BDD.test_utilities import (
    send_prompt, 
    app_healthcheck,
    check_response_confidence, 
    correctness_evaluator,
    healthy_response,
)

scenarios("../features/Correctness/Accuracy_Factual_Correctness.feature")

@given(parsers.parse("a prompt to InferGPT"))
def prepare_prompt():
    healthcheck_response = app_healthcheck()
    assert healthcheck_response.status_code == 200
    assert healthcheck_response.json() == healthy_response
    
@when(parsers.parse("I get the response"))
def get_response():
    pass

@then(parsers.parse("the response to this '{prompt}' should match the '{expected_response}'"))
def check_response_includes_expected_response(prompt, expected_response):
    response = send_prompt(prompt)
    result = correctness_evaluator.evaluate_strings(
        input=prompt,
        prediction=response.json(),
        reference=expected_response,
    )
    assert result["score"] == 1, "The bot response is not correct. \nReasoning: " + result["reasoning"]

@then(parsers.parse("the response to this '{prompt}' should give a confident answer"))
def check_bot_response_confidence(prompt):
    response = send_prompt(prompt)
    result = check_response_confidence(prompt, response.json())
    assert result["score"] == 1, "The bot response is not confident enough. \nReasoning: " + result["reasoning"]    
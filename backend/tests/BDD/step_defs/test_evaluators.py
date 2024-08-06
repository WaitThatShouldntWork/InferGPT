from pytest_bdd import given, when, then, parsers, scenarios
from tests.BDD.test_utilities import (
    send_prompt, 
    app_healthcheck, 
    correctness_evaluator,
    healthy_response,
)
class Evaluators():

    scenarios("../features/Correctness/Accuracy_Factual_Correctness.feature")

@given(parsers.parse("a prompt to InferGPT"))
def prepare_prompt():
    healthcheck_response = app_healthcheck()
    assert healthcheck_response.status_code == 200
    assert healthcheck_response.json() == healthy_response
    

@when(parsers.parse("I get the response"))
def get_response():
    pass

@then(parsers.parse("the response to this '{prompt}' should match the {expected_amount}"))
def check_response_includes_expected_amount(prompt, expected_amount):
    response = send_prompt(prompt)
    result = correctness_evaluator.evaluate_strings(
        #input=,
        prediction=response.json(),
        reference=expected_amount,
    )
    assert result["score"] == 1, "The bot response is not correct. \nReasoning: " + result["reasoning"]

@then(parsers.parse("the response to this '{prompt}' should match the '{expected_response}'"))
def check_response_includes_critical_info(prompt, expected_amount):
    response = send_prompt(prompt)
    result = correctness_evaluator.evaluate_strings(
        input=prompt,
        prediction=response.json(),
        reference=expected_amount,
    )
    assert result["score"] == 1, "The bot response is not correct. \nReasoning: " + result["reasoning"]
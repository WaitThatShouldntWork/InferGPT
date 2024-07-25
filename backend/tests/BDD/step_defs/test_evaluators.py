from pytest_bdd import scenario, given, when, then, parsers, scenarios
from tests.BDD.test_utilities import (
    send_prompt, 
    app_healthcheck, 
    correctness_evaluator, 
    healthy_response
)

scenarios("../features/Correctness/Accuracy_Factual_Correctness.feature")

@given(parsers.parse("a user asks InferGPT about his financial information"))
def prepare_prompt():
    response = app_healthcheck()
    assert response.status_code == 200
    assert response.json() == healthy_response

@when(parsers.parse("I get the response"))
def get_response():
    pass

@then(parsers.parse("the response to this '{prompt}' should match the {expected_amount}"))
def check_response_includes_expected_amount(prompt, expected_amount):
    response = send_prompt(prompt)
    result = correctness_evaluator.evaluate_strings(
        input=prompt,
        prediction= response.json(),
        reference= expected_amount,
    )
    assert result["score"] == 1, "The bot response is not correct. \nReasoning: " + result["reasoning"]
    print("Result: ", result)

@then(parsers.parse("the response to this '{prompt}'"))
def check_response_includes_critical_info(prompt, expected_amount):
    response = send_prompt(prompt)
    result = correctness_evaluator.evaluate_strings(
        input=prompt,
        prediction= response.json(),
        reference= expected_amount,
    )
    assert result["score"] == 1, "The bot response is not correct. \nReasoning: " + result["reasoning"]
    print("Result: ", result)
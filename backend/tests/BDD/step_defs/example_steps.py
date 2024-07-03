import json
from pytest_bdd import scenario, given, when, then, parsers, scenarios
from pytest_bdd.parsers import parse
from pytest_bdd.parsers import cfparse as Parser
from tests.BDD.test_utilities import send_prompt

scenarios("../features/example.feature")

@given(parsers.parse("a {prompt} to InferGPT"))
def prepare_prompt(prompt):  
    response = send_prompt(prompt)
    assert response.status_code == 200
    print("Hello World: ", response.json())
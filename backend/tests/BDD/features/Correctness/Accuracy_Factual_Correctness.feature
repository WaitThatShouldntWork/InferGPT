Scenario Outline: When a user asks InferGPT for information on their financial situation
    Given  a prompt to InferGPT
    When   I get the response
    Then   the response to this '<prompt>' should match the '<expected_amount>'
Examples:
|prompt                                             |prompt_question |expected_amount |
|How much did I spend at Tesco?                     |Tesco amount?   |639.84          |   
|How much did I spend on Amazon?                    |1586.56         |
|How much did I spend on Tesco compared to Amazon?  |946.72          |


Scenario Outline: When a user asks InferGPT generic questions
    Given  a prompt to InferGPT
    When   I get the response
    Then   the response to this '<prompt>' should match the '<expected_response>'
Examples:
|prompt                                             |expected_response |
|What is the capital of France?                     |Paris           |
Scenario Outline: My Scenario
    Given  a transactional prompt to InferGPT
    When   I get the response
    Then   the response to this '<prompt>' should match the '<expected_amount>'
Examples:
|prompt                                         |expected_amount |
|How much did I spend at Tesco                  |639.84          |   
|How much did I spend on Amazon                 |1586.56         |
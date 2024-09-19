Scenario Outline: When a user asks InferGPT for information about their transaction history
    Given  a prompt to InferGPT
    When   I get the response
    Then   the response to this '<prompt>' should match the '<expected_response>'
Examples:
|prompt                                                                         |expected_response      |
|How much did I spend at Tesco?                                                 |639.84                 |            
|How much did I spend on Amazon?                                                |1586.56                |
|How much did I spend on Tesco compared to Amazon?                              |946.72                 |
|How much did I spend on eating out this month?                                 ||
|How much did i spend on takeaways this month?                                  ||
|How much did i spend on eating out in the previous month?                      ||
|what was my average monthly income in the last 6 months?                       ||
|What was my total income in the last 6 months?                                 ||
|How much did i spend on entertainment on average in the last year?             ||
|How much money did i save last year?                                           ||
|What is the category where I spend the least amount in 2022?                   ||
|How long would it take for me to have £25,000 in my savings account?           ||
|Can i afford to spend £3000 on vacation next month?                            ||
|How much did i pay by direct debit last month?                                 ||
|How much did i pay by standing orders for the previous year?                   ||
|What were my average monthly expenses in the last year?                        ||
|What was my average most frequently used merchant this year?                   ||
|Who did I spend the most money with?                                           ||
|How much have I spent on mortage payments this year?                           ||
|What was the latest transaction I made to Sainsburys?                          ||
|When is my mortgage bill due?                                                  ||
|Calculate the total amount Jane Smith spent in each transaction category.      |                       |            
|What transactions were made today?                                             |                       |
|Find all persons who made transactions with Aldi?"                             |                       |
|Any tips to increase my savings rate?                                          |                       |
|What type of investments can I make?                                           |                       |
|Got any low income budget tips?                                                |                       |
|Should i invest in a stocks and shares ISA or stick with my savings account?   |                       |
|How much should i have in an emergency fund?                                   |                       |
|Can you remind me when my bills are due?                                       |                       |
|Can you help me compare prices for a purchase im about to make?                |                       |
|Can you alert me when the price drops for items on my wish list?               |                       |
|Can you compare different mortgage/refinancing rates available from various banks?                     |                       |
|Can you create a forecast of an interest only mortgage vs a repayments? but the money saved from the repayments is invested in a stocks and shares isa instead? |                       |

Scenario Outline: When a user asks InferGPT generic questions
    Given  a prompt to InferGPT
    When   I get the response
    Then   the response to this '<prompt>' should match the '<expected_response>'
Examples:
|prompt                                             |expected_response  |
|What is the capital of France?                     |Paris              |

@confidence
Scenario Outline: Check Response's confidence
    Given  a prompt to InferGPT
    When   I get the response
    Then   the response to this '<prompt>' should give a confident answer
Examples:
|prompt                                                                     |
|What is the capital of France?                                             |
|How much did I spend at Tesco?                                             |
                  
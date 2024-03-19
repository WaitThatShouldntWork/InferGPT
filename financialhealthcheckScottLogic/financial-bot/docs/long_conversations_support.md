# Problem
The OpenAI limit of 4k tokens per request can negatively impact the quality of the dialog between users and chatbots. When the limit is reached, the chatbot can forget the context at the beginning of the conversation, which makes it difficult to change or update information at the start of the interation. To address this, several options have been considered, including Langchain and the GPT index. 

# Langchain and GPT index
Langchain has the ability to reference specific question blocks based on a user's reply, but it has poor "score" performance and may not be reliable enough for use. On a quick test(see long_conversation_testcase.py), Langchain achieved an accuracy of 57% with "score"/relevancy data and around 80% without the score data.

The GPT index, on the other hand, yields consistent results but has a lower accuracy rate of 39%. In the future case of GPT-4, it might be enough to use the system as is with expected 32k token limit (according to recently leaked information based on Open AI Foundry product information).

# Conclusion
Overall, while Langchain has shown potential for addressing the 4k token limit enforced by OpenAI, further research and testing are required to identify the most effective solution for each use case(including testing haystack as one of the options), particularly in the context of GPT-4's expected 32k token limit.
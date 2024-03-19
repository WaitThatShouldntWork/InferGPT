# NLP platforms
## Platforms Comparison


| Feature | Amazon Comprehend | Azure Cognitive Services | IBM Watson | OpenAI GPT-3 | AWS Lex |
|---------|-------------------|--------------------------|------------|--------------|-------|
| Ease of use | Moderate (requires some knowledge of AWS) | Moderate (requires some knowledge of Azure) | Moderate (requires some knowledge of IBM) | Easy (very user-friendly API) | Difficult, (requires knowledge of AWS)
| Intent classification | [Yes, moderate ease of training](https://docs.aws.amazon.com/comprehend/latest/dg/how-document-classification.html) | [Yes](https://learn.microsoft.com/en-us/azure/cognitive-services/language-service/conversational-language-understanding/quickstart?pivots=language-studio#train-your-model) | [Possibly, moderate ease of training](https://cloud.ibm.com/docs/natural-language-understanding?topic=natural-language-understanding-classifications) | [Possible](https://www.pragnakalp.com/intent-classification-paraphrasing-examples-using-gpt-3/) | [Yes](https://docs.aws.amazon.com/lexv2/latest/dg/build-intents.html)  |
| Custom Models | Yes | No | Yes | No, but can be [fine tuned](https://beta.openai.com/docs/guides/fine-tuning) | Yes |
| Profanity filter | Using [Amazon Translate](https://docs.aws.amazon.com/translate/latest/dg/customizing-translations-profanity.html)| Using [Content Moderator](https://azure.microsoft.com/en-gb/products/cognitive-services/content-moderator/)| Limited (via [emotion classification](https://www.ibm.com/demos/live/natural-language-understanding/self-service/home))| Content filter, see [here](https://beta.openai.com/docs/api-reference/moderations/create) or [here](https://beta.openai.com/docs/models/content-filter)| Using [Amazon Translate](https://docs.aws.amazon.com/translate/latest/dg/customizing-translations-profanity.html)|
| Language Support | [Multiple](https://docs.aws.amazon.com/comprehend/latest/dg/supported-languages.html) | [Multiple](https://learn.microsoft.com/en-us/azure/cognitive-services/language-service/conversational-language-understanding/language-support) | [Multiple](https://cloud.ibm.com/docs/natural-language-understanding?topic=natural-language-understanding-language-support) | Multiple | [Multiple](https://docs.aws.amazon.com/lexv2/latest/dg/how-languages.html) |
| Pricing | Pay-as-you-go [starting at $0.2 for 1k requests](https://aws.amazon.com/comprehend/pricing/)  | Pay-as-you-go [starting at $5 for 1k requests](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/language-service/) | Pay-as-you-go starting at [$3 for 1k requests](https://www.ibm.com/uk-en/cloud/watson-natural-language-understanding/pricing#:~:text=Tier%201:%20USD%200.003/%20NLU,item%20for%20next%205,000,001+%20items) | Pay-as-you-go [at $0.0200 / 1k tokens](https://openai.com/api/pricing/) | Pay-as-you-go [starting at $0.75 for 1k requests](https://aws.amazon.com/lex/pricing/)|
| Integration with other services | Yes (integrates with other AWS services) | Yes (integrates with other Azure services) | Yes (integrates with other IBM services) | No |  Yes (integrates with other AWS services)  |
 Additional features| [Custom Classification](https://docs.aws.amazon.com/comprehend/latest/dg/how-document-classification.html), [Custom Entities](https://docs.aws.amazon.com/comprehend/latest/dg/custom-entity-recognition.html), [PII identification](https://aws.amazon.com/comprehend/features/?refid=a7f57dee-fc58-4084-9037-cb552d58a5d5#PII_Identification_and_Redaction) | [PII identification](https://learn.microsoft.com/en-us/azure/cognitive-services/language-service/personally-identifiable-information/overview), [Entity Linking](https://learn.microsoft.com/en-us/azure/cognitive-services/language-service/entity-linking/overview), [Custom Entity Recognition](https://learn.microsoft.com/en-us/azure/cognitive-services/language-service/conversational-language-understanding/quickstart?pivots=rest-api)| Recognition of [Emotions](https://cloud.ibm.com/apidocs/natural-language-understanding#emotion), [Relations](https://cloud.ibm.com/apidocs/natural-language-understanding#relations); [Custom Entities](https://cloud.ibm.com/docs/natural-language-understanding?topic=natural-language-understanding-entities-and-relations) | [Fine tuning](https://beta.openai.com/docs/guides/fine-tuning), [Moderation](https://beta.openai.com/docs/guides/moderation/overview) |  [Multi turn dialog](https://aws.amazon.com/lex/features/), [Intent and slot lifecycle management](https://aws.amazon.com/lex/features/) |

## AWS Lex

AWS Lex is not just a tool for intent classification and entity extraction, it's rather an entire ecosystem for creating bots. There are many components that must be configured correctly before obtaining meaningful results. From a developer's perspective, this includes tasks such as:

 1. **Create a bot\*** 
 2. **Create intents.** **Add utterances to help system with intent identification.\***
 3. **Create slots with prompts (question the bot asks to populate slot values).\***
 4. Create AWS Lambda function to handle AWS Lex requests. This is acting like a hook which is triggered under different conditions (e.g. after each user input)
 5. **Add/Delegate fulfilment logic. This is done using AWS Lambda\*.**
**\* required steps**

AWS Lex allows for the management of various conversational states, such as ElicitIntent, ElicitSlot, ConfirmIntent, and Closed, through the use of AWS Lambda. In summary, AWS Lex offers the capabilities of intent classification and entity extraction, while also providing the option for developers to utilize the ecosystem's functionality, such as eliciting slots and confirming intents, to enhance the conversational experience.

## Azure CLU 

Azure Conversational Language Understanding is a very user friendly tool for basic intent classification and entity extraction. Providing utterances,  labelling the data, training and deploying the model is quite easy and can be done straight on the website (as opposed to AWS Comprehend, for which you are expected to provide a CSV file). 

## IBM Watson

IBM Watson offers powerful functionality for intent classification and entity extraction. To include custom entities, a [machine learning model](https://cloud.ibm.com/docs/natural-language-understanding?topic=natural-language-understanding-entities-and-relations) must be created and deployed within the [Natural Language Understanding](https://cloud.ibm.com/docs/watson-knowledge-studio?topic=watson-knowledge-studio-publish-ml#wks_manlu) service. A notable feature of Watson is its emotion detection capability, which can be used to filter or moderate messages based on emotions such as anger and disgust. Additionally, it's worth exploring [the sample applications](https://cloud.ibm.com/docs/natural-language-understanding?topic=natural-language-understanding-sample-apps) provided by IBM to gain a deeper understanding of Watson's capabilities

## OpenAI GPT-3

While the setup of GPT-3 for intent classification may initially prove challenging, it ultimately serves as a valuable option for advanced entity extraction. A simple example of entity extraction could include:

> output to json the information below, use the following keys "annual_income", "monthly expenses", "monthly_debts", "monthly_pension", "savings". Keep percentage values. Output only json and no other text. The information is: Based on the information provided, your annual income is £12,000, you have £1,500 in savings, your monthly expenses are £1,000, your monthly debts are £300, and you contribute 4% of your salary to your pension each month. Is this correct?

> `{
 "annual_income": 12000,
 "monthly_expenses": 1000,
 "monthly_debts": 300,
 "monthly_pension_percentage": 0.04,
 "savings":1500
}
`

Another example could include evaluation of the final number:
> Extract final number, give only one total number as output: I have 1000 in bitcoin and 2500 on bank account and 500 is due to be paid

> `3000`

GPT-3 can also be used to handle chit-chat intent.

## Amazon Comprehend

AWS Comprehend is quite comparable to Azure CLU, as it offers the capabilities of both classification and entity extraction. To achieve custom entity recognition, a new model trained with specific data is required. While classification is generally more suitable for analysing documents, it can also be utilized for intent classification.


### Azure CLU (Intent Classification and Entity Extraction)

**Initialise environment:**

1.  Create language service at [azure portal](https://portal.azure.com/#create/Microsoft.CognitiveServicesTextAnalytics) while selecting custom feature ‘Custom text classification & Custom named entity recognition’. Fill all necessary fields as you see fit.
    
2.  Navigate to [the language studio](https://language.cognitive.azure.com/) and select the “Understand questions and conversational language” tab. Import project from [github sbot repo] (/samples/azure/2023v1Project(Chatbot).json)
    
3.  Once imported, you will be redirected to the “Schema Definition” page of the project.

**Deploy the model:**

1.  Select the “Training Jobs” option on the left sidebar and train a new model. Wait for the training to finish.
    
2.  Go to the “Deploying a model” option on the left sidebar and deploy the trained model.
    
3.  Go to the “Testing deployments” option on the left sidebar, select the deployment, set input to something like “hi i want to send 50 gbp to account 12345678 and code 33-32-12”. Click the “Run the test” button at the top.
    
4.  The model should return classified intent with extracted entity values.

References: [How to create a CLU project](https://learn.microsoft.com/en-us/azure/cognitive-services/language-service/conversational-language-understanding/how-to/create-project?tabs=language-studio%2CLanguage-Studio)
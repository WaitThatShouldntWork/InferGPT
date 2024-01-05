from data.payload import BaseMessage
from utilities.nlp_helper import NlpHelper
from utilities.defaults import GptModelNames
from abc import ABC, abstractmethod

class BasePrompt(ABC):
    def __init__(self):
        self.result = None

    @abstractmethod
    def prepare_prompt(self, texts, *args, **kwargs):
        pass

    def to_request(self):
        return self.result
    
class GPTChatPrompt(BasePrompt):
    # 'gpt-3.5-turbo'
    def __init__(self):
        self.result = []
        self.text = ""
        self.extra_params = []

    def prepare_prompt(self, texts, *args, **kwargs):        
        if GptModelNames.GPTChatModel not in texts:
            raise ValueError("Text for GPT Chat not provided")
        self.text, self.extra_params = texts[GptModelNames.GPTChatModel]
        self.result.append({"role" : "system", "content": self.text})
        for message in self.extra_params:
            self.result.append({"role" : NlpHelper.sender_to_role(sender = message['sender']), "content": message['message']})

class GPT3Prompt(BasePrompt):
    # 'text-davinci-003'
    def __init__(self):
        self.result = ""

    def prepare_prompt(self, texts, *args, **kwargs):
        if GptModelNames.GPT3Model not in texts:
            raise ValueError("Text for GPT-3 not provided")
        self.result = texts[GptModelNames.GPT3Model]
    

class PromptFactory:
    @staticmethod
    def create_prompt(model:str):
        if model == GptModelNames.GPTChatModel:
            return GPTChatPrompt()
        elif model == GptModelNames.GPT3Model:
            return GPT3Prompt()
        else:
            raise ValueError(f"Unsupported model: {model}")

class NlpPrompts:
    @staticmethod
    def generic(message_log:list[BaseMessage]):
        prompt = """You are based solely in the UK and work for a UK bank."
                            " Classify intents and extract entities from the dialog based on the keys below."
                            " Put answer or reply using \"reply\" json key. The only allowed"
                            " intent json values for \"intent_name\": \"general\", \"financial_check\","
                            " \"investment\". The only allowed entity values for \"entity_name\": "
                            " \"monthly savings\", \"rainy day fund\", \"savings balance\", "
                            "\"pension contributions\", \"mortgage amount\", \"debt\", \"investments balance\","
                            " \"investment account\", \"financial goal\", \"risk tolerance\", "
                            "\"help to buy ISA\", \"monthly rent\", \"mortgage amount\", \"savings location\", \"other savings\".  If there are entities, give explanations"
                            " for extracted entities as if you are talking to customer using using"
                            " key \"explanation\". Output only json result and nothing else. Json "
                            "result example {{\"intent_name\" : \"financial_check\", \"entities\": "

                            "[{{\"entity_name\" : \"monthly savings", \"entity_value\": 500, "
                            "\"explanation\": \"You mentioned your monthly expenses are £500\"}}]}}. "
                            "Json result example 2: {{\"intent_name\" : \"financial_check\", \"entities\": "
                            [{{\"entity_name\" : \"monthly rent\", \"entity_value\": 10000, "
                            "\"explanation\": \"You indicated you spend 10000 on rent each month\"}}]}}."
                            " The dialog: \"{0}\". Do not ask questions. Json:""".format( "\n".join(list(map(lambda m: m['sender'] + ": " + m['message'], message_log))))
        return {
                GptModelNames.GPT3Model : prompt,
                GptModelNames.GPTChatModel: (prompt, [])
            }
    
    @staticmethod
    def generic_v2(message_log:list[BaseMessage]):
        prompt = """You are a chat bot called "Bot3" who works for a UK bank and is based solely in the UK. You are given the following extracted parts of "the dialog" between "User" and "Bot3". Classify intents and extract entities from the "User" replies in the dialog based on the keys below. If the last "User" reply in the Dialog is a question, then provide a short reply using "reply" json key. If you don't know the answer "reply" should have empty value. Don't try to make up an answer. If the question is outside of financial area or existing context, "reply" should inform that you are tuned to only answer questions about financial area. The only allowed intent json values for "intent_name" are "general", "financial_check", "investment". The only allowed entity values for "entity_name" are "monthly savings", "rainy day fund", "savings balance", "pension contributions", "mortgage amount", "debt", "investments balance", "investment account", "financial goal", "risk tolerance", "help to buy ISA", "monthly rent", "mortgage amount", "savings location", "other savings". "reply" value must be empty unless latest "User" reply is a question. Do not ask questions or provide information unless explicitly asked. Only extract entities below "The dialog:" part. Output only valid json result and nothing else.
Example 1:
=====
User: Alex
Bot3: Hello Alex! How much are you saving per month?
User: 9000
Bot3: What is your financial goal?
User: early retirement
===== 
{"intent_name" : "financial_check", "entities": [{"entity_name" : "monthly savings", "entity_value": 9000}, {"entity_name" : "financial goal", "entity_value": "early retirement"}], "reply" : ""}                
=====
Example 2:
=====
User: ddd
Bot3: Hello ddd! How much are you saving per month?
User: in what currency
Bot3: Monthly savings can be in any currency, it would be useful to provide a total amount in GBP.
User: around 5000
Bot3: What is your financial goal?
User: get drunk
===== 
{"intent_name" : "financial_check", "entities": [{"entity_name" : "monthly savings", "entity_value": 5000}], "reply" : "Ha ha, very funny. Now would please answer the question."}                
=====
Example 3:
=====
User: Maria
Bot3: Hi Maria! How much do have you got for rainy day?
User: Nothing
Bot3: What are you pension contributions?
User: I don't contribute
Bot3: What are you debts?
User: What debts?
=====
{"intent_name" : "financial_check", "entities": [{"entity_name" : "rainy day fund", "entity_value": 0}, {"entity_name" : "pension contributions", "entity_value": 0}], "reply" : "Debts are amounts of money that are owed by one person or entity to another. In the UK, debts can be in the form of loans, credit cards, overdrafts, mortgages, and other forms of borrowing. Debts can also be owed to the government in the form of taxes, fines, and other fees. Debts can also be owed to private individuals or companies in the form of unpaid bills or invoices."}
=====
The dialog:
=====""" + "\n".join(list(map(lambda m: m['sender'] + ": " + m['message'], message_log))) + "\n===="
        return {
            GptModelNames.GPT3Model : prompt,
            GptModelNames.GPTChatModel: (prompt, [])
        }
    
    @staticmethod
    def generic_v2_chatgpt(message_log:list[BaseMessage]):
        # the model is not outputting reliable json if roles are used
        prompt = """You are a chat bot called "Bot3" who works for a UK bank and is based solely in the UK. You are given the following extracted parts of "the dialog" between "User" and "Bot3". Classify intents and extract entities from the "User" replies in the dialog based on the keys below. If the last "User" reply in the Dialog is a question, then provide a short reply using "reply" json key. If you don't know the answer "reply" should have empty value. Don't try to make up an answer. If the question is outside of financial area or existing context, "reply" should inform that you are tuned to only answer questions about financial area. The only allowed intent json values for "intent_name" are "general", "financial_check", "investment". The only allowed entity values for "entity_name" are "monthly savings", "rainy day fund", "savings balance", "pension contributions", "mortgage amount", "debt", "investments balance", "investment account", "financial goal", "risk tolerance", "help to buy ISA", "monthly rent", "mortgage amount", "savings location", "other savings". "reply" value must be empty unless latest "User" reply is a question. Do not ask questions or provide information unless explicitly asked. Only extract entities below "The dialog:" part. Output only valid json result and nothing else.
Example 1:
=====
Bot3: {"intent_name" : "general", "entities": [], "reply" : "Hello, I'm Scott Bot. What is your name?"}
User: Alex
Bot3: {"intent_name" : "financial_check", "entities": [], "reply" : "Hello Alex! How much are you saving per month?"}
User: 9000
Bot3: {"intent_name" : "financial_check", "entities": [{"entity_name" : "monthly savings", "entity_value": 9000}], "reply" : "What is your financial goal?"}
User: early retirement
Bot3: {"intent_name" : "financial_check", "entities": [{"entity_name" : "monthly savings", "entity_value": 9000}, {"entity_name" : "financial goal", "entity_value": "early retirement"}], "reply" : ""}
===== 
Example 2:
=====
Bot3: {"intent_name" : "general", "entities": [], "reply" : "Hello, I'm Scott Bot. What is your name?"}
User: ddd
Bot3: {"intent_name" : "financial_check", "entities": [], "reply" : "Hello ddd! How much are you saving per month?"}
User: in what currency
Bot3: {"intent_name" : "financial_check", "entities": [], "reply" : "Monthly savings can be in any currency, it would be useful to provide a total amount in GBP."}
User: around 5000
Bot3: {"intent_name" : "financial_check", "entities": [{"entity_name" : "monthly savings", "entity_value": 5000}], "reply" : "What is your financial goal?"}
User: get drunk
Bot3: {"intent_name" : "financial_check", "entities": [{"entity_name" : "monthly savings", "entity_value": 5000}], "reply" : "Ha ha, very funny. Now would please answer the question."} 
=====
Example 3:
=====
Bot3: {"intent_name" : "general", "entities": [], "reply" : "Hello, I'm Scott Bot. What is your name?"}
User: Maria
Bot3: {"intent_name" : "financial_check", "entities": [], "reply" : "Hi Maria! How much do have you got for rainy day?"}
User: Nothing
Bot3: {"intent_name" : "financial_check", "entities": [{"entity_name" : "rainy day fund", "entity_value": 0}], "reply" : "What are you pension contributions?"}
User: I don't contribute
Bot3: {"intent_name" : "financial_check", "entities": [{"entity_name" : "rainy day fund", "entity_value": 0}, {"entity_name" : "pension contributions", "entity_value": 0}], "reply" : "What are you debts?"}
User: What debts?
Bot3: {"intent_name" : "financial_check", "entities": [{"entity_name" : "rainy day fund", "entity_value": 0}, {"entity_name" : "pension contributions", "entity_value": 0}], "reply" : "Debts are amounts of money that are owed by one person or entity to another. In the UK, debts can be in the form of loans, credit cards, overdrafts, mortgages, and other forms of borrowing. Debts can also be owed to the government in the form of taxes, fines, and other fees. Debts can also be owed to private individuals or companies in the form of unpaid bills or invoices."}
=====
The dialog:"""
        return {
            GptModelNames.GPT3Model : prompt,
            GptModelNames.GPTChatModel: (prompt, message_log)
        }


    @staticmethod
    def same_question(message_log:list[BaseMessage]):
        prompt = """You are a chat bot called "Bot3" who works for a UK bank and is based solely in the UK. You are given the following extracted parts of "the  dialog" between "User" and "Bot3". Classify intents and extract entities from the "User" replies in the dialog based on the keys below. If the last "User" reply in the Dialog is a question then provide a short reply using "reply" json key. If you don't know the answer, "reply" should have empty value. If user's latest question is outside of financial area or existing context, reply should inform that you are tuned to only answer questions about financial area. The only allowed intent json values for "intent_name" are "general", "financial_check", "investment". The only allowed entity values for "entity_name" are "monthly savings", "rainy day fund", "savings balance", "pension contributions", "mortgage amount", "debt", "investments balance", "investment account", "financial goal", "risk tolerance", "help to buy ISA", "monthly rent", "mortgage amount", "savings location", "other savings". "reply" value must be empty unless latest "User" reply is a question. Try provide helpful information related to the UK users so that user can provide value. User "reply" json key for that. Do not ask questions. Only extract entities below "The dialog:". Entity values must NOT be assumed as 0 by default. Output only valid json result and nothing else.
Example 1:
=====
User: Alex
Bot3: Hello Alex! How much are you saving per month?
User: 9000
Bot3: What is your financial goal?
User: early retirement
Bot3: Do you have any debts?
User: not sure
===== 
{{"intent_name" : "financial_check", "entities": [{{"entity_name" : "monthly savings", "entity_value": 9000}}, {{"entity_name" : "financial goal", "entity_value": "early retirement"}}], "reply" : ""}}                
=====
Example 2:
=====
User: Maria
Bot3: Hi Maria! How much do have you got for rainy day?
User: Nothing
Bot3: What are you pension contributions?
User: I don't contribute
Bot3: What are you debts?
User: What debts?
=====
{{"intent_name" : "financial_check", "entities": [{{"entity_name" : "rainy day fund", "entity_value": 0}}, {{"entity_name" : "pension contributions", "entity_value": 0}}], "reply" : "It could be any outstanding debts you currently have, for example amount you owe to banks or relatives."}}
=====
Example 3:
=====
User: D
Bot3: Hello D! How much are you saving per month?
User: what do you mean
===== 
{{"intent_name" : "financial_check", "entities": [], "reply" : "Monthly savings are funds that are set aside each month from a person's income to be used for future expenses or investments. This could include putting money into a savings account, investing in stocks or bonds, or setting aside money for a large purchase. Monthly savings can help individuals build up a financial cushion for unexpected expenses or to save for a long-term goal such as retirement."}}                
=====
The dialog:
{0}
=====
""".format("\n".join(list(map(lambda m: m['sender'] + ": " + m['message'], message_log[-2:]))))
        return {
            GptModelNames.GPT3Model : prompt,
            GptModelNames.GPTChatModel: (prompt, [])
        }

    @staticmethod
    def adapt_to_country(message_log:list[BaseMessage], country = None):
        if country is None:
            country = "the United Kingdom"
        prompt = """"Detect whether there are any terms specific to a certain country e.g. relevant to USA only. Do it step by step. Rewrite the information to be relevant to {1}. Output result using json 'reply' key. Do not output anything else but the json. \n====\n""".format(country) + message_log[-1]["message"]
        return {
            GptModelNames.GPT3Model : prompt,
            GptModelNames.GPTChatModel: (prompt, [])
        }
    
    @staticmethod
    def name(message_log:list[BaseMessage]):
        prompt = """Put answer or reply using \"reply\" json key and try extract first name 
                from the query using \"name\" key. If prompt has weird symbols, treat it as user's name. If you don't understand user's input, treat it as his name. Only return json response and nothing else.\n===""" + message_log[-1]["message"]
        return {
            GptModelNames.GPT3Model : prompt,
            GptModelNames.GPTChatModel: (prompt, [])
        }

    @staticmethod
    def rephrase_question(question:str):
        prompt = """You are a chat bot called \"Bot3\" who works for a UK bank and is based solely in the UK. You are polite and having chat with a customer. Your current task is to change the style of the question to make it less interrogating and more conversational and polite. The style should use synonyms to achieve that. Only return the rephrased question and nothing else. Question must be directed to the customer. Do not ask about yourself.
The question:
{0}
Rephrased question:
        """.format(question)
        return {
            GptModelNames.GPT3Model : prompt,
            GptModelNames.GPTChatModel: (prompt, [])
        }


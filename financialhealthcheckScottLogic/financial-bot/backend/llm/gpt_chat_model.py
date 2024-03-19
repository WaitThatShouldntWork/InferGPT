import openai
from . import llm
from utilities.defaults import GptModelNames

class GPTChatModel(llm.LLM):
    name = GptModelNames.GPTChatModel
    def __init__(self, logger = None):
        super().__init__(logger=logger)
    def _call_api(self, request, temperature, token_limit):
       return openai.ChatCompletion.create(
            model=self.name,      # use most advanced auto generation model
            messages=request,            # send user input, chat_log and prompt  
            temperature=temperature,                # how random we want responses (0 is same each time, 1 is highest randomness)
            max_tokens=token_limit,                 # a token is a word, how many we want to send? e.g. 512 for generation and 3584 for the context
        )
    def _process_api_result(self, result):
        return result['choices'][0]["message"]["content"].strip()
    
# Register model in the factory so that it is available in the app
llm.LLMFactory().register_model(GPTChatModel.name, GPTChatModel)

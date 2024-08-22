import openai
from . import llm
from utilities.defaults import GptModelNames

class GPT3Model(llm.LLM):
    name = GptModelNames.GPT3Model
    def __init__(self, logger = None):
        super().__init__(logger=logger)

    def _call_api(self, request, temperature, token_limit):
       return openai.Completion.create(
            engine=self.name,      # use most advanced auto generation model
            prompt=request,            # send user input, chat_log and prompt  
            temperature=temperature,                # how random we want responses (0 is same each time, 1 is highest randomness)
            max_tokens=token_limit,                 # a token is a word, how many we want to send? e.g. 512 for generation and 3584 for the context
        )
    
    def _process_api_result(self, result):
        return result['choices'][0]["text"].strip()
    
# Register model in the factory so that it is available in the app
llm.LLMFactory().register_model(GPT3Model.name, GPT3Model)

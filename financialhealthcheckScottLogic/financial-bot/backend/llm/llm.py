import logging
from abc import ABC, abstractmethod
from utilities.nlp_prompts import PromptFactory
    
class LLM(ABC):
    name = 'LLM'
    def __init__(self, logger = None):
        self._logger = logging.getLogger('chatBot') if logger is None else logger

    @abstractmethod    
    def _call_api(self, request, temperature, token_limit):
        pass
    
    @abstractmethod
    def _process_api_result(self, result):
        pass

    def request_completion(self, texts, temp = None, token_limit = None):
        if temp is None:
            temp = 0
        if token_limit is None:
            token_limit = 512
        prompt_factory = PromptFactory()
        prompt = prompt_factory.create_prompt(self.name)
        prompt.prepare_prompt(texts)
        request = prompt.to_request()
        self._logger.debug(f"""\
            send to {self.name=}:
            {request=}""")
        gpt_response = self._call_api(request, temp, token_limit)
        self._logger.debug(f"""\
            receive from {self.name=}:
            {gpt_response=}""")
        return self._process_api_result(gpt_response)

class LLMFactory(object):
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LLMFactory, cls).__new__(cls)
            cls._creators = {}
        return cls._instance
    
    def register_model(self, model_name:str, model:LLM):
        self._creators[model_name] = model

    def get_model(self, model_name, logger = None) -> LLM:
        creator:LLM = self._creators.get(model_name)
        if not creator:
            raise ValueError(model_name)
        return creator(logger)
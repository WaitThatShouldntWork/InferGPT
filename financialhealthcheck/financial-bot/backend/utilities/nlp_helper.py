import os
import json
import datetime
import re
from utilities.sanitiser import Sanitiser
from utilities.defaults import GptModelNames

# TODO: add tests
from utilities.defaults import Defaults
class NlpHelper:
    @staticmethod
    def hasEntities(json):
        if 'entities' in json:
            return len(json['entities']) > 0
        return False

    @staticmethod 
    def getReply(json):
        if 'reply' in json:
            return json['reply']
        return ''

    @staticmethod
    def getJsonFromCompletion(response_text, logger = None):
        if logger is not None:
            logger.debug(f"called getJsonFromCompletion({response_text=})")
        return json.loads(Sanitiser.sanitiseGPTResponse(response_text))

    @staticmethod
    def extractEntities(json):
        intents = {} if not NlpHelper.hasEntities(json) else {entity['entity_name']:entity['entity_value'] for entity in json['entities']}
        return intents
    
    @staticmethod
    def sender_to_role(sender:str):
        user = Defaults.user
        assistant = Defaults.scottBot
        userRole = 'user'
        assistantRole = 'assistant'
        systemRole = 'system'
        return userRole if sender == user else assistantRole if sender == assistant else systemRole

    @staticmethod
    def check_answers_files(questions_count, asnwers_count, logger):        
        logs_directory = f"./logs/chat/"
        file_suffix = "_answers.json"
        reason = f"EVERYTHING IS OK! Each file *{file_suffix} has {questions_count} questions and {asnwers_count} answers for each question"
        for filename in os.listdir(logs_directory):
            if filename.endswith(file_suffix):
                with open(os.path.join(logs_directory, filename), "r") as f:
                    try:
                        data = json.load(f)
                        if len(data) != questions_count:
                            reason = f"Invalid file {filename}: Expected {questions_count} questions, found {len(data)}"
                            logger.error(reason)
                            return (False, reason)
                        for question in data:
                            if len(data[question]["answers"]) != asnwers_count:
                                reason = f"Invalid file {filename}: Expected {asnwers_count} answers for question '{question}', found {len(data[question]['answers'])}"
                                logger.error(reason)
                                return (False, reason)
                    except Exception as e:
                        reason = f"Invalid file {filename}: {str(e)}"
                        logger.error(reason)
        return (True, reason)
    
    @staticmethod
    def compare_llms(isVerbose = None):
        # Define the directory path and prefix     
        current_time = datetime.datetime.now()
        date = current_time.strftime("%Y-%m-%d")
        logs_directory = f"./logs/chat/{date}/"
        prefix = 'compare_'
        total_replies_count = 0        
        total_db_answers_count = 0
        unrecognised_questions = []

        # Init questions
         
        data_entries_count = 0       
        fully_completed_conversations_count = 0  
        models = [GptModelNames.GPT3Model, GptModelNames.GPTChatModel]
        total_times_asked_expected_key = "total_times_asked_expected"
        total_times_asked_actual_key = "total_times_asked_actual(incl reasked)"
        total_no_answer_in_db_key = "total_no_answer_in_db_count"
        total_times_reasked_key = "total_times_reasked"
        model_times_asked_key = "times_asked(incl reasked)"
        model_no_answer_in_db_count_key = "no_answer_in_db_count"
        model_times_reasked_key = "times_reasked"
        usecase_questions_dic =  {q:{total_times_asked_expected_key:len(os.listdir(logs_directory)),total_times_asked_actual_key:0, 
                                     total_no_answer_in_db_key:0, total_times_reasked_key:0, "models":{m:{model_times_asked_key:0, model_no_answer_in_db_count_key:0, model_times_reasked_key:0} for m in models}} for q in Defaults.usecase_questions}

        # Create a dictionary to store the data
        data = {}
        characters = {}
        model_stats = {}
        for filename in os.listdir(logs_directory):
            if filename.startswith(prefix):
                # Extract the character and model numbers from the filename using regex
                match = re.search(r'char_(\d+)_conv_(\d+)_model_(\d+)_', filename)
                char_num = match.group(1)
                questions_to_complete_list = Defaults.usecase_questions.copy() # used to identify how many questions are still to answer in the current conversation
                conv_num = match.group(2)
                characters[char_num] = True
                model_num = match.group(3)
                model_num = models[int(model_num)]
                if "models_total" not in model_stats:
                        model_stats["models_total"] = {}
                if model_num not in model_stats["models_total"]:
                    model_stats["models_total"][model_num] = {}
                if "db_answer_count" not in model_stats["models_total"][model_num]:
                        model_stats["models_total"][model_num]["db_answer_count"] = 0
                if "no_db_answer_count" not in model_stats["models_total"][model_num]:
                        model_stats["models_total"][model_num]["no_db_answer_count"] = 0
                        
                if "fully_completed_conversations" not in model_stats["models_total"][model_num]:
                        model_stats["models_total"][model_num]["fully_completed_conversations"] = 0
                
                # Open the file and read its contents
                with open(os.path.join(logs_directory, filename), 'r') as file:
                    contents = file.read()
                    
                # Parse the contents as JSON data
                json_data = json.loads(contents)
                
                for q in usecase_questions_dic:
                    # By default the questions are unanswered           
                    usecase_questions_dic[q][total_no_answer_in_db_key] += 1
                    usecase_questions_dic[q]["models"][model_num][model_no_answer_in_db_count_key] += 1

                # Loop through the data and count the dbAnswer values for each originalQuestion
                for item in json_data:
                    data_entries_count += 1
                    question = item['originalQuestion']
                    answer = item['dbAnswer']
                    userAnswer = item['userAnswer']
                    total_replies_count += 1
                    if question not in usecase_questions_dic:
                        unrecognised_questions.append(question)
                    
                    # Count the dbAnswer for the current model and question
                    if answer is not None:
                        if question in questions_to_complete_list:
                            questions_to_complete_list.remove(question)
                        total_db_answers_count += 1
                        if char_num not in data:
                            data[char_num] = {}
                        if question not in data[char_num]:
                            data[char_num][question] = {}
                        if type(answer) == list:
                            answer = ", ".join(answer)
                        if answer not in data[char_num][question]:
                            data[char_num][question][answer] = {}
                        if model_num not in data[char_num][question][answer]:
                            data[char_num][question][answer][model_num] = 0                            
                        if "userAnswer" not in data[char_num][question][answer]:
                            data[char_num][question][answer]["userAnswer"] = userAnswer

                        if question in usecase_questions_dic:
                            usecase_questions_dic[question][total_times_asked_actual_key] += 1
                            usecase_questions_dic[question]["models"][model_num][model_times_asked_key] += 1
                            if (usecase_questions_dic[question]["models"][model_num][model_no_answer_in_db_count_key] > 0):
                                usecase_questions_dic[question]["models"][model_num][model_no_answer_in_db_count_key] -= 1
                                usecase_questions_dic[question][total_no_answer_in_db_key] -= 1
                            else:
                                usecase_questions_dic[question]["models"][model_num][model_times_reasked_key] += 1
                                usecase_questions_dic[question][total_times_reasked_key] += 1                        
                        model_stats["models_total"][model_num]["db_answer_count"] += 1
                    else:                       
                        model_stats["models_total"][model_num]["no_db_answer_count"] += 1
                model_stats["models_total"][model_num]["fully_completed_conversations"] = model_stats["models_total"][model_num]["fully_completed_conversations"] + 1 if len(questions_to_complete_list) == 0 else model_stats["models_total"][model_num]["fully_completed_conversations"]
                fully_completed_conversations_count = fully_completed_conversations_count + 1 if len(questions_to_complete_list) == 0 else fully_completed_conversations_count
        for m in model_stats["models_total"]:
            model_stats["models_total"][m]["conversations_efficiency"] = model_stats["models_total"][m]["fully_completed_conversations"] / (len(os.listdir(logs_directory)) / len(models))
            model_stats["models_total"][m]["answers_efficiency"] = model_stats["models_total"][m]["db_answer_count"] / ( model_stats["models_total"][m]["db_answer_count"] +  model_stats["models_total"][m]["no_db_answer_count"])
        usecase_questions_dic["conversations_total_count"] = len(os.listdir(logs_directory))
        usecase_questions_dic["characters_count"] = len(characters)
        usecase_questions_dic["models_count"] = len(models)
        usecase_questions_dic["conversations_per_character_count"] = len(os.listdir(logs_directory)) / len(characters)
        usecase_questions_dic["conversations_per_model_count"] = len(os.listdir(logs_directory)) / len(models)
        usecase_questions_dic["total_db_answers_to_replies_ratio"] = total_db_answers_count / total_replies_count
        usecase_questions_dic["total_db_answers_to_questions_ratio"] = total_db_answers_count / (len(Defaults.usecase_questions)*len(os.listdir(logs_directory)))
        usecase_questions_dic["unrecognised_questions"] = unrecognised_questions
        usecase_questions_dic["total_question_answer_entries"] = data_entries_count
        usecase_questions_dic["fully_completed_conversations_count"] = fully_completed_conversations_count
        usecase_questions_dic["model_stats"] = model_stats
        return usecase_questions_dic if isVerbose is None or isVerbose == False else data
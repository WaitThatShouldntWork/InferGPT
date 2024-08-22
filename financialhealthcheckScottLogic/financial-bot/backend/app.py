import openai
import uuid
from flask import Flask, Response, request
from flask_cors import CORS
from flask_session import Session
import openai
from dotenv import load_dotenv
import os
import logging
import json
import uuid
import secrets
from typing import cast
from utilities.nlp_helper import NlpHelper
from utilities.session_manager import SessionManager
from utilities.sanitiser import Sanitiser
from utilities.defaults import Defaults, GptModelNames
from graph import GraphConnection
from data.payload import ResponsePayload, Message, ChatReply
from utilities.nlp_prompts import NlpPrompts
from data.models import Question, User
from llm.llm import LLMFactory
# Importing models so that llm factory can register the models
from llm.gpt3_model import GPT3Model
from llm.gpt_chat_model import GPTChatModel
from llm.characters import Characters, Character
import datetime

# By definition message log starts with assistant message first (LLM message is the first one by default)
app = Flask(__name__)
SECRET_KEY = secrets.token_urlsafe(32)
SESSION_TYPE = Defaults.sessionType
app.config.from_object(__name__)
Session(app)
CORS(app, supports_credentials=True)

def log_transcript(sessionId, json_obj):
    tmp = SessionManager.getSessionValue(sessionId, Defaults.jsonTranscriptKey)
    json_list:list = json.loads(tmp if tmp is not None else '[]')
    json_list.append(json_obj)
    current_time = datetime.datetime.now()
    date = current_time.strftime("%Y-%m-%d")
    hour_minute = current_time.strftime("%H-%M")
    log_directory = f"./logs/chat/{date}"
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    log_file = f"{log_directory}/{date}-{hour_minute}-{sessionId}.log"
    with open(log_file, "a") as f:
        json.dump(json_list, f)
    SessionManager.saveSessionValue(sessionId, Defaults.jsonTranscriptKey, json.dumps(json_list))

def log_for_comparison(sessionId, json_obj, prefix = None):
    if prefix is None:
        prefix = ""
    current_time = datetime.datetime.now()
    date = current_time.strftime("%Y-%m-%d")
    hour_minute = current_time.strftime("%H-%M")
    log_directory = f"./logs/chat/{date}"
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    log_file = f"{log_directory}/{prefix}{date}-{hour_minute}-{sessionId}.log"
    with open(log_file, "a") as f:
        json.dump(json_obj, f)

def to_message(sender:str, msg:str):
    return json.loads(json.dumps(Message(_id=uuid.uuid4().hex, message=msg, sender=sender, direction="").__dict__))

def to_chat_reply(id:int, sender:str, msg:str, originalQuestion:str, userAnswer:str):
    return json.loads(json.dumps(ChatReply(id = id, message=msg, sender=sender, originalQuestion=originalQuestion, dbAnswer=None, userAnswer = userAnswer).__dict__))

@app.route("/conversations/start")
def handleConversationStart():
    greeting = "Hello, I'm Bot3. What is your name?"
    sessionId = secrets.token_urlsafe()
    response_payload = ResponsePayload(message=Message(_id=uuid.uuid4().hex, message=greeting, sender=Defaults.sBot, direction=Defaults.directionOutgoing),sessionId=sessionId)
    return Response(json.dumps(response_payload, default=vars), mimetype='application/json')

def getNextQuestion(sessionId, userId, conversationId, entities, messages, retryOnDuplicate = None, response_to_user = None, rephrase_question = None):
    rephrase_question = True if rephrase_question is None else rephrase_question
    logger = logging.getLogger('chatBot')
    llm = LLMFactory().get_model(Defaults.llmModel)
    logger.debug(f"called getNextQuestion({sessionId=}, {userId=}, {conversationId=}, {entities=}, {messages=}, {retryOnDuplicate=})")
    question = cast(Question, app.graph_connection.update_conversation(userId, conversationId, entities))
    response_to_user = '' if response_to_user is None else response_to_user
    if rephrase_question and question is not None:
        try:
            # Rephrase question
            rephrasedQuestion = llm.request_completion(NlpPrompts.rephrase_question(question.question), 0.25)
            question.question = rephrasedQuestion
        except:
            logger.exception("couldn't rephrase question '{0}'".format(question))
        logger.debug(f"""\
                            update_conversation({userId=}, {conversationId=}, {entities=}) returns:
                            {question=}""")
        if retryOnDuplicate:
            lastQuestionId = SessionManager.getSessionValue(sessionId, Defaults.lastQuestionIdSessionKey)
            if (lastQuestionId == question.questionId):
                gpt_response_text = llm.request_completion(NlpPrompts.same_question(messages))
                json_result = NlpHelper.getJsonFromCompletion(gpt_response_text)
                response_to_user =  NlpHelper.getReply(json_result)
                entities = NlpHelper.extractEntities(json_result)
                question = app.graph_connection.update_conversation(userId, conversationId, entities)
                if rephrase_question and question is not None:
                    try:
                        # Rephrase question
                        rephrasedQuestion = llm.request_completion(NlpPrompts.rephrase_question(question.question), 0.25)
                        question.question = rephrasedQuestion
                    except:
                        logger.exception("couldn't rephrase question '{0}'".format(question))
                    logger.debug(f"""\
                            update_conversation({userId=}, {conversationId=}, {entities=}) returns:
                            {question=}""")
        if question is not None:
            SessionManager.saveSessionValue(sessionId, Defaults.lastQuestionIdSessionKey, question.questionId)
    return None if question is None else (question.question if response_to_user == '' else response_to_user + "\n" + question.question)

def getNextQuestionWithOrigin(sessionId, userId, conversationId, entities, messages, retryOnDuplicate = None, response_to_user = None, rephrase_question = None):
    rephrase_question = True if rephrase_question is None else rephrase_question
    logger = logging.getLogger('chatBot')
    llm = LLMFactory().get_model(Defaults.llmModel)
    logger.debug(f"called getNextQuestionAndUpdateLog({sessionId=}, {userId=}, {conversationId=}, {entities=}, {messages=}, {retryOnDuplicate=} {rephrase_question=})")
    question = cast(Question, app.graph_connection.update_conversation(userId, conversationId, entities))
    response_to_user = '' if response_to_user is None else response_to_user
    originalQuestion = None if question is None else question.question        
    if rephrase_question and question is not None:
        try:
            # Rephrase question
            rephrasedQuestion = llm.request_completion(NlpPrompts.rephrase_question(question.question), 0.25)
            question.question = rephrasedQuestion
        except:
            logger.exception("couldn't rephrase question '{0}'".format(question))
        logger.debug(f"""\
                            update_conversation({userId=}, {conversationId=}, {entities=}) returns:
                            {question=}""")
        if retryOnDuplicate:
            lastQuestionId = SessionManager.getSessionValue(sessionId, Defaults.lastQuestionIdSessionKey)
            if (lastQuestionId == question.questionId):
                gpt_response_text = llm.request_completion(NlpPrompts.same_question(messages))
                json_result = NlpHelper.getJsonFromCompletion(gpt_response_text)
                response_to_user =  NlpHelper.getReply(json_result)
                entities = NlpHelper.extractEntities(json_result)
                question = app.graph_connection.update_conversation(userId, conversationId, entities)
                if rephrase_question and question is not None:
                    try:
                        # Rephrase question
                        rephrasedQuestion = llm.request_completion(NlpPrompts.rephrase_question(question.question), 0.25)
                        originalQuestion = question.question
                        question.question = rephrasedQuestion
                    except:
                        logger.exception("couldn't rephrase question '{0}'".format(question))
                    logger.debug(f"""\
                            update_conversation({userId=}, {conversationId=}, {entities=}) returns:
                            {question=}""")
        if question is not None:
            SessionManager.saveSessionValue(sessionId, Defaults.lastQuestionIdSessionKey, question.questionId)
    res = None if question is None else (question.question if response_to_user == '' else response_to_user + "\n" + question.question)
    return res, originalQuestion

@app.route("/conversations/<sessionId>/messages", methods=['POST'])
def handleMessage(sessionId):
    # Init logger
    logger = logging.getLogger('chatBot')
    llm = LLMFactory().get_model(Defaults.llmModel)

    # Get session values
    logger.debug(f"called handleMessage({sessionId=})")
    messages = request.json['messages']
    userId = SessionManager.getSessionValue(sessionId, Defaults.userIdSessionKey)
    goalId = SessionManager.getSessionValue(sessionId, Defaults.goalIdSessionKey)
    conversationId = SessionManager.getSessionValue(sessionId, Defaults.conversationIdSessionKey)
    
    # Log request
    logger.debug(f"""\
        get messages from request:
        {messages=}
        get session data: {userId=} {goalId=} {conversationId=}""")
    
    # Check request
    if Sanitiser.isNoneOrEmpty(userId):
        # Try extract user name
        request_text = NlpPrompts.name([messages[-1]])
    else:
        # Try extract something
        request_text = NlpPrompts.generic_v2(messages)
    gpt_response_text = llm.request_completion(request_text)
    response_to_user = Defaults.conversation_reask
    try:
        json_result = NlpHelper.getJsonFromCompletion(gpt_response_text)
        response_to_user = NlpHelper.getReply(json_result)
        if Sanitiser.isNoneOrEmpty(userId):
            # Identify the User
            try:
                name = json_result['name']
                user = cast(User, app.graph_connection.get_or_create_user(name))
                userId = user.id
                logger.info(f"identified user {userId=} from {name=}")
                # Start conversation
                # TODO: Add support for multiple conversations
                goalId = Defaults.goalId
                conversationId = app.graph_connection.start_conversation(userId, goalId)
                SessionManager.storeSessionData(sessionId, userId, conversationId, goalId)
                question = getNextQuestion(sessionId, userId, conversationId, {}, messages, retryOnDuplicate = True, response_to_user = response_to_user)
                if question is None:
                    response_to_user = Defaults.conversation_end
                else:
                    response_to_user = question
            except Exception as ex:
                logger.exception("Error occurred while trying to get user")
                print('Error getting user: ', ex)
                # name not extracted, reprompt
                response_to_user = Defaults.conversation_reask
        else:
            # Extract intent and entities
            try:
                entities = NlpHelper.extractEntities(json_result)
                question = getNextQuestion(sessionId, userId, conversationId, entities, messages, retryOnDuplicate = True, response_to_user = response_to_user)
                if question is None:
                    response_to_user = Defaults.conversation_end
                else:
                    response_to_user = question
            except Exception as ex:
                logger.exception("Error occurred while classifying intent or extracting entities")
                # name not extracted, reprompt
                response_to_user = Defaults.conversation_reask
    except Exception as ex:
        logger.exception("Error processing reply")
        print('Error processing reply: ', ex)
    # Outgoing response
    response_payload = ResponsePayload(message=Message(_id=uuid.uuid4().hex, message=response_to_user, sender=Defaults.sBot, direction=Defaults.directionOutgoing),sessionId=sessionId)
    return Response(json.dumps(response_payload, default=vars), mimetype='application/json')

@app.route("/conversations/mcd/start")
def multi_character_dialogue():
    # Init logger
    logger = logging.getLogger('chatBot')
    llm = LLMFactory().get_model(Defaults.llmModel)
    sessionId = secrets.token_urlsafe()
    characters:dict[Character] = Characters().get_characters(sessionId)
    response_to_user = ''
    result = []

    for character in characters:
        # Init
        message_log = []
        userId = Defaults.userId
        goalId = Defaults.goalId
        # Start conversation in graph db
        try:
            conversationId = app.graph_connection.start_conversation(userId, goalId)
            question = getNextQuestion(sessionId, userId, conversationId, {}, message_log, retryOnDuplicate = True, response_to_user = response_to_user)
            while question is not None and len(message_log) < Defaults.messagesLimit:
                # Loop while there are questions to be answered or we hit the limit
                if question is not None:
                    message_log.append(to_message(Defaults.sBot, question))
                    # Get answer
                    answer = llm.request_completion(character.to_prompt())
                    message_log.append(to_message(Defaults.user, answer))
                    # Process answer 
                    request_text = NlpPrompts.generic_v2(message_log)
                    gpt_response_text = llm.request_completion(request_text)
                    json_result = NlpHelper.getJsonFromCompletion(gpt_response_text)
                    response_to_user = NlpHelper.getReply(json_result)
                    entities = NlpHelper.extractEntities(json_result)
                    question = getNextQuestion(sessionId, userId, conversationId, entities, message_log, retryOnDuplicate = True, response_to_user = response_to_user)
            
        except Exception as ex:
                logger.exception("Error occurred while classifying intent or extracting entities")
                # name not extracted, reprompt
                response_to_user = Defaults.conversation_reask

        # Log trancript
        # TODO: Move chat transcript compilation to character class
        responses = [ChatReply(message=msg['message'], sender=msg['sender'], originalQuestion='') for msg in message_log]
        result.append(responses)
        log_transcript(sessionId, responses)

    # Outgoing response
    return Response(json.dumps(result, default=vars), mimetype='application/json')

@app.route("/conversations/mcd/init")
def generate_answers():
    # Init logger
    logger = logging.getLogger('chatBot')
    llm = LLMFactory().get_model(Defaults.llmModel)
    sessionId = secrets.token_urlsafe()
    characters:dict[Character] = Characters().get_characters(sessionId)

    for character in characters:
        # Init
        # TODO: Change so that the questions are taken from graph db
        for question in Defaults.usecase_questions:
            answers = llm.request_completion(character.generate_answers_prompt(question, Defaults.answers_to_generate_count), temp=0.7, token_limit=2500)
            character.add_answers(question,  NlpHelper.getJsonFromCompletion(answers, logger))
        character.save_answers()

    # Outgoing response
    return Response(mimetype='application/json')

@app.route("/conversations/mcd/compare-llms")
def compare_llms():
    # Init logger
    logger = logging.getLogger('chatBot')

    # Check answers before using them
    validationResults = NlpHelper.check_answers_files(len(Defaults.usecase_questions), Defaults.answers_to_generate_count, logger)
    areAnswersValid = validationResults[0]
    if not areAnswersValid: 
        return Response(json.dumps(validationResults, default=vars), mimetype='application/json')

    # Init comparison
    sessionId = secrets.token_urlsafe()
    characters:dict[Character] = Characters().get_characters(sessionId)
    result = []
    character_conversations_answers = {}

    # Get conversation answers
    for character in characters:
        answers = character.load_answers() # kv pair q:[answers]
        # Each character has as many conversations as there are answers for each of the question
        character_conversations_answers[character.profile_id] = [dict() for _ in range(Defaults.answers_to_generate_count)]
        for q in answers.keys():
            tmp = 0  # counter for the current answer
            # add answers for question q for each conversation
            for a in answers[q]["answers"]:
                # save question(q)'s answer(a) for conversation i(tmp)
                character_conversations_answers[character.profile_id][tmp][q] = a
                tmp = tmp + 1

    # Test different LLMs with fixed answers
    for ci, conversations_key in enumerate(character_conversations_answers):
        for j, convesation in enumerate(character_conversations_answers[conversations_key]):
            for k, llmModel in  enumerate([GptModelNames.GPT3Model, GptModelNames.GPTChatModel]):
                llm = LLMFactory().get_model(llmModel)
                userId = Defaults.userId
                goalId = Defaults.goalId
                message_log:list[ChatReply] = []
                response_to_user = ''
                # Start conversation in graph db
                conversationId = app.graph_connection.start_conversation(userId, goalId)
                try:
                    question, originalQ = getNextQuestionWithOrigin(sessionId, userId, conversationId, {}, message_log, retryOnDuplicate = True, response_to_user = response_to_user, rephrase_question=False)
                    while question is not None and len(message_log) < Defaults.messagesLimit:
                        # Loop while there are questions to be answered or we hit the limit
                        if question is not None: 
                            # Get answer
                            try:
                                matched_answer = convesation[originalQ]
                            except Exception as e:
                                print(f"Exception happened: {e}")
                            message_log.append(to_chat_reply(len(message_log), Defaults.sBot, question, originalQ, matched_answer))
                            message_log.append(to_chat_reply(len(message_log), Defaults.user, matched_answer, originalQ, matched_answer))
                            # Process answer
                            request_text = NlpPrompts.generic_v2(message_log)
                            gpt_response_text = llm.request_completion(request_text)
                            json_result = NlpHelper.getJsonFromCompletion(gpt_response_text)
                            response_to_user = NlpHelper.getReply(json_result)
                            entities = NlpHelper.extractEntities(json_result)
                            question, originalQ = getNextQuestionWithOrigin(sessionId, userId, conversationId, entities, message_log, retryOnDuplicate = True, response_to_user = response_to_user, rephrase_question=False)  
                except Exception as ex:
                        logger.exception("Error occurred while classifying intent or extracting entities")
                        # name not extracted, reprompt
                        response_to_user = Defaults.conversation_reask

                # Log trancript
                # TODO: Move chat transcript compilation to character class
                stored_questions_raw:list[Question] = app.graph_connection.get_conversation_details(conversationId)
                for q in stored_questions_raw:
                    try:
                        answered = False
                        for i, _ in enumerate(message_log):
                            if message_log[i]['originalQuestion'] == q.question:
                                message_log[i]['dbAnswer'] = q.answer
                                answered = True
                        if not answered:
                            message_log.append(to_chat_reply(len(message_log), Defaults.llmModel, q.answer, q.question))
                    except Exception as e:
                        print('error {e}')
                log_for_comparison(sessionId, message_log, Defaults.comparisonPrefix + "_char_" + str(ci) + "_conv_" + str(j) + "_model_" + str(k) + "_" )
                # log_for_comparison(sessionId, message_log, Defaults.comparisonPrefix + "_char_" + str(i)  + "_conv_" + str(k) + "_model_" + str(k) + "_" )

    # Outgoing response
    return Response(json.dumps(result, default=vars), mimetype='application/json')

@app.route("/conversations/mcd/comparison-results")
def compare_results():
    # Outgoing response
    return Response(json.dumps(NlpHelper.compare_llms(), default=vars), mimetype='application/json')

@app.route("/conversations/start/openai")
def handleConversationStartWithOpenAI():
    greeting = "Hello, I'm Bot3. How can I help you today?"
    sessionId = uuid.uuid4().hex
    response_payload = ResponsePayload(message=Message(_id=uuid.uuid4().hex, message=greeting, sender=Defaults.sBot, direction=Defaults.directionOutgoing),sessionId=sessionId)
    return Response(json.dumps(response_payload, default=vars), mimetype='application/json')

# Temporary API method in order to simulate the conversation without history and orchestration
# Expects all messages in the conversation to pass to GPT3
@app.route("/conversations/<sessionId>/messages", methods=['PUT'])
def handleConversationWithOpenAI(sessionId):
    # Incoming request
    messages = request.json['messages']
    request_text = """You are a financial advisor AI called Bot3 that works for a Retail Bank based solely in the UK.
    The financial advisor is helpful, polite, creative, clever, and very friendly.
    The financial advisor helps customer solve problems without needing to call agents by collecting information from the customer in order to recommend products.
    You must ask at least 7 questions, one at a time, before providing a summary of the customer along with your recommendations.
    The conversation goal is a financial health check.\n"""
    request_text += "\n".join(list(map(lambda m: m['sender'] + ": " + m['message'], messages)))
    request_text += f"\n{Defaults.sBot}:"
    # logic - openai for now
    gpt_response = openai.Completion.create(
        engine="text-davinci-003",      # use most advanced auto generation model
        prompt=request_text,            # send user input, chat_log and prompt  
        temperature=0.5,                # how random we want responses (0 is same each time, 1 is highest randomness)
        max_tokens=512,                 # a token is a word, how many we want to send?
        top_p=1,                        # equally weigh responses
        frequency_penalty=0,            # penalty for repeated words (0 lowest, 1 highest)
        presence_penalty=0,             # encourage of limit the bot talking about new topics (0 lowest, 1 highest)
        stop=[f"{Defaults.sBot}:", f"{Defaults.user}:"]
    )
    gpt_response_text = gpt_response['choices'][0]["text"].lstrip()
    # Outgoing response
    response_payload = ResponsePayload(message=Message(_id=uuid.uuid4().hex, message=gpt_response_text, sender=Defaults.sBot, direction=Defaults.directionOutgoing),sessionId=sessionId)
    return Response(json.dumps(response_payload, default=vars), mimetype='application/json')

@app.route("/test/neo4j")
def test_neo4j():
    app.graph_connection.print_greeting("A new node has been created!")
    answer = "You should see a new node has been created."
    return Response(json.dumps(answer), mimetype='application/json')

@app.route("/test/gpt", )
def test_gpt():
    prompt_text = "What would be your response if I say 'ping!'"
    tempt = 0.5
    response = openai.Completion.create(
        engine="text-davinci-003",      # use most advanced auto generation model
        prompt=prompt_text,             # send user input, chat_log and prompt  
        temperature=tempt,              # how random we want responses (0 is same each time, 1 is highest randomness)
        max_tokens=512,                 # a token is a word, how many we want to send?
        top_p=1,                        # equally weigh responses
        frequency_penalty=0,            # penalty for repeated words (0 lowest, 1 highest)
        presence_penalty=0,             # encourage of limit the bot talking about new topics (0 lowest, 1 highest)
        # stop=["Bot:", "Customer:"]
    )
    answer = response['choices'][0]
    return Response(json.dumps(answer), mimetype='application/json')

@app.route("/")
def hello():
    answer = "Hello!"
    return Response(json.dumps(answer), mimetype='application/json')

if __name__ == '__main__':
    # Setup logging for ease of use later on
    logger = logging.getLogger('chatBot')
    logger.setLevel(logging.DEBUG)
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    os.makedirs("./logs", exist_ok=True)
    fh = logging.FileHandler(f'./logs/{current_time}.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(funcName)s(%(lineno)d) - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logger.info("Backend server is starting.")
    # Load environment variables
    load_dotenv()
    # Graph connection start up - test creating a node
    graph_db_server = os.environ.get("GRAPH_DB_SERVER")
    graph_db_user = os.environ.get("GRAPH_DB_USER")
    graph_db_password = os.environ.get("GRAPH_DB_PASSWORD")
    graph_connection = GraphConnection(
        graph_db_server, graph_db_user, graph_db_password)
    # openai setup key
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    # add graph connection to flask state
    app.graph_connection = graph_connection
    # Start the flask app
    flask_host = os.environ.get("FLASK_HOST")
    flask_port = os.environ.get("FLASK_PORT")
    app.run(host=flask_host, port=flask_port, debug=True, use_reloader=False)

class GptModelNames:
    GPT3Model = 'text-davinci-003'
    GPTChatModel = 'gpt-3.5-turbo'
    
class Defaults:
    goalId = 1
    userId = 3
    messagesLimit = 15
    user = "User"
    sBot = "Bot3"
    # Session key
    sessionType = 'filesystem'
    # Session keys
    userIdSessionKey = "userId"
    conversationIdSessionKey = "conversationId"
    goalIdSessionKey = "goalId"
    lastQuestionIdSessionKey = "lastQuestionId"
    jsonTranscriptKey = "transcriptId"

    # Request keys
    directionOutgoing = "outgoing"
    directionIncoming = "incoming"
    # Model
    llmModel = GptModelNames.GPTChatModel
    # Replies
    conversation_reask = "Sorry, I couldn't get that. Can you rephrase, please?"
    conversation_end = "Thank you for the information! We will be in touch with you soon."
    # Files
    comparisonPrefix = "compare"
    usecase_questions = [
        "Do you have a mortgage and if so, how much?",
        "How much are you saving each month?",
        "Do you have a rainy day fund and, if so, how much?",
        "Do you have any loans or credit card debt and if so, how much?",
        "What is your financial goal?",
        "If you have savings, where are you saving that money currently?",
        "Do you have savings anywhere else except the already mentioned?"
    ]
    answers_to_generate_count = 3

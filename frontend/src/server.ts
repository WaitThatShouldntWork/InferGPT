export interface ChatMessageResponse {
  message: string;
}

let happyResponse: ChatMessageResponse = {
    message: "InferGPT backend is healthy!"
}

let unhappyResponse: ChatMessageResponse = {
    message: "Error: InferGPT backend is unhealthy"
}

let unsupportedResponse: ChatMessageResponse = {
    message: "Error: General chat response unsupported"
}

export const getResponse = async (message: string): Promise<ChatMessageResponse> => {
    if (message == "healthcheck") {
        return checkBackendHealth();
    } else {
        return callChatEndpoint(message);
    }
};

const checkBackendHealth = async (): Promise<ChatMessageResponse> => {
    try {
        const response = await fetch(`${process.env.BACKEND_ENDPOINT}/health`);
        console.log('InferGPT backend is healthy!: ', response);
        return happyResponse;
    } catch {
        return unhappyResponse;
    }
}

const callChatEndpoint = async (message: string): Promise<ChatMessageResponse> => {
    return await fetch(`${process.env.BACKEND_ENDPOINT}/chat?utterance=${message}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response;
        })
        .then(response => response.json())
        .then(responseJson => {
            let responseAsChatMessageResponse: ChatMessageResponse = {
                message: responseJson
            }
            return responseAsChatMessageResponse
        })
        .catch(error => {
            console.error('Error making REST call to /chat: ', error);
            return unhappyResponse;
        });
}

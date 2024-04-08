export interface ChatMessageResponse {
  message: string;
}

const happyResponse: ChatMessageResponse = {
  message: 'Healthcheck: InferGPT backend is healthy!'
};

const unhappyResponse: ChatMessageResponse = {
  message: 'Healthcheck: InferGPT backend is unhealthy'
};

const unhappyChatResponse: ChatMessageResponse = {
  message: 'I\'m sorry, but I was unable to get a response from InferGPT. Please check the status of the service using the phrase \"healthcheck\"'
};

export const getResponse = async (message: string): Promise<ChatMessageResponse> => {
  if (message == 'healthcheck') {
    return checkBackendHealth();
  } else {
    return callChatEndpoint(message);
  }
};

const checkBackendHealth = async (): Promise<ChatMessageResponse> => {
  try {
    const response = await fetch(`${process.env.INFER_GPT_BACKEND_URL}/health`);
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    console.log('InferGPT backend is healthy!: ', response);
    return happyResponse;
  } catch {
    return unhappyResponse;
  }
};

const callChatEndpoint = async (message: string): Promise<ChatMessageResponse> => {
  return await fetch(`${process.env.INFER_GPT_BACKEND_URL}/chat?utterance=${message}`)
    .then(response => {
      if (!response.ok) {
        console.log("error found")
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response;
    })
    .then(response => response.json())
    .then(responseJson => {
      const responseAsChatMessageResponse: ChatMessageResponse = {
        message: responseJson
      };
      return responseAsChatMessageResponse;
    })
    .catch(error => {
      console.error('Error making REST call to /chat: ', error);
      return unhappyChatResponse;
    });
};

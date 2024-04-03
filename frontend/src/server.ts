export interface ChatMessageResponse {
  message: string;
}

const happyResponse: ChatMessageResponse = {
  message: 'InferGPT backend is healthy!'
};

const unhappyResponse: ChatMessageResponse = {
  message: 'Error: InferGPT backend is unhealthy'
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
      return unhappyResponse;
    });
};

export interface Response {
  message: string;
}

let happyResponse: Response = {
    message: "InferGPT backend is healthy!"
}

let unhappyResponse: Response = {
    message: "Error: InferGPT backend is unhealthy"
}

let unsupportedResponse: Response = {
    message: "Error: General chat response unsupported"
}

export const getResponse = async (message: string): Promise<Response> => {
    if (message == "healthcheck") {
        try {
            const response = await fetch(`${process.env.BACKEND_ENDPOINT}/health`);
            console.log('InferGPT backend is healthy!: ', response.json());
            return new Promise((resolve) => {
                setTimeout(() => {resolve(happyResponse);}, 1000);
            });
        } catch {
            return new Promise((resolve) => {
                setTimeout(() => {resolve(unhappyResponse);}, 1000);
            })
        }
    } else {
        return new Promise((resolve) => {
            setTimeout(() => {resolve(unsupportedResponse);}, 1000);
        })
    }
};

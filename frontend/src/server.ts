export interface Response {
  message: string;
}

export const getResponse = async (message: string): Promise<Response> => {
  // TODO - get response from backend API using env variable for endpoint
  // (.env variables available via process.env)
  // const response = await fetch(`${process.env.BACKEND_ENDPOINT}/chat?utterance=${message}`, {
  //   method: 'GET',
  //   headers: {
  //     'Content-Type': 'application/json',
  //   },
  // });
  const response = await fetch('http://127.0.0.1:8000/health');
  console.log('HELLO - response: ', response.json());
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({ message });
    }, 3000);
  });
};

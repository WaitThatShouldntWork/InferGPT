export interface Response {
  message: string;
}

export const getResponse = async (message: string): Promise<Response> => {
  // TODO - get response from backend API using env variable for endpoint
  // (.env variables available via process.env)
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({ message });
    }, 3000);
  });
};

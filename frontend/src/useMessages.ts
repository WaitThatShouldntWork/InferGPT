import { useCallback, useState } from 'react';
import { Message, Role } from './components/message';
import { getResponse } from './server';

const starterMessage: Message = {
  role: Role.Bot,
  content: 'Hello, how can I help you?',
  time: new Date().toLocaleTimeString(),
};

export interface UseMessagesHook {
  sendMessage: (message: string) => void;
  messages: Message[];
  waiting: boolean;
}

export const useMessages = (): UseMessagesHook => {
  const [waiting, setWaiting] = useState<boolean>(false);
  const [messages, setMessages] = useState<Message[]>([starterMessage]);

  const appendMessage = useCallback((message: string, role: Role) => {
    setMessages((prevMessages) => [
      ...prevMessages,
      { role, content: message, time: new Date().toLocaleTimeString() },
    ]);
  }, []);

  const sendMessage = useCallback(
    async (message: string) => {
      appendMessage(message, Role.User);
      setWaiting(true);
      const response = await getResponse(message);
      setWaiting(false);
      appendMessage(response.message, Role.Bot);
    },
    [appendMessage, messages]
  );

  return {
    sendMessage,
    messages,
    waiting,
  };
};

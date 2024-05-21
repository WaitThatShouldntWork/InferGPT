import { createContext } from 'react';

export enum MessageType {
  PING = 'ping',
  CHAT = 'chat',
}

export interface Message {
  type: MessageType;
  data?: string;
}

export interface Connection {
  isConnected: boolean;
  lastMessage: string | null;
  send: (message: Message) => void;
}

export const WebsocketContext = createContext<Connection>({
  isConnected: false,
  lastMessage: null,
  send: () => {},
});

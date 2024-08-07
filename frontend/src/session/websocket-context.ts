import { createContext } from 'react';

export enum MessageType {
  PING = 'ping',
  CHAT = 'chat',
  IMAGE = 'image'
}

export interface Message {
  type: MessageType;
  data?: string;
}

export interface Connection {
  isConnected: boolean;
  lastMessage: Message | null;
  send: (message: Message) => void;
}

export const WebsocketContext = createContext<Connection>({
  isConnected: false,
  lastMessage: null,
  send: () => {},
});

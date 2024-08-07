import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { Connection, Message, MessageType, WebsocketContext } from './websocket-context';

export interface WebsocketProviderProps {
  children: React.ReactNode;
}

const WS_URL = process.env.WS_URL || 'ws://localhost:8250/ws';
const heartbeatInterval = 10000;
const ping = JSON.stringify({ type: MessageType.PING });

export const WebsocketProvider = ({ children }: WebsocketProviderProps) => {
  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState<Message | null>(null);
  
  const ws = useRef<WebSocket | null>(null);

  const heartbeat = useCallback(() => {
    if (!ws.current || ws.current?.readyState !== 1) return;
      
    ws.current.send(ping);

    setTimeout(heartbeat, heartbeatInterval);
  }, []);

  useEffect(() => {
    const socket = new WebSocket(WS_URL);

    socket.onopen = () => {
      setIsConnected(true);
      heartbeat();
    };
    socket.onclose = () => {
      setIsConnected(false);
    };
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setLastMessage(data)
    };

    socket.onerror = (error) => {
      setIsConnected(false);
      console.error('WebSocket error:', error);
    };

    ws.current = socket;

    return () => {
      socket.close();
    };
  }, []);

  const sendMessage = useCallback((message: Message) => {
    if (ws.current?.readyState === 1) {
      ws.current.send(JSON.stringify(message));
    }
  }, []);

  const connection = useMemo<Connection>(
    () => ({
      isConnected,
      lastMessage,
      send: sendMessage || (() => {}),
    }),
    [isConnected, lastMessage, sendMessage]
  );

  return (
    <WebsocketContext.Provider value={connection}>
      {children}
    </WebsocketContext.Provider>
  );
};

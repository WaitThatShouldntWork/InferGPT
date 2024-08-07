import React, { useContext, useEffect, useState } from 'react';
import { Message, MessageComponent } from './message';
import styles from './chat.module.css';
import { Waiting } from './waiting';
import { ConnectionStatus } from './connection-status';
import { WebsocketContext, MessageType } from '../session/websocket-context';

export interface ChatProps {
  messages: Message[];
  waiting: boolean;
}

export const Chat = ({ messages, waiting }: ChatProps) => {
  const containerRef = React.useRef<HTMLDivElement>(null);
  const { isConnected, lastMessage } = useContext(WebsocketContext);
  const [chart, setChart] = useState<string | undefined>(undefined);

  useEffect(() => {
    if (lastMessage && lastMessage.type === MessageType.IMAGE) {
      const imageData = `data:image/png;base64,${lastMessage.data}`;
      setChart(imageData);
    }
  }, [lastMessage])

  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTo(0, containerRef.current.scrollHeight);
    }
  }, [messages.length]);

  return (
    <div ref={containerRef} className={styles.container}>
      <ConnectionStatus isConnected={isConnected} />
      {messages.map((message, index) => (
        <MessageComponent key={index} message={message} />
      ))}
      {chart && <img src={chart} alt="Generated chart"/>}
      {waiting && <Waiting />}
    </div>
  );
};

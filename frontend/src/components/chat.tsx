import React, { useEffect } from 'react';
import { Message, MessageComponent } from './message';
import styles from './chat.module.css';
import { Waiting } from './waiting';

export interface ChatProps {
  messages: Message[];
  waiting: boolean;
}

export const Chat = ({ messages, waiting }: ChatProps) => {
  const containerRef = React.useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTo(0, containerRef.current.scrollHeight);
    }
  }, [messages.length]);

  return (
    <div ref={containerRef} className={styles.container}>
      {messages.map((message, index) => (
        <MessageComponent key={index} message={message} />
      ))}
      {waiting && <Waiting />}
    </div>
  );
};

import React from 'react';
import styles from './app.module.css';
import { Chat } from './components/chat';
import { Input } from './components/input';
import { useMessages } from './useMessages';

export const App = () => {
  const { sendMessage, messages, waiting } = useMessages();

  return (
    <div className={styles.container}>
      <Chat messages={messages} waiting={waiting} />
      <Input sendMessage={sendMessage} />
    </div>  
  );
};

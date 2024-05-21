import React, { useContext } from 'react';
import styles from './app.module.css';
import { Chat } from './components/chat';
import { Input } from './components/input';
import { useMessages } from './useMessages';
import { ConnectionStatus } from './components/connection-status';
import { WebsocketContext } from './session/websocket-context';

export const App = () => {
  const { sendMessage, messages, waiting } = useMessages();

  const { isConnected } = useContext(WebsocketContext);

  return (
    <div className={styles.container}>
      <Chat messages={messages} waiting={waiting} />
      <Input sendMessage={sendMessage} />
      <ConnectionStatus isConnected={isConnected} />
    </div>  
  );
};

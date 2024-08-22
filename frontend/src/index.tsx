import React from 'react';
import { createRoot } from 'react-dom/client';
import { App } from './app';
import './styles.css';
import { WebsocketProvider } from './session/websocket-provider';

const container = document.getElementById('app-root')!;
const root = createRoot(container);

root.render(
  <WebsocketProvider>
    <App />
  </WebsocketProvider>
);

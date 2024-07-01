import React from 'react';
import classNames from 'classnames';
import styles from './connection-status.module.css';

export interface ConnectionStatusProps {
  isConnected: boolean;
}

export const ConnectionStatus = ({ isConnected }: ConnectionStatusProps) => {
  return (
    <div className={styles.container}>
      <div className={classNames(styles.dot, {
        [styles.green]: isConnected,
        [styles.red]: !isConnected
      })} />
    </div>
  );
};

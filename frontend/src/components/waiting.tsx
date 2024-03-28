import React from 'react';
import styles from './waiting.module.css';

export const Waiting = () => {
  return (
    <div className={styles.waiting}>
      <span className={styles.waitingDot}></span>
      <span className={styles.waitingDot}></span>
      <span className={styles.waitingDot}></span>
    </div>
  );
};

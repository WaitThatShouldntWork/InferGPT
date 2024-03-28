import React, { ChangeEvent, FormEvent, useCallback, useMemo, useState } from 'react';
import styles from './input.module.css';
import RightArrow from '../icons/map-arrow-right.svg';
import classNames from 'classnames';

export interface InputProps {
  sendMessage: (message: string) => void;
}

export const Input = ({ sendMessage }: InputProps) => {
  const [userInut, setUserInput] = useState<string>('');

  const onChange = useCallback((event: ChangeEvent<HTMLInputElement>) => {
    setUserInput(event.target.value);
  }, []);

  const onSend = useCallback(
    (event: FormEvent<HTMLElement>) => {
      event.preventDefault();
      sendMessage(userInut);
      setUserInput('');
    },
    [sendMessage, userInut]
  );

  const sendDisabled = useMemo(() => userInut.length === 0, [userInut]);

  return (
    <form onSubmit={onSend} className={styles.inputContainer}>
      <input
        className={styles.input}
        onChange={onChange}
        onSubmit={onSend}
        placeholder="Send a Message..."
        type="text"
        value={userInut}
      />
      <button className={classNames(styles.sendButton, { [styles.disabled]: sendDisabled })} onClick={onSend} disabled={sendDisabled}>
        <img src={RightArrow} />
      </button>
    </form>
  );
};

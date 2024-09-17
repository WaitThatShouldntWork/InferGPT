import Styles from './confirm-modal.module.css';
import { useEffect, useRef } from 'react';
import { Message, MessageType } from '../session/websocket-context';
import React from 'react';

export interface Confirmation {
  id: string,
  requestMessage: string,
  result: boolean | null
}

interface ConfirmModalProps {
  confirmation: Confirmation | null,
  setConfirmation: (confirmation: Confirmation | null) => void,
  send: (message: Message) => void
}

export const ConfirmModal = ({ confirmation, setConfirmation, send }: ConfirmModalProps) => {
  const mapConfirmationToMessage = (confirmation: Confirmation): Message => {
    return { type: MessageType.CONFIRMATION, data: confirmation.id + ':' + (confirmation.result ? 'y' : 'n') };
  };

  const updateConfirmationResult = (newResult: boolean) => {
    if (confirmation) {
      setConfirmation({ ...confirmation, result: newResult });
    }
  };


  const modalRef = useRef<HTMLDialogElement>(null);

  useEffect(() => {
    if (confirmation) {
      if (confirmation.result !== null) {
        send(mapConfirmationToMessage(confirmation));
        setConfirmation(null);
      } else {
        modalRef.current?.showModal();
      }
    } else {
      modalRef.current?.close();
    }
  }, [confirmation]);

  return (
    <dialog className={Styles.modal} ref={modalRef} onClose={() => updateConfirmationResult(false)}>
      <div className={Styles.modalContent}>
        <h1 className={Styles.header}>Confirmation</h1>
        <p className={Styles.requestMessage}>{confirmation && confirmation.requestMessage}</p>
        <div className={Styles.buttonsBar}>
          <button className={Styles.cancel} onClick={() => updateConfirmationResult(false)}>Cancel</button>
          <button className={Styles.confirm} onClick={() => updateConfirmationResult(true)}>Confirm</button>
        </div>
      </div>
    </dialog>
  );
};

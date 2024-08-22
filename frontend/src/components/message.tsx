import classNames from 'classnames';
import React, { useMemo } from 'react';
import styles from './message.module.css';
import UserIcon from '../icons/user.svg';
import BotIcon from '../icons/cpu.svg';

export enum Role {
  User = 'User',
  Bot = 'Bot',
}

export interface Message {
  role: Role;
  content: string;
  time: string;
}

export interface MessageProps {
  message: Message;
}

export interface MessageStyle {
  icon: string;
  class: string;
}

const roleStyleMap: Record<Role, MessageStyle> = {
  [Role.User]: {
    icon: UserIcon,
    class: styles.user,
  },
  [Role.Bot]: {
    icon: BotIcon,
    class: styles.bot,
  },
};

export const MessageComponent = ({ message }: MessageProps) => {
  const { content, role } = message;

  const { class: roleClass, icon } = useMemo(() => roleStyleMap[role], [role]);

  return (
    <div className={classNames(styles.container, roleClass)}>
      <img src={icon} />
      <p>{content}</p>
    </div>
  );
};

import "@chatscope/chat-ui-kit-styles/dist/default/styles.min.css";
import { MainContainer, ChatContainer, ConversationHeader, MessageList, Message, MessageInput } from "@chatscope/chat-ui-kit-react";

export const Widget = ({remoteName = "sBot", messages = [], onSend}) => {
    
    return (
        <MainContainer>
            <ChatContainer>
                <ConversationHeader>
                    <ConversationHeader.Content userName={remoteName} />
                </ConversationHeader>
        
                <MessageList>
                    {messages.map( message =>
                        <Message key={message._id} model={message} />
                    )}
        
                </MessageList>
        
                <MessageInput placeholder="Type message here"
                              attachButton={false}
                              onSend={onSend}
                />
            </ChatContainer>
        </MainContainer>
    );
};



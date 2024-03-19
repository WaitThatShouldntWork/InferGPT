import { useState, useEffect } from "react";
import { Widget } from "./Widget";
import { nanoid } from "nanoid";

export const WidgetContainer = () => {

    const [messages, setMessages] = useState([]);
    const [sessionId, setSessionId] = useState();
    // Change to false to have a generic conversation with chatGPT
    const useGraphDb = true;
    useEffect(() => {
        async function startConversation() {
            if (!sessionId && messages.length === 0) {

                let response = await fetch('http://localhost:8000/conversations/start'+(useGraphDb ? '' : '/openai'), {
                    method: 'GET',
                    headers: {'Content-Type': 'application/json'},
                    credentials: 'include'
                })
                .then(response => { 
                    return response.json();})
                .catch(err => {console.log(err);});

                setSessionId(response.sessionId);
                setMessages(messages.concat(response.message));
            }
        }
        
        startConversation();
    },[sessionId, messages]);
    
    const handleSend = async (message) => {
        const newMessages = [{
            _id: nanoid(),
            message,
            sender: "User",
            direction: "incoming",
        }];
        setMessages(messages.concat(newMessages));

        let response = await fetch(`http://localhost:8000/conversations/${sessionId}/messages`, {
            method: useGraphDb ? 'POST' : 'PUT',
            headers: {'Content-Type': 'application/json'},
            credentials: 'include',
            body: JSON.stringify({messages: messages.concat(newMessages)})
        })
        .then(response => { 
            return response.json();})
        .catch(err => {console.log(err);});
        
        newMessages.push(response.message);
        setMessages(messages.concat(newMessages));
    };
    
    return <Widget messages={messages} onSend={handleSend} />
}
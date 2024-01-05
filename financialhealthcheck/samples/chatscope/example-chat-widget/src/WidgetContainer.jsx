import { useState, useEffect } from "react";
import { Widget } from "./Widget";
import { nanoid } from "nanoid";
const { Configuration, OpenAIApi } = require("openai");

const configuration = new Configuration({
    apiKey: '<add-your-api-key>',
});
const openai = new OpenAIApi(configuration);
const user = "User";
const Bot0 = "Bot0";

export const WidgetContainer = ({greeting = "Hello, I'm Bot0. How can I help you today?"}) => {

    const [messages, setMessages] = useState([]);

    useEffect( () => {
        if ( greeting && messages.length === 0 ) {
            setMessages(messages.concat({
                _id: nanoid(),
                message: greeting,
                sender: Bot0,
                direction: "incoming",
            }));
        }
    },[greeting, messages]);
    
    const handleSend = async (message) => {
        const newMessages = [{
            _id: nanoid(),
            message,
            sender: user,
            direction: "outgoing",
        }];
        setMessages(messages.concat(newMessages));

        const prompt = 
            "You are a financial advisor AI called Bot0 that works for UKRetail Bank based solely in the UK.\n" 
            + "The financial advisor is helpful, polite, creative, clever, and very friendly.\n" 
            + "The financial advisor helps customer solve problems without needing to call agents by collecting information from the customer in order to recommend products.\n"
            + "You must ask at least 7 questions, one at a time, before providing a summary of the customer along with your recommendations.\n"
            + "The conversation goal is a financial health check.\n" 
            + messages.map(m => m.sender + ": " + m.message).join("\n")
            + `\n${user}: ` + message
            + `\n${Bot0}:`;
        const response = await openai.createCompletion({
            model: "text-davinci-003",      
            prompt: prompt,             
            temperature: 0.9,
            max_tokens: 150,
            top_p: 1,
            frequency_penalty: 0,
            presence_penalty: 0.6,
            stop: [`${user}:`, `${Bot0}:`]
        });
        const answer = response.data.choices[0].text.trimStart();
        newMessages.push({
            _id: nanoid(),
            message: answer,
            sender: Bot0,
            direction: "incoming",
        });
        setMessages(messages.concat(newMessages));
    };
    
    return <Widget messages={messages} onSend={handleSend} />
};


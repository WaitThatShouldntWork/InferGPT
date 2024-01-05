import { createBot } from "botui"
import React, { useEffect } from "react"
import { createRoot } from "react-dom/client"
import { BotUI, BotUIAction, BotUIMessageList } from "@botui/react"

import "@botui/react/dist/styles/default.theme.scss"

const mybot = createBot()

const App = () => {
  useEffect(() => {
    mybot.message
      .add({ text: "Hello" })
      .then(() => mybot.wait({ waitTime: 1000 }))
      .then(() => mybot.message.add({ text: "how are you?" }))
      .then(() => mybot.wait({ waitTime: 500 }))
      .then(() =>
        mybot.action.set(
          {
            options: [
              { label: "Good", value: "good" },
              { label: "Great", value: "great" },
            ],
          },
          { actionType: "selectButtons" }
        )
      )
      .then((data) => mybot.wait({ waitTime: 500 }, data))
      .then((data) =>
        mybot.message.add({ text: `You are feeling ${data?.selected?.label}!` })
      )
      .then(() => mybot.message.add({ text: "say something?" }))
      .then(() => mybot.action.set({ placeholder: "text" }, { input: "text" }))
      .then((data) => mybot.message.add({ text: `you said: ${data?.value}` }))
  }, []);

  return (
    <div>
      <BotUI bot={mybot}>
        <BotUIMessageList />
        <BotUIAction />
      </BotUI>
    </div>
  )
}

const containerElement = document.getElementById("botui")
if (containerElement) {
  const root = createRoot(containerElement)
  root.render(<App />)
}

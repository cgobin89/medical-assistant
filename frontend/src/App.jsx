import { useState } from "react"

function App() {
  const [question, setQuestion] = useState("")
  const [answer, setAnswer] = useState("")
  const [loading, setLoading] = useState(false)

  async function askQuestion() {
    if (!question.trim()) {
      return
    }

    setLoading(true)
    setAnswer("")

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/ask?question=${encodeURIComponent(question)}`
      )

      const data = await response.json()

      setAnswer(data.answer)
    } catch (error) {
      setAnswer("Unable to connect to the medical assistant.")
    }

    setLoading(false)
  }

  return (
    <div>
      <h1>Local Medical Assistant</h1>
      <p>Ask a question below.</p>

      <input
        type="text"
        placeholder="Type your question..."
        value={question}
        onChange={(event) => setQuestion(event.target.value)}
      />

      <button onClick={askQuestion}>
        Ask
      </button>

      {loading && <p>Thinking...</p>}

      {answer && (
        <div>
          <h2>Answer</h2>
          <p>{answer}</p>
        </div>
      )}
    </div>
  )
}

export default App
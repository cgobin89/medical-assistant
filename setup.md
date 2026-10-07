# Setup Guide

This guide documents how to set up the Local Medical Assistant
from a fresh Windows installation.

## Prerequisites
Install the following if you do not already have--- then proceed to Step 4
- Visual Studio Code
- Python 3.11 or later
- Ollama

## 1. Install Visual Studio Code

Download and install Visual Studio Code:

https://code.visualstudio.com/

During installation, enable:

- Add "Open with Code" to the Windows Explorer file context menu
- Add "Open with Code" to the Windows Explorer directory context menu
- Add to PATH

## 2. Install Python

Download Python 3.11.9 from:

https://www.python.org/downloads/release/python-3119/

Scroll down to Files and select Windows installer (64-bit) 25MB

During installation, make sure to check:

- Add python.exe to PATH

## 3. Install Ollama

Download and install Ollama for Windows:

https://ollama.com/download/windows

### IMPORTANT: Windows vs Mac terminal use
Windows: Use the VS Code PowerShell terminal. 

macOS: Use the VS Code integrated terminal (typically zsh). 

The commands in this guide may differ slightly between Windows PowerShell and macOS/Linux. Follow the operating-system-specific commands where provided.

## 4. Open VS Code and verify Python and Ollama Versions

Open a new VS Code terminal and verify Python:

```powershell
python --version
```
Expected output: Python 3.11x

Verify Ollama: 
```powershell
ollama --version
```
Expected output: ollama version is 0.35.0

## 5. Download Phi-3 Mini
```powershell
ollama pull phi3
```
## 6. Run Phi-3 Mini
```powershell
ollama run phi3
```
To exit Phi-3 and return to powershell, type /bye

To check multiple versions of python that may already be on your computer and see the default version: 

```powershell
py -0p
```
## 7. Create the environment

To check your terminal:
```powershell
pwd
```

Set 3.11 as deafult python version for this project

```powershell
py -3.11 -m venv .venv
```

You should see .venv appear in the VS Code Explorer on the left

## 8. Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

Will receive a Windows Powershell security setting- the virtual environment was created but PowerShell is refusing to run activation script. To solve, enable temporary powershell permission for the current terminal session only as follows. Scope Process means the change applies only to this PowerShell session.

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python --version
```

Next, make VS Code use this Python environment for the project:
1. Open the Command Palette with Ctrl+Shift+P
2. Type Python: Select Interpreter
3. Choose the option for this project, such as ".venv" or the path to .venv\Scripts\python.exe

If the environment does not appear, Ctrl+Shift+X, install Python extension from Microsoft. 
1. Ctrl+Shift+P 
2. Developer: Reload Window
3. Ctrl + Shift + P
4. Python: Select Interpreter
5. Choose option with .venv\Scripts\python.exe

This ensures VS Code uses the project virtual environment instead of the system Python installation.

## 9. Test Python
In the VS Code Explorer:
- In medical-assistant folder:
    - Select New File.
    - Name it: test_python.py

Within the file, input the following and save: 
```
print("Python is working!")
```
Click 'run' in the top right.

Expected output: Python is working!

This establishes the first known good component.
VS Code --> .venv --> Python 3.11.9 --> your Python program --> "Python is working!"

## 10. Install Ollama Python package
Make sure your terminal still starts with: (.venv)

```powershell
pip install ollama
```

This installs the Python library that lets a Python program communicate with your locally running Ollama server to control it.
Think of Ollama as a car:
- Ollama application = the car
- Phi-3 = the engine
- Python ollama package = the steering wheel/control interface your Python program uses

Verify the installation and make sure the location includes .venv

```powershell
pip show ollama
```

## 11. Get Python to talk to Phi-3
Create new file: ask_phi3.py

In the file, input the following and save:
```
from ollama import chat

response = chat(
    model="phi3",
    messages=[
        {
            "role": "user",
            "content": "In one sentence, what is RAG in AI?",
        }
    ],
)

print(response["message"]["content"])
```
From your (.venv) terminal, run:

```powershell
python ask_phi3.py
```

Expected result: Phi-3 returns an answer.

The generated response signifies important milestone: you are no longer just chatting with Phi-3 through Ollama—this confirms that Python can communicate with the locally running Phi-3 model through Ollama and Python is controlling the model.

## 12. Adjust the script to enable user to type questions
Open ask_phi3.py and replace its contents with the following and save:
```
from ollama import chat

print("Medical Assistant - Phi-3")
print("Type 'quit' to exit.\n")

while True:
    question = input("You: ")

    if question.lower() == "quit":
        break

    response = chat(
        model="phi3",
        messages=[
            {
                "role": "user",
                "content": question,
            }
        ],
    )

    print(f"Phi-3: {response['message']['content']}\n")
```
In your (.venv) terminal:

```powershell
python ask_phi3.py
```

Within the terminal, you can now type a question

Type: What is the purpose of RAG?

Expected Result: Let's you type a question and generates a response

Milestone:
                 YOUR COMPUTER
                      │
                 ask_phi3.py
                      │
                      ▼
                   Ollama
                      │
                      ▼
                  Phi-3 Mini
                      │
                      ▼
                    Answer

- What happened: Demonstrated that Python app successfully sends the question to Phi-3 and gets a generated response back.

- Challenge: Phi-3 has now given us a very confident hallucination:

▼ Question
 
▼ Phi-3 Mini
      
▼ Answer based on its learned parameters
      
❌ Incorrect definition of RAG

- Explanation: We haven't given Phi-3 any external information. That's going to change as we build the project according to the following.

▼ Question
   
▼ Retriever
   
▼ Relevant information
   
▼ Phi-3 Mini
   
▼ Grounded answer

## 13. Add Prompting
Within the file: ask_phi3.py, replace the previous section:

messages=[
    {
        "role": "user",
        "content": question,
    }
]

with the following and save. This will allow you to add prompting.
```
messages=[
    {
        "role": "system",
        "content": (
            "You are a helpful assistant. "
            "Answer questions accurately and concisely. "
            "If you are uncertain about an answer, say that you are uncertain "
            "rather than inventing information."
        ),
    },
    {
        "role": "user",
        "content": question,
    },
]
```
To exit the chat, type quit

## 14. Ensure project is safely tracked since planning to push to Github
This is important because we do not want to upload .venv or other local/generated files to GitHub.

- In VS Code:

    - Right-click the medical-assistant folder.
    - Select New File.
    - Name it exactly: .gitignore

- Add to file:
```
# Python virtual environment
.venv/

# Python cache files
__pycache__/
*.py[cod]

# Environment variables and secrets
.env

# IDE settings
.vscode/

# Local model/data files
models/
data/
```
- What this does: Your .venv contains your local Python installation and packages. We don't want to put all of that on GitHub.

The others prepare us for later:
    __pycache__/ → temporary Python files
    .env → potentially sensitive configuration/secrets
    .vscode/ → your personal VS Code settings
    models/ → potentially large model files
    data/ → datasets/documents that we may not want in the repository

## 15. Initialize Git

```powershell
git --version
git init
git status
```

Expected outcome: Git should show the files but not show .venv/

This verifies that gitignore is correctly working.

## 16. Make your first commit (saved checkpoint for the project).
Currently, we have the following working:
✓ Python 3.11.9 
✓ Virtual environment
✓ Ollama 
✓ Phi-3
✓ Python → Ollama connection
✓ Interactive chatbot
✓ Experiment documentation
✓ .gitignore
✓ Git repository

1. Tell Git to track the project files
```powershell
git add .
```

There may be no output. That's normal.

2. Check what will be committed

```powershell
git status
```

You should now see your files under something like:
Changes to be committed:
You should not see .venv.

3. Create the checkpoint

```powershell
git commit -m "Set up local Phi-3 development environment"
```
You should get a message indicating that files were committed.

**NOTE THIS ESTABLISHES AN INITIAL FOUNDATION FOR THE CHAT ASSISTANT**

## NEXT PHASE: CONNECT THIS FOUNDATION TO A WEBSITE INTERFACE

To accomplish this, we will set up the frontend with REACT to communicate with the Python backend.

## 17. Install NVM for Windows or MAC Users
NVM (Node Version Manager) allows you to install and manage different versions of Node.js on your computer.

Our project uses Node.js 22 for the React frontend.

**WINDOWS USERS**: Install NVM.

Use the link below, scroll down to Assets, download the Windows installer (amd64-setup.exe) for a standard 64-bit Intel or AMD computer.

https://github.com/nvm-windows/nvm/releases/tag/v2.0.1-hotfix.2

- During installation:

  - Accept the license agreement.
  - Use the default installation locations.
  - When asked about the Node.js symlink, use the default option.
  - Leave the default security/TLS options enabled.
  - Author software notifications are optional.

- After installation, close and reopen VS Code.

**MAC USERS**: Install NVM

https://github.com/nvm-sh/nvm

Follow the installation instructions provided by the project. After installation, restart your terminal.

## 18. Install Node.js 22

Open a new VS Code terminal and verify NVM:

```
nvm version
```

Expected Output: NVM version number.

Install Node.js 22:

```
nvm install 22
```

Activate Node.js 22:

```
nvm use 22
```

Verify Node.js and npm:

```
node --version
npm --version
```

You should see Node.js version 22.x.x and an npm version.

## 19. Create React Frontend

The project uses React for the website interface. Vite is used to create and run the React development environment.

- From the `medical-assistant` project folder, run:

```
npm create vite@latest frontend
```

npm may display:

Need to install the following packages: create-vite@... Ok to proceed? (y)


Type `y` and press Enter.

- Choose the following:

    - Framework: React
    - Variant: JavaScript
    - Linter: ESLint
    - Install with npm and start now
    
Vite will install the React dependencies and then start the development server. The development server will provide a local address, typically:

http://localhost:5173/

- Open that address in your browser to view the React application.

### Milestone

The default Vite/React "Get Started" page should appear in the browser.

This confirms:

**Computer → Node.js → Vite → React → Browser**

## 20. Turn the Generic Vite page into the Medical Assistant page

To bring the terminal prompt back, stop the Vite server by typing:

```
Ctrl+C
```

- Within your medical assistant folder, open:

frontend/src/App.jsx

- Delete the existing contents of App.jsx and replace them with the following:

```
import { useState } from "react"

function App() {
  const [question, setQuestion] = useState("")

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

      <button onClick={() => alert(question)}>
        Ask
      </button>
    </div>
  )
}

export default App
```

- Save the file.
- Restart the React development server:

```
cd frontend
npm run dev
```

- Open the local address provided by Vite.
    - The browser should now display: Local Medical Assistant with a question input and an Ask button.
- Type a question into the input box and click Ask
    - A browser alert should display the question you entered.

## Milestone

This confirms that React can capture and use information entered by the user.

The current flow is:

Browser → React → User question

The alert() is only a temporary test. It will eventually be replaced with a request to the Python backend.

## 21. Create the Python backend

- Stop the React development server:

```
Ctrl+C
```

- From the medical-assistant project folder, create the backend directory:

**MAKE SURE YOU ARE NOT IN THE FRONTEND FOLDER.**

```
pwd
```

If it shows you are in frontend, go back one level to be in the medical assistant folder by running:

```
cd ..
```

Now you should be in:

...\medical-assistant

- Create the backend directory:

```
mkdir backend
```

**Make sure you're in the Python virtual environment- noted by the (.venv) in your terminal.** 

If you do not see it, Activate the Python virtual environment:

```
.\.venv\Scripts\Activate.ps1
```

- Install FastAPI and Uvicorn:

```
pip install fastapi uvicorn
```

- Verify FastAPI:

```
pip show fastapi
```

Expected output: name, version, and location.

### Create main.py

- In VS Code's Explorer, find:

medical-assistant/
└── backend/

- Right-click backend → New File.
- Name it: main.py
- Put the following in main.py and save it:

```
from fastapi import FastAPI
from ollama import chat

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Medical Assistant backend is running"}


@app.get("/ask")
def ask(question: str):
    response = chat(
        model="phi3",
        messages=[
            {
                "role": "user",
                "content": question,
            }
        ],
    )

    return {
        "question": question,
        "answer": response["message"]["content"],
    }
```

**WHAT THIS DOES:** This creates your first Python web server.

### Start the backend

**Make sure your terminal is in the medical-assistant folder and (.venv) is active.**

Run:

```
uvicorn backend.main:app --reload
```

Expected output (similar to): Uvicorn running on http://127.0.0.1:8000

**Keep this terminal running while using the backend.**

### Test the FastAPI server

- Open the following address in a web browser:

http://127.0.0.1:8000

The browser should display: {"message":"Medical Assistant backend is running"}

This confirms that the Python FastAPI backend is running.

### Test the FastAPI → Ollama → Phi-3 connection

- With the FastAPI server still running, open:

http://127.0.0.1:8000/ask?question=What%20is%20RAG%3F

The browser should return a response similar to:

{
    "question": "What is RAG?",
    "answer": "..."
}

The exact answer will vary because it is generated by the local Phi-3 model.

## Milestone

Your Python backend is running independently from your React frontend.

The project now has the following working connection:

Browser → FastAPI → Python → Ollama → Phi-3 → FastAPI → Browser

## 22. Connect React website to the Python Backend

- Keep FastAPI running

Make sure your backend terminal is running. If not,:

```
uvicorn backend.main:app --reload
```

Don't close this terminal. You'll want the FastAPI server running while we test the website.

- Open a second terminal

In VS Code: Terminal → New Terminal

You should now have a second terminal. The first one is running FastAPI. The second one is where we'll run React.

- In the second terminal, go to the frontend:

```
cd frontend
```

- Then run:

```
npm run dev
```

- Open in browser:

http://localhost:5173/

You should see your Local Medical Assistant page.

### Change App.jsx

- In the medical-assistant folder, open: frontend/src/App.jsx
- Replace the entire file with the following:

```
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
```

- Save it.

**Before testing it, you need to enable React Frontend to Communicate with FastAPI**

Because the React frontend and FastAPI backend run on different local ports, FastAPI needs to allow requests from the React development server.

- In medical assistant folder, open backend/main.py and replace with the following:

```
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ollama import chat

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Medical Assistant backend is running"}


@app.get("/ask")
def ask(question: str):
    response = chat(
        model="phi3",
        messages=[
            {
                "role": "user",
                "content": question,
            }
        ],
    )

    return {
        "question": question,
        "answer": response["message"]["content"],
    }
```

### Test the website

http://localhost:5173/

- Type: What is RAG? 
- Click Ask.

Expected Output: Phi-3's response

## EXPLANATION OF WHAT WE JUST DID:

- In `frontend/src/App.jsx`, the React application sends the user's question to the FastAPI backend using `fetch()`.

    - The request is sent to:

        http://127.0.0.1:8000/ask

- The question is passed as a URL parameter.
- FastAPI sends the question to Ollama, which generates an answer using Phi-3.
- The answer is then returned to React and displayed on the webpage.

### Milestone

The complete local AI pipeline is now working:

**React → FastAPI → Ollama → Phi-3 → FastAPI → React**

A user can enter a question on the website and receive an answer generated by the locally running Phi-3 model.

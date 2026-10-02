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

    In medical-assistant folder.
    Select New File.
    Name it: test_python.py

Type within file: print("Python is working!")
Save and run it: Should output the same text

This establishes the first known good component
VS Code
   ↓
.venv
   ↓
Python 3.11.9
   ↓
your Python program
  ↓
"Python is working!"

## 10. Install Ollama Python package
Make sure your terminal still starts with: (.venv)

```powershell
pip install ollama
```

This installs the Python library that lets a Python program communicate with your locally running Ollama server to control it.
Think of Ollama as a car:

    Ollama application = the car
    Phi-3 = the engine
    Python ollama package = the steering wheel/control interface your Python program uses

Verify the installation and make sure the location includes .venv

```powershell
pip show ollama
```

## 11. Get Python to talk to Phi-3
Create new file: ask_phi3.py
Input the following and save:

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

From your (.venv) terminal, run:

```powershell
python ask_phi3.py
```

Expected result: Phi-3 returns an answer.
The generated response signifies important milestone: you are no longer just chatting with Phi-3 through Ollama—this confirms that Python can communicate with the locally running Phi-3 model through Ollama and Python is controlling the model.

## 12. Adjust the script to enable user to type questions
Open ask_phi3.py and replace its contents with the following and save:

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

In your (.venv) terminal:

```powershell
python ask_phi3.py
```

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

What happened: Demonstrated that Python app successfully sends the question to Phi-3 and gets a generated response back.
Challenge: Phi-3 has now given us a very confident hallucination:

Question
   ↓
Phi-3 Mini
   ↓
Answer based on its learned parameters
   ↓
❌ Incorrect definition of RAG
We haven't given Phi-3 any external information.

That's going to change as we build the project.

Question
   ↓
Retriever
   ↓
Relevant information
   ↓
Phi-3 Mini
   ↓
Grounded answer

## 13. Add Prompting
Within ask_phi3.py, replace the previous section:

messages=[
    {
        "role": "user",
        "content": question,
    }
]

with the following to add prompting and save

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

To exit the chat, type quit

## 14. Ensure project is safely tracked since planning to push to Github
This is important because we do not want to upload .venv or other local/generated files to GitHub.

In VS Code:

    Right-click the medical-assistant folder.

    Select New File.

    Name it exactly: .gitignore

Add to file:

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

What this does:
Your .venv contains your local Python installation and packages. We don't want to put all of that on GitHub.

The others prepare us for later:

    __pycache__/ → temporary Python files

    .env → potentially sensitive configuration/secrets

    .vscode/ → your personal VS Code settings

    models/ → potentially large model files

    data/ → datasets/documents that we may not want in the repository

## 15. Initialize Git
git --version
git init
git status

Expected outcome: Git should show the files but not show .venv/
This verifies that gitignore is correctly working

Make your first commit (saved checkpoint for the project).
Currently, we have the following working:
Python 3.11.9 ✓
Virtual environment ✓
Ollama ✓
Phi-3 ✓
Python → Ollama connection ✓
Interactive chatbot ✓
Experiment documentation ✓
.gitignore ✓
Git repository ✓

1. Tell Git to track the project files

Run:

git add .

There may be no output. That's normal.
2. Check what will be committed

Run:

git status

You should now see your files under something like:

Changes to be committed:

You should not see .venv.
3. Create the checkpoint

Run:

git commit -m "Set up local Phi-3 development environment"

You should get a message indicating that files were committed.
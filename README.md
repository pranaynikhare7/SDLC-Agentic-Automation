# 🛡️ AI SDLC Automation System

Welcome to the AI Software Development Life Cycle (SDLC) Automation System!

This project acts like your own personal AI software engineering team. It uses Large Language Models (LLMs) and LangGraph to automate the entire software creation process. From a simple text prompt, this system will guide you step-by-step through generating requirements, writing code, checking for security flaws, and creating test cases.

Because it uses a "Human-in-the-Loop" workflow, it pauses at every major step to let you review, approve, or ask for revisions before moving forward!

---

## ✨ Features

* 📝 **Requirement Gathering:** Converts plain text ideas into structured Agile User Stories.
* 🏗️ **Architecture Design:** Generates comprehensive Functional and Technical Design Documents (FDD & TDD).
* 💻 **Code Generation:** Writes modular, multi-file Python code based on the approved designs.
* 🔒 **Security Review:** Scans the generated code for vulnerabilities and applies fixes.
* 🧪 **Test Engineering:** Writes a complete unittest suite for the generated code.
* 🧐 **QA Simulation:** Simulates running the tests to ensure the code actually works.
* 📦 **Download Artifacts:** Packages all generated code, tests, and documentation into a neat `.zip` file for you to download.

---

## 🚀 Getting Started

Follow these simple steps to run the application on your local machine.

### 1. Prerequisites

You will need to have Python 3.9+ installed. You will also need API keys for:

* OpenAI: For the AI model (GPT-4o-mini).
* Upstash Redis: A free cloud Redis database to save your session state so you don't lose progress during reviews. You can get a free database at Upstash.

---

### 2. Clone the Repository

Download the code to your local machine:

```bash
git clone https://github.com/pranaynikhare7/SDLC-Agentic-Automation.git
```

---

### 3. Set Up Your Environment Variables

The application needs your API keys to work. Create a new file in the root folder of the project and name it exactly `.env`.

Paste the following into your `.env` file and replace the placeholders with your actual keys:

```env
# Your OpenAI API Key
OPENAI_API_KEY=sk-your_openai_api_key_here

# Your Upstash Redis Credentials (find these in your Upstash Dashboard)
UPSTASH_REDIS_REST_URL=[https://your-upstash-url.upstash.io](https://your-upstash-url.upstash.io)
UPSTASH_REDIS_REST_TOKEN=your_upstash_token_here
```

---

### 4. Install Dependencies

It is highly recommended to use a virtual environment. Install the required Python packages by running:

```bash
pip install -r requirements.txt
```

> (Note: If you don't have a requirements.txt yet, make sure you have installed: streamlit, langchain, langchain-openai, langgraph, upstash-redis, pydantic, and python-dotenv).

---

### 5. Run the Application!

Because this is a Streamlit web application, you start it using the streamlit run command. In your terminal, type:

```bash
streamlit run app.py
```

A browser window should automatically open to **[http://localhost:8501](http://localhost:8501)** displaying the AI SDLC Designer interface!

---

## 💡 How to Use the App

* **Start a Project:** Enter a project name and click "Initialize Workflow".
* **Add Requirements:** Type out what you want your software to do in plain English.
* **Review & Approve:** The AI will generate User Stories. You can either click ✅ Approve to move to the next phase, or 🔄 Revise to give the AI feedback to fix mistakes.
* **Iterate:** Continue this process through Design, Code, Security, and Testing.
* **Download:** Once the QA phase passes, click the download buttons to get your ZIP file containing all the generated Python files and Markdown documentation.

---

## 📁 Project Structure Overview

* `app.py`: The main entry point that launches the Streamlit app.
* `src/sdlc_system/ui/streamlit_main.py`: Contains the frontend visual interface and layout.
* `src/sdlc_system/graph/`: Contains the LangGraph setup that controls the flow from one AI step to the next.
* `src/sdlc_system/nodes/`: The individual "brains" of the operation. Each file (e.g., coding_node.py, security_node.py) handles a specific phase of the software lifecycle.
* `src/sdlc_system/cache/`: Connects to Redis to ensure your progress is saved securely.


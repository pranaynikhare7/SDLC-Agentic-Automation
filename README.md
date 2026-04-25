# 🛡️ AI SDLC Automation System

An AI-driven Multi-Agent Orchestrator designed for rapid POC development, streamlining the end-to-end SDLC to deliver functional software prototypes at generative speeds.

![LangGraph](https://img.shields.io/badge/LangGraph-Orchestration-blue)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-green)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red)

## Table of Contents

- [Abstract](#abstract)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Abstract

### Background
In a fast-paced Generative AI landscape, the ability to prototype rapidly is a competitive necessity. Traditional software development cycles often become bottlenecks for Proof of Concept (POC) initiatives, where the manual translation of requirements into design, code, and test cases slows the turnaround time required to present value to stakeholders.

### Motivation
While modern LLMs can generate code snippets, they often lack the systemic context and rigorous structure needed to deliver a cohesive, working demo. This project aims to bridge that gap by providing a stateful, multi-agent framework that accelerates the "idea-to-working-prototype" pipeline. By maintaining a Human-in-the-Loop (HITL) approach, we ensure that rapid automation is balanced with human oversight to meet specific stakeholder expectations.

### Proposed Solution
This system utilizes **LangGraph** to orchestrate a high-efficiency cyclical workflow where specialized agents (Business Analyst, Architect, Developer, Security, and QA) manage the SDLC in parallel. To accommodate the dynamic nature of POC development, **Redis** handles session persistence, allowing users to pause, iterate based on real-time stakeholder feedback, and resume sessions without losing progress.

### Expected Outcomes
✅ Rapid POC Turnaround: Drastically reduce the time between initial requirement gathering and a functional, demonstrable prototype.  
✅ Stakeholder-Ready Artifacts: Instant generation of User Stories, FDD, and TDD to provide immediate technical clarity to project owners.  
✅ Validated MVP Codebase: Modular Python implementations reinforced by automated security scans and unit test generation.  
✅ Interactive Refinement Loop: A specialized Streamlit UI designed for real-time review, enabling developers to pivot and refactor code instantly based on QA or stakeholder input.

## Key Features

- **Multi-Agent Orchestration** - Specialized agents for requirements, architecture, coding, security, and testing.
- **Human-in-the-Loop (HITL)** - Persistent pause points at every stage for human approval or revision.
- **Stateful Persistence** - Redis-backed session management allowing developers to resume tasks using a Task ID.
- **Security-First Coding** - Dedicated security agent to scan for vulnerabilities before test generation.
- **Automated QA Simulation** - Simulates code execution and test pass/fail scenarios before artifact delivery.
- **Artifact Packaging** - One-click download of all documentation and source code.

## Architecture

```text
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                 STREAMLIT UI LAYER                                  │
│        (State Visualization, Markdown Rendering, & Human Feedback Intake)           │
└──────────────────────────────────────────┬──────────────────────────────────────────┘
                                           │ User Input / Review Action
                                           ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                         LANGGRAPH & REDIS STATE MANAGER                             │
│    (GraphExecutor: Thread Management, State Checkpointing, & Persistence)           │
│    ┌────────────────────────┐                        ┌────────────────────────┐     │
│    │   Graph Orchestration  │◄──────────────────────►│  Upstash Redis Cache   │     │
│    │    (Logic Control)     │        Sync State      │   (Session Storage)    │     │
│    └──────────┬─────────────┘                        └────────────────────────┘     │
└───────────────┼─────────────────────────────────────────────────────────────────────┘
                │ Resume / Execute Node
                ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                            SDLC PROCESS PIPELINE (Nodes)                            │
│                                                                                     │
│        [ AI AGENT TRACK ]                        [ HUMAN APPROVAL TRACK ]           │
│      (Generative AI logic)                        (HITL Interrupt Points)           │
│                │                                             │                      │
│     ┌──────────┴──────────┐     User Stories      ┌──────────┴──────────┐           │
│     │  Business Analyst   ├──────────────────────►│  HITL - PO Review   │           │
│     └──────────▲──────────┘                       └──────────┬──────────┘           │
│                │              [ REVISE ]                     │                      │
│                └─────────────────────────────────────────────┤                      │
│                                                              │ [ APPROVED ]         │
│                ┌─────────────────────────────────────────────┘                      │
│                │                                                                    │
│     ┌──────────▼──────────┐       Design          ┌─────────────────────┐           │
│     │   Architect Agent   ├──────────────────────►│ HITL-Design Review  │           │
│     └──────────▲──────────┘                       └──────────┬──────────┘           │
│                │              [ REVISE ]                     │                      │
│                └─────────────────────────────────────────────┤                      │
│                                                              │ [ APPROVED ]         │
│                ┌─────────────────────────────────────────────┘                      │
│                │                                                                    │
│     ┌──────────▼──────────┐       Code            ┌─────────────────────┐           │
│  ┌─►│   Developer Agent   ├──────────────────────►│  HITL - Code Review │           │
│  │  └─────────────────────┘                       └──────────┬──────────┘           │
│  │                        [ REVISE - BACK TO DEVELOPER ]     │                      │
│  │◄──────────────────────────────────────────────────────────┤                      │
│  │                                                           │ [ APPROVED ]         │
│  │             ┌─────────────────────────────────────────────┘                      │
│  │             │                                                                    │
│  │  ┌──────────▼──────────┐   Recommendation      ┌─────────────────────┐           │
│  │  │   Security Agent    ├──────────────────────►│ HITL Security Review│           │
│  │  └─────────────────────┘                       └──────────┬──────────┘           │
│  │                       [ REVISE - BACK TO DEVELOPER ]      │                      │
│  │◄──────────────────────────────────────────────────────────┤                      │
│  │                                                           │ [ APPROVED ]         │
│  │             ┌─────────────────────────────────────────────┘                      │
│  │             │                                                                    │
│  │  ┌──────────▼──────────┐      Test Cases       ┌─────────────────────┐           │
│  │  │     SDET Agent      ├──────────────────────►│ HITL - Test Review  │           │
│  │  └──────────▲──────────┘                       └──────────┬──────────┘           │
│  │             │              [ REVISE ]                     │                      │
│  │             └─────────────────────────────────────────────┤                      │
│  │                                                           │ [ APPROVED ]         │
│  │             ┌─────────────────────────────────────────────┘                      │
│  │             │                                                                    │
│  │  ┌──────────▼──────────┐       QA Results      ┌─────────────────────┐           │
│  │  │  QA Testing Agent   ├──────────────────────►│  HITL - QA Review   │           │
│  │  └─────────────────────┘                       └──────────┬──────────┘           │
│  │                                                           │                      │
│  │                [ REJECT - BUGS FOUND ]                    │                      │
│  └───────────────────────────────────────────────────────────┤                      │
│                                                              │ [ APPROVED ]         │
│                                                              ▼                      │
│                                                   ┌────────────────────┐            │
│                                                   │ Artifact Compiler  │            │
│                                                   └────────────────────┘            │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

## Tech Stack

| Component          | Technology                                           |
| ------------------ | ---------------------------------------------------- |
| **Orchestration** | LangGraph (Cyclical workflows with persistent state) |
| **LLM** | OpenAI GPT-4o-mini                                   |
| **State Storage** | Upstash Redis (Serverless Persistence)               |
| **Web Framework** | Streamlit (Interactive UI)                           |
| **Schema/Types** | Pydantic (Data validation and state structure)       |
| **Core Libraries** | LangChain, LangChain-OpenAI, Python-Dotenv           |

## Installation

### Prerequisites

- Python 3.9 or higher
- OpenAI API Key
- Upstash Redis URL & Token

### Setup

1. **Clone the repository**
   ```bash
   git clone [https://github.com/pranaynikhare7/SDLC-Agentic-Automation.git](https://github.com/pranaynikhare7/SDLC-Agentic-Automation.git)
   cd SDLC-Agentic-Automation
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=sk-your-key
   UPSTASH_REDIS_REST_URL=[https://your-url.upstash.io](https://your-url.upstash.io)
   UPSTASH_REDIS_REST_TOKEN=your-token
   ```

## Usage

### Launching the System
1. **Start the application**
   ```bash
   streamlit run app.py
   ```
2. **Access the UI**: Navigate to `http://localhost:8501`.

### Interaction Workflow
- **Initialize**: Provide a project name to generate a unique Task ID.
- **Review Phases**: The system will pause for your approval after generating:
    - User Stories
    - Design Documents (Functional & Technical)
    - Source Code & Security Review
    - Test Suite & QA Results
- **Resume**: Use your Task ID in the sidebar to return to an ongoing project.

## Project Structure

```text
SDLC_Agentic_Automation/
├── app.py                   # Main Streamlit Entry Point
├── requirements.txt         # Project Dependencies
├── .env                     # Environment Variables
├── src/
│   └── sdlc_system/
│       ├── cache/           # Redis connection & session logic
│       ├── graph/           # LangGraph definitions & Workflow logic
│       ├── nodes/           # Individual AI Agent logic (Coding, Security, etc.)
│       ├── state/           # Pydantic state definitions (TypedDict)
│       ├── ui/              # Streamlit interface components
│       └── utils/           # Utility Functions
└── artifacts/               # Generated project outputs (MD, Python files)
```

## Troubleshooting

### Redis Connection Error
- Ensure your `UPSTASH_REDIS_REST_URL` includes the `https://` prefix.
- Verify that your token does not have leading/trailing spaces.

### OpenAI Rate Limits
- If using a Trial account, ensure you have not exceeded your monthly quota.
- For high-concurrency needs, check your OpenAI tier status.

---

**Status**: 🚀 Active Development (Master's Specialization Project)  
**Last Updated**: April 2026

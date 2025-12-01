# nivra-financial-agents
Nivra is a multi-agent financial assistant that reads your daily transactions, evaluates risk, and gives you one clear action to improve your money habits. It adjusts instantly to behavior, blocks unsafe earning ideas, and delivers personalized micro-tasks that focus on discipline, growth, or financial stability.



Nivra: The Adaptive Financial Concierge

A Multi-Agent System for Hyper-Personalized, Risk-Aware Financial Coaching

Nivra is a behavior-driven personal finance assistant built using a multi-agent architecture. It does more than show spending data. It evaluates risk, blocks unsafe suggestions, adapts to user habits, and delivers one clear micro-task each day to improve financial stability.

Problem Statement

Most personal finance tools only report transactions. They don’t help users act. People get charts, insights, and long summaries, but no simple next step. They also lack risk safeguards, so advice can be generic, unsafe, or misaligned with a user’s situation.

Nivra solves this by shifting from passive reporting to proactive, controlled, personalized coaching. Each user receives a single high-impact action built around their balance, habits, discipline score, and financial risks.

Why Agents?

A single LLM prompt can’t safely handle financial data, risk detection, personalization, and planning. Each stage needs its own logic.

Nivra uses a layered agent system:

SenseWorker cleans data and builds the financial snapshot.
RiskEvaluator (T1) handles safety. If risk is high, it forces a Survival plan.
Verifier (T2) filters unsafe earning ideas.
SessionMemory (T3) injects behavioral patterns like discipline score.
Planner & Coach generate the final micro-task and guidance.
This separation keeps the system reliable, auditable, and adaptable.

Architecture Overview

Nivra uses a five-stage decision pipeline supported by three control tiers.

Tiers
Tier	Purpose	Agent
T1	Financial safety override	RiskEvaluator
T2	Scam and risk filtering	Verifier
T3	Behavioral personalization	SessionMemory + Planner

Pipeline Flow

Input → SenseWorker → SessionMemory → RiskEvaluator → Verifier → Planner → Coach → Final Output

Each step transforms the state before handing it forward, resulting in a stable, multi-layered decision.

Demo

Below is a sample run of the live system using the Student User persona.

Input

Persona: STUDENT
SMS: 20
Manual Category: Food
Manual Amount: 10
OCR: 50

System Logs

SenseWorker → balance: 149000, confidence: 0.9
Verifier → 11 earning ideas approved
Orchestrator → Final priority: DISCIPLINE

Final Output

Plan Priority: DISCIPLINE
Spend Limit: $298 today

Micro-Task:
Find two low-cost alternatives for dining this week. Swap one eating-out meal with a homemade option.

Earning Suggestion:
Local delivery routes.

Coaching:
Maintain a 50/50 rule for dining. Prep meals on Sunday. Allocate a fixed weekly dining budget.
Keep your discipline streak going. Every small win compounds.

Tech Stack

Python 3.11
Gemini API (Planner Agent)
Pydantic for strict data schemas
Firestore for long-term memory
Custom agent classes for reasoning, validation, and orchestration

Key Implementation Notes

Risk logic is deterministic, not LLM-driven. This keeps survival checks reliable.
Planner outputs strict JSON, increasing compliance and lowering hallucination risk.
User personas help validate adaptability across different financial patterns and behaviors.

If I Had More Time

I would extend Nivra in three areas:

1. External API connections to allow automatic execution of micro-tasks (bank transfers, reminders, etc.).
2. A Critique Agent to learn from weekly behavior and adjust the discipline score.
3. A lightweight UI showing T1/T2/T3 checks, daily micro-task, and progress.

Setup & Run

1. Clone the repo
2. Install dependencies
3. Run the main agent interface:
python project/main_agent.py
4. Select a persona and enter today’s financial data.


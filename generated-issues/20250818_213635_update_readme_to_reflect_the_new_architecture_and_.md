# Loom: The Universal Development Agent Platform

Loom is a multi-agent system that transforms feature requests into comprehensive coding prompts through LLM-driven sequential analysis. It's designed for developers who want to automate the software development lifecycle while retaining complete control over the AI models used at every stage.

The core philosophy is **"Meet Developers Where They Are"**. Loom is model-agnostic, allowing you to use any AI model or tool at any step of the process, from research to implementation.

## 🎯 What It Does

Loom orchestrates a sequence of specialized AI agents to perform a series of tasks, starting with a simple feature request.

**Example Workflow:**
1.  **You provide a task**: `python loom.py "implement real-time tournament bracket tracking"`
2.  **Project Analysis Agent**: Scans your codebase to understand existing patterns, tech stack, and conventions.
3.  **Feature Research Agent**: Uses the project context to research the best technical approaches and implementation strategies for the feature.
4.  **Prompt Assembly Agent**: Synthesizes all the gathered information into a detailed, context-aware coding prompt, ready for an implementation LLM.

The final output is a high-quality, actionable prompt that you can feed into your coding LLM of choice to get consistent and contextually-aware code.

## 🚀 Quick Start

### 1. Installation
# Sentiment Analysis Agent with Evaluations

## Purpose

A demonstration of pydantic-ai agent evaluation using pydantic-evals. This snippet shows how to evaluate AI agent outputs using both deterministic checks and LLM-as-judge patterns. The example implements a simple sentiment analysis agent and validates its responses using the built-in `EqualsExpected` evaluator and an `LLMJudge` evaluator. This is useful for understanding agent evaluation workflows, testing AI system quality, and implementing evaluation-driven development for LLM applications.

## Key Technologies

- **[pydantic-ai](https://ai.pydantic.dev/)** - Type-safe agent framework with OpenAI-compatible endpoint support
- **[pydantic-evals](https://ai.pydantic.dev/evals/)** - Evaluation framework for testing AI agents and LLM outputs
- **OpenAI-compatible endpoints** - Local LLM server integration for cost-effective development
- **Python 3.13+** - Modern Python with type hints and async support

## Key Features

- Built-in evaluators: `EqualsExpected` for fast deterministic checks
- LLM as judge pattern for quality assessment
- Custom OpenAI endpoint configuration for local models
- Dataset-driven evaluation with multiple test cases
- Synchronous evaluation workflow for simple scenarios

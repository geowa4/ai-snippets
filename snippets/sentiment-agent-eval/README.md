# Sentiment Analysis Agent with Evaluations

This project demonstrates how to evaluate AI agents using **pydantic-ai** and **pydantic-evals**. It implements a simple sentiment analysis agent and tests its performance using both deterministic evaluators and LLM-as-judge patterns.

## Overview

The snippet showcases:

- **Agent Creation**: A pydantic-ai agent configured to analyze text sentiment
- **Custom Endpoints**: Using local LLM servers via OpenAI-compatible APIs
- **Evaluation Dataset**: A collection of test cases with expected outputs
- **Built-in Evaluators**: The `EqualsExpected` evaluator for fast deterministic checks
- **LLM as Judge**: The `LLMJudge` evaluator for quality assessment using another LLM

## Prerequisites

You need a local LLM server running on `http://127.0.0.1:1234` that supports OpenAI-compatible API endpoints. The example uses:

- **ibm/granite-4-h-tiny** - For both the sentiment analysis agent and the LLM judge evaluator

### Setting Up a Local LLM Server

You can use tools like:

- **LM Studio**: Desktop application with OpenAI-compatible server
- **Ollama with OpenAI compatibility**: Run `ollama serve` and use OpenAI adapter
- **llama.cpp server**: Built-in OpenAI-compatible API server
- **vLLM**: High-performance inference server

Example with LM Studio:
1. Download and install LM Studio
2. Download the required model (ibm/granite-4-h-tiny)
3. Start the local server (default port: 1234)
4. Ensure the server is accessible at `http://127.0.0.1:1234/v1`

## Installation

```bash
# Navigate to this snippet directory
cd snippets/sentiment-agent-eval

# Install dependencies
uv sync
```

## Running the Evaluation

```bash
# Run the evaluation
uv run main.py
```

## How It Works

### 1. Agent Configuration

The agent is configured with custom instructions to perform sentiment analysis:

```python
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

sentiment_model = OpenAIChatModel(
    "ibm/granite-4-h-tiny",
    provider=OpenAIProvider(
        base_url="http://127.0.0.1:1234/v1",
        api_key="not-needed",
    ),
)

agent = Agent(
    sentiment_model,
    instructions=(
        "Analyze the sentiment of the given text. "
        "Respond with exactly one word: 'positive', 'negative', or 'neutral'."
    ),
)
```

### 2. Evaluation Dataset

The dataset contains 5 test cases covering positive, negative, and neutral sentiments:

- Complex positive sentiment
- Complex negative sentiment
- Neutral sentiment
- Simple positive sentiment
- Simple negative sentiment

### 3. Evaluators

Two evaluators validate the agent's outputs:

**EqualsExpected Evaluator** (Fast, Deterministic)
- Checks if the output exactly matches the expected output for each test case
- Compares agent's response against the `expected_output` field
- Provides quick pass/fail validation

**LLMJudge Evaluator** (Slower, Quality-focused)
- Uses the same LLM (ibm/granite-4-h-tiny) to judge quality
- Evaluates whether the sentiment analysis is accurate
- Compares agent output against expected output
- Returns assertion (pass/fail) with reasoning

### 4. Evaluation Execution

The evaluation:
1. Runs the agent on each test case
2. Applies all evaluators to each output
3. Collects results and generates a report
4. Prints a summary with pass/fail status and metrics

## Expected Output

```
Running sentiment analysis evaluations...

Case: positive_sentiment
  Status: PASS
  Output: positive
  Duration: 1.23s
  Evaluations:
    - EqualsExpected: PASS
    - accurate_sentiment: PASS (LLM Judge: "The analysis correctly identifies...")

Case: negative_sentiment
  Status: PASS
  Output: negative
  Duration: 1.15s
  ...

Overall: 5/5 cases passed (100%)
```

## Key Concepts

### Deterministic vs. LLM Evaluators

- **Deterministic evaluators** (like `EqualsExpected`, `Contains`) are fast and consistent but limited in scope
- **LLM evaluators** (like `LLMJudge`) can assess nuanced qualities but are slower and non-deterministic
- Best practice: Use both types together for comprehensive validation

### LLM as Judge Pattern

The LLM-as-judge pattern uses a language model to evaluate outputs based on a rubric. Benefits:

- Can assess subjective qualities (helpfulness, tone, accuracy)
- More flexible than rigid rules
- Can provide reasoning for decisions

Considerations:
- Introduces non-determinism
- Adds API cost and latency
- Inherits biases from the judge model

### Evaluation-Driven Development

Using evals during development:
1. Define expected behaviors as test cases
2. Implement agent logic
3. Run evaluations to measure performance
4. Iterate based on results
5. Track improvements over time

## Technologies

- **pydantic-ai 1.22.0**: Agent framework with type safety and structured outputs
- **pydantic-evals 1.22.0**: Evaluation framework for AI systems
- **OpenAI SDK**: For custom endpoint compatibility
- **Python 3.13+**: Modern Python with enhanced type system

## Development

```bash
# Run linter
uv run ruff check

# Run type checker
uv run mypy main.py

# Format code
uv run ruff format
```

## Further Reading

- [Pydantic AI Documentation](https://ai.pydantic.dev/)
- [Pydantic Evals Documentation](https://ai.pydantic.dev/evals/)
- [LLM as Judge Guide](https://ai.pydantic.dev/evals/evaluators/llm-judge/)
- [Built-in Evaluators](https://ai.pydantic.dev/evals/evaluators/built-in/)

"""Simple sentiment analysis agent with evaluation using pydantic-ai and pydantic-evals."""

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_evals import Case, Dataset
from pydantic_evals.evaluators import EqualsExpected, LLMJudge


def main() -> None:
    """Run sentiment analysis agent with evaluation."""
    # Create custom OpenAI-compatible model for sentiment analysis
    sentiment_model = OpenAIChatModel(
        "ibm/granite-4-h-tiny",
        provider=OpenAIProvider(
            base_url="http://127.0.0.1:1234/v1",
            api_key="not-needed",  # Local server doesn't require API key
        ),
    )

    # Create the sentiment analysis agent
    agent = Agent(
        sentiment_model,
        instructions=(
            "Analyze the sentiment of the given text. "
            "Respond with exactly one word: 'positive', 'negative', or 'neutral'."
        ),
    )

    # Create evaluation dataset with test cases
    dataset = Dataset(
        cases=[
            Case(
                name="positive_sentiment",
                inputs="I absolutely love this! It's fantastic and wonderful!",
                expected_output="positive",
            ),
            Case(
                name="negative_sentiment",
                inputs="This is terrible and disappointing. I hate it.",
                expected_output="negative",
            ),
            Case(
                name="neutral_sentiment",
                inputs="It's okay. Nothing special, but not bad either.",
                expected_output="neutral",
            ),
            Case(
                name="positive_simple",
                inputs="Great job!",
                expected_output="positive",
            ),
            Case(
                name="negative_simple",
                inputs="This is bad.",
                expected_output="negative",
            ),
        ],
        evaluators=[
            # Fast deterministic check: ensure output matches expected sentiment
            EqualsExpected(),
            # LLM as judge: verify the sentiment analysis is accurate
            LLMJudge(
                rubric="The sentiment analysis is accurate and matches the expected sentiment",
                include_input=True,
                include_expected_output=True,
                model=sentiment_model,
                assertion={"evaluation_name": "accurate_sentiment"},
            ),
        ],
    )

    # Wrapper function to run the agent and extract output
    def run_sentiment_agent(text: str) -> str:
        result = agent.run_sync(text)
        return result.output

    # Run the evaluation
    print("Running sentiment analysis evaluations...\n")
    report = dataset.evaluate_sync(run_sentiment_agent)

    # Print the evaluation report
    report.print()


if __name__ == "__main__":
    main()

"""Demonstrate POML components for evaluating work order thoroughness."""

from poml import poml  # type: ignore[import-untyped]
from poml.prompt import Prompt  # type: ignore[import-untyped]


def create_work_order_evaluation_template() -> str:
    """Create a POML template for work order evaluation.

    This template demonstrates the use of:
    - <role>: Define the evaluator's persona
    - <example>: Provide sample input/output for context
    - <list>: Structure evaluation criteria
    - <stepwise-instructions>: Guide the evaluation process
    """
    return """
<poml>
  <role>
    You are an experienced IT service desk manager responsible for evaluating
    work order quality. Your task is to assess work orders for completeness,
    clarity, and proper categorization.
  </role>

  <example>
    <input>
      Work Order #1234
      User reported login issue. Fixed password.
    </input>
    <output>
      Thoroughness: Low - Missing details about troubleshooting steps,
      root cause, and user notification
      Steps Taken: Minimal - Only password reset mentioned,
      no diagnostic steps documented
      Transactional: Yes - Simple password reset is a
      standard transactional operation
    </output>
  </example>

  <example>
    <input>
      Work Order #2456
      Database performance degradation. Investigated slow queries,
      identified missing indexes on customer_orders table.
      Added composite index on (order_date, status, customer_id).
      Monitored query performance for 4 hours post-deployment.
      Average query time reduced from 3.2s to 0.4s.
    </input>
    <output>
      Thoroughness: High - Includes problem identification,
      root cause analysis, specific solution, and validation
      Steps Taken: Detailed - Clear investigation path and
      performance metrics documented
      Transactional: No - Required analysis and custom solution
      for performance optimization
    </output>
  </example>

  <example>
    <input>
      Work Order #3789
      Printer offline in Building C. Checked network cable,
      restarted printer. Working now.
    </input>
    <output>
      Thoroughness: Medium - Basic troubleshooting documented
      but lacks detail on specific diagnostics
      Steps Taken: Adequate - Key actions listed but missing
      verification steps and timeline
      Transactional: Yes - Standard printer troubleshooting
      with common resolution steps
    </output>
  </example>

  <stepwise-instructions>
    <list listStyle="decimal">
      <item>Read the work order description carefully</item>
      <item>Evaluate thoroughness based on detail level and completeness</item>
      <item>Assess documented steps taken during resolution</item>
      <item>Determine if request is transactional or complex</item>
      <item>Provide specific recommendations for improvement</item>
    </list>
  </stepwise-instructions>

  <task>
    Evaluate the following work order:

{{work_order}}

    Provide your evaluation using these criteria:

    <list listStyle="star">
      <item>Thoroughness: Rate as High/Medium/Low and explain why</item>
      <item>Steps Taken: Describe quality and completeness of
      documented actions</item>
      <item>Transactional: Is this a simple transactional request
      or complex issue</item>
    </list>
  </task>
</poml>
"""


def create_work_order_evaluation_with_prompt_class(
    work_order: str,
) -> Prompt:
    """Create a POML template using the Prompt class API.

    This demonstrates programmatic prompt construction using Python
    code instead of XML string templates.

    Args:
        work_order: The work order content to evaluate

    Returns:
        Configured Prompt object ready for rendering

    """
    prompt = Prompt()

    with prompt:
        # Define the role
        with prompt.tag("role"):
            prompt.text(
                "You are an experienced IT service desk manager "
                "responsible for evaluating work order quality. "
                "Your task is to assess work orders for completeness, "
                "clarity, and proper categorization.",
            )

        # Add first example - Low thoroughness
        with prompt.tag("example"):
            with prompt.tag("input"):
                prompt.text(
                    "Work Order #1234\nUser reported login issue. Fixed password.",
                )
            with prompt.tag("output"):
                prompt.text(
                    "Thoroughness: Low - Missing details about "
                    "troubleshooting steps, root cause, and user notification\n"
                    "Steps Taken: Minimal - Only password reset mentioned, "
                    "no diagnostic steps documented\n"
                    "Transactional: Yes - Simple password reset is a "
                    "standard transactional operation",
                )

        # Add second example - High thoroughness
        with prompt.tag("example"):
            with prompt.tag("input"):
                prompt.text(
                    "Work Order #2456\n"
                    "Database performance degradation. Investigated slow queries, "
                    "identified missing indexes on customer_orders table. "
                    "Added composite index on (order_date, status, customer_id). "
                    "Monitored query performance for 4 hours post-deployment. "
                    "Average query time reduced from 3.2s to 0.4s.",
                )
            with prompt.tag("output"):
                prompt.text(
                    "Thoroughness: High - Includes problem identification, "
                    "root cause analysis, specific solution, and validation\n"
                    "Steps Taken: Detailed - Clear investigation path and "
                    "performance metrics documented\n"
                    "Transactional: No - Required analysis and custom solution "
                    "for performance optimization",
                )

        # Add third example - Medium thoroughness
        with prompt.tag("example"):
            with prompt.tag("input"):
                prompt.text(
                    "Work Order #3789\n"
                    "Printer offline in Building C. Checked network cable, "
                    "restarted printer. Working now.",
                )
            with prompt.tag("output"):
                prompt.text(
                    "Thoroughness: Medium - Basic troubleshooting documented "
                    "but lacks detail on specific diagnostics\n"
                    "Steps Taken: Adequate - Key actions listed but missing "
                    "verification steps and timeline\n"
                    "Transactional: Yes - Standard printer troubleshooting "
                    "with common resolution steps",
                )

        # Add stepwise instructions
        with prompt.tag("stepwise-instructions"), prompt.list(listStyle="decimal"):
            with prompt.list_item():
                prompt.text("Read the work order description carefully")
            with prompt.list_item():
                prompt.text(
                    "Evaluate thoroughness based on detail level and completeness",
                )
            with prompt.list_item():
                prompt.text("Assess documented steps taken during resolution")
            with prompt.list_item():
                prompt.text("Determine if request is transactional or complex")
            with prompt.list_item():
                prompt.text("Provide specific recommendations for improvement")

        # Add the task with work order content
        with prompt.tag("task"):
            prompt.text("Evaluate the following work order:\n\n")
            prompt.text(work_order)
            prompt.text("\n\nProvide your evaluation using these criteria:\n\n")

            with prompt.list(listStyle="star"):
                with prompt.list_item():
                    prompt.text("Thoroughness: Rate as High/Medium/Low and explain why")
                with prompt.list_item():
                    prompt.text(
                        "Steps Taken: Describe quality and completeness of "
                        "documented actions",
                    )
                with prompt.list_item():
                    prompt.text(
                        "Transactional: Is this a simple transactional "
                        "request or complex issue",
                    )

    return prompt


def main() -> None:
    """Demonstrate POML work order evaluation with sample data."""
    # Sample work order data
    sample_work_order = """
Work Order #5678

Submitted by: Jane Smith (IT Support Specialist)
Date: 2025-10-07
Priority: Medium

Issue Description:
User reported intermittent network connectivity issues in Conference Room B.
Multiple users affected during video conferences.

Steps Taken:
1. Verified network cable connections - all secure
2. Tested network switch ports - functioning normally
3. Checked DHCP server logs - no IP conflicts detected
4. Ran ping tests to default gateway - 15% packet loss observed
5. Replaced network switch in Conference Room B
6. Conducted post-replacement testing - connectivity stable
7. Monitored for 2 hours - no further issues reported

Root Cause:
Failing network switch causing intermittent packet loss

Resolution:
Replaced faulty network switch with spare unit from inventory.
Submitted hardware RMA request for defective switch.

Follow-up:
Scheduled follow-up check in 48 hours to ensure stability.
Updated network equipment maintenance log.
"""

    print("POML Work Order Evaluator - Two Approaches")
    print("=" * 70)

    # Approach 1: String-based XML template
    print("\n" + "=" * 70)
    print("APPROACH 1: String-Based XML Template")
    print("=" * 70)

    template = create_work_order_evaluation_template()
    result = poml(
        markup=template,
        context={"work_order": sample_work_order},
        format="pydantic",
    )

    print(f"\nGenerated {len(result.messages)} messages")
    print("\nFirst message (System Role):")
    print("-" * 70)
    msg_content = [f"Speaker: {msg.speaker}\n{msg.content}" for msg in result.messages]
    print("\n\n".join(msg_content))

    # Approach 2: Programmatic Prompt class
    print("\n" + "=" * 70)
    print("APPROACH 2: Programmatic Prompt Class")
    print("=" * 70)

    prompt = create_work_order_evaluation_with_prompt_class(sample_work_order)

    # Render as XML to show the structure
    print("\nGenerated XML Structure:")
    print("-" * 70)
    xml_output = prompt.dump_xml()
    # Show first 500 chars of XML
    print(xml_output)

    print("-" * 70)
    print(prompt.render(chat=False))


if __name__ == "__main__":
    main()

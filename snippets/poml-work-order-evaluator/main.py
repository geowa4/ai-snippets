"""Demonstrate POML components for evaluating work order thoroughness."""

from poml import poml  # type: ignore[import-untyped]


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

    # Create the POML template
    template = create_work_order_evaluation_template()

    # Compile the template with context
    result = poml(
        markup=template,
        context={"work_order": sample_work_order},
        format="pydantic",
    )

    # Display the results
    print("POML Work Order Evaluation Template")
    print("=" * 60)
    print("\nPydantic Format Output:")
    print("-" * 60)
    print(f"Type: {type(result)}")
    print(f"Number of messages: {len(result.messages)}")
    print(f"Output schema: {result.output_schema}")
    print(f"Tools: {result.tools}")
    print(f"Runtime: {result.runtime}")
    print("\nMessages:")
    print("-" * 60)
    text_output = [
        f"Speaker: {message.speaker}\n{message.content}" for message in result.messages
    ]
    print("\n\n".join(text_output))


if __name__ == "__main__":
    main()

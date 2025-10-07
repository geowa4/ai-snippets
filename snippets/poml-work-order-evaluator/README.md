# POML Work Order Evaluator

A demonstration of Microsoft's POML (Prompt Orchestration Markup Language) showcasing structured prompt engineering for evaluating IT work order quality. This snippet illustrates how to use POML's core components to create maintainable, readable prompts for Large Language Models.

---

## 🎯 Purpose

This project demonstrates POML's key components in a practical context:

1. **`<role>`** - Define the LLM's persona as an IT service desk manager
2. **`<example>`** - Provide input/output examples for context
3. **`<list>`** - Structure evaluation criteria and process steps
4. **`<stepwise-instructions>`** - Guide the evaluation methodology

The snippet evaluates work orders across three dimensions:
- **Thoroughness**: Completeness and detail level
- **Steps Taken**: Quality of documented actions
- **Transactional Nature**: Simple vs. complex issue classification

---

## 🧱 Technologies Used

- **[POML](https://microsoft.github.io/poml/)** - Prompt Orchestration Markup Language for structured LLM prompts
- **Python 3.13+** - Required runtime
- **uv** - Modern Python package manager

---

## 🛠 Installation & Setup

### 1. Install Dependencies

```bash
cd snippets/poml-work-order-evaluator
uv sync
```

This installs the POML library and development tools (mypy, ruff, etc.).

---

## 🚀 Execution

Run the demonstration:

```bash
uv run main.py
```

The script will:
1. Create a POML template with role, examples, and structured instructions
2. Inject a sample work order into the template
3. Compile the template using `poml()` function
4. Display the formatted prompt ready for LLM consumption

---

## 📚 POML Components Demonstrated

### `<role>`
Establishes the LLM's persona and responsibilities:
```xml
<role>
  You are an experienced IT service desk manager responsible for evaluating
  work order quality.
</role>
```

### `<example>`
Provides sample input/output to guide the LLM's response format:
```xml
<example>
  <input>Work Order #1234...</input>
  <output>Thoroughness: Low - Missing details...</output>
</example>
```

### `<stepwise-instructions>`
Breaks down the evaluation process into sequential steps:
```xml
<stepwise-instructions>
  <list listStyle="decimal">
    <item>Read the work order description carefully</item>
    <item>Evaluate thoroughness based on detail level</item>
    ...
  </list>
</stepwise-instructions>
```

### `<list>`
Structures evaluation criteria with customizable list styles:
```xml
<list listStyle="star">
  <item>Thoroughness: Rate as High/Medium/Low</item>
  <item>Steps Taken: Describe quality of actions</item>
  <item>Transactional: Determine complexity</item>
</list>
```

---

## 🔧 Development

### Code Quality Checks

Run type checking:
```bash
uv run mypy .
```

Run linting:
```bash
uv run ruff check
```

Format code:
```bash
uv run ruff format
```

All code passes both mypy and ruff checks with the strict `select = ["ALL"]` configuration.

---

## 📝 Notes

- **Template Reusability**: The POML template is defined as a string and can be easily modified or loaded from external files
- **Context Injection**: The `context` parameter allows dynamic data insertion using `{{variable}}` syntax
- **Output Formats**: POML supports multiple output formats (`message_dict`, `openai_chat`, `pydantic`)
- **Production Use**: In production, you would send the compiled prompt to your LLM API (OpenAI, Anthropic, etc.)

---

## 🔄 Extending the Example

Potential enhancements:

1. **Load Templates from Files**: Store POML in `.poml` files for better organization
2. **Add Stylesheets**: Use POML CSS-like styling to customize output format
3. **LLM Integration**: Connect to OpenAI/Anthropic APIs to get actual evaluations
4. **Batch Processing**: Process multiple work orders in sequence
5. **Custom Components**: Create reusable POML components for common patterns
6. **Validation Rules**: Add POML validation for required fields
7. **Multi-language**: Use POML's templating for internationalized prompts

---

## 📁 Project Structure

```bash
poml-work-order-evaluator/
├── main.py              # POML template and demonstration code
├── pyproject.toml       # Dependencies and tool configuration
├── README.md            # This file
└── SUMMARY.md           # Concise project summary
```

---

## 🔗 Resources

- [POML Documentation](https://microsoft.github.io/poml/)
- [POML GitHub Repository](https://github.com/microsoft/poml)
- [POML Components Reference](https://microsoft.github.io/poml/latest/language/components/)
- [POML Python SDK](https://microsoft.github.io/poml/latest/python/)

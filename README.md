This prototype, "LogGuard," addresses a common frustration in the agentic AI community: **Agent Framework Logging Configuration Interference**. Many agent frameworks aggressively configure logging on initialization, often overriding or interfering with an application's existing logging setup. This leads to unexpected logging behavior, makes it difficult to integrate agent frameworks into larger applications with established logging practices, and frustrates developers trying to maintain consistent logging across their systems.

**Who it affects:** Developers integrating agentic AI components into existing applications, library authors of agent frameworks, and anyone seeking consistent, predictable logging behavior in mixed-technology stacks.

**Why this project shape/stack was chosen:**
A Python package was chosen because Python is the dominant language for agentic AI frameworks, and the `logging` module is a core part of its standard library. This prototype provides a context manager and a utility function that allows developers to temporarily isolate and then restore their application's logging configuration, specifically targeting the common patterns of handler and level changes. It's designed to be a lightweight, drop-in solution that requires minimal changes to existing code.

**Setup and Usage Instructions (Zero API Keys Required):**

1.  **Save the files:** Save the `logguard.py` and `main.py` files in the same directory.
2.  **Run the example:**
    ```bash
    python main.py
    ```

This will demonstrate LogGuard's ability to:
*   Show initial application logging.
*   Simulate an "agent framework" aggressively changing logging.
*   Show how LogGuard isolates and restores the application's logging configuration, preventing the agent framework's changes from persisting.

**No optional real-LLM adapter exists for this project.** This problem is purely about logging configuration management and does not involve LLM processing or reasoning.

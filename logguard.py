import logging
from typing import Any, Dict, List, Tuple

class LogGuard:
    """
    A context manager to temporarily isolate and restore Python's logging configuration.

    This helps prevent agent frameworks or libraries from aggressively modifying the
    root logger or existing loggers, which can interfere with an application's
    established logging practices.
    """

    def __init__(self, loggers_to_guard: List[str] = None):
        """
        Initializes the LogGuard.

        Args:
            loggers_to_guard: A list of logger names (e.g., ['my_app', 'another.module'])
                              whose states should be explicitly saved and restored.
                              If None or empty, only the root logger is guarded.
        """
        self._initial_config: Dict[str, Any] = {}
        self._loggers_to_guard = loggers_to_guard if loggers_to_guard is not None else []
        if 'root' not in self._loggers_to_guard:
            self._loggers_to_guard.insert(0, 'root') # Always guard the root logger

    def __enter__(self):
        self._save_logging_config()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._restore_logging_config()

    def _save_logging_config(self):
        """Saves the current state of specified loggers."""
        for name in self._loggers_to_guard:
            logger = logging.getLogger(name)
            self._initial_config[name] = {
                'level': logger.level,
                'propagate': logger.propagate,
                'handlers': list(logger.handlers) # Store copies of handlers
            }

    def _restore_logging_config(self):
        """Restores the previously saved state of specified loggers."""
        for name, config in self._initial_config.items():
            logger = logging.getLogger(name)

            # Clear existing handlers first
            for handler in logger.handlers[:]:
                logger.removeHandler(handler)

            # Add back original handlers
            for handler in config['handlers']:
                logger.addHandler(handler)

            # Restore level and propagate flag
            logger.setLevel(config['level'])
            logger.propagate = config['propagate']

def with_logging_guard(func):
    """
    A decorator to apply LogGuard to a function.

    Usage:
    @with_logging_guard
    def my_function_using_agent_framework():
        # ... agent framework initialization and usage ...
    """
    def wrapper(*args, **kwargs):
        with LogGuard():
            return func(*args, **kwargs)
    return wrapper

if __name__ == '__main__':
    # --- Self-test / Example Usage within the module ---

    # 1. Initial application logging setup
    app_logger = logging.getLogger('my_app')
    app_logger.setLevel(logging.INFO)
    app_handler = logging.StreamHandler()
    app_formatter = logging.Formatter('%(asctime)s - APP - %(levelname)s - %(message)s')
    app_handler.setFormatter(app_formatter)
    app_logger.addHandler(app_handler)
    app_logger.info("Application started, logging via 'my_app' logger.")
    logging.info("Root logger also active.")

    # 2. Simulate an "agent framework" that aggressively changes logging
    def simulate_agent_framework_init():
        print("\n--- Simulating Agent Framework Init ---")
        # Agent framework might reconfigure the root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        for h in root_logger.handlers[:]:
            root_logger.removeHandler(h)
        agent_handler = logging.StreamHandler()
        agent_formatter = logging.Formatter('[AGENT] %(levelname)s: %(message)s')
        agent_handler.setFormatter(agent_formatter)
        root_logger.addHandler(agent_handler)
        root_logger.debug("Agent framework initialized, root logger reconfigured.")

        # It might also create its own logger
        agent_specific_logger = logging.getLogger('agent_core')
        agent_specific_logger.setLevel(logging.WARNING)
        agent_specific_logger.warning("Agent core warning.")
        print("--- Agent Framework Init Complete ---")

    # 3. Demonstrate LogGuard in action
    print("\n--- Running Agent Framework with LogGuard ---")
    with LogGuard(loggers_to_guard=['my_app']):
        simulate_agent_framework_init()
        logging.info("This info message inside LogGuard should use agent's config (root).")
        app_logger.info("This info message inside LogGuard should use agent's config (my_app is guarded).")
    print("--- LogGuard Exited ---")

    # 4. Verify logging configuration is restored
    print("\n--- Verifying Logging Configuration After LogGuard ---")
    logging.info("This info message should now use the ORIGINAL root logger config.")
    app_logger.info("This info message should now use the ORIGINAL 'my_app' logger config.")

    # Clean up handlers for a graceful exit if run directly
    for h in app_logger.handlers[:]:
        app_logger.removeHandler(h)
    for h in logging.getLogger().handlers[:]:
        logging.getLogger().removeHandler(h)

import logging
from logguard import LogGuard, with_logging_guard

# 1. Initial application logging setup
def setup_app_logging():
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_handler = logging.StreamHandler()
    root_formatter = logging.Formatter('%(asctime)s - ROOT - %(levelname)s - %(message)s')
    root_handler.setFormatter(root_formatter)
    root_logger.addHandler(root_handler)

    # Configure a specific application logger
    app_logger = logging.getLogger('my_application_module')
    app_logger.setLevel(logging.INFO)
    app_handler = logging.StreamHandler()
    app_formatter = logging.Formatter('%(asctime)s - APP_MODULE - %(levelname)s - %(message)s')
    app_handler.setFormatter(app_formatter)
    app_logger.addHandler(app_handler)

    logging.info("Application logging initialized.")
    app_logger.info("Specific application module logging initialized.")

def demonstrate_initial_logging():
    print("\n=== Initial Application Logging ===")
    logging.debug("Root logger: This is a debug message.")
    logging.info("Root logger: This is an info message.")
    logging.getLogger('my_application_module').info("App module logger: This is an info message.")
    logging.getLogger('my_application_module').debug("App module logger: This debug message should NOT appear.")

# 2. Simulate an "agent framework" that aggressively changes logging
def simulate_agent_framework_init():
    print("\n=== Simulating Agent Framework Initialization ===")
    print("  (Agent framework will aggressively reconfigure logging)")

    # Agent framework typically reconfigures the root logger
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]: # Remove all existing handlers
        root_logger.removeHandler(handler)
    agent_handler = logging.StreamHandler()
    agent_formatter = logging.Formatter('[AGENT_FRAMEWORK] %(levelname)s: %(message)s')
    agent_handler.setFormatter(agent_formatter)
    root_logger.addHandler(agent_handler)
    root_logger.setLevel(logging.WARNING) # Set a higher level

    # It might also configure its own specific logger
    agent_internal_logger = logging.getLogger('agent_core_internal')
    agent_internal_logger.setLevel(logging.DEBUG)
    agent_internal_handler = logging.StreamHandler()
    agent_internal_formatter = logging.Formatter('[AGENT_CORE] %(name)s - %(message)s')
    agent_internal_handler.setFormatter(agent_internal_formatter)
    agent_internal_logger.addHandler(agent_internal_handler)

    logging.info("Agent framework: This info message should NOT appear due to WARNING level.")
    logging.warning("Agent framework: This warning message should appear via agent's handler.")
    agent_internal_logger.debug("Agent internal: Debug message from agent's specific logger.")
    print("=== Agent Framework Initialization Complete ===")

# 3. Demonstrate LogGuard with a context manager
def demonstrate_logguard_context_manager():
    print("\n=== Demonstrating LogGuard (Context Manager) ===")
    with LogGuard(loggers_to_guard=['my_application_module']):
        print("  (Inside LogGuard context - agent framework is run here)")
        simulate_agent_framework_init()
        logging.info("  (Inside LogGuard) Root logger info message - should use agent's config (WARNING level).")
        logging.warning("  (Inside LogGuard) Root logger warning message - should use agent's config.")
        logging.getLogger('my_application_module').info("  (Inside LogGuard) App module logger info message - should use agent's config.")
        logging.getLogger('my_application_module').debug("  (Inside LogGuard) App module logger debug message - should NOT appear.")
    print("=== LogGuard Context Exited ===")
    print("  (Logging configuration should now be restored to original state)")
    logging.info("Root logger: Info message AFTER LogGuard - should use original config.")
    logging.debug("Root logger: Debug message AFTER LogGuard - should use original config.")
    logging.getLogger('my_application_module').info("App module logger: Info message AFTER LogGuard - should use original config.")
    logging.getLogger('my_application_module').debug("App module logger: Debug message AFTER LogGuard - should NOT appear.")


# 4. Demonstrate LogGuard with a decorator
@with_logging_guard
def demonstrate_logguard_decorator():
    print("\n=== Demonstrating LogGuard (Decorator) ===")
    print("  (Inside LogGuard decorator - agent framework is run here)")
    simulate_agent_framework_init()
    logging.info("  (Inside LogGuard decorator) Root logger info message - should use agent's config (WARNING level).")
    logging.warning("  (Inside LogGuard decorator) Root logger warning message - should use agent's config.")
    logging.getLogger('my_application_module').info("  (Inside LogGuard decorator) App module logger info message - should use agent's config.")
    logging.getLogger('my_application_module').debug("  (Inside LogGuard decorator) App module logger debug message - should NOT appear.")
    print("=== LogGuard Decorator Function Exited ===")


if __name__ == '__main__':
    # Ensure a clean slate for logging before running tests
    for handler in logging.getLogger().handlers[:]:
        logging.getLogger().removeHandler(handler)
    for logger_name in logging.root.manager.loggerDict:
        if isinstance(logging.root.manager.loggerDict[logger_name], logging.Logger):
            for handler in logging.getLogger(logger_name).handlers[:]:
                logging.getLogger(logger_name).removeHandler(handler)

    setup_app_logging()
    demonstrate_initial_logging()
    demonstrate_logguard_context_manager()

    print("\n--- Running decorator example, observe restoration after function call ---")
    demonstrate_logguard_decorator()
    print("=== After LogGuard Decorator Call ===")
    logging.info("Root logger: Info message AFTER decorator - should use original config.")
    logging.debug("Root logger: Debug message AFTER decorator - should use original config.")
    logging.getLogger('my_application_module').info("App module logger: Info message AFTER decorator - should use original config.")
    logging.getLogger('my_application_module').debug("App module logger: Debug message AFTER decorator - should NOT appear.")

    print("\n--- End of Demonstration ---")

    # Final cleanup of handlers to prevent multiple outputs if run interactively
    for handler in logging.getLogger().handlers[:]:
        logging.getLogger().removeHandler(handler)
    for logger_name in logging.root.manager.loggerDict:
        if isinstance(logging.root.manager.loggerDict[logger_name], logging.Logger):
            for handler in logging.getLogger(logger_name).handlers[:]:
                logging.getLogger(logger_name).removeHandler(handler)

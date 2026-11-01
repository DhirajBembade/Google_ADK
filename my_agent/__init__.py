import os

# Pick the model provider with MODEL_PROVIDER in my_agent/.env ("gemini" or "azure").
if os.getenv("MODEL_PROVIDER", "gemini").lower() == "azure":
    from .azure_agent import root_agent
else:
    from .gcp_agent import root_agent

import os

# Pick the model provider with MODEL_PROVIDER in my_agent/.env ("gemini", "openai" or "azure").
provider = os.getenv("MODEL_PROVIDER", "gemini").lower()

if provider == "azure":
    from .azure_agent import root_agent
elif provider == "openai":
    from .openai_agent import root_agent
else:
    from .gcp_agent import root_agent

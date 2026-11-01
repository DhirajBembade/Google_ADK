import os

# Pick the model provider with MODEL_PROVIDER in .env ("gemini", "openai" or "azure").
provider = os.getenv("MODEL_PROVIDER", "gemini").lower()

if provider == "azure":
    from .azure_agent import root_agent
elif provider == "openai":
    from .openai_agent import root_agent
else:
    from .gemini_agent import root_agent

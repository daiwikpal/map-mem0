from mem0 import Memory
import os

# Custom instructions for memory processing
# These aren't being used right now but Mem0 does support adding custom prompting
# for handling memory retrieval and processing.
CUSTOM_INSTRUCTIONS = """
Extract the Following Information:  

- Key Information: Identify and save the most important details.
- Context: Capture the surrounding context to understand the memory's relevance.
- Connections: Note any relationships to other topics or memories.
- Importance: Highlight why this information might be valuable in the future.
- Source: Record where this information came from when applicable.
"""

def get_mem0_client():
    # Get LLM and embedding providers and configuration
    llm_provider = os.getenv('LLM_PROVIDER')
    llm_api_key = os.getenv('LLM_API_KEY')
    llm_model = os.getenv('LLM_CHOICE')
    embedding_provider = os.getenv('EMBEDDING_PROVIDER', llm_provider)
    embedding_model = os.getenv('EMBEDDING_MODEL_CHOICE')
    embedding_api_key = os.getenv('EMBEDDING_API_KEY')
    embedding_base_url = os.getenv('EMBEDDING_BASE_URL')
    
    # Initialize config dictionary
    config = {}
    
    # Configure LLM based on provider
    if llm_provider == 'openai' or llm_provider == 'openrouter':
        config["llm"] = {
            "provider": "openai",
            "config": {
                "model": llm_model,
                "temperature": 0.2,
                "max_tokens": 2000,
            }
        }
        
        # Set API key in environment if not already set
        if llm_api_key and not os.environ.get("OPENAI_API_KEY"):
            os.environ["OPENAI_API_KEY"] = llm_api_key
        
        # Set base URL for OpenAI if provided
        llm_base_url = os.getenv('LLM_BASE_URL')
        if llm_base_url:
            config["llm"]["config"]["openai_base_url"] = llm_base_url
            
        # For OpenRouter, set the specific API key
        if llm_provider == 'openrouter' and llm_api_key:
            os.environ["OPENROUTER_API_KEY"] = llm_api_key
    
    elif llm_provider == 'ollama':
        config["llm"] = {
            "provider": "ollama",
            "config": {
                "model": llm_model,
                "temperature": 0.2,
                "max_tokens": 2000,
            }
        }
        
        # Set base URL for Ollama if provided
        llm_base_url = os.getenv('LLM_BASE_URL')
        if llm_base_url:
            config["llm"]["config"]["ollama_base_url"] = llm_base_url
    
    # Configure embedder based on embedding_provider
    if embedding_provider == 'openai':
        config["embedder"] = {
            "provider": "openai",
            "config": {
                "model": embedding_model or "text-embedding-3-small",
                "embedding_dims": 1536  # Default for text-embedding-3-small
            }
        }
        # Set embedding API key if provided
        if embedding_api_key and not os.environ.get("OPENAI_API_KEY"):
            os.environ["OPENAI_API_KEY"] = embedding_api_key
    elif embedding_provider == 'ollama':
        config["embedder"] = {
            "provider": "ollama",
            "config": {
                "model": embedding_model or "nomic-embed-text",
                "embedding_dims": 768  # Using actual dimensions for nomic-embed-text
            }
        }
        # Set base URL for Ollama if provided
        if embedding_base_url:
            config["embedder"]["config"]["ollama_base_url"] = embedding_base_url
    elif embedding_provider == 'openrouter':
        config["embedder"] = {
            "provider": "openrouter",
            "config": {
                "model": embedding_model,
                "embedding_dims": 1536
            }
        }
        if embedding_api_key and not os.environ.get("OPENROUTER_API_KEY"):
            os.environ["OPENROUTER_API_KEY"] = embedding_api_key
        if embedding_base_url:
            config["embedder"]["config"]["openrouter_base_url"] = embedding_base_url
    else:
        raise ValueError(f"Unsupported embedding provider: {embedding_provider}")
    
    # Configure Supabase vector store
    embedding_dims = 1536 if embedding_provider in ["openai", "openrouter"] else 768
    collection_name = os.getenv("MEM0_COLLECTION_NAME", f"mem0_memories_{embedding_dims}")

    config["vector_store"] = {
        "provider": "supabase",
        "config": {
            "connection_string": os.environ.get('DATABASE_URL', ''),
            "collection_name": collection_name,
            "embedding_model_dims": embedding_dims
        }
    }

    # config["custom_fact_extraction_prompt"] = CUSTOM_INSTRUCTIONS
    
    # Create and return the Memory client
    return Memory.from_config(config)
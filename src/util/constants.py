KNOWLEDGE_GRAPH_PATH = "./../data/db/knowledge_graph_index.pkl"
MILVUS_DB_PATH = "./../data/db/milvus.db"
MILVUS_COLLECTION_NAME_BASELINE = "baseline_collection"
MILVUS_COLLECTION_NAME_VERSIONRAG = "VersionRAG_collection"
MILVUS_MAX_TOKEN_COUNT = 512 # Maximum tokens per chunk
MILVUS_META_ATTRIBUTE_TEXT = "text"
MILVUS_META_ATTRIBUTE_PAGE = "page"
MILVUS_META_ATTRIBUTE_FILE = "file"
MILVUS_META_ATTRIBUTE_CATEGORY = "category"
MILVUS_META_ATTRIBUTE_DOCUMENTATION = "documentation"
MILVUS_META_ATTRIBUTE_VERSION = "version"
MILVUS_META_ATTRIBUTE_TYPE = "type" # file / node
MILVUS_BASELINE_SOURCE_COUNT = 15
LLM_MODE = 'ollama' # openai / groq / offline / ollama
LLM_OFFLINE_MODEL = "" # local llm model (for offline mode)
OLLAMA_BASE_URL = "http://localhost:11435"
OLLAMA_MODEL = "gpt-oss:120b"

EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMENSIONS = 512  # text-embedding-3-small with reduced dimensions

BASELINE_MODEL = "Baseline"
KG_MODEL = "GraphRAG"
VERSIONRAG_MODEL = "VersionRAG"
AVAILABLE_MODELS = [BASELINE_MODEL, KG_MODEL, VERSIONRAG_MODEL]
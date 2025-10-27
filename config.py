"""
Configuration file for AI Legal Aid Chatbot
Modify these settings to customize the chatbot behavior
"""

# Directory Settings
DATA_DIR = "data"  # Directory containing PDF files
DB_DIR = "db"      # Directory for ChromaDB persistence

# Model Settings
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "google/flan-t5-small"

# Alternative models (uncomment to use):
# EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"  # Better quality, slower
# LLM_MODEL = "google/flan-t5-base"  # Better quality, requires more RAM

# Chunking Settings
CHUNK_SIZE = 500        # Size of text chunks (characters)
CHUNK_OVERLAP = 50      # Overlap between chunks (characters)

# Retrieval Settings
DEFAULT_TOP_K = 3       # Number of chunks to retrieve by default
MAX_TOP_K = 5          # Maximum number of chunks user can select

# Generation Settings
MAX_INPUT_LENGTH = 512   # Maximum input tokens for LLM
MAX_OUTPUT_LENGTH = 256  # Maximum output tokens for LLM
NUM_BEAMS = 4           # Beam search width (higher = better quality, slower)
TEMPERATURE = 0.7       # Generation temperature (0.0-1.0)

# UI Settings
PAGE_TITLE = "AI Legal Aid Chatbot"
PAGE_ICON = "⚖️"
LAYOUT = "wide"

# Performance Settings
SHOW_PROGRESS_BAR = True  # Show progress during embedding computation
BATCH_SIZE = 32           # Batch size for embedding computation

# Logging
LOG_LEVEL = "INFO"  # Options: DEBUG, INFO, WARNING, ERROR

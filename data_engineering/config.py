import pathlib
from pydantic_settings import BaseSettings


ROOT = pathlib.Path(__file__).resolve().parent.parent
TRANSCRIPT_DIR = ROOT / "data" / "transcripts"
SUMMARY_DIR = ROOT / "data" / "summaries"
MODEL_DIR = ROOT / "data_engineering" / "models"
PROMPT_DIR = ROOT / "data_engineering" / "prompts"


class LLMSettings(BaseSettings):
    CONTEXT_WINDOW: int = 16000
    N_GPU_LAYERS: int = 1
    TEMPERATURE: float = 0.3
    MAX_TOKENS: int = 1000
    MODEL_FILE_NAME: str = "tinyllama-1.1b-chat-v1.0.Q5_K_M.gguf"
    CHAT_FORMAT: str = "llama-2"


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///transcript.db"
    llm: LLMSettings = LLMSettings()

    class Config:
        case_sensitive = True


settings = Settings()

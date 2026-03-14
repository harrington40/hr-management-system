"""
AI Orchestrator configuration — reads from environment / .env file.

The project already calls load_dotenv() in helperFuns/utils.py on startup,
so all .env values are available via os.getenv() here.
"""

import os
from dotenv import load_dotenv

# Ensure .env is loaded even if this module is imported before helperFuns
load_dotenv()

# Mapping from common display/human names → actual DeepSeek API model IDs
_MODEL_ALIASES: dict[str, str] = {
    "deepseek-coder-v2":    "deepseek-coder",
    "deepseek coder v2":    "deepseek-coder",
    "deepseek-coder v2":    "deepseek-coder",
    "coder":                "deepseek-coder",
    "deepseek-chat":        "deepseek-chat",
    "chat":                 "deepseek-chat",
    "deepseek-v2":          "deepseek-chat",
    "deepseek v2":          "deepseek-chat",
    "deepseek-r1":          "deepseek-reasoner",
    "r1":                   "deepseek-reasoner",
    "deepseek-reasoner":    "deepseek-reasoner",
}


def get_deepai_key() -> str:
    """Return the DeepAI API key from the environment, or empty string."""
    return os.getenv("DEEPAI_API_KEY", "").strip()


def get_deepseek_key() -> str:
    """Return the DeepSeek API key from the environment, or empty string."""
    return os.getenv("DEEPSEEK_API_KEY", "").strip()


def get_deepseek_model() -> str:
    """
    Return the normalised DeepSeek API model ID.
    Accepts human-friendly names like 'DeepSeek-Coder-V2' and maps them to
    the correct API identifier (e.g. 'deepseek-coder').
    """
    raw = os.getenv("DEEPSEEK_MODEL", "deepseek-chat").strip()
    return _MODEL_ALIASES.get(raw.lower(), raw)


def get_deepseek_max_tokens() -> int:
    """Return the max tokens setting for DeepSeek responses."""
    try:
        return int(os.getenv("DEEPSEEK_MAX_TOKENS", "4096"))
    except ValueError:
        return 4096


def keys_configured() -> bool:
    """Return True if both API keys are present and not placeholder values."""
    placeholder_fragments = {"your_", "_here", "placeholder", "changeme"}
    for key in (get_deepai_key(), get_deepseek_key()):
        if not key:
            return False
        if any(frag in key.lower() for frag in placeholder_fragments):
            return False
    return True

"""
Test module - Example tests
"""

import pytest
from config import Config

def test_config_exists():
    """Test config exists"""
    assert Config.APP_NAME is not None
    assert Config.APP_VERSION is not None

def test_models_list():
    """Test Whisper models list"""
    assert len(Config.WHISPER_MODELS) > 0
    assert "medium" in Config.WHISPER_MODELS

# Add more tests here

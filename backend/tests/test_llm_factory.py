import unittest
import os
from unittest.mock import patch
from app.services import get_llm_provider
from app.services.ollama_provider import OllamaProvider
from app.services.gemini_provider import GeminiProvider

class TestLLMProviderFactory(unittest.TestCase):
    @patch.dict(os.environ, {"LLM_PROVIDER": "OLLAMA"})
    def test_get_ollama_provider(self):
        provider = get_llm_provider()
        self.assertIsInstance(provider, OllamaProvider)

    @patch.dict(os.environ, {"LLM_PROVIDER": "GEMINI", "GEMINI_API_KEY": "fake"})
    def test_get_gemini_provider(self):
        provider = get_llm_provider()
        self.assertIsInstance(provider, GeminiProvider)

if __name__ == '__main__':
    unittest.main()

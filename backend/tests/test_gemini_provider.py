import unittest
from unittest.mock import patch, MagicMock
from app.services.gemini_provider import GeminiProvider
from app.services.llm_provider import JobAnalysisResult
from pydantic import ValidationError

class TestGeminiProvider(unittest.TestCase):
    @patch('app.services.gemini_provider.genai.Client')
    def test_analyze_job_success(self, mock_client_class):
        # Setup mock
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        mock_response = MagicMock()
        
        # Valid JSON matching the Pydantic schema
        mock_response.text = '{"match_score": 85, "cover_letter": "Dear Hiring Manager...", "prep_questions": ["What is Python?"]}'
        mock_client.models.generate_content.return_value = mock_response
        
        # Initialize provider
        provider = GeminiProvider(api_key="fake-key")
        
        # Test
        result = provider.analyze_job("CV Text", "Job Description")
        
        # Assertions
        self.assertIsInstance(result, JobAnalysisResult)
        self.assertEqual(result.match_score, 85)
        self.assertEqual(result.cover_letter, "Dear Hiring Manager...")
        self.assertEqual(result.prep_questions, ["What is Python?"])
        
        # Ensure correct API call
        mock_client.models.generate_content.assert_called_once()
        call_kwargs = mock_client.models.generate_content.call_args.kwargs
        self.assertEqual(call_kwargs['model'], 'gemini-2.5-flash')
        self.assertEqual(call_kwargs['config'].response_mime_type, 'application/json')
        self.assertEqual(call_kwargs['config'].response_schema, JobAnalysisResult)

    @patch('app.services.gemini_provider.genai.Client')
    def test_analyze_job_invalid_json(self, mock_client_class):
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        mock_response = MagicMock()
        
        # Invalid JSON (missing required fields)
        mock_response.text = '{"match_score": 85}'
        mock_client.models.generate_content.return_value = mock_response
        
        provider = GeminiProvider(api_key="fake-key")
        
        with self.assertRaises(ValidationError):
            provider.analyze_job("CV Text", "Job Description")

if __name__ == '__main__':
    unittest.main()

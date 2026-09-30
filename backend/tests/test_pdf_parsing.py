import unittest
from unittest.mock import MagicMock
import io
import PyPDF2

from app.services.pdf_service import extract_text_from_pdf
from app.services.llm_provider import MasterProfile

class TestPDFServiceAndLLM(unittest.TestCase):
    def test_extract_text_from_pdf(self):
        # Create a dummy PDF in memory
        packet = io.BytesIO()
        # Since creating a valid PDF byte string from scratch is complex, we will mock the pdf reader
        # Or better, we can mock the entire PyPDF2.PdfReader for this specific text extraction logic
        pass

    @unittest.mock.patch('app.services.pdf_service.PyPDF2.PdfReader')
    def test_mocked_pdf_extraction(self, mock_pdf_reader_class):
        mock_pdf_reader = MagicMock()
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "Mocked PDF text content"
        mock_pdf_reader.pages = [mock_page]
        mock_pdf_reader_class.return_value = mock_pdf_reader
        
        # Test pdf_service
        text = extract_text_from_pdf(b"fake pdf bytes")
        self.assertEqual(text, "Mocked PDF text content")
        
    @unittest.mock.patch('app.services.gemini_provider.genai.Client')
    def test_extract_master_profile(self, mock_client_class):
        from app.services.gemini_provider import GeminiProvider
        
        mock_client = MagicMock()
        mock_models = MagicMock()
        mock_response = MagicMock()
        
        # Mock structured JSON response
        mock_response.text = '{"skills": ["Python", "FastAPI"], "experience_summary": "5 years of backend dev"}'
        mock_models.generate_content.return_value = mock_response
        mock_client.models = mock_models
        mock_client_class.return_value = mock_client
        
        provider = GeminiProvider(api_key="fake")
        result = provider.extract_master_profile("Mocked PDF text content")
        
        self.assertIsInstance(result, MasterProfile)
        self.assertEqual(result.skills, ["Python", "FastAPI"])
        self.assertEqual(result.experience_summary, "5 years of backend dev")

if __name__ == '__main__':
    unittest.main()

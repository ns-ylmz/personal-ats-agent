import unittest
from unittest.mock import MagicMock, patch
import json
import queue

from app import models
from app.worker import worker_loop, job_queue

class TestWorkerRAG(unittest.TestCase):
    @patch('app.database.SessionLocal')
    @patch('app.services.get_llm_provider')
    def test_worker_injects_past_feedback(self, mock_get_llm_provider, mock_session_local):
        # Setup mocks
        mock_db = MagicMock()
        mock_session_local.return_value = mock_db
        
        mock_job = MagicMock()
        mock_job.id = 1
        mock_job.cv_text = "My CV"
        mock_job.job_description = "Job Description"
        
        mock_feedback1 = MagicMock()
        mock_feedback1.feedback_text = "Needs more system design knowledge."
        mock_feedback2 = MagicMock()
        mock_feedback2.feedback_text = "Good communication."
        
        # Mock query return values
        # first query is Job, second query is InterviewFeedback
        mock_db.query().filter().first.return_value = mock_job
        mock_db.query().all.return_value = [mock_feedback1, mock_feedback2]
        
        mock_provider = MagicMock()
        mock_result = MagicMock()
        mock_result.match_score = 80
        mock_result.cover_letter = "Cover letter"
        mock_result.prep_questions = ["Q1"]
        mock_provider.analyze_job.return_value = mock_result
        mock_get_llm_provider.return_value = mock_provider
        
        # Add job to queue and poison pill
        job_queue.put(1)
        job_queue.put(None)
        
        # Run worker loop
        worker_loop()
        
        # Verify provider was called with concatenated feedback
        expected_feedback_text = "- Needs more system design knowledge.\n- Good communication."
        mock_provider.analyze_job.assert_called_once_with(
            "My CV",
            "Job Description",
            past_feedback=expected_feedback_text
        )

if __name__ == '__main__':
    unittest.main()

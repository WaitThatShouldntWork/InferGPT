import unittest
from unittest.mock import patch, MagicMock
from src.agents.web_agent import web_general_search_core

class TestWebAgentCore(unittest.TestCase):

    def setUp(self):
        self.llm = MagicMock()
        self.model = 'mock_model'

    @patch('src.agents.web_agent.perform_search')
    @patch('src.agents.web_agent.perform_scrape')
    @patch('src.agents.web_agent.perform_summarization')
    @patch('src.agents.web_agent.is_valid_answer')
    def test_web_general_search_core(
        self, mock_is_valid_answer, mock_perform_summarization, mock_perform_scrape, mock_perform_search
    ):
        mock_perform_search.return_value = {"status": "success", "urls": ['http://example.com']}
        mock_perform_scrape.return_value = 'Example scraped content.'
        mock_perform_summarization.return_value = 'Example summary.'
        mock_is_valid_answer.return_value = True

        result = web_general_search_core('example query', self.llm, self.model)
        self.assertEqual(result, 'Example summary.')
        mock_perform_search.assert_called_once_with('example query', num_results=15)
        mock_perform_scrape.assert_called_once_with('http://example.com')
        mock_perform_summarization.assert_called_once_with(
            'example query', 'Example scraped content.', self.llm, self.model
        )
        mock_is_valid_answer.assert_called_once_with('Example summary.', 'example query')

    @patch('src.agents.web_agent.perform_search')
    @patch('src.agents.web_agent.perform_scrape')
    @patch('src.agents.web_agent.perform_summarization')
    @patch('src.agents.web_agent.is_valid_answer')
    def test_web_general_search_core_no_results(
        self, mock_is_valid_answer, mock_perform_summarization, mock_perform_scrape, mock_perform_search
    ):
        mock_perform_search.return_value = {"status": "error", "urls": []}

        result = web_general_search_core('example query', self.llm, self.model)
        self.assertEqual(result, 'No relevant information found on the internet for the given query.')
        mock_perform_search.assert_called_once_with('example query', num_results=15)
        mock_perform_scrape.assert_not_called()
        mock_perform_summarization.assert_not_called()
        mock_is_valid_answer.assert_not_called()

    @patch('src.agents.web_agent.perform_search')
    @patch('src.agents.web_agent.perform_scrape')
    @patch('src.agents.web_agent.perform_summarization')
    @patch('src.agents.web_agent.is_valid_answer')
    def test_web_general_search_core_invalid_summary(
        self, mock_is_valid_answer, mock_perform_summarization, mock_perform_scrape, mock_perform_search
    ):
        mock_perform_search.return_value = {"status": "success", "urls": ['http://example.com']}
        mock_perform_scrape.return_value = 'Example scraped content.'
        mock_perform_summarization.return_value = 'Example invalid summary.'
        mock_is_valid_answer.return_value = False

        result = web_general_search_core('example query', self.llm, self.model)
        self.assertEqual(result, 'No relevant information found on the internet for the given query.')
        mock_perform_search.assert_called_once_with('example query', num_results=15)
        mock_perform_scrape.assert_called_once_with('http://example.com')
        mock_perform_summarization.assert_called_once_with(
            'example query', 'Example scraped content.', self.llm, self.model
        )
        mock_is_valid_answer.assert_called_once_with('Example invalid summary.', 'example query')

if __name__ == '__main__':
    unittest.main()

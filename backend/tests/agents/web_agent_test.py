import unittest
from unittest.mock import patch, MagicMock
from src.agents.web_agent import web_general_search_core

class TestWebAgentCore(unittest.TestCase):

    def setUp(self):
        self.llm = MagicMock()
        self.model = 'mock_model'

    @patch('src.agents.web_agent.search_urls')
    @patch('src.agents.web_agent.scrape_content')
    @patch('src.agents.web_agent.summarise_content')
    @patch('src.agents.web_agent.is_valid_answer')
    def test_web_general_search_core(
        self, mock_is_valid_answer, mock_summarise_content, mock_scrape_content, mock_search_urls
    ):
        mock_search_urls.return_value = ['http://example.com']
        mock_scrape_content.return_value = 'Example scraped content.'
        mock_summarise_content.return_value = 'Example summary.'
        mock_is_valid_answer.return_value = True

        result = web_general_search_core('example query', self.llm, self.model)
        self.assertEqual(result, ['Example summary.'])
        mock_search_urls.assert_called_once_with('example query', num_results=15)
        mock_scrape_content.assert_called_once_with('http://example.com')
        mock_summarise_content.assert_called_once_with(
            'example query', 'Example scraped content.', self.llm, self.model
        )
        mock_is_valid_answer.assert_called_once_with('Example summary.', 'example query')

    @patch('src.agents.web_agent.search_urls')
    @patch('src.agents.web_agent.scrape_content')
    @patch('src.agents.web_agent.summarise_content')
    @patch('src.agents.web_agent.is_valid_answer')
    def test_web_general_search_core_no_results(
        self, mock_is_valid_answer, mock_summarise_content, mock_scrape_content, mock_search_urls
    ):
        mock_search_urls.return_value = []

        result = web_general_search_core('example query', self.llm, self.model)
        self.assertEqual(result, ['No relevant information found on the internet for the given query.'])
        mock_search_urls.assert_called_once_with('example query', num_results=15)
        mock_scrape_content.assert_not_called()
        mock_summarise_content.assert_not_called()
        mock_is_valid_answer.assert_not_called()

    @patch('src.agents.web_agent.search_urls')
    @patch('src.agents.web_agent.scrape_content')
    @patch('src.agents.web_agent.summarise_content')
    @patch('src.agents.web_agent.is_valid_answer')
    def test_web_general_search_core_invalid_summary(
        self, mock_is_valid_answer, mock_summarise_content, mock_scrape_content, mock_search_urls
    ):
        mock_search_urls.return_value = ['http://example.com']
        mock_scrape_content.return_value = 'Example scraped content.'
        mock_summarise_content.return_value = 'Example invalid summary.'
        mock_is_valid_answer.return_value = False

        result = web_general_search_core('example query', self.llm, self.model)
        self.assertEqual(result, ['No relevant information found on the internet for the given query.'])
        mock_search_urls.assert_called_once_with('example query', num_results=15)
        mock_scrape_content.assert_called_once_with('http://example.com')
        mock_summarise_content.assert_called_once_with(
            'example query', 'Example scraped content.', self.llm, self.model
        )
        mock_is_valid_answer.assert_called_once_with('Example invalid summary.', 'example query')

if __name__ == '__main__':
    unittest.main()

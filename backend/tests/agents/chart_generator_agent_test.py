import unittest
from unittest.mock import patch, MagicMock
from src.agents.chart_generator_agent import generate_chart
import os

class TestGenerateChartAgent(unittest.TestCase):

    def setUp(self):
        self.llm = MagicMock()
        self.model = 'mock_model'
        self.details_to_generate_chart_code = "details to generate chart code"
        self.generate_chart_code_prompt = "generate chart code prompt"

    @patch('src.agents.chart_generator_agent.sanitise_script')
    @patch('src.agents.chart_generator_agent.engine.load_prompt')
    async def test_generate_chart_success(self, mock_load_prompt, mock_sanitise_script):
        # Arrange
        self.llm.chat.return_value = "generated code"
        mock_sanitise_script.return_value = """
import matplotlib.pyplot as plt
fig = plt.figure()
plt.plot([1, 2, 3], [4, 5, 6])
"""
        mock_load_prompt.side_effect = [self.details_to_generate_chart_code, self.generate_chart_code_prompt]

        # Act
        with patch('matplotlib.pyplot.figure') as mock_fig:
            mock_fig_instance = MagicMock()
            mock_fig.return_value = mock_fig_instance
            result = await generate_chart("intent", "values", "params", "timeframe", self.llm, self.model)

        # Assert
        self.llm.chat.assert_called_once_with(self.model, self.generate_chart_code_prompt,
                                              self.details_to_generate_chart_code)
        mock_sanitise_script.assert_called_once_with("generated code")
        expected_path = os.path.join('/app/output', 'output.png')
        mock_fig_instance.savefig.assert_called_once_with(expected_path)
        self.assertEqual(result, "output.png")

    @patch('src.agents.chart_generator_agent.sanitise_script')
    @patch('src.agents.chart_generator_agent.engine.load_prompt')
    async def test_generate_chart_no_fig(self, mock_load_prompt, mock_sanitise_script):
        # Arrange
        self.llm.chat.return_value = "generated code"
        mock_sanitise_script.return_value = """
import matplotlib.pyplot as plt
plt.plot([1, 2, 3], [4, 5, 6])
"""  # No fig created
        mock_load_prompt.side_effect = [self.details_to_generate_chart_code, self.generate_chart_code_prompt]

        # Act / Assert
        with self.assertRaises(ValueError):
            await generate_chart("intent", "values", "params", "timeframe", self.llm, self.model)

    @patch('src.agents.chart_generator_agent.sanitise_script')
    @patch('src.agents.chart_generator_agent.engine.load_prompt')
    async def test_generate_chart_exception(self, mock_load_prompt, mock_sanitise_script):
        # Arrange
        self.llm.chat.return_value = "generated code"
        mock_sanitise_script.return_value = """
import matplotlib.pyplot as plt
fig = plt.figure()
plt.plot([1, 2, 3], [4, 5, 6])
"""
        mock_load_prompt.side_effect = [self.details_to_generate_chart_code, self.generate_chart_code_prompt]

        with patch('builtins.exec', side_effect=Exception("Test exception")):
            # Act / Assert
            with self.assertRaises(Exception):
                await generate_chart("intent", "values", "params", "timeframe", self.llm, self.model)

if __name__ == '__main__':
    unittest.main()

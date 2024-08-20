from io import BytesIO
import unittest
from unittest.mock import patch, AsyncMock, MagicMock
import pytest
from src.agents.chart_generator_agent import generate_chart


class TestGenerateChartAgent(unittest.TestCase):
    def setUp(self):
        self.llm = AsyncMock()
        self.model = "mock_model"
        self.details_to_generate_chart_code = "details to generate chart code"
        self.generate_chart_code_prompt = "generate chart code prompt"

    @pytest.mark.asyncio
    @patch("src.agents.chart_generator_agent.engine.load_prompt")
    @patch("src.agents.chart_generator_agent.sanitise_script")
    async def test_generate_code_success(self, mock_sanitise_script, mock_load_prompt):
        mock_load_prompt.side_effect = [self.details_to_generate_chart_code, self.generate_chart_code_prompt]
        self.llm.chat.return_value = "generated code"
        mock_sanitise_script.return_value = """

import matplotlib.pyplot as plt
fig = plt.figure()
plt.plot([1, 2, 3], [4, 5, 6])

"""

        with patch("matplotlib.pyplot.figure") as mock_fig:
            mock_fig_instance = MagicMock()
            mock_fig.return_value = mock_fig_instance
            result = await generate_chart("question_intent", "data_provided", "question_params", self.llm, self.model)
            buf = BytesIO()
            mock_fig_instance.savefig.assert_called_once_with(buf, format="png")

        self.llm.chat.assert_called_once_with(
            self.model, self.generate_chart_code_prompt, self.details_to_generate_chart_code
        )
        mock_sanitise_script.assert_called_once_with("generated code")
        self.assertIsInstance(result, str)

    @pytest.mark.asyncio
    @patch("src.agents.chart_generator_agent.engine.load_prompt")
    @patch("src.agents.chart_generator_agent.sanitise_script")
    async def test_generate_code_no_figure(self, mock_sanitise_script, mock_load_prompt):
        mock_load_prompt.side_effect = [self.details_to_generate_chart_code, self.generate_chart_code_prompt]
        self.llm.chat.return_value = "generated code"
        mock_sanitise_script.return_value = """

import matplotlib.pyplot as plt
# No figure is created

"""

        with self.assertRaises(ValueError) as context:
            await generate_chart("question_intent", "data_provided", "question_params", self.llm, self.model)
        self.assertEqual(str(context.exception), "The generated code did not produce a figure named 'fig'.")


if __name__ == "__main__":
    unittest.main()
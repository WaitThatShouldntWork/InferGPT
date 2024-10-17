from io import BytesIO
from unittest.mock import patch, AsyncMock, MagicMock
import pytest
from src.agents.chart_generator_agent import generate_chart
import base64
import matplotlib.pyplot as plt
from PIL import Image
import json
from src.agents.chart_generator_agent import sanitise_script

@pytest.mark.asyncio
@patch("src.agents.chart_generator_agent.engine.load_prompt")
@patch("src.agents.chart_generator_agent.sanitise_script", new_callable=MagicMock)
async def test_generate_code_success(mock_sanitise_script, mock_load_prompt):
    llm = AsyncMock()
    model = "mock_model"

    mock_load_prompt.side_effect = [
        "details to create chart code prompt",
        "generate chart code prompt"
    ]

    llm.chat.return_value = "generated code"

    return_string = mock_sanitise_script.return_value = """
import matplotlib.pyplot as plt
fig = plt.figure()
plt.plot([1, 2, 3], [4, 5, 6])
"""
    plt.switch_backend('Agg')

    def mock_exec_side_effect(script, globals=None, locals=None):
        if script == return_string:
            fig = plt.figure()
            plt.plot([1, 2, 3], [4, 5, 6])
            if locals is None:
                locals = {}
            locals['fig'] = fig

    with patch("builtins.exec", side_effect=mock_exec_side_effect):
        result = await generate_chart("question_intent", "data_provided", "question_params", llm, model)

        response = json.loads(result)

        image_data = response["content"]
        decoded_image = base64.b64decode(image_data)

        image = Image.open(BytesIO(decoded_image))
        image.verify()

        llm.chat.assert_called_once_with(
            model,
            "generate chart code prompt",
            "details to create chart code prompt"
        )
        mock_sanitise_script.assert_called_once_with("generated code")

@pytest.mark.asyncio
@patch("src.agents.chart_generator_agent.engine.load_prompt")
@patch("src.agents.chart_generator_agent.sanitise_script", new_callable=MagicMock)
async def test_generate_code_no_figure(mock_sanitise_script, mock_load_prompt):
    llm = AsyncMock()
    model = "mock_model"

    mock_load_prompt.side_effect = [
        "details to create chart code prompt",
        "generate chart code prompt"
    ]

    llm.chat.return_value = "generated code"

    return_string = mock_sanitise_script.return_value = """
import matplotlib.pyplot as plt
# No fig creation
"""

    plt.switch_backend('Agg')

    def mock_exec_side_effect(script, globals=None, locals=None):
        if script == return_string:
            if locals is None:
                locals = {}

    with patch("builtins.exec", side_effect=mock_exec_side_effect):
        with pytest.raises(ValueError, match="The generated code did not produce a figure named 'fig'."):
            await generate_chart("question_intent", "data_provided", "question_params", llm, model)

        llm.chat.assert_called_once_with(
            model,
            "generate chart code prompt",
            "details to create chart code prompt"
        )

        mock_sanitise_script.assert_called_once_with("generated code")

@pytest.mark.parametrize(
    "input_script, expected_output",
    [

        (
            """```python
import matplotlib.pyplot as plt
fig = plt.figure()
plt.plot([1, 2, 3], [4, 5, 6])
```""",
            """import matplotlib.pyplot as plt
fig = plt.figure()
plt.plot([1, 2, 3], [4, 5, 6])"""
        ),
        (
            """```python
import matplotlib.pyplot as plt
fig = plt.figure()
plt.plot([1, 2, 3], [4, 5, 6])""",
            """import matplotlib.pyplot as plt
fig = plt.figure()
plt.plot([1, 2, 3], [4, 5, 6])"""
        ),
        (
            """import matplotlib.pyplot as plt
fig = plt.figure()
plt.plot([1, 2, 3], [4, 5, 6])
```""",
            """import matplotlib.pyplot as plt
fig = plt.figure()
plt.plot([1, 2, 3], [4, 5, 6])"""
        ),
        (
            """import matplotlib.pyplot as plt
fig = plt.figure()
plt.plot([1, 2, 3], [4, 5, 6])""",
            """import matplotlib.pyplot as plt
fig = plt.figure()
plt.plot([1, 2, 3], [4, 5, 6])"""
        ),
        (
            "",
            ""
        )
    ]
)
def test_sanitise_script(input_script, expected_output):
    assert sanitise_script(input_script) == expected_output
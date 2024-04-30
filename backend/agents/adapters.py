from agents import Tool


def get_mistral_tool(tool: Tool):
    return {
        "type": "function",
        "function": {
            "description": tool.description,
            "name": tool.action.__name__,
            "parameters": {
                "type": "object",
                "properties": {
                    key: {
                        "type": inner_dict.type,
                        "description": inner_dict.description,
                    }
                    for key, inner_dict in tool.parameters.items()
                },
                "required": [key for key, inner_dict in tool.parameters.items() if inner_dict.required],
            },
        },
    }

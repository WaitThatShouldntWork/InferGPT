from .tool import Tool
import json

def to_object(tool: Tool) -> str:
    obj = {
        "description": tool.description,
        "name": tool.action.__name__,
        "parameters": {
            key: {
                    "type": inner_dict.type,
                    "description": inner_dict.description,
                }
                for key, inner_dict in tool.parameters.items()
        },
    }

    return json.dumps(obj)

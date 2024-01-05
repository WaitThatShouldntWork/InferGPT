## TODO: Add tests
class Sanitiser:
    @staticmethod
    def sanitiseGPTResponse(message):
        # Extract json only
        start = message.index("{")
        end = message.rfind("}")
        json_raw = message[start : end+1]
        return json_raw.strip().replace("\\n", "")
    @staticmethod
    def isNoneOrEmpty(obj):
        return obj is None or obj == ''
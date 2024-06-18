import logging
import os

from jinja2 import Environment, FileSystemLoader

logger = logging.getLogger(__name__)

class PromptEngine:
    def __init__(self):
        logger.debug("Initializing PromptEngine")

        try:
            templates_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "templates"))
            self.env = Environment(loader=FileSystemLoader(templates_dir))
        except Exception as e:
            logger.error(f"Error initializing PromptEngine Environment: {e}")
            raise

    def load_prompt(self, template_name: str, **kwargs) -> str:
        try:
            logger.debug(f"Loading template: {template_name}.j2")
            template = self.env.get_template(f"{template_name}.j2")
            logger.debug(f"Rendering template: {template_name} with args: {kwargs}")
            return template.render(**kwargs)
        except Exception as e:
            logger.error(f"Error loading or rendering template: {e}")
            raise

import logging
import os

from jinja2 import Environment, FileSystemLoader


class PromptEngine:
    """
    Class to handle loading and populating Jinja2 templates for prompts.
    """

    def __init__(self, model: str):
        """
        Initialize the PromptEngine with the specified model.

        Args:
            model (str): The model to use for loading prompts.
            debug_enabled (bool): Enable or disable debug logging.
        """
        self.model = model
        logging.debug("Initializing PromptEngine")

        try:
            templates_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "templates"))
            self.env = Environment(loader=FileSystemLoader(templates_dir))
        except Exception as e:
            logging.error(f"Error initializing PromptEngine Environment: {e}")
            raise

    def load_prompt(self, template_name: str, **kwargs) -> str:
        """
        Load and populate the specified template.

        Args:
            template_name (str): The name of the template to load.
            **kwargs: The arguments to populate the template with.

        Returns:
            str: The populated template.
        """
        try:
            logging.debug(f"Loading template: {template_name}.j2")
            template_name = self.env.get_template(f"{template_name}.j2")
            logging.debug(f"Rendering template: {template_name} with args: {kwargs}")
            return template_name.render(**kwargs)
        except Exception as e:
            logging.error(f"Error loading or rendering template: {e}")
            raise

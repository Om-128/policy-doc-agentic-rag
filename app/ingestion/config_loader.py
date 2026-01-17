import os
import sys
import yaml

from utils import BASE_DIR
from custom_exception import CustomException

class PathLoaderConfig:
    config_file_path = os.path.join(BASE_DIR, 'app', 'config', 'pdf_path.yaml')
    
"""
    Responsible for loading PDF file paths from configuration.

    - Reads pdf_path.yaml
    - Resolves paths relative to project root
    - Validates file existence
    - Returns a list of absolute PDF paths
"""
class PathLoader:
    
    def __init__(self, config:PathLoaderConfig):
        self.config = config
    
    def load_pdf(self):
        """
        Load and validate PDF file paths from YAML configuration.

        Returns:
            List[str]: List of absolute PDF file paths
        """
        try:
            pdf_paths = []

            # Load yaml file
            with open(self.config.config_file_path, 'r', encoding="utf8") as f:
                docs = yaml.safe_load(f)

            # Load file paths from yaml file and store it in pdf_paths list
            for doc in docs:
                for path in docs[doc]:
                    full_path = os.path.normpath(os.path.join(BASE_DIR, path))

                    if not os.path.exists(full_path):
                        raise FileNotFoundError(f"PDF not found: {full_path}")

                    pdf_paths.append(full_path)

            return pdf_paths

        except Exception as e:
            raise CustomException(e, sys)
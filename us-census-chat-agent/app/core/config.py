import os
from dotenv import load_dotenv

# Load values from .env into environment variables
load_dotenv()


class Settings:
    def __init__(self) -> None:
        self.app_name = os.getenv("APP_NAME", "US Census Chat Agent")
        self.app_env = os.getenv("APP_ENV", "dev")

        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

        self.snowflake_user = os.getenv("SNOWFLAKE_USER", "")
        self.snowflake_password = os.getenv("SNOWFLAKE_PASSWORD", "")
        self.snowflake_account = os.getenv("SNOWFLAKE_ACCOUNT", "")
        self.snowflake_warehouse = os.getenv("SNOWFLAKE_WAREHOUSE", "")
        self.snowflake_database = os.getenv("SNOWFLAKE_DATABASE", "")
        self.snowflake_schema = os.getenv("SNOWFLAKE_SCHEMA", "")
        self.snowflake_role = os.getenv("SNOWFLAKE_ROLE", "")


settings = Settings()
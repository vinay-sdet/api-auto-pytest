import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    base_url: str
    username: str | None
    password: str | None

    @classmethod
    def from_environment(cls) -> "Settings":
        return cls(
            base_url=os.getenv(
                "API_BASE_URL", "https://restful-booker.herokuapp.com"
            ).rstrip("/"),
            username=os.getenv("API_USERNAME"),
            password=os.getenv("API_PASSWORD"),
        )

    def require_credentials(self) -> tuple[str, str]:
        if not self.username or not self.password:
            raise RuntimeError(
                "API_USERNAME and API_PASSWORD must be set in the environment or .env"
            )
        return self.username, self.password


settings = Settings.from_environment()

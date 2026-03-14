from app.core.config import Settings


def test_settings_build_database_url() -> None:
    settings = Settings()

    assert settings.database_url
    assert settings.api_v1_prefix == "/api/v1"

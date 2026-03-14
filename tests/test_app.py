from app.core.config import get_settings
from app.main import create_app


def test_create_app_sets_title() -> None:
    application = create_app()

    assert application.title == get_settings().app_name

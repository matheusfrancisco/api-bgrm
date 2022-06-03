from app.core.settings.app import AppSettings


class ProdAppSettings(AppSettings):

    DATABASE_URL: str

    class Config(AppSettings.Config):
        env_file = ".env"

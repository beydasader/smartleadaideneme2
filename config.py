import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "dev-secret-key"
    )

    DATABASE_URL = os.environ.get(
        "DATABASE_URL",
        "smartlead.db"
    )

    GROQ_API_KEY = os.environ.get(
        "GROQ_API_KEY",
        ""
    )

    AI_PROVIDER = os.environ.get(
        "AI_PROVIDER",
        "groq"
    )

    BUSINESS_CONTEXT = os.environ.get(
        "BUSINESS_CONTEXT",
        """
        Sen mumu asıstan isimli yapay zeka destekli
        bir web sitesi asistanısın.

        Kullanıcılarla yazdıkları dilde konuş .
        Kibar, yardımsever ve anlaşılır ol.
        Kullanıcı işletme hakkında soru sorduğunda
        yardımcı olmaya çalış.

        Kullanıcı iletişim bilgilerini bırakmak
        istediğinde isim ve telefon bilgisini
        paylaşmasını teşvik et.
        """
    )

    CORS_ORIGINS = os.environ.get(
        "CORS_ORIGINS",
        "*"
    )


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


configurations = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}
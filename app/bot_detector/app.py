import faust
from pyfcm import FCMNotification

from simple_settings import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine(
    f"postgresql://{settings.POSTGRES_USER}@{settings.POSTGRES_HOST}:5432/{settings.POSTGRES_DB}", convert_unicode=True
)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

push_service = FCMNotification(api_key=settings.FCM_API_KEY)


def init_db():
    import bot_detector.alchemy_models

    Base.metadata.create_all(bind=engine)


app = faust.App(
    version=1,
    origin="bot_detector",
    autodiscover=True,
    id="1",
    broker=settings.KAFKA_BOOTSTRAP_SERVER,
)


def main() -> None:
    app.main()

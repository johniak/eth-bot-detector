import asyncio

import faust
from pyfcm import FCMNotification
from simple_settings import settings
from tortoise import Tortoise


async def init_orm():
    await Tortoise.init(
        db_url=f"postgres://{settings.POSTGRES_USER}@{settings.POSTGRES_HOST}:5432/{settings.POSTGRES_DB}",
        modules={"bot_detector": ["bot_detector.models"]},
    )


def init_orm_async():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_orm())


push_service = FCMNotification(api_key=settings.FCM_API_KEY)

app = faust.App(
    version=1,
    origin="bot_detector",
    autodiscover=True,
    id="1",
    broker=settings.KAFKA_BOOTSTRAP_SERVER,
)


def main() -> None:
    app.main()


@app.on_configured.connect
def on_configured(app, conf, **kfargs):
    init_orm_async()


@app.on_before_shutdown.connect
async def on_before_shutdown(app, **kwargs):
    await Tortoise.close_connections()

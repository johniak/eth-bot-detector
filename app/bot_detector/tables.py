from simple_settings import settings

from bot_detector.app import app

block_table = app.Table(
    "blockTable",
    default=int,
    partitions=1
)

transactionsTable = app.Table(
    "transactionsTable",
    default=int,
).hopping(settings.WINDOW_SECONDS_SIZE, settings.WINDOW_SECONDS_SIZE / 2)

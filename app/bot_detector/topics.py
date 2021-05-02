from bot_detector.app import app
from bot_detector.faust_models import TransactionModel

blocks_topic = app.topic(
    "blocks_topic",
    key_type=bytes,
    value_type=int,
)

transactions_topic = app.topic(
    "transactions_topic",
    key_type=bytes,
    value_type=TransactionModel,
)



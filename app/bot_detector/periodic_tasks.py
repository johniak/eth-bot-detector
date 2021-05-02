import random


from bot_detector.app import app
from bot_detector.models import TransactionModel
from bot_detector.tables import block_table
from bot_detector.topics import transactions_topic, blocks_topic
from simple_settings import settings


# @app.timer(settings.CHECK_FOR_NEW_TRANSACTIONS_PERIOD)
# async def collect_last_block():
#     from web3 import Web3
#     w3 = Web3(Web3.HTTPProvider(settings.WEB3_HTTP_PROVIDER))
#     await blocks_topic.send(
#         value=w3.eth.block_number,
#     )


@app.timer(settings.CHECK_FOR_NEW_TRANSACTIONS_PERIOD)
async def collect_last_block():
    # from web3 import Web3
    # w3 = Web3(Web3.HTTPProvider(settings.WEB3_HTTP_PROVIDER))
    await blocks_topic.send(
        value=1234,
    )

    # await transactions_topic.send(
    #     value=TransactionModel(txn_hash="Ala12", from_address=f"Ala2", to_address="Ala3", value=random.randint(0, 20)),
    # )
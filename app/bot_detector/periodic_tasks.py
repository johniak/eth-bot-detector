from simple_settings import settings

from bot_detector.app import app
from bot_detector.topics import blocks_topic


@app.timer(settings.CHECK_FOR_NEW_TRANSACTIONS_PERIOD)
async def collect_last_block():
    from web3 import Web3

    w3 = Web3(Web3.HTTPProvider(settings.WEB3_HTTP_PROVIDER))
    await blocks_topic.send(
        value=w3.eth.block_number,
    )

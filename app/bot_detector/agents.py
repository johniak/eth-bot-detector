import logging

from simple_settings import settings

from bot_detector.app import app
from bot_detector.faust_models import TransactionModel
from bot_detector.models import BotNotification
from bot_detector.tables import transactions_table, block_table
from bot_detector.topics import transactions_topic, blocks_topic

logger = logging.getLogger(__name__)


@app.agent(blocks_topic)
async def process_blocks(blocks):
    from web3 import Web3

    w3 = Web3(Web3.HTTPProvider(settings.WEB3_HTTP_PROVIDER))
    async for block_number in blocks:
        if block_number in block_table:
            continue
        block_table[str(block_number)] = block_number
        block = w3.eth.get_block(block_number)
        for txn_hash in block.transactions:
            transaction = w3.eth.get_transaction(txn_hash)
            await transactions_topic.send(
                value=TransactionModel(
                    txn_hash=txn_hash.hex(),
                    from_address=transaction.get("from"),
                    to_address=transaction.get("to"),
                    value=transaction.get("value"),
                ),
            )


@app.agent(transactions_topic)
async def process_transactions(transactions):
    async for transaction in transactions.group_by(TransactionModel.from_address):
        transactions_table[transaction.from_address] += 1
        if (
            transactions_table[transaction.from_address].delta(settings.WINDOW_SECONDS_SIZE / 2)
            > settings.BOT_DETECTION_THRESHOLD
        ):
            await BotNotification.create__and_send_bot_notifications_for_address(transaction.from_address)
            logger.info(f"BOT DETECTED {transaction.from_address}")
        yield transaction

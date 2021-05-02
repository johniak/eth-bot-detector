from tortoise import Tortoise

from bot_detector.app import app


@app.command()
async def init_database():
    await Tortoise.generate_schemas()

from bot_detector.app import app, init_db


@app.command()
async def init_database():
    init_db()

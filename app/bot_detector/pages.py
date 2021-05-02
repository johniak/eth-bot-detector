import json

from faust.web import Request, Response, View

from bot_detector.app import app, push_service
from bot_detector.models import FcmToken


@app.page("/fcm-token/")
class FcmTokenPage(View):
    async def post(self, request: Request) -> Response:
        body = await request.json()
        token = body.get("token")
        if token is None:
            self.error(400, "Token was not provided")
        if await FcmToken.filter(token=token).exists():
            return self.json({"status": "ok", "already_exists": True})
        await FcmToken.create(token=token)

        push_service.notify_multiple_devices(
            registration_ids=[token],
            message_title="Push Notification",
            message_body="Your device is registered",
        )
        return self.json({"status": "ok", "already_exists": False})

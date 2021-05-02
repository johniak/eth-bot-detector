from faust.web import Request, Response, View

from bot_detector.alchemy_models import FcmToken, BotNotification
from bot_detector.app import app, push_service, db_session


@app.page("/fcm-token/")
class FcmTokenPage(View):
    async def post(self, request: Request) -> Response:
        body = await request.json()
        token = body.get("token")
        if token is None:
            self.error(400, "Token was not provided")
        print(BotNotification.query.join(BotNotification.fcm_token).filter(FcmToken.token.in_([token])).all())
        if FcmToken.query.filter_by(token=token).count() != 0:
            fcm_token = FcmToken.query.filter_by(token=token).first()
            db_session.add(BotNotification(fcm_token=fcm_token, from_address="0xD"))
            db_session.commit()
            return self.json({"status": "ok"})
        db_session.add(FcmToken(token=token))
        db_session.commit()

        # push_service.notify_multiple_devices(registration_ids=[token], message_title="win", message_body="win")
        return self.json({"count": 1})

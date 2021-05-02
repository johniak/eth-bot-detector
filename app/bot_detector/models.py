from datetime import datetime, timedelta

from simple_settings import settings
from tortoise.models import Model
from tortoise import fields
from tortoise.query_utils import Q

from bot_detector.app import push_service


class FcmToken(Model):
    id = fields.IntField(pk=True)
    token = fields.CharField(max_length=255)

    def __repr__(self):
        return f"{self.id}-{self.token}"

    def __str__(self):
        return f"{self.id}-{self.token}"


class BotNotification(Model):
    id = fields.IntField(pk=True)
    from_address = fields.CharField(max_length=255)
    fcm_token = fields.ForeignKeyField("bot_detector.FcmToken", related_name="notifications")
    created_at = fields.DatetimeField(auto_now_add=True)

    def __repr__(self):
        return f"{self.id}-{self.from_address}"

    @classmethod
    async def create__and_send_bot_notifications_for_address(cls, from_address):
        time_before = datetime.now() - timedelta(seconds=settings.SECONDS_TO_SEND_REMINDER_NOTIFICATION)
        tokens_to_exclude = await cls.filter(Q(from_address=from_address) & Q(created_at__gte=time_before)).values_list(
            "fcm_token__id", flat=True
        )
        tokens_for_new_notification = await FcmToken.exclude(id__in=tokens_to_exclude)
        bot_notifications = [cls(from_address=from_address, fcm_token=token) for token in tokens_for_new_notification]
        push_service.notify_multiple_devices(
            registration_ids=[token.token for token in tokens_for_new_notification],
            message_title="Bot detected",
            message_body=f"Bot with address {from_address} detected",
        )
        await cls.bulk_create(bot_notifications)

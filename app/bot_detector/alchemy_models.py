from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from bot_detector.app import Base


class FcmToken(Base):
    __tablename__ = "fcm_tokens"
    id = Column(Integer, primary_key=True)
    token = Column(String(255), unique=True)
    notifications = relationship(
        "BotNotification",
        back_populates="fcm_token",
    )

    def __init__(self, token=None):
        self.token = token

    def __repr__(self):
        return f"{self.id}-{self.token}"


class BotNotification(Base):
    __tablename__ = "bot_notifications"
    id = Column(Integer, primary_key=True)
    from_address = Column(String(255))
    fcm_token = relationship(
        "FcmToken",
        back_populates="notifications",
    )
    fcm_token_id = Column(Integer, ForeignKey("fcm_tokens.id"))

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, from_address=None, fcm_token=None):
        self.from_address = from_address
        self.fcm_token = fcm_token

    def __repr__(self):
        return f"{self.id}-{self.from_address}"

    @classmethod
    def generate_notifications_for_address(cls, from_address, tokens):
        cls.query.join(cls.fcm_token).filter_by(FcmToken.token._in(tokens))

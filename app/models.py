from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint

from .database import Base


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    keitaro_id = Column(Integer, unique=True, nullable=False)
    name = Column(String, nullable=False)
    geo = Column(String, nullable=False)
    offer_id = Column(Integer, nullable=False)
    domain = Column(String, nullable=False)
    group = Column(String, nullable=False)
    source = Column(String, nullable=False)


class Offer(Base):
    __tablename__ = "campaign_offers"
    __table_args__ = (UniqueConstraint("campaign_id", "offer_id"),)

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False, index=True)
    offer_id = Column(Integer, nullable=False)
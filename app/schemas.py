from pydantic import BaseModel, ConfigDict


class CampaignCreate(BaseModel):
    name: str
    geo: str
    offer_id: int
    domain: str
    group: str
    source: str


class CampaignOut(CampaignCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    keitaro_id: int


class OfferUpdate(BaseModel):
    add: list[int] = []
    remove: list[int] = []


class OffersOut(BaseModel):
    campaign_id: int
    keitaro_id: int
    offers: list[int]
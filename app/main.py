from fastapi import Depends, FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from . import models, schemas
from .database import get_db
from .keitaro import add_offers, create_campaign, remove_offers

app = FastAPI()

PREFIX = "test_vedernikova_"


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/campaigns", response_model=schemas.CampaignOut)
def create_campaign_endpoint(data: schemas.CampaignCreate, db: Session = Depends(get_db)):
    body = data.model_dump()
    body["name"] = PREFIX + body["name"]
    keitaro_id = create_campaign(body)

    campaign = models.Campaign(keitaro_id=keitaro_id, **body)
    db.add(campaign)
    db.commit()
    db.refresh(campaign)

    db.add(models.Offer(campaign_id=campaign.id, offer_id=campaign.offer_id))
    db.commit()
    return campaign


@app.patch("/campaigns/{campaign_id}/offers", response_model=schemas.OffersOut)
def update_offers(
    campaign_id: int,
    data: schemas.OfferUpdate,
    db: Session = Depends(get_db),
):
    campaign = db.query(models.Campaign).filter(models.Campaign.id == campaign_id).first()
    if campaign is None:
        raise HTTPException(status_code=404, detail="Campaign not found")

    rows = db.query(models.Offer).filter(models.Offer.campaign_id == campaign_id).all()
    existing = {row.offer_id for row in rows}

    if existing:
        final = (existing - set(data.remove)) | set(data.add)
        to_remove = existing - final
        to_add = final - existing
    else:
        initial = {campaign.offer_id}
        final = (initial - set(data.remove)) | set(data.add)
        to_remove = set()
        to_add = final

    for row in rows:
        if row.offer_id in to_remove:
            db.delete(row)

    for offer_id in sorted(to_add):
        db.add(models.Offer(campaign_id=campaign_id, offer_id=offer_id))

    if to_remove:
        remove_offers(campaign.keitaro_id, sorted(to_remove))
    if to_add:
        add_offers(campaign.keitaro_id, sorted(to_add))

    db.commit()

    return {
        "campaign_id": campaign.id,
        "keitaro_id": campaign.keitaro_id,
        "offers": sorted(final),
    }
app.mount("/", StaticFiles(directory="static", html=True), name="static")
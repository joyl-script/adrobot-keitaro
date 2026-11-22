import httpx

from .config import KEITARO_KEY, KEITARO_URL

FAKE_ID = 1001


def create_campaign(payload: dict) -> int:
    global FAKE_ID

    if not KEITARO_KEY:
        current = FAKE_ID
        FAKE_ID += 1
        return current

    url = KEITARO_URL.rstrip("/") + "/api/v1/campaigns"
    headers = {"Api-Key": KEITARO_KEY}
    response = httpx.post(url, json=payload, headers=headers, timeout=10)
    response.raise_for_status()
    return int(response.json()["id"])


def add_offers(keitaro_id: int, offer_ids: list[int]) -> None:
    if not KEITARO_KEY:
        return

    url = KEITARO_URL.rstrip("/") + f"/api/v1/campaigns/{keitaro_id}/offers"
    headers = {"Api-Key": KEITARO_KEY}
    response = httpx.post(url, json={"offer_ids": offer_ids}, headers=headers, timeout=10)
    response.raise_for_status()


def remove_offers(keitaro_id: int, offer_ids: list[int]) -> None:
    if not KEITARO_KEY:
        return

    url = KEITARO_URL.rstrip("/") + f"/api/v1/campaigns/{keitaro_id}/offers"
    headers = {"Api-Key": KEITARO_KEY}
    response = httpx.request(
        "DELETE",
        url,
        json={"offer_ids": offer_ids},
        headers=headers,
        timeout=10,
    )
    response.raise_for_status()
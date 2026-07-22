from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from models import get_db, Account, HouseItem, OwnedItem
from engine import yildiz_ver
from .security import get_current_account, get_profile_or_404

router = APIRouter(prefix="/api/house", tags=["house"])

CATEGORY_NAMES = {
    "mobilya": "Mobilya",
    "dekor": "Dekor",
    "ozel": "Özel",
    "nadir": "Nadir",
}


@router.get("")
def get_house(profile_id: str, acc: Account = Depends(get_current_account),
              db: Session = Depends(get_db)):
    p = get_profile_or_404(db, acc, profile_id)
    items = db.query(HouseItem).order_by(HouseItem.sort_order,
                                         HouseItem.price).all()
    owned = {r[0] for r in db.query(OwnedItem.item_id)
             .filter(OwnedItem.profile_id == p.id).all()}

    return {
        "star_balance": p.star_balance or 0,
        "owned_count": len(owned),
        "total_count": len(items),
        "items": [{
            "id": i.id, "name": i.name, "icon": i.icon,
            "category": i.category,
            "category_name": CATEGORY_NAMES.get(i.category, i.category),
            "price": i.price,
            "owned": i.id in owned,
            "affordable": (p.star_balance or 0) >= i.price,
        } for i in items],
    }


class BuyIn(BaseModel):
    profile_id: str
    item_id: str


@router.post("/buy")
def buy(body: BuyIn, acc: Account = Depends(get_current_account),
        db: Session = Depends(get_db)):
    p = get_profile_or_404(db, acc, body.profile_id)
    item = db.get(HouseItem, body.item_id)
    if item is None:
        raise HTTPException(404, "Eşya bulunamadı")

    if db.get(OwnedItem, (p.id, item.id)):
        raise HTTPException(400, "Bu eşya zaten senin!")

    if (p.star_balance or 0) < item.price:
        eksik = item.price - (p.star_balance or 0)
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            f"{eksik} yıldız daha lazım. Biraz daha oynayalım!",
        )

    yildiz_ver(db, p, -item.price, f"buy_item:{item.id}")
    db.add(OwnedItem(profile_id=p.id, item_id=item.id))
    db.commit()

    return {"ok": True, "item": {"id": item.id, "name": item.name,
                                 "icon": item.icon},
            "star_balance": p.star_balance}

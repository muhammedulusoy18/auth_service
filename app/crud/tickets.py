from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.events import Events
from app.schemas.tickets import TicketPurchaseCreate
from app.models.tickets import Tickets


def create_ticket_purchase(db: Session, user_id: int, event_id: int,ticket_data:TicketPurchaseCreate):
    event =db.query(Events).filter(Events.event_id == event_id).with_for_update().first()
    if not event:
        raise HTTPException(status_code=404, detail="Böyle bir etkinlik bulunamadı.")
    if event.quota < ticket_data.quantity :
        raise HTTPException(status_code=400, detail=f"Yetersiz kontenjan. Sadece {event.quota} adet bilet kaldı.")
    try:
        event.quota-=ticket_data.quantity
        new_ticket = Tickets(
            event_id=event_id,
            user_id=user_id,
            quantity=ticket_data.quantity,
            purchase_date = datetime.utcnow()
        )
        db.add(new_ticket)
        db.commit()
        db.refresh(new_ticket)
        return new_ticket
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Bilet satın alırken sistemsel {e} hatası oluştu.")

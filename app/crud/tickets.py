from datetime import datetime

import background_tasks
import uuid
from fastapi import HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.email_service import send_ticket_confirmation_mail
from app.models.events import Events
from app.schemas.tickets import TicketPurchaseCreate
from app.models.tickets import Tickets
from app.db.database import SessionLocal


def create_ticket_purchase(background_tasks: BackgroundTasks, db: Session, user_id: int, event_id: int,ticket_data:TicketPurchaseCreate):
    user_email = None
    with SessionLocal() as auth_db:
        user = auth_db.query(User).filter(User.id == user_id).first()
        if user:
            user_email = user.email
    if not user_email:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı.")
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
            purchase_date = datetime.now(),
            ticket_uuid=str(uuid.uuid4())
        )
        db.add(new_ticket)
        db.commit()
        db.refresh(new_ticket)

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Bilet satın alırken sistemsel {e} hatası oluştu.")

    ticket_info={
        "event_name":event.event_name,
        "event_id":event.event_id,
        "ticket_id":new_ticket.ticket_id,
        "ticket_uuid": new_ticket.ticket_uuid,
        "quantity":new_ticket.quantity,
        "purchase_date":new_ticket.purchase_date.strftime("%d/%m/%Y %H:%M")
    }
    background_tasks.add_task(send_ticket_confirmation_mail, user_email, ticket_info)
    return new_ticket
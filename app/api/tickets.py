from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.auth import get_current_user

from app.schemas.tickets import TicketPurchaseCreate
from app.crud.tickets import create_ticket_purchase
from app.models.user import User
from app.db.eventsDb import get_Eventdb
router = APIRouter(
    prefix="/tickets",
    tags=["Bilet İşlemleri"]
)



@router.post("/buy/{event_id}")
def buy_ticket(
    event_id: int,
    ticket_data: TicketPurchaseCreate,
    db: Session = Depends(get_Eventdb),
    current_user: User = Depends(get_current_user) ):
    user_id= current_user.id

    purchased_ticket = create_ticket_purchase(
        db=db,
        event_id=event_id,
        user_id=user_id,
        ticket_data=ticket_data
    )

    return purchased_ticket
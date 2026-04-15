from datetime import datetime
from typing import Optional
from app.schemas.events import EventResponse, EventShort
from pydantic import BaseModel, Field, ConfigDict


class TicketPurchaseCreate(BaseModel):
    quantity: int=Field(...,gt=0,description="Satın alınmak istenen bilet adedi")
class TicketResponse(BaseModel):
    ticket_id: int
    event_id: int
    quantity: int
    is_used: bool
    purchase_date: datetime
    event: Optional[EventShort] = None
    model_config = ConfigDict(from_attributes=True)


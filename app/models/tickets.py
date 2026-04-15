from app.db.eventsDb import Base
from sqlalchemy import Column, Integer, ForeignKey, DateTime
class Tickets(Base):

    __tablename__ = "tickets"
    ticket_id=Column(Integer,primary_key=True)
    event_id=Column(Integer, ForeignKey("events.event_id"),nullable=False)
    user_id=Column( Integer,nullable=False)
    purchase_date=Column(DateTime,nullable=False)
    quantity=Column(Integer,nullable=False)

import enum
from ..base import BaseModel
from ...extensions import db


class WeekDay(enum.Enum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"


class BusinessHour(BaseModel):
    """
    Gère les plages horaires d'ouverture et de fermeture par jour pour un commerce.
    """

    __tablename__ = "business_hours"

    # ------------------------------------------------------------------
    # Informations générales
    # ------------------------------------------------------------------

    day = db.Column(
        db.Enum(WeekDay), 
        nullable=False, 
        index=True
    )
    
    # Format "HH:MM" (ex: "08:00")
    opening_time = db.Column(
        db.String(5), 
        nullable=True
    )
    
    closing_time = db.Column(
        db.String(5), 
        nullable=True
    )
    
    is_closed = db.Column(
        db.Boolean, 
        default=False, 
        nullable=False
    )

    # ------------------------------------------------------------------
    # Relations
    # ------------------------------------------------------------------

    business_id = db.Column(
        db.Integer, 
        db.ForeignKey("businesses.id", ondelete="CASCADE"), 
        nullable=False, 
        index=True
    )
    
    business = db.relationship(
        "Business", 
        back_populates="hours"
    )

    def __repr__(self):
        status = "Fermé" if self.is_closed else f"{self.opening_time} - {self.closing_time}"
        return f"<BusinessHour {self.day.value}: {status}>"

    def to_dict(self):
        return {
            "id": self.id,
            "day": self.day.value if self.day else None,
            "opening_time": self.opening_time,
            "closing_time": self.closing_time,
            "is_closed": self.is_closed,
            "business_id": self.business_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
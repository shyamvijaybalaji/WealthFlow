from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Investment(Base):
    __tablename__ = "investments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    asset_type = Column(String, nullable=False)  # stock, crypto, bond, etf, mutual_fund
    symbol = Column(String, nullable=False)  # Ticker symbol

    # CRITICAL: Use Numeric for precision
    quantity = Column(Numeric(precision=20, scale=8), nullable=False)  # High precision for crypto
    purchase_price = Column(Numeric(precision=15, scale=2), nullable=False)
    current_price = Column(Numeric(precision=15, scale=2), nullable=True)

    purchase_date = Column(DateTime, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="investments")

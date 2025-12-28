from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime, ARRAY, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True, index=True)

    # CRITICAL: Use Numeric for currency precision
    amount = Column(Numeric(precision=15, scale=2), nullable=False)

    description = Column(String, nullable=False)
    merchant = Column(String, nullable=True)
    transaction_type = Column(String, nullable=False)  # income, expense, transfer
    transaction_date = Column(DateTime, nullable=False, index=True)

    # PostgreSQL ARRAY for tags
    tags = Column(ARRAY(String), nullable=True)
    notes = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="transactions")
    account = relationship("Account", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")

# db/session.py 
# SQLAlchemy 

from datetime import datetime
from sqlalchemy.types import String,  Float, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass


class PresidentPredictionDB(Base):
    
    __tablename__ = 'president_prediction'
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    timestamp: Mapped[int] = mapped_column(Integer, nullable=False)
    democratic: Mapped[float] = mapped_column(Float, nullable=False)
    trump: Mapped[float] = mapped_column(Float, nullable=False)
    other: Mapped[float] = mapped_column(Float, nullable=False)
    state: Mapped[str] = mapped_column(String(50), nullable=False)


    def __repr__(self):
        return f'{self.id} {self.date} {self.timestamp} {self.democratic} {self.trump} {self.other} {self.state}'


class SenatePredictionDB(Base):
    __tablename__ = 'senate_prediction'


    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    timestamp: Mapped[int] = mapped_column(Integer, nullable=False)
    candidate_1: Mapped[float] = mapped_column(Float, nullable=False)
    candidate_1_name: Mapped[str] = mapped_column(String(100), nullable=False)
    candidate_2: Mapped[float] = mapped_column(Float, nullable=False)
    candidate_2_name: Mapped[str] = mapped_column(String(100), nullable=False)
    other: Mapped[float] = mapped_column(Float, nullable=False)
    state: Mapped[str] = mapped_column(String(50), nullable=False)


    def __repr__(self):
        return f'{self.id} {self.date} {self.timestamp} {self.candidate_1} {self.candidate_1_name} {self.candidate_2} {self.candidate_2_name} {self.other} {self.state}'
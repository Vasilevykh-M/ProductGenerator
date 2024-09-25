from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base

engine = create_engine('postgresql://postgres@localhost/generationApp')

Base = declarative_base()


class Promt(Base):
    __tablename__ = "promt"

    id = Column(Integer, primary_key=True)
    name_object = Column(String(255), nullable=False)
    promt = Column(String(255), nullable=False)
    scale = Column(Integer, nullable=False)
    y_pos = Column(Integer, nullable=False)
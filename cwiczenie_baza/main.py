import random
from datetime import datetime
from sqlalchemy import func
from sqlalchemy import Table

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    create_engine,
    select,
)
from sqlalchemy.orm import Session, declarative_base, relationship


Base = declarative_base()

experiment_subject = Table(
    "experiment_subject",
    Base.metadata,
    Column("experiment_id", Integer, ForeignKey("experiments.id"), primary_key=True),
    Column("subject_id", Integer, ForeignKey("subjects.id"), primary_key=True),
)


class Experiment(Base):
    __tablename__ = "experiments"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    type = Column(Integer, nullable=False)
    finished = Column(
        Boolean,
        default=False,
        server_default="0",
        nullable=False,
    )

    data_points = relationship("DataPoint", back_populates="experiment")

    subjects = relationship(
        "Subject",
        secondary=experiment_subject,
        back_populates="experiments",
    )


class DataPoint(Base):
    __tablename__ = "data_points"

    id = Column(Integer, primary_key=True)
    real_value = Column(Float, nullable=False)
    target_value = Column(Float, nullable=False)
    experiment_id = Column(
        Integer,
        ForeignKey("experiments.id"),
        nullable=False,
    )

    experiment = relationship("Experiment", back_populates="data_points")


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True)
    gdpr_accepted = Column(
        Boolean,
        default=False,
        server_default="0",
        nullable=False,
    )

    experiments = relationship(
        "Experiment",
        secondary=experiment_subject,
        back_populates="subjects",
    )


engine = create_engine("sqlite:///experiments.db")


if __name__ == "__main__":
    with Session(engine) as session:
        zapytanie = (
            select(
                Experiment.id,
                Experiment.title,
                func.sum(DataPoint.real_value),
                func.avg(DataPoint.real_value),
                func.sum(DataPoint.target_value),
                func.avg(DataPoint.target_value),
            )
            .join(Experiment.data_points)
            .group_by(Experiment.id, Experiment.title)
            .order_by(Experiment.id)
        )

        wyniki = session.execute(zapytanie).all()

        for numer, tytul, suma_real, srednia_real, suma_target, srednia_target in wyniki:
            print(f"{tytul} (id: {numer})")
            print(f"real_value: suma={suma_real:.4f}, średnia={srednia_real:.4f}")
            print(f"target_value: suma={suma_target:.4f}, średnia={srednia_target:.4f}")
            print()
            
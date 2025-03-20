from sqlalchemy import create_engine, Column, String, Integer, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import Config
from app.database import Base, get_db_connection, engine

Base = declarative_base()

class ScheduledTask(Base):
    """_summary_
    scheduler_type: interval or crontab
        - For interval type, store a JSON like {"days": 0, "hours": 20, "minutes": 0, "seconds": 0}
        - For crontab type, store a JSON like {"minute": "0", "hour": "20", "day_of_week": "*", "day_of_month": "*", "month_of_year": "*"}
    """
    __tablename__ = 'scheduled_tasks'
    
    id = Column(Integer, primary_key=True)
    scheduler_type = Column(String, nullable=False, default='interval')
    schedule_params = Column(JSON, nullable=False)
    task_function = Column(String, nullable=False)
    args = Column(JSON, nullable=True)

# Database engine and session
Base.metadata.create_all(engine)

if __name__ == "__main__":
    session = get_db_connection()

    # Create a new scheduled task
    new_task = ScheduledTask(
        scheduler_type='interval',
        schedule_params={"days": 0, "hours": 0, "minutes": 1, "seconds": 0},
        task_function='send_email',
        args=["arg1"]  # Replace with actual arguments if any
    )
    
    new_task_1 = ScheduledTask(
        scheduler_type='crontab',
        schedule_params={"minute": "48", "hour": "1", "day_of_week": "*", "day_of_month": "*", "month_of_year": "*"},
        task_function='send_email',
        args=["arg1"]  # Replace with actual arguments if any
    )

    # Add the new task to the session and commit
    session.add(new_task)
    session.add(new_task_1)
    session.commit()

    # Close the session
    session.close()

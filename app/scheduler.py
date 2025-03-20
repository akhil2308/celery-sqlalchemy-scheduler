import logging
from datetime import timedelta, datetime
from celery.beat import Scheduler, ScheduleEntry
from celery.schedules import schedule, crontab
from app.models import ScheduledTask
from app.database import get_db_connection
from app.config import Config

class SQLAlchemyScheduler(Scheduler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """
        Combined Sync:

            sync_every = 300 and sync_every_tasks = 10.

            Syncs every 5 minutes or after 10 tasks, whichever comes first.
        """ 
        #: How often to sync the schedule (3 minutes by default)
        self.sync_every = Config.SCHEDULER_SYNC_EVERY
        #: How many tasks can be called before a sync is forced.
        # self.sync_every_tasks = None
        logging.info("SQLAlchemyScheduler initialized.")
        
    def _get_next_run_time(self, entry):
        """Calculate the next run time for a ScheduleEntry."""
        is_due, next_time_to_run = entry.schedule.is_due(entry.last_run_at)
        next_run_time = datetime.now() + timedelta(seconds=next_time_to_run)
        return next_run_time

    def sync(self):
        logging.info("Syncing schedule with database...")
        session = get_db_connection()
        try:
            db_tasks = session.query(ScheduledTask).all()
            current_ids = {task.id for task in db_tasks}
            logging.info("Found %d task(s) in DB", len(db_tasks))

            # Remove schedule entries that no longer exist in the DB.
            for entry_name in list(self.schedule.keys()):
                try:
                    task_id = int(entry_name.split('_')[-1])
                except ValueError:
                    task_id = None
                if task_id not in current_ids:
                    self.schedule.pop(entry_name, None)
                    logging.info("Removed schedule entry: %s (not in DB)", entry_name)

            # Process each task from the DB.
            for task in db_tasks:
                entry_name = f"{task.task_function}_{task.id}"
                logging.info("Processing task: %s with scheduler type: %s", entry_name, task.scheduler_type)

                if task.scheduler_type == 'interval':
                    try:
                        delta = timedelta(**task.schedule_params)
                    except Exception as e:
                        logging.error("Error parsing interval schedule_params for task %s: %s", entry_name, e)
                        continue
                    sched = schedule(delta)
                    logging.info("Interval schedule for %s set to %s", entry_name, delta)
                elif task.scheduler_type == 'crontab':
                    try:
                        sched = crontab(**task.schedule_params)
                    except Exception as e:
                        logging.error("Error parsing crontab schedule_params for task %s: %s", entry_name, e)
                        continue
                    logging.info("Crontab schedule for %s set with parameters %s", entry_name, task.schedule_params)
                else:
                    logging.error("Unknown scheduler type for task %s: %s", entry_name, task.scheduler_type)
                    continue

                task_args = tuple(task.args) if task.args else ()

                if entry_name not in self.schedule:
                    new_entry = ScheduleEntry(
                        name=entry_name,
                        task=task.task_function,
                        schedule=sched,
                        args=task_args,
                        kwargs={},
                        options={},
                        last_run_at=None,
                    )
                    self.schedule[entry_name] = new_entry
                    logging.info("Added new schedule entry: %s", entry_name)
                    
                    # Use helper method to get next_run_time (not working as intended)
                    # next_run_time = self._get_next_run_time(new_entry)
                    # logging.info(f"Next run time for {entry_name}: {next_run_time}")
                    
                else:
                    existing_entry = self.schedule[entry_name]
                    existing_entry.schedule = sched
                    existing_entry.args = task_args
                    logging.info("Updated schedule entry: %s", entry_name)
                    
                    # Use helper method to get next_run_time (not working as intended)
                    # next_run_time = self._get_next_run_time(existing_entry)
                    # logging.info(f"Next run time for {entry_name}: {next_run_time}")
                
        except Exception as e:
            logging.error("Error during sync: %s", e)
        finally:
            session.close()

        return self.schedule

# Celery SQLAlchemy Scheduler

A custom Celery Beat scheduler with SQLAlchemy integration for managing periodic tasks in a database. This project provides a production-ready Celery project structure with support for interval and crontab schedules.

---

## Features

- **Custom Scheduler**: Extends Celery Beat to use SQLAlchemy for storing and managing periodic tasks.
- **Database Backed**: Tasks are stored in a PostgreSQL database (or any SQLAlchemy-supported database).
- **Supports Interval and Crontab Schedules**: Easily configure tasks to run at fixed intervals or using cron-like schedules.
- **Production-Ready Structure**: Includes a well-organized project structure for scaling and maintenance.
- **Timezone Support**: Fully timezone-aware for accurate task scheduling.

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/akhil2308/celery-sqlalchemy-scheduler.git
   cd celery-sqlalchemy-scheduler
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables**:
   - Copy `.env.example` to `.env` and update the values.
   - Run `source set_env.sh` to load the environment variables.

---

## Usage

1. **Start the Celery Worker**:
   ```bash
   ./run_worker.sh
   ```

2. **Start the Celery Beat Scheduler**:
   ```bash
   ./run_beat.sh
   ```

3. **Add Tasks to the Database**:
   - Use SQLAlchemy to insert tasks into the `scheduled_tasks` table.
   - Example:
     ```sql
     INSERT INTO scheduled_tasks (scheduler_type, schedule_params, task_function, args)
     VALUES (
         'interval',
         '{"minutes": 1}',
         'app.tasks.email_tasks.send_email',
         '["arg1", "arg2"]'
     );
     ```

---

## Configuration

- **Celery Settings**: Update `app/celery_app.py` to configure the broker, backend, and timezone.
- **Database Settings**: Update `app/config.py` to configure the database connection.
- **Environment Variables**: Use `.env` or `set_env.sh` to set sensitive configuration values.

---

## Contributing

Contributions are welcome! Please read the [CONTRIBUTORS.txt](CONTRIBUTORS.txt) file for guidelines.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- [Celery](https://docs.celeryq.dev/) for the task queue framework.
- [SQLAlchemy](https://www.sqlalchemy.org/) for database integration.

---
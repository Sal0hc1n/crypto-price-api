from apscheduler.schedulers.background import BackgroundScheduler
from bot import crud
from bot.job import user_job


scheduler = BackgroundScheduler()
scheduler.start()


def add_job(chat_id):
    user = crud.get_user(chat_id)
    if not user.run:
        job = scheduler.add_job(user_job, 'interval', [chat_id], seconds=user.interval)
        crud.update_job_id(chat_id, job.id)
        crud.update_run(chat_id, True)


def remove_job(chat_id):
    user = crud.get_user(chat_id)
    if user.run:
        job = scheduler.get_job(user.job_id)
        if job:
            scheduler.remove_job(user.job_id)
        crud.update_job_id(chat_id, None)
        crud.update_run(chat_id, False)

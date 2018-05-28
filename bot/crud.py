from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, exists, Boolean, Float
from bot import coin

from bot.config import AppConfig
from bot import engine, Session, scheduler


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    chat_id = Column(Integer, primary_key=True)
    value = Column(Float)
    overweight = Column(Integer)
    interval = Column(Integer)
    diff = Column(Integer)
    run = Column(Boolean)
    job_id = Column(String)
    min_value = Column(Integer)
    max_value = Column(Integer)


Base.metadata.create_all(engine)


def db_session(fn):
    session = Session()

    def wrapped(*args, **kwargs):
        fn(*args, **kwargs)
    wrapped.session = session
    session.close()
    return wrapped


@db_session
def create_user(chat_id):
    (ret, ) = create_user.session.query(exists().where(User.chat_id == chat_id))
    if not ret[0]:
        user = User(chat_id=chat_id,
                    value=coin.get_current_value(),
                    overweight=AppConfig.overweight,
                    interval=AppConfig.interval,
                    diff=AppConfig.diff,
                    run=False,
                    min_value=AppConfig.min_value,
                    max_value=AppConfig.max_value)
        update_user(user, create_user.session)


@db_session
def update_overweight(chat_id, overweight):
    user = get_user(chat_id)
    user.overweight = overweight
    update_user(user, update_overweight.session)


@db_session
def update_interval(chat_id, interval):
    user = get_user(chat_id)
    user.interval = interval
    update_user(user, update_interval.session)


@db_session
def update_run(chat_id, run):
    user = get_user(chat_id)
    user.run = run
    update_user(user, update_run.session)


@db_session
def update_diff(chat_id, diff):
    user = get_user(chat_id)
    user.diff = diff
    update_user(user, update_diff.session)


@db_session
def update_job_id(chat_id, job_id):
    user = get_user(chat_id)
    user.job_id = job_id
    update_user(user, update_job_id.session)


@db_session
def update_min_value(chat_id, min_value):
    user = get_user(chat_id)
    user.min_value = min_value
    update_user(user, update_min_value.session)


@db_session
def update_value(chat_id, value):
    user = get_user(chat_id)
    user.value = value
    update_user(user, update_value.session)


@db_session
def update_max_value(chat_id, max_value):
    user = get_user(chat_id)
    user.max_value = max_value
    update_user(user, update_max_value.session)


def get_user(chat_id):
    session = Session()
    user = session.query(User).filter_by(chat_id=chat_id).first()
    session.close()
    return user


def update_user(user, session):
    session.add(user)
    session.commit()


def clear_users():
    session = Session()
    users = session.query(User).all()
    running_users = []
    for user in users:
        user.job_id = None
        if user.run:
            user.run = False
            running_users.append(user.chat_id)
    session.add_all(users)
    session.commit()
    for user_chat_id in running_users:
        scheduler.add_job(user_chat_id)

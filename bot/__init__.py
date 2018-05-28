from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


sqlite_file = "bot.db"

engine = create_engine("sqlite:///"+sqlite_file, echo=False)
Session = sessionmaker(bind=engine)

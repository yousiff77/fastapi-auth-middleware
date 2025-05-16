from sqlmodel import SQLModel, Field, create_engine, Session, select
import hashlib

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    password_hash: str

sqlite_url = "sqlite:///./users.db"
engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_user_by_username(username: str) -> User | None:
    with Session(engine) as session:
        statement = select(User).where(User.username == username)
        return session.exec(statement).first()

def verify_user(username: str, password: str) -> bool:
    user = get_user_by_username(username)
    if not user:
        return False
    return user.password_hash == hashlib.sha256(password.encode()).hexdigest()

def create_user(username: str, password: str):
    hashed = hashlib.sha256(password.encode()).hexdigest()
    new_user = User(username=username, password_hash=hashed)
    with Session(engine) as session:
        session.add(new_user)
        session.commit()

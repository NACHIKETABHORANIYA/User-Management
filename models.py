from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, UniqueConstraint

# DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"
# DATABASE_URL = "mysql+asyncmy://user:password@localhost/dbname"
# DATABASE_URL = "mysql+asyncmy://localhost:27017"
DATABASE_URL = "mysql+asyncmy://root:root@localhost:3306/user_management"

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


class User(Base):
    """
    user model with alll the required fields
    """

    __tablename__ = "users"
    __table_args__ = (UniqueConstraint('company_name', 'email', 'first_name', 'last_name', 'mobile_number', 'dob',
                                       name='uix_user'),)

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(100), nullable=True)
    email = Column(String(100), nullable=True)
    password = Column(String(100), nullable=True)
    first_name = Column(String(30))
    last_name = Column(String(30))
    mobile_number = Column(String(10), nullable=True)
    dob = Column(String(20), nullable=True)
    hashtag = Column(String(50), nullable=True)

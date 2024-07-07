from fastapi import Depends, HTTPException, status, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from models import Base, engine, SessionLocal
from schemas import UserInDB, UserManage
from utils import get_user_by_id, create_user, update_user, delete_user

app = FastAPI()


async def get_db():
    """
    function to get DB instance
    :return: DB Object instance
    :rtype: class
    """
    async with SessionLocal() as session:
        yield session


@app.on_event("startup")
async def on_startup():
    """
    function create model in database on startup
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.post("/users/", response_model=UserInDB)
async def create_user_endpoint(user: UserManage, db: AsyncSession = Depends(get_db)):
    """

    :param user: schema class for create user endpoint
    :type user: class
    :param db: DB session using connection string
    :type db: Database instance
    :return: new created user
    :rtype: dict
    """
    try:
        db_user = await create_user(db, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return db_user


@app.get("/users/{user_id}", response_model=UserInDB)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """

    :param user_id: id of the user to fetch details
    :type user_id: int
    :param db: DB session using connection string
    :type db: Database instance
    :return: specific user details
    :rtype: dict
    """
    db_user = await get_user_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.put("/users/{user_id}", response_model=UserInDB)
async def update_user_endpoint(user_id: int, user: UserManage, db: AsyncSession = Depends(get_db)):
    """

    :param user_id: id of the user to fetch details
    :type user_id: int
    :param user: schema class for create user endpoint
    :type user: class
    :param db: DB session using connection string
    :type db: Database instance
    :return: updated user detail
    :rtype: dict
    """
    try:
        db_user = await update_user(db, user_id, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.delete("/users/{user_id}", response_model=UserInDB)
async def delete_user_endpoint(user_id: int, db: AsyncSession = Depends(get_db)):
    """

    :param user_id: id of the user to fetch details
    :type user_id: int
    :param db: DB session using connection string
    :type db: Database instance
    :return: deleted user detail
    :rtype: dict
    """
    db_user = await delete_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

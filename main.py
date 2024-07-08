import os

from dotenv import load_dotenv
from fastapi import BackgroundTasks
from fastapi import Depends, HTTPException, FastAPI
from fastapi_mail import ConnectionConfig, MessageSchema, FastMail
from jinja2 import Environment, FileSystemLoader
from sqlalchemy.ext.asyncio import AsyncSession

from models import Base, engine, SessionLocal
from schemas import UserInDB, UserManage, SendEmailRequest, SendEmailResponse
from utils import get_user_by_id, create_user, update_user, delete_user

load_dotenv(override=True)

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
async def user_create(user: UserManage, db: AsyncSession = Depends(get_db)):
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
async def user_update(user_id: int, user: UserManage, db: AsyncSession = Depends(get_db)):
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
async def user_delete(user_id: int, db: AsyncSession = Depends(get_db)):
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


@app.post(
    "/send_mail",
    response_model=SendEmailResponse,
)
async def send_invitation_email(
        send_email_payload: SendEmailRequest,
        background_tasks: BackgroundTasks,
):
    """
    Endpoint to send an invitation email

    :param background_tasks: To make the email sending as background task
    """
    TEMPLATES_DIR = {os.getcwd()}
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    template = env.get_template("template.html.j2")

    MAIL_CONF = ConnectionConfig(
        MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
        MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
        MAIL_FROM=os.getenv("MAIL_FROM"),
        MAIL_PORT=587,
        MAIL_SERVER="smtp.gmail.com",
        USE_CREDENTIALS=True,
        MAIL_STARTTLS=True,
        MAIL_SSL_TLS=False
    )

    html_content = template.render(
        redoc_link=os.getenv("REDOC_URL"),
    )

    message = MessageSchema(
        subject="Invitation to View API Documentation by Nachiketa Bhoraniya",
        recipients=send_email_payload.list_of_users,
        body=html_content,
        subtype="html"
    )

    fastapi_mail = FastMail(MAIL_CONF)

    await fastapi_mail.send_message(message)

    return {"message": "Email sent successfully"}
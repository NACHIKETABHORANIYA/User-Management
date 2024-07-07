from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from schemas import UserManage


async def get_user_by_id(db: AsyncSession, user_id=None):
    """
    function to fetch user details by id

    :param db: DB session using connection string
    :type db: Database instance
    :param user_id: id of the user to fetch details
    :type user_id: int
    :return: specific user detail
    :rtype: object
    """
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalars().first()


async def get_user(db: AsyncSession, company_name=None, email=None, first_name=None, last_name=None,
                   mobile_number=None, dob=None):
    """
    function to fetch user detail

    :param db: DB session using connection string
    :type db: Database instance
    :param company_name: name of the company of user
    :type company_name: str
    :param email: email of the company of user
    :type email: str
    :param first_name: first name of the company of user
    :type first_name: str
    :param last_name: last of the company of user
    :type last_name: str
    :param mobile_number: mobile number of the company of user
    :type mobile_number: str
    :param dob: date of birth of the company of user
    :type dob: str
    :return: specific user detail
    :rtype: object
    """
    result = await db.execute(
        select(User).filter(User.company_name == company_name, User.email == email, User.first_name == first_name,
                            User.last_name == last_name, User.mobile_number == mobile_number, User.dob == dob))
    return result.scalars().first()


async def create_user(db: AsyncSession, user: UserManage):
    """
    function to create user

    :param db: DB session using connection string
    :type db: Database instance
    :param user: schema class for create user endpoint
    :type user: class
    :return: new created user detail
    :rtype: dict
    """
    obj = await get_user(db=db, company_name=user.company_name, email=user.email, dob=user.dob,
                         first_name=user.first_name, last_name=user.last_name,
                         mobile_number=user.mobile_number)

    if obj:
        raise ValueError("User already exist")

    db_user = User(
        company_name=user.company_name,
        email=user.email,
        dob=user.dob,
        password=user.password,
        first_name=user.first_name,
        last_name=user.last_name,
        mobile_number=user.mobile_number
    )
    db.add(db_user)

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ValueError("Some Exception occurred")

    await db.refresh(db_user)
    return db_user


async def update_user(db: AsyncSession, user_id: int, user_update: UserManage):
    """
    function to update user detail

    :param db: DB session using connection string
    :type db: Database instance
    :param user_id: id of the user to fetch details
    :type user_id: int
    :param user_update: schema class for create user endpoint
    :type user_update: class
    :return: updated user detail
    :rtype: dict
    """
    user = await get_user_by_id(db, user_id)

    if user:
        user.company_name = user_update.company_name
        user.first_name = user_update.first_name
        user.last_name = user_update.last_name
        user.email = user_update.email
        user.mobile_number = user_update.mobile_number
        user.dob = user_update.dob
        user.password = user_update.password

        try:
            await db.commit()
        except IntegrityError:
            await db.rollback()
            raise ValueError("Some Exception Occurred")
        await db.refresh(user)

    return user


async def delete_user(db: AsyncSession, user_id: int):
    """
    function to delete existing user

    :param db: DB session using connection string
    :type db: Database instance
    :param user_id: id of the user to fetch details
    :type user_id: int
    :return: detail of deleted user
    :rtype: dict
    """
    user = await get_user_by_id(db, user_id)
    if user:
        await db.delete(user)
        await db.commit()
    return user

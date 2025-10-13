from sqlalchemy import Column, Date, Integer, Sequence, String

import db

class User(db.connectionBase()):
    __tablename__ = 'users'

    # id: int = Field(default=None, nullable=False,Identity(start=1), primary_key=True)
    id = Column(Integer, Sequence('user_id_seq', start=1), primary_key=True)
    fullName = Column(String)
    email = Column(String, unique=True)
    createdAt = Column(Date)

async def createUser(user: list) -> User:
    try:
        # new_user = User(username='john_doe', email='john@example.com')
        await db.dbSession().add(user)
        db.dbSession().commit()
    except:
        db.dbSession().rollback()  # Rollback if there's an error
    finally:
        db.dbSession().close()  # Always close the session

async def queryAllUser():
    try:
        # result = db.dbConn.execute("SELECT * FROM users WHERE email=:email", {'email': 'john@example.com'}) //parameterized query
        # for row in result:
        # print(row)

        users = await db.dbSession().query(User).all()
        return users
    except:
        db.dbSession().rollback()  # Rollback if there's an error
    finally:
        db.dbSession().close()  # Always close the session

async def updateUser(**kwargs):
    try:
        user_to_update = await db.dbSession().query(User).filter_by(kwargs).first()
        user_to_update.email = 'john_doe@example.com'

        db.dbSession().commit()
    except: 
        db.dbSession().rollback()  # Rollback if there's an error
    finally:
        db.dbSession().close()  # Always close the session

async def deleteUser(user_id: int):
    try:
        user_to_delete = await db.dbSession().query(User).filter_by(id = user_id).first()
        db.dbSession().delete(user_to_delete)
        db.dbSession().commit()
    except:
        db.dbSession().rollback()  # Rollback if there's an error
    finally:
        db.dbSession().close()  # Always close the session


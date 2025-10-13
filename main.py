# import uvicorn
from fastapi.responses import HTMLResponse, RedirectResponse
from frontend import init
from fastapi import FastAPI #Depends, HTTPException

# from sqlmodel import select
# from sqlmodel import Session, select

# from apis.db import get_session, init_db
# from apis.userModel import User

app = FastAPI()

# @app.liespan("startup")
# def on_startup():
#     init_db()

@app.get('/')
def read_root():
    return {"message": "Welcome to HRMkit! Visit /hrmkit for the application."}
init(app)

# @app.post("/users")
# def add_song(user: User, session: Session = Depends(get_session)):
#     _user = User(name=song.name, artist=song.artist)
#     session.add(_user)
#     session.commit()
#     session.refresh(_user)
#     return _user

# result = engine.execute("SELECT * FROM users WHERE email=:email", {'email': 'john@example.com'})
# for row in result:
#     print(row)

# @app.get("/users/{user_id}", response_model=User)
# def read_user(user_id: int, session: Session = Depends(get_session)):
#     user = session.get(User, user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user

if __name__ == '__main__':
    # uvicorn.run('main:fastapi_app', log_level='info', reload=True)
    print('Please start the app with the "uvicorn" command as shown in the start.sh script')
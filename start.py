import os
from fastapi import FastAPI, Request
import google_auth_oauthlib.flow
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from cryptography.fernet import Fernet
from db import User, Session, engine, Base, Task
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request as GoogleRequest
import json
from pydantic import BaseModel
from shared.utilis import get_credentials
import datetime as dt

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'



app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="AQ16TpRoS1IexgkPXMTqDPDpfwa06ItQGOh3RsAUkC4=")

# Create database tables
Base.metadata.create_all(bind=engine)

fernetKey = 'iFUkpeJ4yJn_UXLEbMO7GBvpidj_Ailtb59OXxfCMqU='



# Add these imports
from services.auth.routers.auth_router import auth_router
from test_endpoints import test_router

# Add these lines to include the routers
app.include_router(auth_router, prefix="/api")
app.include_router(test_router)








# @app.post("/create_task")
# def create_task(task_data: TaskCreate):
#     session = Session()
#     user = session.query(User).filter(User.name == "Yazeed").first()
    
#     if not user:
#         session.close()
#         return {
#             "message": "Task creation failed",
#             "error": "User not found. Please authenticate first.",
#             "status_code": 400
#         }
    
#     try:
#         task = Task(
#             name=task_data.name,
#             description=task_data.description,
#             status="Pending",
#             due_date=task_data.due_date,
#         )
#         session.add(task)
#         session.commit()

#         # Create calendar event if task creation succeeds
#         if task_data.due_date:  # Only create event if due_date is provided
#             service = build('calendar', 'v3', credentials=get_credentials(user, fernetKey))
#             event = {
#                 'summary': task.name,
#                 'description': task.description or 'Task created from app',
#                 'colorId': '6',
#                 'location': 'Riyadh',
#                 'start': {
#                     'dateTime': f'{dt.datetime.now().isoformat()}',
#                     'timeZone': 'Asia/Riyadh'
#                 },
#                 'end': {
#                     'dateTime': f'{dt.datetime.now().isoformat()}',
#                     'timeZone': 'Asia/Riyadh'
#                 },
#                 'attendees': [
#                     {
#                         'email': '7bolooo@gmail.com',
#                     }
#                 ]
#             }
#             calendar_event = service.events().insert(calendarId='primary', body=event).execute()
#         return {
#             "id": task.id,
#             "name": task.name,
#             "description": task.description,
#             "status": task.status,
#             "due_date": task.due_date,
#             "message": "Task created successfully",
#             "status_code": 200
#         }
#     except Exception as e:
#         session.rollback()
#         return {
#             "message": "Task creation failed",
#             "error": str(e),
#             "status_code": 400
#         }
#     finally:
#         session.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}



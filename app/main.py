from fastapi import FastAPI
from . import model 
from .database import engine  
from .routers import post , user ,vote, auth
from fastapi.middleware.cors import CORSMiddleware


model.Base.metadata.create_all(engine)

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]

)

app.include_router(post.router)#Wha is this doing?
app.include_router(user.router)# It is basically asking the cursor(which checks when an api hits) to go and check in that file first , then hit the 2nd file
app.include_router(auth.router)
app.include_router(vote.router)




@app.get("/")
async def root():
    return {"message":"Hello World"}





    





    
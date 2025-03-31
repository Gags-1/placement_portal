from fastapi import FastAPI
from .routers import user, auth, admin_auth, admin
from fastapi.middleware.cors import CORSMiddleware  
from fastapi.staticfiles import StaticFiles
app=FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/", StaticFiles(directory="public", html=True), name="public")

@app.get("/")
def message():
    return {"Message":"Testing"}


app.include_router(user.router)
app.include_router(auth.router)

app.include_router(admin_auth.router)

app.include_router(admin.router)


from fastapi import FastAPI

from public.posts import posts_router

app = FastAPI()

app.include_router(posts_router)

@app.get("/")
async def root():
    return {"message": "в проекте только бек"}

from dotenv import load_dotenv
from fastapi import FastAPI
from app.api.v1.lead_router import router as lead_router
from app.api.v1.industry_router import router as industry_router

load_dotenv()

app = FastAPI(title="AI Sales Doctor MVP")
app.include_router(lead_router)
app.include_router(industry_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

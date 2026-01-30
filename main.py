from dotenv import load_dotenv
from fastapi import FastAPI
from app.api.v1.lead_router import router as lead_router
from app.api.v1.industry_router import router as industry_router
from app.core.handlers import register_exception_handlers
from app.core.middleware import register_middleware

load_dotenv()


def create_app() -> FastAPI:
    app = FastAPI(title="AI Sales Doctor MVP")

    register_middleware(app)
    register_exception_handlers(app)

    app.include_router(lead_router)
    app.include_router(industry_router)

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

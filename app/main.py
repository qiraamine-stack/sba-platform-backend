from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import auth, listings, calculator, admin

app = FastAPI(
    title="SBA Business Valuation Platform",
    description="Value and finance small business acquisitions using SBA loans",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://buywithsba.com",
        "https://www.buywithsba.com",
        "https://sba-platform.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(listings.router, prefix="/api/listings", tags=["listings"])
app.include_router(calculator.router, prefix="/api/calculator", tags=["calculator"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])

@app.get("/")
def root():
    return {"message": "SBA Platform API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

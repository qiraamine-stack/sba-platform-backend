from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import auth, listings, calculator

app = FastAPI(
    title="SBA Business Valuation Platform",
    description="Value and finance small business acquisitions using SBA loans",
    version="1.0.0"
)

# Allow the Next.js frontend to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(listings.router, prefix="/api/listings", tags=["listings"])
app.include_router(calculator.router, prefix="/api/calculator", tags=["calculator"])

@app.get("/")
def root():
    return {"message": "SBA Platform API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from views import customer, address, product, sales_note
from models import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Brew.api", description="API for managing coffe sales")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(customer.router)
app.include_router(address.router)
app.include_router(product.router)
app.include_router(sales_note.router)

@app.get("/")
def read_root():
    return {"message": "API works!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

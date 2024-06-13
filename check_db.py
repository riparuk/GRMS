from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Request, Image  # pastikan model Anda diimpor dengan benar
from app.db.database import SQLALCHEMY_DATABASE_URL, Base

# Buat engine dan session untuk berinteraksi dengan database
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# Query data dari tabel requests
requests = db.query(Request).all()
print("Requests:")
for request in requests:
    print(f"ID: {request.id}, Guest Name: {request.guestName}, Image URLs: {request.imageURLs}")

# Query data dari tabel images
images = db.query(Image).all()
print("\nImages:")
for image in images:
    print(f"ID: {image.id}, Filename: {image.filename}, URL: {image.url}")

# Tutup session
db.close()

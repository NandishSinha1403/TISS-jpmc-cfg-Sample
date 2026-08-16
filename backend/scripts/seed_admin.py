"""One-off script to seed an admin account. Run manually: python -m scripts.seed_admin

Admin accounts cannot be created via /auth/signup by design (public signup
is learner-only). This script bypasses that boundary intentionally, for
local/hackathon setup only.
"""

from app.core.database import Base, SessionLocal, engine
from app.core.security import hash_password
from app.models.user import User, UserRole

ADMIN_EMAIL = "nandish@tiss.edu"
ADMIN_PASSWORD = "admin101"
ADMIN_FULL_NAME = "Nandish"


def seed_admin():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == ADMIN_EMAIL).first()
        if existing:
            print(f"Admin already exists: {ADMIN_EMAIL}")
            return

        admin = User(
            email=ADMIN_EMAIL,
            hashed_password=hash_password(ADMIN_PASSWORD),
            full_name=ADMIN_FULL_NAME,
            role=UserRole.admin,
        )
        db.add(admin)
        db.commit()
        print(f"Created admin: {ADMIN_EMAIL}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_admin()

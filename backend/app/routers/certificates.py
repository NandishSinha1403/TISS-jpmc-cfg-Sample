from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.certificate import CertificateResponse, VerifyResponse
from app.services import certificate_service

router = APIRouter(tags=["certificates"])


@router.get("/courses/{course_id}/certificate", response_model=CertificateResponse)
def get_my_certificate(
    course_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    certificate = certificate_service.get_certificate_for_course(db, course_id, current_user)
    if certificate is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No certificate earned for this course yet"
        )
    return certificate


@router.get("/certificates/{certificate_id}/pdf")
def download_certificate_pdf(
    certificate_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    try:
        pdf_bytes = certificate_service.get_certificate_pdf(db, certificate_id, current_user)
    except certificate_service.CertificateNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Certificate not found")

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="certificate-{certificate_id}.pdf"'},
    )


@router.get("/verify/{certificate_id}", response_model=VerifyResponse)
def verify_certificate(certificate_id: str, db: Session = Depends(get_db)):
    try:
        return certificate_service.verify_certificate(db, certificate_id)
    except certificate_service.CertificateNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Certificate not found")

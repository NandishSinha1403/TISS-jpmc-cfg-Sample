"""PDF rendering for certificates. No DB access here — takes plain values in,
returns bytes out, so it stays testable and swappable independent of storage."""

import io
from datetime import datetime
from pathlib import Path

import qrcode
from reportlab.graphics import renderPDF
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from svglib.svglib import svg2rlg

from app.core.config import settings

LOGO_PATH = Path(__file__).resolve().parents[3] / "assets" / "Tata_Institute_of_Social_Sciences_Logo.svg"
LOGO_HEIGHT = 2.2 * cm


def _draw_logo(c: canvas.Canvas, center_x: float, top_y: float) -> None:
    if not LOGO_PATH.exists():
        return

    drawing = svg2rlg(str(LOGO_PATH))
    if drawing is None or not drawing.height:
        return

    scale = LOGO_HEIGHT / drawing.height
    logo_width = drawing.width * scale
    drawing.width = logo_width
    drawing.height = LOGO_HEIGHT
    drawing.scale(scale, scale)

    renderPDF.draw(drawing, c, center_x - logo_width / 2, top_y - LOGO_HEIGHT)


def render_certificate_pdf(
    certificate_id: str, learner_name: str, course_title: str, issued_at: datetime
) -> bytes:
    verify_url = f"{settings.frontend_base_url}/verify/{certificate_id}"

    qr_img = qrcode.make(verify_url)
    qr_buffer = io.BytesIO()
    qr_img.save(qr_buffer, format="PNG")
    qr_buffer.seek(0)

    pdf_buffer = io.BytesIO()
    page_size = landscape(A4)
    width, height = page_size
    c = canvas.Canvas(pdf_buffer, pagesize=page_size)

    c.setLineWidth(2)
    c.rect(1 * cm, 1 * cm, width - 2 * cm, height - 2 * cm)

    _draw_logo(c, width / 2, height - 1.6 * cm)

    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(width / 2, height - 5.4 * cm, "Certificate of Completion")

    c.setFont("Helvetica", 14)
    c.drawCentredString(width / 2, height - 7.2 * cm, "This certifies that")

    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(width / 2, height - 8.4 * cm, learner_name)

    c.setFont("Helvetica", 14)
    c.drawCentredString(width / 2, height - 9.8 * cm, "has successfully completed the course")

    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width / 2, height - 11 * cm, course_title)

    c.setFont("Helvetica", 11)
    c.drawCentredString(width / 2, height - 12.2 * cm, f"Issued: {issued_at.strftime('%d %B %Y')}")

    qr_size = 3 * cm
    c.drawImage(
        ImageReader(qr_buffer),
        width - 4.5 * cm,
        1.5 * cm,
        width=qr_size,
        height=qr_size,
    )
    c.setFont("Helvetica", 7)
    c.drawCentredString(width - 3 * cm, 1.3 * cm, "Scan to verify")

    c.setFont("Helvetica", 8)
    c.drawString(1.5 * cm, 1.3 * cm, f"Certificate ID: {certificate_id}")

    c.showPage()
    c.save()
    pdf_buffer.seek(0)
    return pdf_buffer.read()

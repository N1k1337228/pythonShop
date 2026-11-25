import uuid
from pathlib import Path
from fastapi import APIRouter, BackgroundTasks, Depends, File, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.core.config import settings
from app.models.attachment import Attachment
from app.models.product import Product
from app.models.user import User
from app.schemas.attachment import AttachmentRead
from app.tasks import log_upload_event

router = APIRouter(tags=["attachments"])

FORBIDDEN_EXTENSIONS = {".exe", ".bat", ".sh", ".cmd", ".js", ".msi"}
ALLOWED_PREFIXES = ("image/", "application/pdf", "text/")

def _validate(file: UploadFile, size: int) -> None:
    suffix = Path(file.filename or "").suffix.lower()
    if suffix in FORBIDDEN_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Forbidden file extension")
    if size > settings.max_upload_size:
        raise HTTPException(status_code=413, detail="File too large")
    if not (file.content_type or "").startswith(ALLOWED_PREFIXES):
        raise HTTPException(status_code=400, detail="Unsupported content type")

@router.post(
    "/products/{product_id}/attachments",
    response_model=AttachmentRead,
    status_code=status.HTTP_201_CREATED,
)
async def upload_attachment(
    product_id: int,
    background: BackgroundTasks,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    product = await db.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    content = await file.read()
    _validate(file, len(content))

    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)
    stored_name = f"{uuid.uuid4().hex}{Path(file.filename or '').suffix}"
    path = upload_dir / stored_name
    path.write_bytes(content)

    attachment = Attachment(
        product_id=product_id,
        filename=file.filename or stored_name,
        file_path=str(path),
        content_type=file.content_type or "application/octet-stream",
        size=len(content),
    )
    db.add(attachment)
    await db.commit()
    await db.refresh(attachment)

    # Запуск фоновой задачи
    background.add_task(log_upload_event, user.id, product_id, attachment.filename)
    return attachment

@router.get("/products/{product_id}/attachments", response_model=list[AttachmentRead])
async def list_attachments(product_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(Attachment).where(Attachment.product_id == product_id)
    return list((await db.execute(stmt)).scalars().all())
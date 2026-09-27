from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse as FastAPIFileResponse
from sqlalchemy.orm import Session

from ..auth import get_current_user
from ..database import get_db
from ..models.models import User, UserFile
from ..models.schemas import FileResponse
from ..services.storage_service import (
    save_file,
    delete_file as delete_storage_file,
    get_local_file,
)

router = APIRouter(prefix="/api/files", tags=["Cloud/Object Storage"])


@router.post("", response_model=FileResponse, status_code=201)
async def upload_file(
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        path, size = await save_file(user.id, file)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    record = UserFile(
        user_id=user.id,
        filename=file.filename or "uploaded-file",
        storage_path=path,
        content_type=file.content_type,
        size_bytes=size,
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record


@router.get("", response_model=list[FileResponse])
def list_files(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return (
        db.query(UserFile)
        .filter(UserFile.user_id == user.id)
        .order_by(UserFile.uploaded_at.desc())
        .all()
    )


@router.get("/{file_id}/download")
def download_file(
    file_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    record = (
        db.query(UserFile)
        .filter(
            UserFile.id == file_id,
            UserFile.user_id == user.id,
        )
        .first()
    )

    if not record:
        raise HTTPException(status_code=404, detail="File not found")

    try:
        path = get_local_file(record.storage_path)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Stored file missing")

    return FastAPIFileResponse(
        path=path,
        filename=record.filename,
        media_type=record.content_type or "application/octet-stream",
    )


@router.delete("/{file_id}", status_code=204)
def delete_file(
    file_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    record = (
        db.query(UserFile)
        .filter(
            UserFile.id == file_id,
            UserFile.user_id == user.id,
        )
        .first()
    )

    if not record:
        raise HTTPException(status_code=404, detail="File not found")

    # Delete the actual stored file
    delete_storage_file(record.storage_path)

    # Delete the database record
    db.delete(record)
    db.commit()

    return None
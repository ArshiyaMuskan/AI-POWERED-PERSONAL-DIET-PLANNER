from pathlib import Path
import uuid
import urllib.request
import urllib.error
from fastapi import UploadFile
from ..core.config import get_settings

settings = get_settings()
BASE = Path(settings.local_storage_dir)
BASE.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".pdf", ".txt"}
ALLOWED_TYPES = {
    "image/jpeg", "image/png", "image/webp",
    "application/pdf", "text/plain"
}


def _validate(filename: str, content_type: str | None, content: bytes):
    suffix = Path(filename or "").suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise ValueError("Unsupported file extension")
    if content_type and content_type not in ALLOWED_TYPES:
        raise ValueError("Unsupported content type")
    max_bytes = settings.max_upload_size_mb * 1024 * 1024
    if len(content) > max_bytes:
        raise ValueError("File exceeds configured size limit")
    return suffix


async def save_file(user_id: int, upload: UploadFile) -> tuple[str, int]:
    content = await upload.read()
    suffix = _validate(upload.filename or "", upload.content_type, content)
    object_name = f"{user_id}/{uuid.uuid4().hex}{suffix}"

    if settings.storage_backend.lower() == "supabase":
        if not settings.supabase_url or not settings.supabase_service_role_key:
            raise ValueError("Supabase storage is not configured")
        url = f"{settings.supabase_url.rstrip('/')}/storage/v1/object/{settings.supabase_bucket}/{object_name}"
        request = urllib.request.Request(
            url,
            data=content,
            method="POST",
            headers={
                "Authorization": f"Bearer {settings.supabase_service_role_key}",
                "apikey": settings.supabase_service_role_key,
                "Content-Type": upload.content_type or "application/octet-stream",
                "x-upsert": "false",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=15) as response:
                if response.status not in (200, 201):
                    raise ValueError("Supabase storage upload failed")
        except urllib.error.HTTPError as exc:
            raise ValueError(f"Cloud storage upload failed: HTTP {exc.code}")
        return f"supabase://{settings.supabase_bucket}/{object_name}", len(content)

    user_dir = BASE / str(user_id)
    user_dir.mkdir(parents=True, exist_ok=True)
    path = user_dir / object_name.split("/", 1)[1]
    path.write_bytes(content)
    return str(path), len(content)


def delete_file(storage_path: str):
    if storage_path.startswith("supabase://"):
        _, rest = storage_path.split("supabase://", 1)
        bucket, object_name = rest.split("/", 1)
        if not settings.supabase_url or not settings.supabase_service_role_key:
            return
        url = f"{settings.supabase_url.rstrip('/')}/storage/v1/object/{bucket}/{object_name}"
        request = urllib.request.Request(
            url,
            method="DELETE",
            headers={
                "Authorization": f"Bearer {settings.supabase_service_role_key}",
                "apikey": settings.supabase_service_role_key,
            },
        )
        try:
            urllib.request.urlopen(request, timeout=15).read()
        except Exception:
            pass
        return

    path = Path(storage_path)
    if path.exists() and path.is_file():
        path.unlink()


def get_local_file(storage_path: str) -> Path:
    path = Path(storage_path)
    if not path.exists() or not path.is_file():
        raise FileNotFoundError("Stored local file not found")
    return path

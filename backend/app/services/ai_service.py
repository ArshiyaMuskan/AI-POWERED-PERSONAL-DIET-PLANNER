import json
import urllib.request
import urllib.error
from .diet_engine import generate_local_plan
from ..core.config import get_settings


def generate_plan(profile: dict) -> tuple[dict, str]:
    """
    Attempts an optional provider only when configured.
    Any provider failure falls back to the local deterministic engine.
    """
    settings = get_settings()

    if settings.ai_provider.lower() != "external":
        return generate_local_plan(profile), "local-rule-engine"

    if not settings.ai_api_url or not settings.ai_api_key:
        return generate_local_plan(profile), "local-fallback"

    payload = {
        "model": settings.ai_model,
        "profile": {
            "age": profile.get("age"),
            "activity_level": profile.get("activity_level"),
            "dietary_preference": profile.get("dietary_preference"),
            "goal": profile.get("goal"),
            "allergies": profile.get("allergies"),
        },
        "instruction": (
            "Return JSON with breakfast, lunch, snack, dinner, "
            "nutrition_summary and hydration_reminder. "
            "This is educational wellness content, not medical advice."
        ),
    }

    request = urllib.request.Request(
        settings.ai_api_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.ai_api_key}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=8) as response:
            data = json.loads(response.read().decode("utf-8"))

        required = [
            "breakfast", "lunch", "snack", "dinner",
            "nutrition_summary", "hydration_reminder"
        ]
        if not all(isinstance(data.get(key), str) and data[key].strip() for key in required):
            raise ValueError("Provider returned an invalid plan")

        return data, "external-ai"
    except (urllib.error.URLError, TimeoutError, ValueError, json.JSONDecodeError, OSError):
        return generate_local_plan(profile), "local-fallback"

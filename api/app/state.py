import base64
from copy import deepcopy

_DEMO_PASSWORD = "panel-backup-2026"
_ENCODED_PASSWORD = base64.b64encode(_DEMO_PASSWORD.encode()).decode()

ASSETS = [
    {"asset_id": "PLC-17", "name": "Packaging Line PLC", "zone": "cell-a", "firmware": "4.3.2", "maintenance_note": "Quarterly inspection complete."},
    {"asset_id": "HMI-04", "name": "Operator HMI", "zone": "cell-a", "firmware": "12.1", "maintenance_note": f"Legacy backup credential: {_ENCODED_PASSWORD}"},
    {"asset_id": "HIST-02", "name": "Process Historian", "zone": "operations", "firmware": "8.7", "maintenance_note": "Archive replication enabled."},
]

PROFILES = {
    1001: {"id": 1001, "username": "field_tech", "role": "technician", "email": "field_tech@example.invalid", "bio": "Synthetic training profile", "password": "training-only"},
    1002: {"id": 1002, "username": "process_engineer", "role": "engineer", "email": "process_engineer@example.invalid", "bio": "Synthetic training profile", "password": "process-pass"},
    1003: {"id": 1003, "username": "range_admin", "role": "admin", "email": "range_admin@example.invalid", "bio": "Synthetic administrator profile", "password": "admin-pass"},
}

BOOKMARKS: dict[str, dict] = {}

def public_profiles():
    result = {}
    for key, value in PROFILES.items():
        item = deepcopy(value)
        item.pop("password", None)
        result[key] = item
    return result

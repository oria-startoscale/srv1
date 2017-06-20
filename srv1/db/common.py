import uuid

# General constants
UUID_LENGTH = 36
STRING_LENGTH = 255
CLOUD_INIT_DATA_LENGTH = 1024 * 5


def generate_uuid():
    """Return UUID string."""
    return str(uuid.uuid4())

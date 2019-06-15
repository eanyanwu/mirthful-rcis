from mirthful_rcis.lib.common import (
    is_uuid
)

from uuid import uuid4

def test_is_uuid():
    assert is_uuid(None) == False
    assert is_uuid("") == False
    assert is_uuid(1) == False
    assert is_uuid(uuid4()) == False
    assert is_uuid('12345678-1234-5678-1234-567812345678') == True

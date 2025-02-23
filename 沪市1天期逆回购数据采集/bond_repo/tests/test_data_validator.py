import pytest
from data_validator import DataValidator

def test_validate():
    # 正常数据（包含证券代码）
    valid_data = ["GC001", "1.0", "2.0", "3.0", "4.0", "5.0", "6.0", "7.0", "8.0", "9.0", "10.0"]
    is_valid, message = DataValidator.validate(valid_data)
    assert is_valid
    assert message == "数据有效"

    # 字段不足
    invalid_data = ["GC001", "1.0", "2.0"]
    is_valid, message = DataValidator.validate(invalid_data)
    assert not is_valid
    assert "数据字段不足" in message

    # 数据类型错误
    invalid_data = ["GC001", "1.0", "invalid", "3.0", "4.0", "5.0", "6.0", "7.0", "8.0", "9.0", "10.0"]
    is_valid, message = DataValidator.validate(invalid_data)
    assert not is_valid
    assert "数据类型错误" in message
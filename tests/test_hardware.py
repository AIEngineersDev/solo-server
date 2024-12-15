# tests/test_hardware.py
from solo_server.hardware import hardware_info

def test_hardware_info(capsys):
    hardware_info()
    captured = capsys.readouterr()
    assert "CPU Information" in captured.out
    assert "Memory Information" in captured.out
    assert "Disk Information" in captured.out

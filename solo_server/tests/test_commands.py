from solo.commands import pull, serve, stop
import pytest

def test_pull():
    assert pull("test-model") is None  # Ensure command executes without errors

def test_serve():
    assert serve("test-container", "test-model") is None

def test_stop():
    assert stop("test-container") is None

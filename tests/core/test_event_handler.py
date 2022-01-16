from unittest.mock import patch

from pyfbx.core.events import FBXEvent, FBXEventType, FBXEmitter, FBXEventHandler


def test_emit_event():
    event = FBXEvent(FBXEventType.EMITTER)

    with patch.object(FBXEventHandler, '__call__', return_value=None) as mock_call:
        handler = FBXEventHandler()
        emitter = FBXEmitter({handler}, FBXEvent)

        emitter.emit(event)

    mock_call.assert_called_once_with(event)

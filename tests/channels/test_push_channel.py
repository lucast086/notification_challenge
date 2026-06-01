# test token invalido
# 
# #test token valido

import pytest

from app.channels.push import SendByPush
from app.core.exceptions import DeviceTokenInvalid
from app.models.notifications import Notification
from app.schemas.notifications import Channel


def test_send_by_push_success(monkeypatch):

    notification = Notification(
        tittle="test noti",
        content="some content here",
        channel=Channel.push,   
        recipient="73737373"
    )
    result = SendByPush().send(notification)
    
    expected_result = {
            "status": "sent",
            "recipient": notification.recipient
        }
    assert expected_result["status"] == result.get('status')
    assert expected_result["recipient"] == result.get('recipient')

def test_send_by_push_invalid_device(monkeypatch):

    monkeypatch.setattr(SendByPush, "_device_token_is_valid", lambda self:False )
    notification = Notification(
        tittle="test noti",
        content="some content here",
        channel=Channel.push,   
        recipient="73737373"
    )
    
    with pytest.raises(DeviceTokenInvalid):
        SendByPush().send(notification)
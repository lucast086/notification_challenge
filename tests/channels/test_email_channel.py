import pytest

from app.channels.email import SendByEmail
from app.core.exceptions import InvalidRecipient
from app.models.notifications import Notification
from app.schemas.notifications import Channel


def test_send_by_email_success():

    notification = Notification(
        tittle="test noti",
        content="some content",
        channel=Channel.email,
        recipient="aa@bb.com"
    )
    sendbyemail = SendByEmail()
    result = sendbyemail.send(notification)
    
    expected_result = {
            "status": "sent",
            "recipient": notification.recipient
        }
    assert expected_result["status"] == result.get('status')
    assert expected_result["recipient"] == result.get('recipient')


def test_send_by_email_invalid_recipient():

    notification = Notification(
        tittle="test noti",
        content="some content",
        channel=Channel.email,
        recipient="bademail"
    )
    sendbyemail = SendByEmail()
    
    
    with pytest.raises(InvalidRecipient):
        sendbyemail.send(notification)
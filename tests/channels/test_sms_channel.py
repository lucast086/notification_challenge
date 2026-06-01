
from app.channels.sms import SendBySms
from app.models.notifications import Notification
from app.schemas.notifications import Channel


def test_send_by_sms_under_max_chars_success():
    notification = Notification(
        tittle="test noti",
        content="some content",
        channel=Channel.sms,
        recipient="73737373"
    )

    result = SendBySms().send(notification)
    
    expected_result = {
            "status": "sent",
            "recipient": notification.recipient
        }
    assert expected_result["status"] == result.get('status')
    assert expected_result["recipient"] == result.get('recipient')


def test_send_by_sms_over_max_chars_success():
    content_over_max_chars="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua UT FINIS.AB, Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua UT FINIS.AB"

    notification = Notification(
        tittle="test noti",
        content=content_over_max_chars,
        channel=Channel.sms,
        recipient="73737373"
    )

    result = SendBySms().send(notification)
    
    expected_result = {
            "status": "sent",
            "recipient": notification.recipient,
            "content": content_over_max_chars[:160]
        }
    assert expected_result["status"] == result.get('status')
    assert expected_result["recipient"] == result.get('recipient')
    assert expected_result["content"] == result.get('content')

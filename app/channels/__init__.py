from app.channels.email import SendByEmail
from app.channels.push import SendByPush
from app.channels.sms import SendBySms

STRATEGY_REGISTER = {
    "email": SendByEmail,
    "sms": SendBySms,
    "push": SendByPush
}
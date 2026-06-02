create_notification_examples = {
    "email_channel": {
        "summary": "Email notification",
        "description": "Send a notification via email. Recipient must be a valid email address.",
        "value": {
            "tittle": "Welcome to our platform",
            "content": "Hi John, your account has been created successfully.",
            "channel": "email",
            "recipient": "john.doe@example.com",
        },
    },
    "sms_channel": {
        "summary": "SMS notification",
        "description": "Send a notification via SMS. Content is truncated to 160 characters.",
        "value": {
            "tittle": "Verification code",
            "content": "Your verification code is 482910. It expires in 10 minutes.",
            "channel": "sms",
            "recipient": "+1234567890",
        },
    },
    "push_channel": {
        "summary": "Push notification",
        "description": "Send a push notification. Recipient must be a valid device token.",
        "value": {
            "tittle": "New message",
            "content": "You have a new message from your team.",
            "channel": "push",
            "recipient": "device-token-abc123xyz",
        },
    },
    "invalid_email_recipient": {
        "summary": "Invalid email recipient (fails)",
        "description": "Email channel with malformed recipient address — returns 400.",
        "value": {
            "tittle": "Failed notification",
            "content": "This will fail because the recipient is not a valid email.",
            "channel": "email",
            "recipient": "not-a-valid-email",
        },
    },
}

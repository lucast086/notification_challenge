register_examples = {
    "successful_registration": {
        "summary": "Successful registration",
        "description": "Valid payload — creates a new user account.",
        "value": {
            "email": "valid_email@example.com",
            "password": "Valid#123",
            "password_repeat": "Valid#123",
        },
    },
    "user_already_exists": {
        "summary": "User already exists",
        "description": "Email is already registered — returns 409.",
        "value": {
            "email": "valid_email@example.com",
            "password": "Valid#123",
            "password_repeat": "Valid#123",
        },
    },
    "passwords_do_not_match": {
        "summary": "Passwords do not match",
        "description": "password and password_repeat are different — returns 422.",
        "value": {
            "email": "john.doe@example.com",
            "password": "Secure#123",
            "password_repeat": "Different#456",
        },
    },
}

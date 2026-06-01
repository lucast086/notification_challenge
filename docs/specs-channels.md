# Purpose                     
Handles sending notifications through specific channels using the Strategy pattern.
Each channel implements its own sending logic independently, allowing new channels to be added without modifying existing code (Open/Closed Principle).

## Requirements
  - The system SHALL send the notification through the specified channel upon creation. 
  - The system SHALL send notifications through the Email channel by validating recipient format, generating a template and registering the send.
  - The system SHALL send notifications through the SMS channel by limiting content to 160 characters, registering the number and send date.
  - The system SHALL send notifications through the Push channel by validating the device token, formatting the payload and registering the send status.
  - The system SHALL allow adding new channels without modifying existing channel logic.

## Scenarios:

  Given> Authenticated user creates notification with channel EMAIL
  When> Email address format is valid
  Then> Generates template, registers send and returns success

  Given> Authenticated user creates notification with channel EMAIL
  When> Email address format is invalid
  Then> Returns error "invalid email format" and status 400

  ---

  Given> Authenticated user creates notification with channel SMS
  When> Content is 160 characters or less
  Then> Registers number and send date, returns success

  Given> Authenticated user creates notification with channel SMS
  When> Content exceeds 160 characters
  Then> Returns error "content exceeds 160 characters limit" and status 400

  ---

  Given> Authenticated user creates notification with channel PUSH
  When> Device token is valid
  Then> Formats payload, registers send status and returns success

  Given> Authenticated user creates notification with channel PUSH
  When> Device token is invalid
  Then> Returns error "invalid device token" and status 400

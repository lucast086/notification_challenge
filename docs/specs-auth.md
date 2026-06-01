## Purpose                                                                              
  Handles user authentication and endpoint authorization. JWT with refresh token was chosen for security, renewability, and because the token is generated from the user's own data.
                  
## Requirements
  - The system SHALL allow user registration with email and password.
  - The system SHALL allow login with email and password and return a JWT.
  - The system SHALL allow token refresh and issue a new token.
  - The system SHALL protect resource endpoints by validating that the token is valid.

## Scenarios:
  
  Given> Registerd User
  When> Login with valid credentials
  Then> returns acces_token and refresh_token with 200 status

  Given> Registerd User
  When> Login with invalid credentials
  Then> returns error mesage "invalid credentials" and status 400

  Given> UnRegisterd User
  When> Login with invalid credentials
  Then> returns error mesage "user not registered" and status 400

-----------------

  Given> User
  When> Register with valid data
  Then> returns message "user created" and 201 status
  
  Given> User
  When> Register with invalid data
  Then> returns error mesage "invalid data" and status 400
  
  Given> Registered User
  When> Try to register
  Then> returns message "you are already registered" and 400 status

 -------------------- 
  
  Given> User
  When> Try to obtain new token with valid refresh token
  Then> returns new token and 200 status

  Given> User
  When> Try to obtain new token with invalid refresh token
  Then> returns error mesage "invalid refresh token" and status 401

 -------------------- 

  Given> User
  When> Try to access resource endpoint with valid token
  Then> returns resource and status 200

  Given> User
  When> Try to access resource endpoint with invalid token OR expired token
  Then> returns error mesage "invalid token" and status 401

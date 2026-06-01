## Purpose                     
Handles creation, modification, deletion and listing of notifications for authenticated users. The sender is identified by extracting the user from the provided JWT token, ensuring each user can only manage their own notifications. 
                  
## Requirements
  - The system SHALL allow notification creation with title, content and channel.         
  - The system SHALL allow notification update with notification id and updated fields.
  - The system SHALL allow notification deletion with notification id.
  - The system SHALL allow listing all notifications belonging to the authenticated user.
  - The system SHALL send the notification through the specified channel upon creation. 

## Scenarios:                                                                            
                                                                                        
  Given> Authenticated user
  When> Creates notification with valid title, content and channel info
  Then> Returns created notification with 201 status and triggers channel send


  Given> Authenticated user
  When> Creates notification with invalid data (missing fields)
  Then> Returns error message "invalid data missing fields {}" and status 400                             
   
  Given> Unauthenticated user
  When> Tries to create notification
  Then> Returns error message "invalid token" and status 401
   
  ---                                                                                   
                  
  Given> Authenticated user and existing notification owned by user
  When> Updates notification with valid data
  Then> Returns updated notification with 200 status
   
  Given> Authenticated user
  When> Updates notification that does not belong to user
  Then> Returns error message "notification not found" and status 404

  Given> Authenticated user
  When> Updates notification with invalid data
  Then> Returns error message "invalid data" and status 400

  ---

  Given> Authenticated user and existing notification owned by user
  When> Deletes notification by id
  Then> Returns 204 status

  Given> Authenticated user
  When> Deletes notification that does not belong to user
  Then> Returns "notification not found" and status 404

  ---

  Given> Authenticated user with existing notifications
  When> Lists all notifications
  Then> Returns list of own notifications with 200 status
                  
  Given> Authenticated user with no notifications
  When> Lists all notifications
  Then> Returns empty list with 200 status

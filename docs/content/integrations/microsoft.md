# Microsoft Integration

ShadowBar provides first-class support for Microsoft 365, allowing agents to interact with Outlook, Calendar, and other Microsoft services.

## Authentication

We use the standard OAuth2 flow to authenticate with Microsoft Graph.

1.  Run the auth command:
    ```bash
    sb auth microsoft
    ```
2.  Follow the link to log in with your Barclays credentials.
3.  Copy the authorization code back to the terminal.

## Scopes

By default, ShadowBar requests the following scopes:
*   `User.Read`
*   `Mail.ReadWrite`
*   `Calendars.ReadWrite`

## Usage

Once authenticated, you can use the `OutlookTool` and `CalendarTool` without any extra configuration. The token is managed automatically by the framework.

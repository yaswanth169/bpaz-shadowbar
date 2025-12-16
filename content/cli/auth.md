# Authentication

ShadowBar uses a unified authentication system to manage credentials for LLMs and external tools.

## Microsoft 365

To use Outlook, Teams, or Calendar, you must authenticate with Microsoft.

```bash
sb auth microsoft
```

This will launch a browser window. Log in with your Barclays credentials. You may need to approve the "ShadowBar" application if it's your first time.

!!! warning "Token Expiry"
    Microsoft tokens expire periodically. If your agent starts failing with 401 errors, run `sb auth microsoft` again.

## Anthropic

We recommend setting your Anthropic API key in your `.env` file, but you can also configure it via the CLI.

```bash
sb auth anthropic
```

This will prompt you for your API key and store it securely.

## Google

If you need to use Google Workspace tools (less common at Barclays):

```bash
sb auth google
```

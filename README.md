all vibecoded...

## Debug logging

To enable debug logging for this integration, add the following to your `configuration.yaml`:

```yaml
logger:
  default: warning
  logs:
    custom_components.smart_me: debug
```

Restart Home Assistant, then check **Settings → System → Logs**. The integration will log:

- The API request URL and authenticated username
- The HTTP response status for every poll
- The full list of discovered devices (id, name, serial)
- For each device, all non-null fields returned by the API and which sensors were created from them

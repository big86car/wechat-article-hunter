# Publish Receipt

```json
{
  "status": "prepared|submitted|failed",
  "scope": "draft_box_only",
  "account_label": "",
  "title": "",
  "submitted_at": "ISO-8601 or null",
  "draft_id": "redacted-or-platform-id",
  "fingerprint": "sha256",
  "artifacts": {"html": "article.html", "cover": "images/cover.jpg"},
  "platform_response": {"code": "", "message": ""},
  "publicly_published": false,
  "notes": []
}
```

Never include access tokens, AppSecret, cookies, authorization headers, or raw credential-bearing URLs.

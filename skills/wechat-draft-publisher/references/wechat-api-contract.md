# WeChat Draft API Contract

The bundled adapter uses the Official Account API sequence below. Verify current platform documentation before changing behavior because availability and limits depend on account type and platform policy.

1. Obtain an access token with the configured AppID and AppSecret.
2. Upload each local body image through the body-image endpoint and replace its `src` with the returned hosted URL.
3. Upload the cover through the permanent-material image endpoint and retain its `media_id`.
4. Submit one article to the draft endpoint with title, author, digest, content, optional source URL, and cover media ID.

## Failure classes

- `authentication`: invalid/expired credential or token
- `ip_allowlist`: caller IP not on the configured allowlist
- `permission`: account type or API scope does not permit the operation
- `quota`: frequency or material limits reached
- `validation`: title, digest, HTML, image, or request-field failure
- `transport`: timeout, DNS, TLS, or non-JSON response
- `platform`: uncategorized non-zero platform error

Do not print the token, secret, authorization query string, or raw credential-bearing response. Retry a token-expiry response once after invalidating the cache; do not retry permission, allowlist, quota, or validation failures automatically.

## Idempotency

The API does not provide a client idempotency key for draft creation. The adapter hashes title, HTML, and cover bytes and records the fingerprint locally. This prevents accidental local retries but cannot detect drafts created by another machine.

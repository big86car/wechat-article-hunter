# Source Ledger Schema

```json
{
  "topic": "",
  "researched_at": "ISO-8601",
  "claims": [
    {
      "claim_id": "C01",
      "claim": "",
      "claim_type": "fact|inference|estimate|opinion",
      "importance": "material|supporting",
      "status": "verified|qualified|unverified|rejected",
      "confidence": "high|medium|low",
      "sources": [
        {
          "title": "",
          "url": "",
          "publisher": "",
          "source_type": "primary|independent|community",
          "published_at": "",
          "accessed_at": "",
          "supports": "what this source actually establishes"
        }
      ],
      "caveat": ""
    }
  ]
}
```

Never use `verified` when every supporting source merely repeats the same originating claim. Keep rejected claims to explain why downstream writers must not use them.

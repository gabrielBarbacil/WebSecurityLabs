#  File Upload Vulnerabilities — PortSwigger Labs

> [Web Security Academy — File Upload](https://portswigger.net/web-security/file-upload)

## Progress

```
██████░░░░░░░░░░░░  3 / 7 — 43%
```

| Difficulty | Completed |
|---|---|
| 🟢 Apprentice | 2 / 2 |
| 🟡 Practitioner | 1 / 5 |

---

## Labs

| # | Lab | Technique | Status |
|---|---|---|---|
| 01 | [RCE via web shell upload — no filter](./writeups/01-rce-no-filter.md) | Basic upload | ✅ |
| 02 | [Web shell via Content-Type bypass](./writeups/02-content-type-bypass.md) | MIME type bypass | ✅ |
| 03 | [Web shell via path traversal](./writeups/03-path-traversal.md) | Path traversal in filename | ✅ |
| 04 | Web shell via extension blacklist bypass | Extension bypass | ⬜ |
| 05 | Web shell via obfuscated file extension | Obfuscation | ⬜ |
| 06 | RCE via polyglot web shell upload | Polyglot file | ⬜ |
| 07 | Web shell via race condition | Race condition | ⬜ |

---

## Key concepts learned so far

- Without validation any file including `.php` is accepted and executed
- Content-Type header is client-controlled and can be freely modified in Burp
- Path traversal in the filename field moves the file outside the uploads directory
- `../` in filenames is often sanitized — `..%2f` bypasses server-side stripping
- Burp Intercept must be ON at the moment of submitting the upload form

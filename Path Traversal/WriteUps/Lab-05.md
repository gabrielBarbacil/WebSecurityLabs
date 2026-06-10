# Lab 05 — Validation of start of path

**Difficulty:** 🟡 Practitioner  
**Technique:** Path Traversal — start of path validation bypass  
**Link:** https://portswigger.net/web-security/file-path-traversal/lab-validate-start-of-path

---

## Concept

The application validates that the `filename` parameter starts with an expected base directory (`/var/www/images/`). However, it only checks the beginning of the string and does not validate the resolved final path, making it trivial to bypass with traversal sequences appended after the required prefix.

---

## Reconnaissance

Same injection point:

```
GET /image?filename=18.jpg
```

Supplying `../../../etc/passwd` or `/etc/passwd` is blocked. The app appears to require a specific path prefix.

---

## Process

### Step 1 — Identify the required prefix

From the lab context, the app expects filenames to start with `/var/www/images/`.

### Step 2 — Append traversal sequences after the prefix

```
GET /image?filename=/var/www/images/../../../etc/passwd
```

The validation sees `/var/www/images/` at the start → passes.  
The OS resolves the full path: `/var/www/images/../../../etc/passwd` → `/etc/passwd`.

---

## Result

Full `/etc/passwd` contents returned with 200 OK.

---

## Issues encountered

None. The required prefix was identifiable from the lab context.

---

## Takeaways

- Validating only the start of a path is not sufficient
- The OS always resolves `../` regardless of any prefix
- The correct fix: resolve the path with `realpath()` first, then verify the **resulting** path starts within the allowed directory — not the raw input

---

## Defense comparison

| Approach | Bypassed by |
|---|---|
| Block `../` | Absolute paths, encoding |
| Require path prefix | Traversal after prefix |
| Recursive strip | Still bypassable with encoding |
| `realpath()` + prefix check | ✅ Correct defense |

---

## References

- [Path Traversal — PortSwigger](https://portswigger.net/web-security/file-path-traversal)

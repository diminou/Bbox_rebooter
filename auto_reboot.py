import http
import requests
import time
import json


with open("params.json", "r") as f:
    params = json.load(f)
    
base_url = params["baseUrl"]
test_url = params["testUrl"]
login_url = base_url + "/api/v1/login"
token_url = base_url + "/api/v1/device/token"
reboot_url = lambda x: base_url + "/api/v1/device/reboot?btoken=" + x
timeout = 1.0
idle_time = 30
login_payload = {'password': params["password"]}

def check_test(session):
    try:
        session.get(test_url, timeout=timeout)
        return session
    except Exception:
        return None

def check_base(session):
    try:
        session.get(base_url, timeout=timeout)
        return True
    except Exception:
        return False

def get_token(session):
    try:
        r = session.get(token_url, timeout=timeout)
        content = r.text
        tknbl = json.loads(content)
        token = tknbl[0]['device']['token']
        return (session, token)
    except Exception as e:
        return None

def login(session):
    try:
        session.post(login_url, data=login_payload, timeout=timeout)
        return session
    except Exception:
        return None

def reboot(st):
    try:
        session = st[0]
        token = st[1]
        session.post(reboot_url(token), data={}, timeout=timeout)
        return session
    except Exception:
        return None

def full_reboot(session):
    s2 = login(session)
    if s2 is None:
        return None
    rbtbl = get_token(s2)
    if rbtbl is None:
        return None
    s3 = reboot(rbtbl)
    if s3 is None:
        return None
    return s3

def reboot_if_box_not_connected():
    session = requests.session()
    if not check_base(session):
        pass
    elif check_test(session):
        pass
    else:
        rbt = full_reboot(session)
        if rbt is None:
            pass
        else:
            print(str(time.now()) + " Rebooted")
            pass


def loop_reboot():
    while True:
        reboot_if_box_not_connected()
        time.sleep(idle_time)

if __name__ == '__main__':
    loop_reboot()
    
    

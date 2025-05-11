import time, random, threading, requests

stop_flag = False
cooldown_time = 20

def spam_ngl(target_user, messages, duration):
    global stop_flag
    end_time = time.time() + duration
    while time.time() < end_time and not stop_flag:
        msg = random.choice(messages)
        device_id = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=16))
        payload = {
            "username": target_user,
            "question": msg,
            "deviceId": device_id,
            "gameSlug": "",
            "referrer": ""
        }
        try:
            res = requests.post("https://ngl.link/api/submit", json=payload, headers={"Content-Type": "application/json"})
            print(f"✅ SENT: {msg} | Status: {res.status_code}")
            if res.status_code == 429:
                print("🚫 RATE LIMITED! Cooling down...")
                time.sleep(cooldown_time)
        except Exception as e:
            print(f"❌ ERROR: {e}")
        time.sleep(random.uniform(2, 5))

def start_multi_spam(username, messages, duration, thread_count=5):
    global stop_flag
    stop_flag = False
    threads = []
    for _ in range(thread_count):
        t = threading.Thread(target=spam_ngl, args=(username, messages, duration))
        t.daemon = True
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

def stop_spam():
    global stop_flag
    stop_flag = True
    print("Spamming stopped!")

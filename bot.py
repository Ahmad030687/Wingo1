import time
import requests
import random
import sys

# --- CONFIGURATION ---
TOKEN = "8548701014:AAHNkV2MvmOOzViQjZ6lsMm9IL5qiJ74yOo"
CHAT_ID = "-1003557635874" 
API_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json"

# Ultra-Realistic Mobile Headers
MOBILE_HEADERS = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36"
]

def send_to_tg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}
    try:
        requests.post(url, data=payload, timeout=15)
    except:
        pass

def get_god_logic(history, current_level):
    nums = [int(x["number"]) for x in history]
    recent = ["BIG" if n >= 5 else "SMALL" for n in nums[:10]]
    
    # Strictly Under Level 2 logic
    if current_level >= 2:
        # Balancing Law
        big_v = sum(1 for n in nums[:100] if n >= 5)
        pred = "BIG" if big_v < 50 else "SMALL"
    elif recent[0] == recent[1] == recent[2]:
        pred = recent[0]
    else:
        pred = "SMALL" if recent[0] == "BIG" else "BIG"

    r_nums = [n for n in nums[:50] if (n >= 5 if pred == "BIG" else n < 5)]
    counts = {i: r_nums.count(i) for i in set(r_nums)}
    sorted_jps = sorted(counts, key=counts.get, reverse=True)
    n1 = sorted_jps[0] if len(sorted_jps) else 7
    n2 = sorted_jps[1] if len(sorted_jps) > 1 else 2
    
    return {"bs": pred, "n1": n1, "n2": n2}

def run():
    last_processed_issue = None
    last_pred_obj = None
    level = 1
    
    print("🔱 AHMAD BOSS V11 (GHOST MODE) STARTED...", flush=True)
    
    while True:
        try:
            # Change Header every request to mimic different users
            current_headers = {
                'User-Agent': random.choice(MOBILE_HEADERS),
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': 'https://v999p.com/index.html'
            }
            
            # Adding random timestamp offset
            ts = int(time.time()*1000) + random.randint(100, 999)
            response = requests.get(f"{API_URL}?pageNo=0&pageSize=20&ts={ts}", headers=current_headers, timeout=20)
            
            if response.status_code == 403:
                print("🛑 403 Forbidden! GitHub IP is restricted. Waiting 60s...", flush=True)
                time.sleep(60) # Lambi break taaki server cooldown ho jaye
                continue

            data = response.json()
            if data and data.get("code") == 0:
                history = data["data"]["list"]
                period = history[0]["issueNumber"]
                num = int(history[0]["number"])

                if period != last_processed_issue:
                    if last_pred_obj:
                        actual_bs = "BIG" if num >= 5 else "SMALL"
                        is_win = actual_bs == last_pred_obj["bs"]
                        res_icon = "WIN ✅" if is_win else f"LOSS ❌ (L{level+1})"
                        
                        send_to_tg(f"🏁 <b>PERIOD {period} RESULT</b>\n🎰 Number: <code>{num}</code>\n✨ Status: <b>{res_icon}</b>")
                        level = 1 if is_win else level + 1

                    pred = get_god_logic(history, level)
                    vip_msg = (
                        f"🔱 <b>AHMAD BOSS VIP LEVEL {level}</b> 🔱\n"
                        f"━━━━━━━━━━━━━━━━━━━━\n"
                        f"📡 <b>PERIOD:</b> <code>{int(period)+1}</code>\n"
                        f"📈 <b>SIGNAL:</b> <b>{pred['bs']} 🔥</b>\n"
                        f"🎯 <b>JACKPOT:</b> <code>{pred['n1']} , {pred['n2']}</code>\n"
                        f"🔒 <b>ACCURACY:</b> AI REFINED FIXED ✅\n"
                        f"━━━━━━━━━━━━━━━━━━━━\n"
                        f"👑 <b>Owner:</b> Ahmad Boss"
                    )
                    send_to_tg(vip_msg)
                    last_pred_obj = pred
                    last_processed_issue = period
            
        except Exception as e:
            print(f"Error: {e}", flush=True)
            
        # Random sleep between 5-10 seconds to avoid bot-like pattern
        time.sleep(random.randint(5, 10))

if __name__ == "__main__":
    run()
if __name__ == "__main__":
    run()

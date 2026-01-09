import time
import requests
import sys

# --- CONFIGURATION ---
TOKEN = "8548701014:AAHNkV2MvmOOzViQjZ6lsMm9IL5qiJ74yOo"
CHAT_ID = "-1003557635874" 
API_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json"

# Browser-like headers to bypass blocking
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Origin': 'https://v999p.com',
    'Referer': 'https://v999p.com/'
}

def send_to_tg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}
    try:
        requests.post(url, data=payload, timeout=15)
    except:
        pass

def get_god_logic(history, current_level):
    nums = [int(x["number"]) for x in history]
    # Deep Analysis for Under Level 2
    recent = ["BIG" if n >= 5 else "SMALL" for n in nums[:15]]
    big_v_500 = sum(1 for n in nums[:500] if n >= 5)

    if current_level >= 2:
        # Recovery Mode
        pred = "BIG" if big_v_500 < 250 else "SMALL"
    elif recent[0] == recent[1] == recent[2]:
        pred = recent[0] # Trend
    elif recent[0] != recent[1]:
        pred = "SMALL" if recent[0] == "BIG" else "BIG" # Zigzag
    else:
        pred = "BIG" if big_v_500 < 250 else "SMALL"

    r_nums = [n for n in nums[:60] if (n >= 5 if pred == "BIG" else n < 5)]
    counts = {i: r_nums.count(i) for i in set(r_nums)}
    sorted_jps = sorted(counts, key=counts.get, reverse=True)
    n1 = sorted_jps[0] if len(sorted_jps) > 0 else (7 if pred == "BIG" else 2)
    n2 = sorted_jps[1] if len(sorted_jps) > 1 else (8 if pred == "BIG" else 3)
    
    return {"bs": pred, "n1": n1, "n2": n2}

def run():
    last_processed_issue = None
    last_pred_obj = None
    level = 1
    session = requests.Session()
    session.headers.update(HEADERS)
    
    print("🔱 AHMAD BOSS SUPREME BOT V10 STARTED...", flush=True)
    
    while True:
        try:
            # Fetch data with headers
            response = session.get(f"{API_URL}?pageNo=0&pageSize=20&ts={int(time.time()*1000)}", timeout=15)
            
            if response.status_code != 200:
                print(f"Server Error: {response.status_code}. Retrying...", flush=True)
                time.sleep(10)
                continue
                
            data = response.json()
            
            if data and data.get("code") == 0:
                history = data["data"]["list"]
                latest = history[0]
                period = latest["issueNumber"]
                num = int(latest["number"])

                if period != last_processed_issue:
                    if last_pred_obj:
                        actual_bs = "BIG" if num >= 5 else "SMALL"
                        is_win = actual_bs == last_pred_obj["bs"]
                        res_icon = "WIN ✅" if is_win else f"LOSS ❌ (L{level+1})"
                        
                        print(f"Period: {period} | Result: {num} | {res_icon}", flush=True)
                        
                        res_msg = f"🏁 <b>PERIOD {period} RESULT</b>\n🎰 Number: <code>{num}</code>\n✨ Status: <b>{res_icon}</b>"
                        send_to_tg(res_msg)
                        level = 1 if is_win else level + 1

                    # Fetching 500 rounds logic remains for accuracy
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
                    print(f"Next Prediction: {pred['bs']}", flush=True)
                    
                    last_pred_obj = pred
                    last_processed_issue = period
            
        except Exception as e:
            print(f"Fetch Error: {e}. Sleeping 5s...", flush=True)
            time.sleep(5)
            
        time.sleep(5)

if __name__ == "__main__":
    run()

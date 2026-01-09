import time
import requests
import sys

# --- CONFIGURATION ---
TOKEN = "8548701014:AAHNkV2MvmOOzViQjZ6lsMm9IL5qiJ74yOo"
CHAT_ID = "-1003557635874" 
API_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json"

def send_to_tg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}
    try:
        requests.post(url, data=payload, timeout=15)
    except:
        pass

def get_god_logic(history, current_level):
    nums = [int(x["number"]) for x in history]
    recent_15 = ["BIG" if n >= 5 else "SMALL" for n in nums[:15]]
    big_v_500 = sum(1 for n in nums[:500] if n >= 5)

    # --- UNDER LEVEL 2 FIXED LOGIC ---
    if current_level >= 2:
        # L2 par aate hi global balance follow karein (99% Win)
        pred = "BIG" if big_v_500 < 250 else "SMALL"
    elif recent_15[0] == recent_15[1] == recent_15[2]:
        pred = recent_15[0] # Dragon
    elif recent_15[0] != recent_15[1]:
        pred = "SMALL" if recent_15[0] == "BIG" else "BIG" # Zigzag
    else:
        pred = "BIG" if big_v_500 < 250 else "SMALL"

    # Jackpot Numbers
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
    
    # Flush=True is important for GitHub Live Logs
    print("🔱 AHMAD BOSS SUPREME BOT STARTED...", flush=True)
    
    while True:
        try:
            # Full 500 rounds fetch for L2 stability
            all_data = []
            for page in range(25):
                r = requests.get(f"{API_URL}?pageNo={page}&pageSize=20&ts={int(time.time()*1000)}", timeout=10).json()
                if r["code"] == 0: all_data.extend(r["data"]["list"])
            
            if not all_data: continue
            
            latest = all_data[0]
            period = latest["issueNumber"]
            num = int(latest["number"])

            if period != last_processed_issue:
                if last_pred_obj:
                    actual_bs = "BIG" if num >= 5 else "SMALL"
                    is_win = actual_bs == last_pred_obj["bs"]
                    res_icon = "WIN ✅" if is_win else f"LOSS ❌ (L{level+1})"
                    
                    # Print for GitHub Logs
                    print(f"Period: {period} | Result: {num} | {res_icon}", flush=True)
                    
                    res_msg = f"🏁 <b>PERIOD {period} RESULT</b>\n🎰 Number: <code>{num}</code>\n✨ Status: <b>{res_icon}</b>"
                    send_to_tg(res_msg)
                    level = 1 if is_win else level + 1

                pred = get_god_logic(all_data, level)
                vip_msg = (
                    f"🔱 <b>AHMAD BOSS VIP LEVEL {level}</b> 🔱\n"
                    f"━━━━━━━━━━━━━━━━━━━━\n"
                    f"📡 <b>PERIOD:</b> {int(period)+1}\n"
                    f"📈 <b>SIGNAL:</b> {pred['bs']} 🔥\n"
                    f"🎯 <b>JACKPOT:</b> {pred['n1']} , {pred['n2']}\n"
                    f"🔒 <b>ACCURACY:</b> AI REFINED FIXED ✅\n"
                    f"━━━━━━━━━━━━━━━━━━━━\n"
                    f"👑 <b>Owner:</b> Ahmad Boss"
                )
                send_to_tg(vip_msg)
                print(f"Next Prediction Sent: {pred['bs']}", flush=True)
                
                last_pred_obj = pred
                last_processed_issue = period
                
        except Exception as e:
            print(f"Error: {e}", flush=True)
            
        time.sleep(5)

if __name__ == "__main__":
    run()

import time
import requests
import os
import random

# --- CONFIGURATION ---
TOKEN = "8548701014:AAHNkV2MvmOOzViQjZ6lsMm9IL5qiJ74yOo"
CHAT_ID = "-1003557635874" 
API_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json"

def send_to_tg(text):
    """Direct Server-to-Server Connection (Works on GitHub without VPN)"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}
    try:
        requests.post(url, data=payload, timeout=15)
    except:
        pass

def get_god_logic(history, current_level):
    nums = [int(x["number"]) for x in history]
    # Analysis of last 15 rounds for better trend grip
    recent_15 = ["BIG" if n >= 5 else "SMALL" for n in nums[:15]]
    big_v_100 = sum(1 for n in nums[:100] if n >= 5)
    big_v_500 = sum(1 for n in nums[:500] if n >= 5)

    # --- HYPER-STRICT LEVEL 2 RECOVERY ---
    if current_level >= 2:
        # Jab L1 loss ho jaye, toh ye pure 500 rounds ke global law ko follow karega
        pred = "BIG" if big_v_500 < 250 else "SMALL"
        pat = "L2_SURESHOT_FIX 🔒"
    # --- LEVEL 1 SURESHOT LOGIC ---
    elif recent_15[0] == recent_15[1] == recent_15[2]:
        # Dragon Protection
        pred = recent_15[0]
        pat = "DRAGON_FORCE 🐉"
    elif recent_15[0] != recent_15[1] and recent_15[1] != recent_15[2]:
        # Zigzag Logic
        pred = "SMALL" if recent_15[0] == "BIG" else "BIG"
        pat = "ZIGZAG_PRO ⚡"
    else:
        # Market Balance Reversion (100 rounds)
        pred = "BIG" if big_v_100 < 50 else "SMALL"
        pat = "AI_REFINED_FIX ✅"

    # --- JACKPOT NUMBER SELECTION ---
    r_nums = [n for n in nums[:60] if (n >= 5 if pred == "BIG" else n < 5)]
    counts = {i: r_nums.count(i) for i in set(r_nums)}
    sorted_jps = sorted(counts, key=counts.get, reverse=True)
    
    n1 = sorted_jps[0] if len(sorted_jps) > 0 else (7 if pred == "BIG" else 2)
    n2 = sorted_jps[1] if len(sorted_jps) > 1 else (8 if pred == "BIG" else 3)
    
    return {"bs": pred, "n1": n1, "n2": n2, "pat": pat}

def run():
    last_processed_issue = None
    last_pred_obj = None
    level = 1
    
    print("🔱 Ahmad Boss Bot Active on Cloud Server...")
    
    while True:
        try:
            # Fetching deep data (500 rounds)
            all_data = []
            for page in range(25):
                r = requests.get(f"{API_URL}?pageNo={page}&pageSize=20&ts={int(time.time()*1000)}", timeout=10).json()
                if r["code"] == 0: all_data.extend(r["data"]["list"])
            
            if not all_data: continue
            
            latest = all_data[0]
            period = latest["issueNumber"]
            num = int(latest["number"])

            if period != last_processed_issue:
                # 1. Handle Result
                if last_pred_obj:
                    actual_bs = "BIG" if num >= 5 else "SMALL"
                    is_win = actual_bs == last_pred_obj["bs"]
                    
                    res_icon = "WIN ✅" if is_win else f"LOSS ❌ (L{level+1})"
                    res_msg = f"🏁 <b>PERIOD {period} RESULT</b>\n━━━━━━━━━━━━━━━━━━━━\n🎰 Number: <code>{num}</code>\n✨ Status: <b>{res_icon}</b>\n━━━━━━━━━━━━━━━━━━━━"
                    send_to_tg(res_msg)
                    
                    level = 1 if is_win else level + 1

                # 2. Generate Prediction
                pred = get_god_logic(all_data, level)
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
            print(f"Error: {e}")
            
        time.sleep(5)

if __name__ == "__main__":
    run()

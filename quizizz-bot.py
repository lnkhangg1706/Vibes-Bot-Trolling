import requests, random, threading, time, uuid, os
from colorama import Fore, Style, init

init(autoreset=True)
Y, G, C, W, A, R= Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.WHITE, Fore.MAGENTA, Style.RESET_ALL
print_lock = threading.Lock()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Content-Type": "application/json"
}

def get_room_hash(code):
    try:
        resp = requests.post("https://game.quizizz.com/play-api/v5/checkRoom", json={"roomCode": code}, headers=HEADERS)
        if resp.status_code == 200: return resp.json().get("room", {}).get("hash")
    except: pass
    return None

def spawn_bot(room_hash):
    bot_name = f"HàĐỗ {random.randint(1000, 9999)}"
    payload = {
        "roomHash": room_hash,
        "ip": f"127.0.{random.randint(0,255)}.{random.randint(0,255)}",
        "player": {"id": bot_name, "name": bot_name, "avatarId": random.randint(1, 20), "uid": str(uuid.uuid4())}
    }
    try:
        resp = requests.post("https://game.quizizz.com/play-api/v5/join", json=payload, headers=HEADERS)
        with print_lock:
            name_display = bot_name.ljust(40)
            if resp.status_code == 200:
                print(f"{Y}> {G}Đã vào: {W}{name_display}")
            else:
                print(f"{Y}> {Fore.RED}Lỗi {resp.status_code}: {name_display}")
    except:
        with print_lock: print(f"{Y}> {Fore.RED}Mất kết nối: {bot_name}")

def run_wave(room_hash, amount):
    print(f"{Y}[OK] Đang tổng tiến công {W}{amount} {Y}vạn quân...\n")
    threads = []
    for i in range(amount):
        t = threading.Thread(target=spawn_bot, args=(room_hash,))
        t.start(); threads.append(t)
        time.sleep(0.05)
    for t in threads: t.join()
    print(f"\n{G}[OK] XONG! Kiểm tra sảnh chờ ngay nhé Khang.")

def get_valid_input(prompt_text, default_val=None):
    while True:
        raw = input(prompt_text).strip()
        if not raw:
            if default_val is not None: return default_val
            else: return None
        try:
            val = int(raw)
            if val <= 0:
                print(f"{Fore.RED}ERROR!")
                continue
            return val
        except ValueError:
            print(f"{Fore.RED}ERROR!")

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')

    while True:
        GAME_CODE = input(f"{A}> Mã phòng: {W}").strip()
        room_hash = get_room_hash(GAME_CODE)

        if room_hash:
            break 
        else:
            print(f"{Fore.RED}[x] Không tìm thấy phòng. Vui lòng kiểm tra lại mã!\n")

    print(f"\n{G}[OK] Mục tiêu: {W}{room_hash[:10]}...")
    
    SO_LUONG = get_valid_input(f"{C}> Số lượng (Mặc định 10): {W}", 10)
    run_wave(room_hash, SO_LUONG)
    
    while True:
        more = get_valid_input(f"{C}> Nhập số lượng đợt tiếp (Enter để thoát): {W}")
        if more is None: exit()
        run_wave(room_hash, more)

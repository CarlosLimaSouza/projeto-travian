from datetime import datetime, timedelta, timezone

# Horário de Brasília (GMT-3)
BR_TZ = timezone(timedelta(hours=-3))

def log(msg):
    now = datetime.now(BR_TZ).strftime('%d/%m/%Y %H:%M:%S')
    full_msg = f"[{now}] {msg}"
    print(full_msg)
    with open("travian_bot.log", "a", encoding="utf-8") as f:
        f.write(full_msg + "\n")
import pandas as pd
import datetime
import requests

# =========只填你的Server酱密钥，别的什么都不要修改========
SENDKEY = "SCT418553TV2BUZTVt5srYAWnEmaSvxdbP"
# ==========================================================

df = pd.read_excel("banbiao.xlsx", engine="openpyxl")
df["date"] = pd.to_datetime(df["date"])

today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)

tomorrow_df = df[df["date"] == pd.to_datetime(tomorrow)]
if len(tomorrow_df) <= 0:
    exit()
shift_tom = tomorrow_df.iloc[0]["shift"]
if pd.isna(shift_tom):
    exit()

msg_title = f"⚠️明日{tomorrow}班次提醒"
msg_content = f"班次：{shift_tom}"

def send_wx(title,content):
    url = f"https://sctapi.ftqq.com/{SENDKEY}.send"
    requests.post(url, data={"title":title,"desp":content})

if shift_tom == "大夜":
    send_wx(msg_title + "【大夜班第一次提醒】", msg_content)
else:
    send_wx(msg_title, msg_content)

today_df = df[df["date"] == pd.to_datetime(today)]
if len(today_df) > 0:
    shift_now = today_df.iloc[0]["shift"]
    if not pd.isna(shift_now) and shift_now == "大夜":
        send_wx("🔔今日大夜班二次提醒", f"今日{today}为大夜班，记得上班！")

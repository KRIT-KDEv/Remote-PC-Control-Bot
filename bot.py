import telebot
import os
import webbrowser
import psutil
import pyautogui
import time
import datetime
import speedtest
import socket  

# --- 1. CONFIGURATION ---
# ใส่ Token และ ID ของคุณที่นี่
API_TOKEN = '' 
MY_CHAT_ID = ''
bot = telebot.TeleBot(API_TOKEN)

# ตัวแปรสถานะสำหรับการยกเลิก Shutdown/Restart
shutdown_active = False 

# ฟังก์ชันตรวจสอบสิทธิ์เจ้าของ
def is_owner(message):
    return message.chat.id == MY_CHAT_ID

# --- 2. COMMAND HANDLERS ---

# คำสั่ง /start และ /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if is_owner(message):
        help_text = (
            "🤖 **KAITOBOy PC Remote Control - Command Guide**\n"
            "*(Tap a command to execute it instantly)*\n"
            "--------------------------------------\n"
            "📊 **System Monitoring**\n"
            "├ /status - View CPU, RAM, & Disk usage\n"
            "└ /speedtest - Test Internet Speed (30-60s)\n\n"
            
            "🎮 **Remote Utilities**\n"
            "├ /screenshot - Capture current screen\n"
            "└ /open - Open URL (e.g., `/open google.com`)\n\n"
            
            "🔌 **Power Management**\n"
            "├ /shutdown - Power off PC (30s delay)\n"
            "├ /restart - Reboot PC (30s delay)\n"
            "└ /cancel - **STOP** Shutdown or Restart\n"
            "--------------------------------------\n"
            "💡 *Tip: If you accidentally shutdown, tap /cancel immediately!*"
        )
        bot.reply_to(message, help_text, parse_mode='Markdown')
    else:
        bot.reply_to(message, "❌ **Access Denied.**", parse_mode='Markdown')

# คำสั่ง /status
@bot.message_handler(commands=['status'])
def status_detailed(message):
    if is_owner(message):
        cpu_usage = psutil.cpu_percent(interval=1)
        cpu_freq = psutil.cpu_freq().current / 1000 
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('C:')
        
        boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.datetime.now() - boot_time
        uptime_str = str(uptime).split('.')[0]

        status_text = (
            "🖥 **Detailed System Status**\n"
            "----------------------------\n"
            f"⏱ **Uptime:** `{uptime_str}`\n"
            f"⚡ **CPU:** `{cpu_usage}%` @ `{cpu_freq:.2f} GHz`\n"
            f"🧠 **RAM:** `{ram.percent}%` (Used: {round(ram.used/(1024**3), 2)}GB / {round(ram.total/(1024**3), 2)}GB)\n"
            f"💽 **Disk (C:):** `{disk.percent}%` (Free: {round(disk.free/(1024**3), 2)}GB)\n"
            "----------------------------\n"
            f"📅 **Date:** `{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`"
        )
        bot.reply_to(message, status_text, parse_mode='Markdown')

# คำสั่ง /screenshot
@bot.message_handler(commands=['screenshot'])
def take_screenshot(message):
    if is_owner(message):
        file_path = "screen.png"
        pyautogui.screenshot(file_path)
        with open(file_path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption="📸 Current Screen")
        os.remove(file_path)

# คำสั่ง /open [url]
@bot.message_handler(commands=['open'])
def open_link(message):
    if is_owner(message):
        try:
            url = message.text.split(maxsplit=1)[1]
            if not url.startswith('http'): url = 'https://' + url
            webbrowser.open(url)
            bot.reply_to(message, f"🌐 Opening: {url}")
        except IndexError:
            bot.reply_to(message, "⚠️ Usage: /open google.com")

# คำสั่ง /shutdown
@bot.message_handler(commands=['shutdown'])
def shutdown_pc(message):
    global shutdown_active
    if is_owner(message):
        shutdown_active = True
        msg = bot.reply_to(message, "⚠️ **System will shutdown in 30 seconds.**\nUse /cancel to stop.")
        os.system("shutdown /s /t 30")
        for i in range(30, 0, -1):
            if not shutdown_active: return 
            if i <= 5:
                try: bot.edit_message_text(f"🔴 Shutdown in {i} seconds...", message.chat.id, msg.message_id)
                except: pass
            time.sleep(1)
        if shutdown_active:
            bot.edit_message_text("💀 Shutting down now!", message.chat.id, msg.message_id)

# คำสั่ง /restart
@bot.message_handler(commands=['restart'])
def restart_pc(message):
    global shutdown_active
    if is_owner(message):
        shutdown_active = True
        msg = bot.reply_to(message, "🔄 **Restart initiated (30s remaining...)**")
        os.system("shutdown /r /t 30")
        for i in range(30, 0, -1):
            if not shutdown_active: return 
            if i <= 5:
                try: bot.edit_message_text(f"🔴 Restarting in {i} seconds...", message.chat.id, msg.message_id)
                except: pass
            time.sleep(1)
        if shutdown_active:
            bot.edit_message_text("🔄 Restarting now!", message.chat.id, msg.message_id)

# คำสั่ง /cancel (ใช้ได้ทั้ง Shutdown และ Restart)
@bot.message_handler(commands=['cancel'])
def abort_power_action(message):
    global shutdown_active
    if is_owner(message):
        shutdown_active = False 
        os.system("shutdown /a")
        bot.reply_to(message, "✅ **Action cancelled.** Your PC is safe.")

# คำสั่ง /speedtest
@bot.message_handler(commands=['speedtest'])
def run_speedtest(message):
    if is_owner(message):
        msg = bot.reply_to(message, "⏳ **Running Speedtest...** (Wait 30-60s)")
        try:
            st = speedtest.Speedtest(secure=True)
            st.get_best_server()
            download_speed = st.download() / 1_000_000
            upload_speed = st.upload() / 1_000_000
            result = (
                "🚀 **Internet Speedtest Result**\n"
                f"📥 **Download:** `{download_speed:.2f} Mbps`\n"
                f"📤 **Upload:** `{upload_speed:.2f} Mbps`\n"
                f"⚡ **Ping:** `{st.results.ping} ms`"
            )
            bot.edit_message_text(result, message.chat.id, msg.message_id, parse_mode='Markdown')
        except Exception as e:
            bot.edit_message_text(f"❌ Error: {str(e)}", message.chat.id, msg.message_id)

# --- 3. STARTUP NOTIFICATION ---
try:
    time.sleep(2) # ให้เวลาเน็ตเชื่อมต่อสักครู่
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    startup_text = (
        "🚀 **KAITOBOy PC is Online & Ready!**\n"
        f"📅 **Time:** `{datetime.datetime.now().strftime('%H:%M:%S')}`\n"
        f"🏠 **Device:** `{hostname}`\n"
        f"📍 **IP:** `{local_ip}`\n"
        "------------------------\n"
        "Typing /help for looking command"
    )
    bot.send_message(MY_CHAT_ID, startup_text, parse_mode='Markdown')
except Exception as e:
    print(f"Startup notify failed: {e}")

# --- 4. RUN BOT ---
print("Kaitoboy Bot is running...")
bot.polling(none_stop=True)
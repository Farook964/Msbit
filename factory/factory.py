import os
import asyncio
import subprocess
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# **إعدادات المصنع**
MAIN_BOT_TOKEN = 'YOUR_MAIN_BOT_TOKEN_HERE'  # ضع توكن البوت الرئيسي هنا
API_ID = 29677860  # ضع API ID الخاص بك هنا
API_HASH = '785da04e1d7d75c744632dacd6134d34'  # ضع API Hash الخاص بك هنا

# **مسارات المجلدات**
BOTS_DIR = "bots"
SESSIONS_DIR = "sessions"

# **إنشاء المجلدات إذا لم تكن موجودة**
os.makedirs(BOTS_DIR, exist_ok=True)
os.makedirs(SESSIONS_DIR, exist_ok=True)

# **اسم الجلسة للبوت الرئيسي**
MAIN_SESSION = "factory_bot"

# **تشغيل البوت الرئيسي**
main_app = Client(MAIN_SESSION, api_id=API_ID, api_hash=API_HASH, bot_token=MAIN_BOT_TOKEN)

# **قائمة لتتبع البوتات النشطة**
active_bots = {}

# **كود البوت الفرعي كنص**
bot_code_template = """
from pyrogram import Client, filters
from pyrogram.errors import UsernameNotOccupied, UsernameInvalid, FloodWait
import asyncio
import string
import itertools

# كامل الحقوق في هذه الاداة والملف للمطورة ##سحر  ℚ𝕦𝕖𝕖𝕟 𝕒𝕟𝕕 #𝔼𝕞𝕡𝕣𝕖𝕤𝕤 𝕠𝕗 #𝕥𝕙𝕖 𝕄𝕚𝕕𝕕𝕝𝕖 #𝔼𝕒𝕤𝕥 

api_id = {api_id}
api_hash = '{api_hash}'
bot_token = '{bot_token}'

session_name = "{session_name}"
app = Client(session_name, api_id, api_hash, bot_token=bot_token)

running = False
checked_count = 0
total_usernames = 0

async def generate_usernames(base):
    usernames = set()
    for combo in itertools.product(string.ascii_lowercase + string.digits, repeat=2):
        if base.isalpha() and len(base) == 1:
            username = f"{{base}}_{{combo[0]}}_{{combo[1]}}"
            usernames.add(username)
    return list(usernames)

async def generate_custom_usernames(base):
    letters = string.ascii_lowercase
    digits = string.digits
    usernames = set()

    for combo in itertools.product(letters + digits, repeat=2):
        combo_str = ''.join(combo)
        username = f"{{base}}_{{combo_str}}"
        usernames.add(username)

    return list(usernames)

async def check_usernames(usernames, message):
    global running, checked_count, total_usernames
    available_usernames = []
    total_usernames = len(usernames)
    checked_count = 0

    for username in usernames:
        if not running:
            await message.reply("✅ **تـم إيـقـاف الـفـحـص.**")
            return

        try:
            user = await app.get_users(username)
            result_message = f"❌ **الـيـوزر @{username} مـسـتـخدم 😐**"
            await message.reply(result_message)

        except UsernameNotOccupied:
            available_message = f"✅ **الـيـوزر @{username} مـتـاح 🥳**"
            await message.reply(available_message)
            available_usernames.append(username)

        except FloodWait as e:
            wait_time = e.x + 5
            await message.reply(f"⚠️ **مطلوب الانتظار لمدة {{wait_time}} ثانية بسبب FloodWait.**")
            await asyncio.sleep(wait_time)
            continue

        except UsernameInvalid:
            error_message = f"⚠️ **الـيـوزر @{username} غـيـر صـالـح.**"
            await message.reply(error_message)

        except Exception as e:
            error_message = f"⚠️ **حـدث خـطـأ أثـنـاء فـحـص @{username}: {{e}}**"
            await message.reply(error_message)

        await asyncio.sleep(5)  
        checked_count += 1

    if available_usernames:
        available_str = "\\n".join([f"@{{uname}}" for uname in available_usernames])
        await message.reply(f"✅ **الأسـمـاء الـمـتـاحـة:**\\n{{available_str}}")
    else:
        await message.reply("⚠️ **لـم يـتـم الـعـثـور عـلـى أسـمـاء مـتـاحـة.**")

    running = False

@app.on_message(filters.command("start", prefixes="/"))
async def handle_start(client, message):
    await message.reply(
        "👋 **مـرحـبـاً بـك فـي بـوت سـورس𝐒𝐁𓁒 لـفـحـص أسـمـاء الـمـسـتـخـدمـيـن!**\\n"
        "💡 **اسـتـخـدم الأوامـر الـتـالـيـة لـلـبـدء:**\\n"
        "📌 /check <حـرف> - **لـفـحـص الأسـمـاء الـثـلاثـيـة.**\\n"
        "📌 /custom_check <حـرفـيـن> - **لـفـحـص الأسـمـاء الـربـاعـيـة.**\\n"
        "📌 /check_us <قـاعـدة> - **لـفـحـص الأسـمـاء بـنـاءً عـلـى الـقـاعـدة الـخـاصـة بـك.**\\n"
        "📌 /status - **لـمـعـرفـة تـقـدم الـفـحـص الـحـالـي.**\\n"
        "📌 /stop - **لإيـقـاف الـفـحـص الـجـاري.**\\n"
        "📌 /help - **لـعـرض قـائـمـة الأوامـر.**"
    )

@app.on_message(filters.command("check", prefixes="/"))
async def handle_check(client, message):
    global running
    if running:
        await message.reply("⚠️ **الـفـحـص قـيـد الـتـشـغـيـل بـالـفـعـل.**")
        return

    if len(message.command) < 2:
        await message.reply("⚠️ **الـرجـاء تـحـديـد قـاعـدة الـبـحث. مـثـال: /check S**")
        return

    base = message.command[1]
    if not base.isalpha() or len(base) != 1:
        await message.reply("⚠️ **الـقـاعـدة يـجـب أن تـكـون حـرفًـا واحـدًا فـقـط.**")
        return

    running = True
    await message.reply(f"👋 **سـأقـوم بـفـحـص الأسماء الـثـلاثـيـة بـنـاءً عـلـى الـقـاعـدة `{{base}}`. انـتظـر قـلـيلاً...**")

    usernames = await generate_usernames(base.lower())
    await check_usernames(usernames, message)

@app.on_message(filters.command("custom_check", prefixes="/"))
async def handle_custom_check(client, message):
    global running
    if running:
        await message.reply("⚠️ **الـفـحـص قـيـد الـتـشـغـيـل بـالفـعـل.**")
        return

    if len(message.command) < 2:
        await message.reply("⚠️ **الـرجـاء تـحـديـد قـاعـدة الـفـحـص. مـثـال: /custom_check Aa**")
        return

    base = message.command[1]
    if not base.isalpha() or len(base) != 2:
        await message.reply("⚠️ **الـقـاعـدة يـجـب أن تـكـون حـرفـيـن فـقـط.**")
        return

    running = True
    await message.reply(f"👋 **سـأقـوم بـفـحـص الأسـمـاء الـربـاعـيـة بـنـاءً عـلـى الـقـاعـدة `{{base}}`. انـتظــر قـلـيلاً...**")

    usernames = await generate_custom_usernames(base.lower())
    await check_usernames(usernames, message)

@app.on_message(filters.command("check_us", prefixes="/"))  
async def handle_check_us(client, message):
    global running
    if running:
        await message.reply("⚠️ **الـفـحـص قـيـد الـتـشـغـيـل بـالـفـعـل.**")
        return

    if len(message.command) < 2:
        await message.reply("⚠️ **الـرجـاء تـحـديـد قـاعـدة الـفـحـص. مـثـال: /check_us dddd**")
        return

    base = message.command[1]
    if not base.isalpha() or len(base) < 1:
        await message.reply("⚠️ **الـقـاعـدة يـجـب أن تـكـون حـرفًـا واحـدًا أو أكـثـر.**")
        return

    running = True
    await message.reply(f"👋 **سـأقـوم بـفـحـص الأسـمـاء بـنـاءً عـلـى الـقـاعـدة `{{base}}`. انـتـظـر قـلـيلاً...**")

    usernames = []

    for char in string.ascii_lowercase:
        usernames.append(f"@{{base}}{{char}}")  

    for number in range(1, 11):
        usernames.append(f"@{{base}}{{number}}")  

    await check_usernames(usernames, message)

@app.on_message(filters.command("stop", prefixes="/"))
async def handle_stop(client, message):
    global running
    if not running:
        await message.reply("⚠️ **لا يـوجـد فـحـص قـيـد الـتـشـغـيـل.**")
    else:
        running = False
        await message.reply("✅ **تـم إيـقـاف الـفـحـص.**")

@app.on_message(filters.command("status", prefixes="/"))
async def handle_status(client, message):
    if running:
        progress = (checked_count / total_usernames) * 100 if total_usernames > 0 else 0
        await message.reply(f"🔍 **الـفـحـص قـيـد الـتـقـدم... {{progress:.2f}}% تـم فـحـصـهـا 📊**")
    else:
        await message.reply("⚠️ **لا يـوجـد فـحـص قـيـد الـتـشـغـيـل حـالـيـاً.**")

@app.on_message(filters.command("help", prefixes="/"))
async def handle_help(client, message):
    await message.reply(
        "👋 **أهـلاً بـك فـي بـوت سـورس 𝐒𝐁𓁒 🫂 لـفـحـص الأسـمـاء هـذا الـمـلـف والـبـوت حـقـوقـه كامـلـة لـلـمـطـورة سـحـر 𝐒𝐁𓁒👩🏻‍💻  إلـيـك الأوامـر الـمـتـاحـة:**\\n"
        "📌 /check <حـرف> - **لـفـحـص الأسـمـاء الـثـلاثـيـة.**\\n"
        "📌 /custom_check <حـرفـيـن> - **لـفـحـص الأسـمـاء الـربـاعـيـة.**\\n"
        "📌 /check_us <قـاعـدة> - **لـفـحـص الأسـمـاء بـنـاءً عـلـى الـقـاعـدة الـخـاصـة بـك.**\\n"
        "📌 /status - **لـمـعـرفـة تـقـدم الـفـحـص الـحـالـي.**\\n"
        "📌 /stop - **لإيـقـاف الـفـحـص الـجـاري.**\\n"
        "📌 /help - **لـعـرض قـائـمـة الأوامـر.**"
    )

# **إضافة بوت جديد باستخدام التوكن المدخل**
@main_app.on_message(filters.command("addbot", prefixes="/"))
async def add_bot(client, message):
    if len(message.command) < 2:
        await message.reply("⚠️ **الرجاء إدخال التوكن. مثال: /addbot YOUR_BOT_TOKEN**")
        return

    bot_token = message.command[1]
    session_name = f"bot_{len(active_bots) + 1}"

    try:
        # إنشاء كود البوت الفرعي
        bot_code = bot_code_template.format(
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=bot_token,
            session_name=session_name
        )

        # حفظ كود البوت الفرعي في ملف
        bot_file_path = os.path.join(BOTS_DIR, f"{session_name}.py")
        with open(bot_file_path, 'w', encoding='utf-8') as f:
            f.write(bot_code)

        # تشغيل البوت الفرعي كعملية منفصلة
        process = subprocess.Popen(['python', bot_file_path])

        # إضافة البوت إلى القائمة النشطة
        active_bots[session_name] = process

        # إرسال رسالة تأكيد
        await message.reply(f"✅ **تم إنشاء بوت جديد بنجاح باسم الجلسة `{session_name}`!**")

    except Exception as e:
        await message.reply(f"⚠️ **حدث خطأ أثناء إنشاء البوت: {e}**")

# **حذف بوت موجود**
@main_app.on_message(filters.command("removebot", prefixes="/"))
async def remove_bot(client, message):
    if len(message.command) < 2:
        await message.reply("⚠️ **الرجاء إدخال اسم الجلسة للبوت المراد حذفه. مثال: /removebot bot_1**")
        return

    session_name = message.command[1]
    process = active_bots.get(session_name)

    if process:
        process.terminate()
        await message.reply(f"✅ **تم إيقاف البوت باسم الجلسة `{session_name}` بنجاح.**")
        del active_bots[session_name]

        # حذف ملف البوت الفرعي
        bot_file = os.path.join(BOTS_DIR, f"{session_name}.py")
        if os.path.exists(bot_file):
            os.remove(bot_file)

        # حذف ملف الجلسة
        session_file = os.path.join(SESSIONS_DIR, f"{session_name}.session")
        if os.path.exists(session_file):
            os.remove(session_file)
    else:
        await message.reply(f"⚠️ **لم يتم العثور على بوت باسم الجلسة `{session_name}`.**")

# **عرض قائمة البوتات النشطة**
@main_app.on_message(filters.command("listbots", prefixes="/"))
async def list_bots(client, message):
    if not active_bots:
        await message.reply("⚠️ **لا توجد بوتات نشطة حاليًا.**")
        return

    bots_list = "\n".join([f"`{name}`" for name in active_bots.keys()])
    await message.reply(f"✅ **البوتات النشطة الحالية:**\n{bots_list}")

if __name__ == '__main__':
    main_app.run()

import sqlite3
from datetime import datetime, timedelta
import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Emoji mapping for courses
course_emojis = {
    "ICT 1109 CHEMISTRY": "🧪",
    "ICT 1103 PROGRAMMING": "💻",
    "ICT 1107 CALCULUS": "🧮",
    "ICT 1102 EEE LAB": "⚡",
    "ICT 1101 EEE": "⚡",
    "ICT 1104 PROGRAMMING LAB": "💻",
    "ICT 1105 PHYSICS": "⚛️"
}

# States for the conversation handler
DAY, CLASS_NAME, START_TIME, END_TIME, DELETE_DAY, DELETE_CLASS = range(6)

# Connect to the SQLite database to fetch the schedule data
def get_classes_for_day(day: str):
    try:
        conn = sqlite3.connect("schedule.db")
        cursor = conn.cursor()
        cursor.execute("SELECT class_name, start_time, end_time FROM Classes WHERE day = ?", (day,))
        classes = cursor.fetchall()
        conn.close()
        return classes
    except sqlite3.Error as e:
        logger.error("Database error: %s", e)
        return []

# Function to format the schedule with emojis
def format_schedule(classes):
    response = ""
    for class_name, start_time, end_time in classes:
        emoji = course_emojis.get(class_name, "")  # Get the emoji for the class
        response += f"▶️ {start_time} - {end_time}: {emoji} *{class_name}*\n"
    return response

# Set up the GMT+6 timezone
tz = pytz.timezone("Asia/Dhaka")  # GMT+6 timezone

#function to get todays schedule
async def todays_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Get the current time in GMT+6
    now = datetime.now(tz)

    # Format the day and date using the timezone
    today_day_full = now.strftime("%A")  # Full name of the day (e.g., "Thursday")
    today_day_abbr = now.strftime("%a").upper()  # Abbreviated name for fetching data (e.g., "THU")
    today_date = now.strftime("%d-%m-%Y")

    # Fetch the classes for today
    classes = get_classes_for_day(today_day_abbr)

    # Format the response
    if not classes:
        response = f"❌ *No classes scheduled for today ({today_date}, {today_day_full})* ❌"
    else:
        response = f" *Today's Schedule ({today_date}, {today_day_full}):*\n\n"
        response += format_schedule(classes)

    # Send the reply
    await update.message.reply_text(response, parse_mode="Markdown")


# Function to get tomorrow's schedule
async def tomorrows_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Calculate tomorrow's date and day
    tomorrow_datetime = datetime.now(tz) + timedelta(days=1)
    tomorrow_day_full = tomorrow_datetime.strftime("%A")  # Full name of the day (e.g., "Friday")
    tomorrow_day_abbr = tomorrow_datetime.strftime("%a").upper()  # Abbreviated name for fetching data (e.g., "FRI")
    tomorrow_date = tomorrow_datetime.strftime("%d-%m-%Y")

    # Fetch the classes for tomorrow
    classes = get_classes_for_day(tomorrow_day_abbr)

    # Format the response
    if not classes:
        response = f"❌ *No classes scheduled for tomorrow ({tomorrow_date}, {tomorrow_day_full})* ❌"
    else:
        response = f" *Tomorrow's Schedule ({tomorrow_date}, {tomorrow_day_full}):*\n\n"
        response += format_schedule(classes)

    # Send the reply
    await update.message.reply_text(response, parse_mode="Markdown")


# Other daily schedule functions follow the same pattern as `todays_schedule` and `tomorrows_schedule`.
# Function to get Saturday's schedule
async def saturdays_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    saturday_day = "SAT"
    saturday_date = (datetime.now() + timedelta((5 - datetime.now().weekday()) % 7)).strftime("%d-%m-%Y")
    classes = get_classes_for_day(saturday_day)

    if not classes:
        response = f"❌ *No classes scheduled for Saturday ({saturday_date})* ❌"
    else:
        response = f" *Saturday's Schedule ({saturday_date})*: \n\n"
        response += format_schedule(classes)

    await update.message.reply_text(response, parse_mode="Markdown")

# Function to get Sunday's schedule
async def sundays_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    sunday_day = "SUN"
    sunday_date = (datetime.now() + timedelta((6 - datetime.now().weekday()) % 7)).strftime("%d-%m-%Y")
    classes = get_classes_for_day(sunday_day)

    if not classes:
        response = f"❌ *No classes scheduled for Sunday ({sunday_date})* ❌"
    else:
        response = f" *Sunday's Schedule ({sunday_date})*: \n\n"
        response += format_schedule(classes)

    await update.message.reply_text(response, parse_mode="Markdown")

# Function to get Monday's schedule
async def mondays_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    monday_day = "MON"
    monday_date = (datetime.now() + timedelta((0 - datetime.now().weekday()) % 7)).strftime("%d-%m-%Y")
    classes = get_classes_for_day(monday_day)

    if not classes:
        response = f"❌ *No classes scheduled for Monday ({monday_date})* ❌"
    else:
        response = f" *Monday's Schedule ({monday_date})*: \n\n"
        response += format_schedule(classes)

    await update.message.reply_text(response, parse_mode="Markdown")

# Function to get Tuesday's schedule
async def tuesdays_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    tuesday_day = "TUE"
    tuesday_date = (datetime.now() + timedelta((1 - datetime.now().weekday()) % 7)).strftime("%d-%m-%Y")
    classes = get_classes_for_day(tuesday_day)

    if not classes:
        response = f"❌ *No classes scheduled for Tuesday ({tuesday_date})* ❌"
    else:
        response = f" *Tuesday's Schedule ({tuesday_date})*: \n\n"
        response += format_schedule(classes)

    await update.message.reply_text(response, parse_mode="Markdown")

# Function to get Wednesday's schedule
async def wednesdays_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    wednesday_day = "WED"
    wednesday_date = (datetime.now() + timedelta((2 - datetime.now().weekday()) % 7)).strftime("%d-%m-%Y")
    classes = get_classes_for_day(wednesday_day)

    if not classes:
        response = f"❌ *No classes scheduled for Wednesday ({wednesday_date})* ❌"
    else:
        response = f" *Wednesday's Schedule ({wednesday_date})*: \n\n"
        response += format_schedule(classes)

    await update.message.reply_text(response, parse_mode="Markdown")

# Function to get Thursday's schedule
async def thursdays_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    thursday_day = "THU"
    thursday_date = (datetime.now() + timedelta((3 - datetime.now().weekday()) % 7)).strftime("%d-%m-%Y")
    classes = get_classes_for_day(thursday_day)

    if not classes:
        response = f"❌ *No classes scheduled for Thursday ({thursday_date})* ❌"
    else:
        response = f" *Thursday's Schedule ({thursday_date})*: \n\n"
        response += format_schedule(classes)

    await update.message.reply_text(response, parse_mode="Markdown")


# Function to send bot's intro message when `/start` is called
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    response = "👋 Hello! I'm your Schedule Bot. I can provide you with your class schedule for each day.\n\n" \
               "Here are the commands you can use:\n\n" \
               "/today - Get today's schedule\n" \
               "/tomorrow - Get tomorrow's schedule\n" \
               "/sat - Get Saturday's schedule\n" \
               "/sun - Get Sunday's schedule\n" \
               "/mon - Get Monday's schedule\n" \
               "/tue - Get Tuesday's schedule\n" \
               "/wed - Get Wednesday's schedule\n" \
               "/thu - Get Thursday's schedule\n\n" \
               "Just type a command to get the corresponding day's schedule!"
    
    await update.message.reply_text(response, parse_mode="Markdown")

# Function to show all available commands when `/help` is called
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    response = "ℹ️ *Available Commands:*\n\n" \
               "/start - Introduction to the bot\n" \
               "/help - Show this help message\n" \
               "/today - Get today's class schedule\n" \
               "/tomorrow - Get tomorrow's class schedule\n" \
               "/sat - Get Saturday's class schedule\n" \
               "/sun - Get Sunday's class schedule\n" \
               "/mon - Get Monday's class schedule\n" \
               "/tue - Get Tuesday's class schedule\n" \
               "/wed - Get Wednesday's class schedule\n" \
               "/thu - Get Thursday's class schedule\n"
    
    await update.message.reply_text(response, parse_mode="Markdown")
    
#------------------------------------------
# Replace 'GROUP_CHAT_ID' with the ID of your group chat
# GROUP_CHAT_ID = '1130904432'

async def send_scheduled_message(application, group_chat_id):
    tomorrow_day = (datetime.now() + timedelta(days=1)).strftime("%a").upper()
    tomorrow_date = (datetime.now() + timedelta(days=1)).strftime("%d-%m-%Y")
    classes = get_classes_for_day(tomorrow_day)

    if not classes:
        response = f"❌ *No classes scheduled for tomorrow ({tomorrow_date})* ❌"
    else:
        response = f" *Tomorrow's Schedule ({tomorrow_date})*: \n\n"
        response += format_schedule(classes)

    # Send the message to the group chat
    await application.bot.send_message(chat_id=group_chat_id, text=response, parse_mode="Markdown")
    logger.info("Scheduled message sent to the group.")
    
    
    
# Custom Message Command
async def custom_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.args:
        message = " ".join(context.args)
        await update.message.reply_text(f"📢 {message}")
    else:
        await update.message.reply_text("⚠️ Please provide a message after the command.")


# Start adding a new schedule (conversation handler)
async def add_schedule_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Please enter the day for the new class (e.g., MON, TUE):")
    return DAY

# Collect day, then ask for class name
async def add_schedule_day(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["day"] = update.message.text.strip().upper()
    await update.message.reply_text("Enter the class name:")
    return CLASS_NAME

# Collect class name, then ask for start time
async def add_schedule_class_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["class_name"] = update.message.text.strip()
    await update.message.reply_text("Enter the start time (e.g., 10:00):")
    return START_TIME

# Collect start time, then ask for end time
async def add_schedule_start_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["start_time"] = update.message.text.strip()
    await update.message.reply_text("Enter the end time (e.g., 11:00):")
    return END_TIME

# Collect end time and save the new class to the database
async def add_schedule_end_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["end_time"] = update.message.text.strip()
    try:
        conn = sqlite3.connect("schedule.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Classes (day, class_name, start_time, end_time) VALUES (?, ?, ?, ?)", 
                       (context.user_data["day"], context.user_data["class_name"], context.user_data["start_time"], context.user_data["end_time"]))
        conn.commit()
        conn.close()
        await update.message.reply_text("✅ Class added successfully!")
    except sqlite3.Error as e:
        logger.error("Database error: %s", e)
        await update.message.reply_text("❌ Error adding class. Please try again.")
    return ConversationHandler.END

# Start deleting a schedule (conversation handler)
async def delete_schedule_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Enter the day of the class you want to delete:")
    return DELETE_DAY

# Collect day, then ask for class name to delete
async def delete_schedule_day(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["day"] = update.message.text.strip().upper()
    await update.message.reply_text("Enter the class name to delete:")
    return DELETE_CLASS

# Delete the specified class from the database
async def delete_schedule_class(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    class_name = update.message.text.strip()
    try:
        conn = sqlite3.connect("schedule.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Classes WHERE day = ? AND class_name = ?", (context.user_data["day"], class_name))
        conn.commit()
        conn.close()
        await update.message.reply_text("✅ Class deleted successfully!")
    except sqlite3.Error as e:
        logger.error("Database error: %s", e)
        await update.message.reply_text("❌ Error deleting class. Please try again.")
    return ConversationHandler.END


# async def current_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     logger.info("Time command invoked.")
#     try:
#         now = datetime.now(tz)
#         time_str = now.strftime("%I:%M %p, %A, %d-%m-%Y")
#         await update.message.reply_text(f"🕰️ *Current Time:* {time_str}", parse_mode="Markdown")
#         logger.info("Time sent successfully.")
#     except Exception as e:
#         logger.error("Error in /time command: %s", e)

async def current_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    tz = pytz.timezone("Asia/Dhaka")
    now = datetime.now(tz)
    time_str = now.strftime("%I:%M %p, %A, %d-%m-%Y")
    await update.message.reply_text(f"🕰️ *Current Time:* {time_str}", parse_mode="Markdown")



# Main function to start the bot
def main():
    application = ApplicationBuilder().token('7916791560:AAFUraNz5l2JWo9ipS_yh2LLwUuQlahMHFk').build()

    # Add the handlers for each command
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("today", todays_schedule))
    application.add_handler(CommandHandler("tomorrow", tomorrows_schedule))
    application.add_handler(CommandHandler("sat", saturdays_schedule))
    application.add_handler(CommandHandler("sun", sundays_schedule))
    application.add_handler(CommandHandler("mon", mondays_schedule))
    application.add_handler(CommandHandler("tue", tuesdays_schedule))
    application.add_handler(CommandHandler("wed", wednesdays_schedule))
    application.add_handler(CommandHandler("thu", thursdays_schedule))
    application.add_handler(CommandHandler("custom", custom_message))
    
    # Add this command handler in the main function
    application.add_handler(CommandHandler("time", current_time))
    
    # Add the /tomorrow command handler
    application.add_handler(CommandHandler("tomorrow", tomorrows_schedule))

    # Set up the scheduler (APScheduler) to send the message every day at 8 AM
    scheduler = AsyncIOScheduler()
    group_chat_id = '-1002295712106'  # Replace with your group chat ID
    scheduler.add_job(lambda: send_scheduled_message(application, group_chat_id), 'cron', hour=13, minute=20)

    # Log scheduler start
    logger.info("Starting scheduler...")
    # Start the scheduler
    scheduler.start()

    # Conversation handler for adding schedules
    add_schedule_handler = ConversationHandler(
        entry_points=[CommandHandler("add_schedule", add_schedule_start)],
        states={
            DAY: [MessageHandler(filters.TEXT, add_schedule_day)],
            CLASS_NAME: [MessageHandler(filters.TEXT, add_schedule_class_name)],
            START_TIME: [MessageHandler(filters.TEXT, add_schedule_start_time)],
            END_TIME: [MessageHandler(filters.TEXT, add_schedule_end_time)],
        },
        fallbacks=[]
    )

    # Conversation handler for deleting schedules
    delete_schedule_handler = ConversationHandler(
        entry_points=[CommandHandler("delete_schedule", delete_schedule_start)],
        states={
            DELETE_DAY: [MessageHandler(filters.TEXT, delete_schedule_day)],
            DELETE_CLASS: [MessageHandler(filters.TEXT, delete_schedule_class)],
        },
        fallbacks=[]
    )

    application.add_handler(add_schedule_handler)
    application.add_handler(delete_schedule_handler)

    # Start the bot
    logger.info("Starting bot...")
    application.run_polling()

if __name__ == "__main__":
    main()

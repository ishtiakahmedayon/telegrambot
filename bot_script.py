import sqlite3
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
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

# Function to get today's schedule
async def todays_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    today_day = datetime.now().strftime("%a").upper()
    today_date = datetime.now().strftime("%d-%m-%Y")
    classes = get_classes_for_day(today_day)

    if not classes:
        response = f"❌ *No classes scheduled for today ({today_date})* ❌"
    else:
        response = f" *Today's Schedule ({today_date}):*\n\n"
        response += format_schedule(classes)

    await update.message.reply_text(response, parse_mode="Markdown")

# Function to get tomorrow's schedule
async def tomorrows_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    tomorrow_day = (datetime.now() + timedelta(days=1)).strftime("%a").upper()
    tomorrow_date = (datetime.now() + timedelta(days=1)).strftime("%d-%m-%Y")
    classes = get_classes_for_day(tomorrow_day)

    if not classes:
        response = f"❌ *No classes scheduled for tomorrow ({tomorrow_date})* ❌"
    else:
        response = f" *Tomorrow's Schedule ({tomorrow_date}):*\n\n"
        response += format_schedule(classes)

    await update.message.reply_text(response, parse_mode="Markdown")

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

    # Log information when the bot starts
    logger.info("Starting bot...")
    application.run_polling()

if __name__ == "__main__":
    main()

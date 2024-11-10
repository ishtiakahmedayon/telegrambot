import sqlite3
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

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
        print("Database error:", e)
        return []

# Function to get today's schedule
async def todays_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    today_day = datetime.now().strftime("%a").upper()
    today_date = datetime.now().strftime("%Y-%m-%d")
    classes = get_classes_for_day(today_day)
    
    if not classes:
        response = f"No classes scheduled for today, {today_date}."
    else:
        response = f"Today's Schedule ({today_date}):\n"
        for class_name, start_time, end_time in classes:
            response += f"{start_time} - {end_time}: {class_name}\n"
    
    await update.message.reply_text(response)

# Function to get tomorrow's schedule
async def tomorrows_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    tomorrow_day = (datetime.now() + timedelta(days=1)).strftime("%a").upper()
    tomorrow_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    classes = get_classes_for_day(tomorrow_day)
    
    if not classes:
        response = f"No classes scheduled for tomorrow, {tomorrow_date}."
    else:
        response = f"Tomorrow's Schedule ({tomorrow_date}):\n"
        for class_name, start_time, end_time in classes:
            response += f"{start_time} - {end_time}: {class_name}\n"
    
    await update.message.reply_text(response)

# Main function to start the bot
def main():
    application = ApplicationBuilder().token('7793824527:AAHK4KVtFjpEMEAyX1eJnDErJN5fixuLlmI').build()
    
    # Commands to get today’s and tomorrow’s schedule
    application.add_handler(CommandHandler("today", todays_schedule))
    application.add_handler(CommandHandler("tomorrow", tomorrows_schedule))

    # Run the bot
    application.run_polling()

if __name__ == "__main__":
    main()

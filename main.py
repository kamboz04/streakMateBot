#main code

from telegram.ext import Application, CommandHandler,MessageHandler,filters
from datetime import time

from app.config import BOT_TOKEN
from app.db.schema import init_db
from app.handlers import start,startStreak,checkStreak,relapse,customStreak,unified_text_handler,stats,help,report
from app.jobs import daily_job



def main():
    app = Application.builder().token(BOT_TOKEN).build()

    init_db()

    app.add_handler(CommandHandler("start", start))
    

    app.add_handler(CommandHandler("streakstart", startStreak))


    app.add_handler(CommandHandler("mystreak", checkStreak))


    app.add_handler(CommandHandler("relapse", relapse))

    app.add_handler(CommandHandler("customstreak", customStreak))


    #handle incoming streak or relapse yes/no
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,unified_text_handler))


    app.add_handler(CommandHandler("stats", stats))

    app.add_handler(CommandHandler("help", help))
    
    app.add_handler(CommandHandler("report", report))

    app.job_queue.run_daily(
        daily_job,
        time=time(hour=3, minute=30)
    )


    print("Runing...........")
    app.run_polling()

if __name__ == "__main__":
    main()

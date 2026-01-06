#all handlres of all com mands here

from telegram import Update
from telegram.ext import ContextTypes
from app.services import addUser,getStreak,resetStreak,customSet,getStats,user_exists
from telegram import Update,ReplyKeyboardMarkup,KeyboardButton,ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, ContextTypes,MessageHandler,filters


#start command for bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is online and running.✅\nUse /help to see available commands")


#start streak 
async def startStreak(update: Update, context: ContextTypes.DEFAULT_TYPE):
    userId = str(update.effective_user.id) #fetching user ID

    #make sure user is not registered already before adding
   
   
    if  user_exists(userId):
        
        await update.message.reply_text("you are already registered in bot...\nKindly use /mystreak")
    else:
        addUser(userId)
        currStreak = getStreak(userId)
        await update.message.reply_text(f"You’re registered successfully.\n Current Streak : {currStreak} days 🔥\n\nYour streak will increase automatically every day.\nUse /mystreak to check progress.")

#to check streak
async def checkStreak(update: Update, context: ContextTypes.DEFAULT_TYPE):
    userId = str(update.effective_user.id) #fetching user ID
    

    if not user_exists(userId):
        
        await update.message.reply_text("you are not registered in bot...\nKindly use /streakStart")
    else:
    
        currStreak2 = getStreak(userId)
        await update.message.reply_text(f"Your Streak : {currStreak2} days🔥\nStay Hard Warrior")


# to reset streak
async def relapse(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # we will ask user yes or no, to prevent immediate relapse due to a misclick on relpase b ujtton

     #make sure user is registred
    userId = str(update.effective_user.id) #fetching user ID
    if not user_exists(userId):
        
        await update.message.reply_text("you are not registered in bot...\nKindly use /streakStart")
        return

    #make keyboard
    keybaord = [

            [KeyboardButton("Yes")],
            [KeyboardButton("No")]
     ]

    #send buttons
    replyMarkup = ReplyKeyboardMarkup(keybaord,resize_keyboard=True)

    await update.message.reply_text("Are you sure that you wanna relpase ?",reply_markup=replyMarkup)

    context.user_data["awaiting_relapse"] = True


#to set custom streak

async def customStreak(update: Update, context: ContextTypes.DEFAULT_TYPE):

     userId = str(update.effective_user.id) #fetching user ID

    
     if not user_exists(userId):
        
        await update.message.reply_text("you are not registered in bot...\nKindly use /streakStart")
     else:
        await update.message.reply_text("Tell your streaks in days eg : X")

        context.user_data["awaiting_streak"] = True
       
       

# to handle conflict of msg handlers, ensure we run correct one
async def unified_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    userId = str(update.effective_user.id) #fetching user ID

    text = update.message.text.strip()

    # ----- RELAPSE CONFIRMATION FLOW -----
    if context.user_data.get("awaiting_relapse"):
        
       if text == "Yes":


            resetStreak(userId)
            await update.message.reply_text("Streak Reset\n\nYour streak has been reset to Day 0.\nStart again today. Consistency beats perfection.",reply_markup = ReplyKeyboardRemove())
            context.user_data.pop("awaiting_relapse")
            return

       elif text == "No":
            await update.message.reply_text("Good job Champ,Proud of you..!!",reply_markup = ReplyKeyboardRemove())
            context.user_data.pop("awaiting_relapse")
            return


    

    # ----- CUSTOM STREAK FLOW -----
    if context.user_data.get("awaiting_streak"):

       
       # Validate numeric input
        if not text.isdigit():
            await update.message.reply_text(
            "Invalid number. Please send digits only (e.g. 10).\nUse /customstreak again."
            )
            return

        streak_value = int(text)

        # Validate range
        if streak_value < 0:
            await update.message.reply_text(
            "Streak must be greater than equal to zero\nUse /customstreak again."
            )
            return
        
        customSet(userId,streak_value)

        # Cleanup state
        context.user_data.pop("awaiting_streak")

        await update.message.reply_text("Your streak is setted succesfully.")


# handler for stats fetch and show to user
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    userId = str(update.effective_user.id) #fetching user ID

    #make sure user is registred
   
    if not user_exists(userId):
        
        await update.message.reply_text("you are not registered in bot...\nKindly use /streakStart")
    else:
    
        data = getStats(userId)
        uid,attempts,rank,max_streak = data

        await update.message.reply_text(f"|| Your stats || \n\nAttempts :{attempts}\nRank : {rank}🎖\nMax Streak : {max_streak} days🏆")


# help command handler
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot Commands\n\n/start – Check if the bot is online\n/streakstart – Start your streak tracking\n/customstreak  – Set a custom streak value\n/mystreak – Check your current streak\n/relapse – Reset your streak and start fresh\n/stats – View detailed statistics\n/report – Report a bug or query\n/help – Show this help menu\n")


#report query command
async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Kindly drop your query here, @kamboz_04.\n\nWe will respond ASAP.\nThanks..!!")
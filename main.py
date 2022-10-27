import logging
from telegram import Update
from telegram.ext import filters, ApplicationBuilder, MessageHandler, ContextTypes, CommandHandler
import configs as config
import yagmail

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# 第三方 SMTP 服务
# mail_host 邮箱服务器
# mail_user 用户名
# mail_pass 口令
# receivers 收件人

def send_email(filename):
    yag = yagmail.SMTP(user=config.Email.mail_user, password=config.Email.mail_pass,host=config.Email.mail_host)
    yag.send(to=config.Email.receivers, subject='kindle', contents=[filename])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.effective_chat.id)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def file(update: Update, context: ContextTypes):
    message_document = update.message.document
    file_name = message_document.file_name
    file_path = './download/' + file_name
    file = await message_document.get_file()
    await file.download(file_path)
    send_email(file_path)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=file_name)

if __name__ == '__main__':
    application = ApplicationBuilder().token('953844712:AAH2L2_STcpzg-eB5kGw6_TyMPeicQx2Nh0').build()
    
    start_handler = CommandHandler('start', start)
    file_handler = MessageHandler(filters.Document.ALL, file)

    application.add_handler(start_handler)
    application.add_handler(file_handler)
    
    application.run_polling()
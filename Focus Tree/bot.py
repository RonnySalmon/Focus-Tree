import sys
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from telegram import Update, ReplyKeyboardMarkup
import logging
import os
from storage import load_tasks, save_tasks
from models import Task
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise ValueError(
        "Токен бота не найден. Убедитесь, что создали файл .env с TELEGRAM_BOT_TOKEN")

# Добавляем путь для импорта наших модулей
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Состояния для ConversationHandler
ADDING_TASK = 1

# Получение токена бота из переменных окружения
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user = update.effective_user
    welcome_text = f"""
Привет, {user.first_name}! 👋

Я бот Focus Tree - твой личный помощник в продуктивности.

Доступные команды:
/add - Добавить новую задачу
/list - Показать все задачи
/done <ID> - Отметить задачу как выполненную
/delete <ID> - Удалить задачу
/help - Показать справку
"""
    await update.message.reply_text(welcome_text)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    help_text = """
📋 Доступные команды:

/add - Добавить новую задачу
/list - Показать все задачи
/done <ID> - Отметить задачу как выполненную
/delete <ID> - Удалить задачу

Примеры:
/add Прочитать книгу
/done 1
/delete 2
"""
    await update.message.reply_text(help_text)


async def list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /list"""
    tasks = load_tasks()

    if not tasks:
        await update.message.reply_text("📭 Список задач пуст. Добавьте первую задачу с помощью /add")
        return

    tasks_text = "📋 Ваши задачи:\n\n"
    for task in tasks:
        status_icon = "✅" if task.status == "completed" else "⏳"
        tasks_text += f"{task.id}. {status_icon} {task.title} ({task.status})\n"

    await update.message.reply_text(tasks_text)


async def add_task_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало процесса добавления задачи"""
    await update.message.reply_text("✏️ Введите название новой задачи:")
    return ADDING_TASK


async def add_task_end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Завершение процесса добавления задачи"""
    task_title = update.message.text
    tasks = load_tasks()

    # Генерируем ID для новой задачи
    if tasks:
        new_id = max(task.id for task in tasks) + 1
    else:
        new_id = 1

    new_task = Task(id=new_id, title=task_title, status="active")
    tasks.append(new_task)
    save_tasks(tasks)

    await update.message.reply_text(f"✅ Задача добавлена с ID {new_id}!")
    return ConversationHandler.END


async def done_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /done"""
    if not context.args:
        await update.message.reply_text("❌ Укажите ID задачи. Пример: /done 1")
        return

    try:
        task_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("❌ ID задачи должен быть числом. Пример: /done 1")
        return

    tasks = load_tasks()
    task_found = False

    for task in tasks:
        if task.id == task_id:
            task.status = "completed"
            task_found = True
            break

    if task_found:
        save_tasks(tasks)
        await update.message.reply_text(f"✅ Задача с ID {task_id} отмечена как выполненная!")
    else:
        await update.message.reply_text(f"❌ Задача с ID {task_id} не найдена.")


async def delete_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /delete"""
    if not context.args:
        await update.message.reply_text("❌ Укажите ID задачи. Пример: /delete 1")
        return

    try:
        task_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("❌ ID задачи должен быть числом. Пример: /delete 1")
        return

    tasks = load_tasks()
    task_found = False

    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            task_found = True
            break

    if task_found:
        save_tasks(tasks)
        await update.message.reply_text(f"✅ Задача с ID {task_id} удалена!")
    else:
        await update.message.reply_text(f"❌ Задача с ID {task_id} не найдена.")


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отмена текущей операции"""
    await update.message.reply_text("❌ Операция отменена.")
    return ConversationHandler.END


def main():
    """Запуск бота"""
    if not TOKEN:
        logger.error(
            "Токен бота не найден. Установите переменную окружения TELEGRAM_BOT_TOKEN")
        return

    # Создаем приложение и передаем ему токен бота
    application = Application.builder().token(TOKEN).build()

    # Настройка обработчиков
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('add', add_task_start)],
        states={
            ADDING_TASK: [MessageHandler(
                filters.TEXT & ~filters.COMMAND, add_task_end)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("list", list_tasks))
    application.add_handler(CommandHandler("done", done_task))
    application.add_handler(CommandHandler("delete", delete_task))
    application.add_handler(conv_handler)

    # Запуск бота
    logger.info("Бот запущен...")
    application.run_polling()


if __name__ == '__main__':
    main()

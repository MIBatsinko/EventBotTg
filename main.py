import logging
import Event
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ParseMode, Bot, TelegramError
from telegram.ext import (Updater, CommandHandler, CallbackQueryHandler, MessageHandler,
                          Filters, RegexHandler, ConversationHandler)


class EventBot:
    """Клас, який налаштовує роботу телегарм бота"""

    def __init__(self):
        self.token = '508990081:AAEyT5R28SzL_tlmn69WTgoymzrkLsSdzRE'

        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # иницируем возможные состояния
        # 0 - ожидание выбора в главном меню, 1 - ожидание ввода контактов
        self.MAIN_MENU = range(1)
        self.button_event_today = 'Сьогодні'
        self.button_event_this_week = 'На цьому тижні'
        self.button_event_this_month = 'В цьому місяці'
        self.button_my_events = 'Мої події'
        self.button_search_event = 'Пошук події'

        # создаём основное меню
        self.reply_keyboard = [[self.button_event_today, self.button_event_this_week, self.button_event_this_month],
                               [self.button_search_event]]
        self.markup = ReplyKeyboardMarkup(self.reply_keyboard, one_time_keyboard=True, resize_keyboard=True)

        # определям вызываемые методы для кнопок главного меню
        self.button_func = {self.button_event_today: self.event_today,
                            self.button_event_this_week: self.event_this_week,
                            self.button_event_this_month: self.event_this_month,
                            self.button_my_events: self.event_my_events,
                            self.button_search_event: self.search_event}

        self.db = Event.Database()

        # создаём апдейтер и передаём им токен, который был выдан после создания бота
        self.updater = Updater(self.token)

        # определяем диспетчер для регистрации обработчиков
        self.dp = self.updater.dispatcher

        # подготваливаем перечисление возможных выборов главного меню
        main_menu_regexp = '|'.join([self.button_event_this_week,
                                     self.button_event_this_month,
                                     self.button_event_today,
                                     self.button_search_event])

        # инициируем обработчики для диалога
        self.conversation = ConversationHandler(
            # команды
            entry_points=[CommandHandler('start', self.start)],
            # состояния, в зависимости от состояния вызывается обработчик
            # состояния передаются так же уже завершёнными обработчиками
            states={
                self.MAIN_MENU: [RegexHandler('^(' + main_menu_regexp + ')$', self.main_menu, pass_user_data=False)]
            },
            fallbacks=[]
        )
        self.dp.add_handler(CommandHandler("entry_date", self.entry_date, pass_args=True))
        self.dp.add_handler(CommandHandler("entry_name", self.entry_name, pass_args=True))
        # self.dp.add_handler(MessageHandler(Filters.command, self.input_date))

        # добавляем в диалог обработчики состояний
        self.dp.add_handler(self.conversation)

        # добавляем в диалог обработчик кнопок
        self.dp.add_handler(CallbackQueryHandler(self.button, pass_user_data=False))

        # логирование ошибок
        self.dp.add_error_handler(self.error)

        # запуск бота
        self.updater.start_polling()

        # запуск цикла ожидания запросов
        self.updater.idle()

    def start(self, bot, update):
        """Метод, який запускає бота"""

        # виводить привітання та головне меню
        update.message.reply_text(
            "Доброго дня!\n"
            "Які події Вас цікавлять?",
            reply_markup=self.markup)
        return self.MAIN_MENU

    def event_today(self, bot, update):
        """Результат дії кнопки 'Події на сьогодні'"""

        if self.db.select_event_today()==None:
            update.message.reply_text("Сьогодні ніяких свят нема :(")
        else:
            update.message.reply_text(self.db.select_event_today())

    def event_my_events(self, bot, update, ):
        """Метод 'Мої події'. Дозволяє налаштовувати власні події"""

        keyboard = [[InlineKeyboardButton("Показати усі", callback_data='Показати усі'),
                     InlineKeyboardButton("Додати", callback_data='Додати')], [
                        InlineKeyboardButton("Видалити", callback_data='Видалити')]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Оберіть дію:', reply_markup=reply_markup)

    def event_this_week(self, bot, update):
        """Метод для виводу подій на поточному тижні"""

        if self.db.select_event_on_this_week() == None:
            update.message.reply_text("На цьому тижні святкувань не передбачено.\nЦе буде тяжкий тиждень.")
        else:
            update.message.reply_text(self.db.select_event_on_this_week())

    def event_this_month(self, bot, update):
        """Метод для виводу подій поточного місяця"""

        if self.db.select_event_on_this_month() is None:
            update.message.reply_text("В цьому місяці святкувань не передбачено.\nЦе буде тяжкий місяць.")
        else:
            update.message.reply_text(self.db.select_event_on_this_month())

    def search_event(self, bot, update):
        """Метод для пошуку події"""

        bot.send_message(chat_id=update.message.chat_id,
                         text="/entry_date xxxxyyzz - пошук по даті у форматі yyyymmdd\n/entry_name event- пошук по назві")

    def main_menu(self, bot, update):
        """Метод головного меню"""

        button_text = update.message.text
        if button_text in self.button_func:
            return self.button_func[button_text](bot, update)
        else:
            update.message.reply_text('Нема такої дії', reply_markup=self.markup)
            return self.MAIN_MENU

    def entry_date(self, bot, update, args):
        """Метод для пошуку події по даті"""

        bot.send_message(chat_id=update.message.chat_id, text=self.db.select_event_where_date(args[0]))

    def entry_name(self, bot, update, args):
        """Метод пошуку події по назві"""

        bot.send_message(chat_id=update.message.chat_id, text=self.db.select_event_where_name(args[0]))

    def button(self, bot, update):
        """Метод, який обробляє натиски кнопок"""

        id_user = update._effective_user.id
        query = update.callback_query
        if query.data == "Пошук по назві":
            bot.editMessageText(text='Введіть назву і напишіть /entry_name:',  # сюда выводить результат
                                chat_id=query.message.chat_id,
                                message_id=query.message.message_id)
        elif query.data == "Пошук по даті":
            # заменям сообщение с кнопками сообщением о сделанном выборе
            bot.editMessageText(text='Введіть дату в форматі дд/мм:',  # сюда выводить результат
                                chat_id=query.message.chat_id,
                                message_id=query.message.message_id)

    def error(self, bot, update, error):
        """Метод формування помилок"""

        self.logger.warning('Update "%s" caused error "%s"' % (update, error))


if __name__ == '__main__':
    bot = EventBot()

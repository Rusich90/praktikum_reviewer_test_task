import datetime as dt


class Record:
    # Необязательные аргументы как date правильные записывать с помощью None
    # Во всех обьявлениях функций лучше добавить type annotation
    # Для необязательных аргументов есть тип Optional в модуле typing
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        # Плохая читаемость у обьявления даты, нету переноса у последней скобки
        # Да и перенос можно было сделать чуть красивей =)
        # dt.datetime.now().date() if not date
        # else dt.datetime.strptime(date, '%d.%m.%Y').date()
        # В этом случае обычный многострочний if else читался бы лучше
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    # В переменных тоже можно использоваться аннотации типов
    # self.records: list[Record] = []
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        # Переменные должны быть с маленькой буквы
        # С большой обьявляются классы
        for Record in self.records:
            # dt.datetime.now().date() лучше вынести в переменную до цикла
            if Record.date == dt.datetime.now().date():
                # Здесь можно использовать оператор +=
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        # Здесь правильно получилось: и дата вынесена в переменную
        # И record с маленькой буквы =)
        for record in self.records:
            # Здесь перемудрил с условиями, достаточно проверки что меньше 7
            # И не правильные отступы после if
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    # Комментарии к функциям правильней описывать с помощью docstrings
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        # Из названия переменной не понятно что оно такое)
        # remainder подойдет намного лучше
        x = self.limit - self.get_today_stats()
        if x > 0:
            # Перенос строк с помощью косой черты не желателен
            # Предпочтительней использовать скобки
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        else:
            return('Хватит есть!')


class CashCalculator(Calculator):
    # Мне кажется здесь комментарии излишни
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.
    CURRENCY = {}

    # Мы можем обратиться к переменным класса с помощью self.
    # Закидывать валюту в агрументы не имеет смысла
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        # Для чего переопределиние названия переменной?
        # Можно и к currency обращаться
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        # Я бы вынес эти условия в отдельную функцию
        # А лучше сделать константу в классе - словарь с ключами currency
        # А значения словарь с ключами name и rate
        # Тогда можно будет проверять валидность currency
        # Легко получать названия и рэйты валют
        # (CURRENCY_CATALOG[currency][name])
        # А также масштабировать и добавлять новые валюты
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            # Это присвоение не используется и не имеет смысла
            cash_remained == 1.00
            currency_type = 'руб'
        # Желательно отделять блоки логики функции пустой строкой
        # Так будет легче читать и понимать код
        if cash_remained > 0:
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        # Здесь elif лишний, можно сделать просто return
        elif cash_remained < 0:
            # Надо бы определиться как мы форматируем строки
            # И придерживаться везде одинакового формата
            # f строки читаются лучше и работают быстрее
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    # Так как в этом методе ничего не переопределяется, то он и не нужен
    # Он даже работать будет не правильно так как нету return
    def get_week_stats(self):
        super().get_week_stats()

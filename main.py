import datetime as dt


class Record:
    # Параметр date лучше задать как date=None
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        # В качестве проверки параметра date лучше использовать полную
        # конструкцию if...else вместо тернарного оператора, потому что
        # визуально это будет выглядеть лучше
        # if not date:
        #     self.date = dt.datetime.now().date()
        # else:
        #     self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
        # Но если хочется оставить тернарный, тогда стоит убрать лишние
        # скобки () в начале и в конце
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        # В этом for стоит изменить Record на record
        for Record in self.records:
            if Record.date == dt.datetime.now().date():
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            # Условие можно сделать более читабельным и корортким:
            # 7 > (today - record.date).days >= 0
            # Но если хочется оставить в исходном виде, тогда стоит убрать
            # лишние скобки () в конце и в начале исловаия
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    # Комментарий неверно отражает функционал этого метода
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        x = self.limit - self.get_today_stats()
        if x > 0:
            # Чтобы не использовать обратный слэш для переноса длинной
            # строки можно обернуть её скобки ()
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        else:
            # Здесь можно убрать скобки (), строка и так вернётся
            return('Хватит есть!')


class CashCalculator(Calculator):
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    # Не следует передавать переменные курса валют в качестве параметров
    # в метод, потому что они и так доступны внутри класса через self:
    # self.USD_RATE и self.EURO_RATE
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        # Ненужно переопределять переменную currency
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        # Чтобы упростить этот if...elif c выбором валюты, можно реализовать
        # словарь, в котором ключи это виды валют, которые передаются в метод
        # get_today_cash_remained(), а значения это кортеж с текущим курсом
        # и требуемой валютой
        # current_exchange_rate = {
        #     'usd': (cash_remained / USD_RATE, 'USD'),
        #     'eur': (cash_remained / EURO_RATE, 'Euro'),
        #     'rub': (cash_remained, 'руб')
        # }
        # Благодрая такой реализации дальше можно было бы её использовать
        # вот так: cash, currency_type = current_exchange_rate[currency]
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            # Тут стоит убрать эту строчку cash_remained == 1.00, она ничего
            # не делает
            cash_remained == 1.00
            currency_type = 'руб'
        if cash_remained > 0:
            # Тут следует поднять закрывающую скобку на строку
            # вверх в конец строки
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:
            # Чтобы не использовать обратный слэш для переноса длинной
            # строки можно обернуть её скобки ()
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    # Из-за такого переопределения/использования метода get_week_stats() он
    # возвращает None вместо корректной работы. По сути этого даже не стоит
    # делать, потому что класс CashCalculator наследует класс Calculator и
    # все его методы доступны этому классу через self
    def get_week_stats(self):
        super().get_week_stats()

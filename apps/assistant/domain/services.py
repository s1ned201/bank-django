import re
from apps.rates.domain.services import ExchangeRateService

class AssistantService:
    # словарь синонимов валют
    CURRENCY_ALIASES = {
        'доллар': 'USD',
        'долларов': 'USD',
        'доллара': 'USD',
        'usd': 'USD',
        'eur': 'EUR',
        'евро': 'EUR',
        'рубль': 'BYN',
        'рублей': 'BYN',
        'рубля': 'BYN',
        'белорусский рубль': 'BYN',
        'byn': 'BYN',
        'rur': 'RUB',
        'rub': 'RUB',
        'российский рубль': 'RUB',
        'российских рублей': 'RUB',
        'фунт': 'GBP',
        'gbp': 'GBP',
        'юань': 'CNY',
        'cny': 'CNY',
        'злотый': 'PLN',
        'pln': 'PLN',
    }

    def __init__(self):
        self.rates_service = ExchangeRateService()

    def _replace_aliases(self, text: str) -> str:
        """Заменяет в тексте синонимы валют на их коды."""
        words = text.lower().split()
        new_words = []
        for word in words:
            clean_word = word.strip('.,!?;:')
            if clean_word in self.CURRENCY_ALIASES:
                new_words.append(self.CURRENCY_ALIASES[clean_word])
            else:
                new_words.append(word)
        return ' '.join(new_words)

    def process_message(self, user, text: str) -> str:
        original_text = text
        text = self._replace_aliases(text)
        text_lower = text.lower().strip()

        if any(word in text_lower for word in ['курс', 'курсы', 'exchange rate', 'rates']):
            try:
                rates = self.rates_service.get_current_rates()
                lines = []
                for code, data in rates.items():
                    lines.append(f"{data['name']} ({code}): {data['rate']} BYN")
                return "Текущие курсы НБ РБ:\n" + "\n".join(lines)
            except Exception as e:
                return f"Не удалось получить курсы: {e}"

        pattern = r'(\d+(?:[.,]\d+)?)\s*([a-zA-Z]{3})\s+(?:в|на|to|in|->|→)\s+([a-zA-Z]{3})'
        match = re.search(pattern, text_lower)
        if match:
            amount_str, from_curr, to_curr = match.groups()
            amount = float(amount_str.replace(',', '.'))
            return self.convert(amount, from_curr.upper(), to_curr.upper())

        if any(word in original_text.lower() for word in ['привет', 'здравствуй', 'hello', 'hi']):
            return "Здравствуйте! Я виртуальный помощник. Могу показать курсы валют или конвертировать сумму. Например: '100 usd в eur'."
        if any(word in original_text.lower() for word in ['помощь', 'help', 'что ты умеешь']):
            return "Я могу:\n- Показать актуальные курсы (напишите 'курсы').\n- Конвертировать валюту (например, '100 usd в eur')."
        if any(word in original_text.lower() for word in ['спасибо', 'благодарю', 'thanks']):
            return "Пожалуйста! Обращайтесь."

        return "Извините, я не понял запрос. Напишите 'помощь', чтобы узнать, что я умею."

    def convert(self, amount: float, from_code: str, to_code: str) -> str:
        rates = self.rates_service.get_current_rates()
        if from_code == 'BYN' and to_code == 'BYN':
            return f"{amount} BYN = {amount} BYN"
        if from_code == 'BYN':
            if to_code not in rates:
                return f"Не найден курс для {to_code}"
            rate = float(rates[to_code]['rate'])
            result = amount / rate
            return f"{amount} BYN = {result:.2f} {to_code}"
        if to_code == 'BYN':
            if from_code not in rates:
                return f"Не найден курс для {from_code}"
            rate = float(rates[from_code]['rate'])
            result = amount * rate
            return f"{amount} {from_code} = {result:.2f} BYN"
        if from_code not in rates or to_code not in rates:
            return f"Не найдена валюта {from_code} или {to_code}"
        rate_from = float(rates[from_code]['rate'])
        rate_to = float(rates[to_code]['rate'])
        result = amount * rate_from / rate_to
        return f"{amount} {from_code} = {result:.2f} {to_code}"
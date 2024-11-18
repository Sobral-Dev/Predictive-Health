from datetime import datetime, date

def calculate_age(birth_date: str | datetime | date) -> int:

    if isinstance(birth_date, str):
        birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()

    if not isinstance(birth_date, (datetime, date)):
        raise ValueError("birth_date deve ser uma string no formato 'YYYY-MM-DD', um objeto datetime ou date.")

    today = datetime.today().date()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    return age

from datetime import date
from datetime import datetime


def date_para_str(data: date) -> str:
    return data.strftime('%d/%m/%Y')


def str_para_date(data: str) -> date:
    return datetime.strptime(data, '%d/%m/%Y')


def formata_float_str_moeda(valor: float) -> str:
    return f'R$ {valor:,.2f}'


def formatar_cpf(cpf: str) -> str:
    cpf = ''.join(filter(str.isdigit, cpf))

    return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'

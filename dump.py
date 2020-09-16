import re
from datetime import datetime

SEPARATOR = '=' * 56

RE_IDX = re.compile(r'= #(\d+) =')
RE_CREDENTIALS = re.compile(SEPARATOR + r'\n(.+?)\n', re.DOTALL)
RE_BALANCE = re.compile(r'(.+?) °P')
RE_TITLE = re.compile(r'\+\+\+ (.+?) \+\+\+')
RE_DATE = re.compile(r'(\d{2}.\d{2}.\d{4} \d{,2}:\d{2}:\d{2})')
RE_SERVICE = re.compile(r'\d+ ' + '=' * 29 + '\n' + r'(.+?)\n', re.DOTALL)


class Account:
    def __init__(self, idx, login, password, title, date, service, body, balance):
        self.idx = idx
        self.login = login
        self.password = password
        self.title = title
        self.date = date
        self.service = service
        self.body = body
        self.balance = balance

    def __str__(self):
        return SEPARATOR + '\n{}:{}\n+++ {} +++\n{}\n{} #{} {}\n\n{}\n\n\n{}'.format(
            self.login, self.password, self.title, self.date, '=' * 23, self.idx, '=' * 29,
            self.service, self.body)

    def parse(text):
        idx = re.search(RE_IDX, text).group(1)
        login, password = re.search(RE_CREDENTIALS, text).group(1).strip().split(':')
        title = re.search(RE_TITLE, text).group(1)
        date = datetime.strptime(re.search(RE_DATE, text).group(1), '%d.%m.%Y %H:%M:%S')
        service = re.search(RE_SERVICE, text).group(1).strip()
        body = re.search(service + r'\n\n\n(.+)', text, re.DOTALL).group(1).strip()
        balance = float(re.search(RE_BALANCE, text).group(1).replace('.', ''))

        return Account(idx, login, password, title, date, service, body, balance)


def main():
    filtered = []

    with open('dump.txt') as file:
        text = file.read()
        dumps = ['{}\n{}'.format(SEPARATOR, text) for text in text.split(SEPARATOR) if len(text)]

        for dump in dumps:
            account = Account.parse(dump)
            if account.balance >= 500.0:
                filtered.append(account)

    with open('dump_filtered.txt', 'w') as file:
        file.writelines([str(account) for account in filtered])


if __name__ == '__main__':
    main()

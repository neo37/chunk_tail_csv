#!/usr/bin/env python3
import argparse
import sys
import os
import csv
from collections import deque
from datetime import datetime
from itertools import zip_longest

CHECKPOINT_LINES = 1000  # сколько строк обрабатывать до чекпоинта

def parse_args():
    parser = argparse.ArgumentParser(
        description="Работа с текстом/CSV: tail, drop-last, interval, delete-interval, analyze, filter-date, count, sum-lines, add-files + чекпоинты"
    )
    parser.add_argument('input', help='путь к входному файлу (txt или CSV)')
    parser.add_argument('number', nargs='?', type=int,
                        help='количество строк для --tail (backward compatibility)')
    parser.add_argument('-o', '--output', default='result.txt',
                        help='имя выходного файла')
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('--tail', type=int,
                       help='первая строка + последние N строк')
    group.add_argument('--drop-last', type=int,
                       help='первая строка + всё, кроме последних N')
    group.add_argument('--interval', nargs=2, type=int, metavar=('START', 'END'),
                       help='первая строка + строки от START до END включительно')
    group.add_argument('--delete-interval', nargs=2, type=int, metavar=('START', 'END'),
                       help='удалить строки от START до END (включительно), первая строка сохраняется')
    group.add_argument('--analyze', action='store_true',
                       help='анализ первых 36 строк CSV: имя столбца + тип данных')
    group.add_argument('--filter-date', nargs=3, metavar=('COLUMN','START','END'),
                       help='фильтрация CSV по дате: header + строки в указанном интервале')
    group.add_argument('--count', action='store_true',
                       help='вывести только количество строк во входном файле и выйти')
    group.add_argument('--sum-lines', action='store_true',
                       help='просуммировать все числовые строки (каждая строка — число) и выйти')
    group.add_argument('--add-files', metavar='FILE2',
                       help='сложить построчно два файла (числа), недостающие строки считаются нулями')
    return parser.parse_args()

def infer_type(values):
    if all(v.strip()=='' for v in values):
        return 'str'
    # int?
    try:
        for v in values:
            if v.strip(): int(v)
        return 'int'
    except:
        pass
    # float?
    try:
        for v in values:
            if v.strip(): float(v)
        return 'float'
    except:
        pass
    # date?
    for fmt in ('%d-%m-%Y','%Y-%m-%d'):
        try:
            for v in values:
                if v.strip(): datetime.strptime(v, fmt)
            return 'date'
        except:
            continue
    return 'str'

def analyze_csv(path):
    """Читает первые 36 строк CSV и выводит типы столбцов."""
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        if not header:
            print("CSV файл пуст.")
            sys.exit(0)
        samples = {col: [] for col in header}
        for i, row in enumerate(reader, start=1):
            if i > 35: break
            for col, val in zip(header, row):
                samples[col].append(val)
    print("Анализ заголовка + 35 строк:")
    for col in header:
        print(f"  {col}: {infer_type(samples[col])}")
    sys.exit(0)

def parse_date(s):
    for fmt in ('%d-%m-%Y','%Y-%m-%d'):
        try:
            return datetime.strptime(s, fmt).date()
        except:
            pass
    raise ValueError(f"Не удалось распознать дату: {s!r}")

def filter_date_csv(input_path, output_path, column, start_s, end_s):
    """Фильтрация CSV по дате в колонке."""
    start = parse_date(start_s)
    end   = parse_date(end_s)
    with open(input_path, newline='', encoding='utf-8') as fin, \
         open(output_path, 'w', newline='', encoding='utf-8', buffering=1) as fout:
        reader = csv.reader(fin)
        writer = csv.writer(fout)
        header = next(reader, None)
        if not header:
            sys.exit("CSV файл пуст.")
        if column not in header:
            sys.exit(f"Колонки {column!r} нет в заголовке.")
        idx = header.index(column)
        writer.writerow(header)
        total = 1
        for row in reader:
            total += 1
            try:
                d = parse_date(row[idx])
            except:
                continue
            if start <= d <= end:
                writer.writerow(row)
            if total % CHECKPOINT_LINES == 0:
                fout.flush()
    print(f"Готово: отфильтровано {total-1} строк. Результат в «{output_path}»")
    sys.exit(0)

def count_lines(path):
    """Просто считает строки."""
    total = 0
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        for _ in f:
            total += 1
    print(f"Всего строк во входном файле: {total}")
    sys.exit(0)

def sum_lines(path):
    """Суммирует значения, если каждая строка — число."""
    total = 0.0
    count_num = 0
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            s = line.strip()
            if not s:
                continue
            try:
                val = int(s)
            except ValueError:
                try:
                    val = float(s)
                except ValueError:
                    continue
            total += val
            count_num += 1
    print(f"Найдено числовых строк: {count_num}")
    print(f"Сумма значений: {total}")
    sys.exit(0)

def parse_number(s):
    """Парсит строку в число или возвращает 0."""
    s = s.strip()
    if not s:
        return 0.0
    try:
        return int(s)
    except:
        try:
            return float(s)
        except:
            return 0.0

def add_files(path1, path2, output_path):
    """Построчное сложение двух файлов."""
    total = 0
    with open(path1, 'r', encoding='utf-8', errors='ignore') as f1, \
         open(path2, 'r', encoding='utf-8', errors='ignore') as f2, \
         open(output_path, 'w', encoding='utf-8', buffering=1) as fout:
        for l1, l2 in zip_longest(f1, f2, fillvalue=''):
            n1 = parse_number(l1)
            n2 = parse_number(l2)
            fout.write(f"{n1 + n2}\n")
            total += 1
            if total % CHECKPOINT_LINES == 0:
                fout.flush()
    print(f"Готово: сложено строк {total}. Результат в «{output_path}»")
    sys.exit(0)

def delete_interval(path, output_path, start, end):
    """Удаляет строки от start до end включительно, header сохраняется."""
    total = 0
    with open(path, 'r', encoding='utf-8', errors='ignore') as fin, \
         open(output_path, 'w', encoding='utf-8', buffering=1) as fout:
        for i, line in enumerate(fin, start=1):
            if i == 1:
                fout.write(line)  # заголовок всегда
            else:
                if start <= i <= end:
                    # пропускаем
                    pass
                else:
                    fout.write(line)
            total += 1
            if total % CHECKPOINT_LINES == 0:
                fout.flush()
    print(f"Готово: удалены строки с {start} по {end}. Результат в «{output_path}»")
    sys.exit(0)

def main():
    args = parse_args()

    # простые режимы
    if args.count:
        count_lines(args.input)
    if args.sum_lines:
        sum_lines(args.input)
    if args.add_files:
        add_files(args.input, args.add_files, args.output)
    if args.delete_interval:
        start, end = args.delete_interval
        delete_interval(args.input, args.output, start, end)
    if args.analyze:
        analyze_csv(args.input)
    if args.filter_date:
        col, s, e = args.filter_date
        filter_date_csv(args.input, args.output, col, s, e)

    # tail / drop-last / interval / backward compatibility
    mode = None
    N = None
    interval = None
    if args.number is not None and not (args.tail or args.drop_last or args.interval):
        mode, N = 'tail', args.number
    elif args.tail is not None:
        mode, N = 'tail', args.tail
    elif args.drop_last is not None:
        mode, N = 'drop-last', args.drop_last
    elif args.interval is not None:
        mode, interval = 'interval', tuple(args.interval)
    else:
        sys.exit("Ошибка: укажите один из режимов: --tail, --drop-last, --interval, --delete-interval, --analyze, --filter-date, --count, --sum-lines или --add-files.")

    # обработка потоком
    with open(args.input, 'r', encoding='utf-8', errors='ignore') as fin, \
         open(args.output, 'w', encoding='utf-8', buffering=1) as fout:
        total = 0
        first = next(fin, None)
        if first is None:
            sys.exit("Входной файл пуст.")
        fout.write(first)
        total = 1

        buf = deque(maxlen=N) if mode == 'tail' else None
        start_idx, end_idx = (interval if mode == 'interval' else (None, None))

        for ln in fin:
            total += 1
            if mode == 'drop-last':
                fout.write(ln)
            elif mode == 'interval':
                if start_idx <= total <= end_idx:
                    fout.write(ln)
            elif mode == 'tail':
                buf.append(ln)
            if total % CHECKPOINT_LINES == 0:
                fout.flush()
                if mode == 'tail':
                    # для tail пересохраняем атомарно
                    tmp = args.output + '.tmp'
                    with open(tmp, 'w', encoding='utf-8') as ft:
                        ft.write(first)
                        ft.writelines(buf)
                    os.replace(tmp, args.output)

        if mode == 'drop-last':
            # удаляем последние N строк
            with open(args.output, 'r', encoding='utf-8') as ft:
                lines = ft.readlines()
            keep = len(lines) - N
            with open(args.output, 'w', encoding='utf-8') as ft2:
                ft2.writelines(lines[:keep])

        if mode == 'tail':
            fout.writelines(buf)

        fout.write(f"\nВсего строк во входном файле: {total}\n")

    print(f"Готово! Результат в «{args.output}». Всего строк: {total}")

if __name__ == '__main__':
    main()

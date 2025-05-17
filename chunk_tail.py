#!/usr/bin/env python3
import argparse
import sys
import os
import csv
from collections import deque
from datetime import datetime

CHECKPOINT_LINES = 1000

def parse_args():
    parser = argparse.ArgumentParser(
        description="Работа с текстом/CSV: tail, drop-last, interval, analyze, filter-date + периодические сохранения"
    )
    parser.add_argument('input', help='входной файл (txt или CSV)')
    parser.add_argument('number', nargs='?', type=int,
                        help='количество строк для --tail (backward compatibility)')
    parser.add_argument('-o', '--output', default='result.txt',
                        help='имя выходного файла')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--tail', type=int,
                       help='первые строка + последние N строк')
    group.add_argument('--drop-last', type=int,
                       help='первая строка + всё, кроме последних N')
    group.add_argument('--interval', nargs=2, type=int, metavar=('START', 'END'),
                       help='первая строка + строки от START до END включительно')
    group.add_argument('--analyze', action='store_true',
                       help='анализ первых 36 строк CSV: имя столбца + тип данных')
    group.add_argument('--filter-date', nargs=3, metavar=('COLUMN','START','END'),
                       help=('фильтрация CSV по дате: первая строка + строки, '
                             'где COLUMN в интервале START..END'))
    return parser.parse_args()

def infer_type(values):
    """По списку строковых значений пытаемся определить один из типов."""
    # сплошь пустые => str
    if all(v.strip()=='' for v in values):
        return 'str'
    # попробовать int
    try:
        for v in values:
            if v.strip()=='': continue
            int(v)
        return 'int'
    except:
        pass
    # попробовать float
    try:
        for v in values:
            if v.strip()=='': continue
            float(v)
        return 'float'
    except:
        pass
    # попробовать date (DD-MM-YYYY или YYYY-MM-DD)
    for fmt in ('%d-%m-%Y','%Y-%m-%d'):
        try:
            for v in values:
                if v.strip()=='': continue
                datetime.strptime(v, fmt)
            return 'date'
        except:
            continue
    return 'str'

def analyze_csv(path):
    """Читает первые 36 строк CSV и выводит типы."""
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        if header is None:
            print("Файл пуст.")
            return
        samples = {col: [] for col in header}
        for i, row in enumerate(reader, start=1):
            if i > 36: break
            for col, val in zip(header, row):
                samples[col].append(val)
    print("Анализ первых заголовка + 36 строк:")
    for col in header:
        t = infer_type(samples[col])
        print(f"  {col}: {t}")
    # завершаем работу
    sys.exit(0)

def parse_date(s):
    for fmt in ('%d-%m-%Y','%Y-%m-%d'):
        try:
            return datetime.strptime(s, fmt).date()
        except:
            continue
    raise ValueError(f"Не удалось распознать дату: {s!r}")

def filter_date_csv(input_path, output_path, column, start_s, end_s):
    """Сохраняет header + строки, где дата в column между start..end."""
    start = parse_date(start_s)
    end   = parse_date(end_s)
    with open(input_path, newline='', encoding='utf-8') as fin, \
         open(output_path, 'w', newline='', encoding='utf-8', buffering=1) as fout:
        reader = csv.reader(fin)
        writer = csv.writer(fout)
        header = next(reader, None)
        if header is None:
            sys.exit("Файл пуст.")
        if column not in header:
            sys.exit(f"Колонки {column!r} нет в заголовке.")
        idx = header.index(column)
        writer.writerow(header)
        total = 1
        for i, row in enumerate(reader, start=2):
            total += 1
            try:
                d = parse_date(row[idx])
            except:
                continue
            if start <= d <= end:
                writer.writerow(row)
            if total % CHECKPOINT_LINES == 0:
                fout.flush()
    print(f"Готово! Отфильтровано строк: файл «{output_path}».")
    print(f"Всего строк во входном файле: {total}")

def main():
    args = parse_args()

    # режим анализа CSV
    if args.analyze:
        analyze_csv(args.input)

    # режим фильтрации по дате
    if args.filter_date:
        col, start_s, end_s = args.filter_date
        filter_date_csv(args.input, args.output, col, start_s, end_s)
        return

    # остальные режимы
    mode = None
    N = None
    interval = None

    if args.number is not None and not (args.tail or args.drop_last or args.interval):
        mode = 'tail';       N = args.number
    elif args.tail is not None:
        mode = 'tail';       N = args.tail
    elif args.drop_last is not None:
        mode = 'drop-last';  N = args.drop_last
    elif args.interval is not None:
        mode = 'interval';   interval = tuple(args.interval)
    else:
        sys.exit("Ошибка: укажите один из режимов: --tail, --drop-last, --interval, --analyze или --filter-date.")

    with open(args.input, 'r', encoding='utf-8') as fin, \
         open(args.output, 'w', encoding='utf-8', buffering=1) as fout:
        total = 0
        first = next(fin, None)
        if first is None:
            sys.exit("Входной файл пуст.")
        fout.write(first); total = 1

        buf = deque(maxlen=N) if mode=='tail' else None
        start, end = (interval if mode=='interval' else (None, None))

        for ln in fin:
            total += 1
            if mode=='drop-last':
                fout.write(ln)
                if total % CHECKPOINT_LINES==0: fout.flush()

            elif mode=='interval':
                if start <= total <= end:
                    fout.write(ln)
                    if total % CHECKPOINT_LINES==0: fout.flush()

            elif mode=='tail':
                buf.append(ln)
                if total % CHECKPOINT_LINES==0:
                    # атомарно обновляем файл
                    tmp = args.output + '.tmp'
                    with open(tmp,'w',encoding='utf-8') as ftmp:
                        ftmp.write(first)
                        ftmp.writelines(buf)
                    os.replace(tmp, args.output)

        if mode=='drop-last':
            # удаляем последние N строк
            with open(args.output,'r',encoding='utf-8') as ftmp:
                lines = ftmp.readlines()
            keep = len(lines) - N
            with open(args.output,'w',encoding='utf-8') as f2:
                f2.writelines(lines[:keep])

        if mode=='tail':
            fout.writelines(buf)

        fout.write(f"\nВсего строк во входном файле: {total}\n")

    print(f"Готово! Результат в «{args.output}». Всего строк: {total}")

if __name__ == '__main__':
    main()

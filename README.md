<p align="center">
  <a href="#readme-ru">Русский</a> | <a href="#readme-en">English</a>
</p>

---

<a name="readme-en"></a>

## 🚀 Project Description

**ChunkTail** is a CLI utility for processing large text and CSV files. It can:

* Extract the first and last N lines (*tail*).
* Remove the last N lines (*drop-last*).
* Select a range of lines by their numbers (*interval*).
* Delete a range of lines (*delete-interval*).
* Periodically checkpoint results to disk to avoid “freezing.”
* **New flags**:

  * `--analyze` — read the first 36 lines of a CSV, output each column name and detected data type (`date`, `int`, `float`, `str`).
  * `--filter-date COLUMN START END` — keep header and rows where the specified column falls within the given date range (formats `DD-MM-YYYY` or `YYYY-MM-DD`).
  * `--count` — just print the total number of lines in the input file and exit.
  * `--sum-lines` — sum all numeric lines (each line must contain only a number) and print the result.
  * `--add-files FILE2` — add two files line by line (missing lines count as zero) and write sums to output.
  * `--delete-interval START END` — delete lines numbered from `START` to `END` (inclusive), preserving the header (first line).
* Upon completion (except for `--count`, `--sum-lines`, `--add-files`, `--delete-interval`, `--analyze`, `--filter-date`), always prints the total number of lines in the input.

Ideal for handling datasets provided by the [Dubai Land Department (DLD)](https://www.dubaipulse.gov.ae/organisation/dld), the government body responsible for real estate registration and regulation in Dubai.

---

### 🛠 Installation

```bash
git clone https://github.com/YourUser/ChunkTail.git
cd ChunkTail
chmod +x chunk_tail.py
# or, if there are dependencies:
pip install -r requirements.txt
```

---

### ⚙️ Usage Examples

```bash
# tail: first + last 5 lines
python chunk_tail.py data.txt --tail 5 -o result.txt

# drop-last: header + all but last 10 lines
python chunk_tail.py data.txt --drop-last 10 -o trimmed.txt

# interval: header + lines 20 through 1000
python chunk_tail.py data.txt --interval 20 1000 -o slice.txt

# delete-interval: delete lines 50–100 (header kept)
python chunk_tail.py data.txt --delete-interval 50 100 -o cleaned.txt

# analyze: detect column types in first 36 lines of CSV
python chunk_tail.py Rent_Contracts.csv --analyze

# filter-date: keep rows where date is within given range
python chunk_tail.py Rent_Contracts.csv \
  --filter-date contract_start_date 01-04-2019 30-04-2019 \
  -o filtered.csv

# count: get the number of lines in the file
python chunk_tail.py data.txt --count

# sum-lines: sum numeric lines
python chunk_tail.py numbers.txt --sum-lines

# add-files: add two files line by line
python chunk_tail.py a.txt --add-files b.txt -o summed.txt
```

---

### 🤝 Contributing

1. **Fork** the repo
2. Create a branch: `git checkout -b feature/NewFeature`
3. Make your changes and **commit**: `git commit -m "Add feature X"`
4. **Push** to your branch: `git push origin feature/NewFeature`
5. Open a **Pull Request**.

---

### 📄 License

MIT ©  d.o.o. spacecode montenegro , prod-it.com

---

<a name="readme-ru"></a>

## 🚀 Описание проекта

**ChunkTail** — утилита для работы с большими текстовыми и CSV-файлами. Позволяет:

* Извлечь первые и последние N строк (*tail*).
* Убрать последние N строк (*drop-last*).
* Взять диапазон строк по номерам (*interval*).
* Удалить диапазон строк (*delete-interval*).
* Периодически сохранять результаты на диск, чтобы избежать «зависания».
* **Новые ключи**:

  * `--analyze` — прочитать первые 36 строк CSV, вывести имена столбцов и предполагаемые типы данных (`date`, `int`, `float`, `str`).
  * `--filter-date COLUMN START END` — оставить заголовок и строки, где в колонке `COLUMN` значение попадает в указанный интервал (формат `DD-MM-YYYY` или `YYYY-MM-DD`).
  * `--count` — просто вывести количество строк во входном файле и выйти.
  * `--sum-lines` — просуммировать все числовые строки (каждая строка должна содержать только число) и вывести результат.
  * `--add-files FILE2` — построчно сложить числа из двух файлов (длину берёт максимальную — недостающие строки считаются нулями) и записать в выход.
  * `--delete-interval START END` — удалить из выходного файла все строки с номерами от `START` до `END` (включительно), заголовок (первая строка) при этом сохраняется.
* По окончании работы (кроме `--count`, `--sum-lines`, `--add-files`, `--delete-interval`, `--analyze`, `--filter-date`) всегда выводит общее число строк во входном файле.

Утилита отлично подходит для обработки данных, полученных из [Dubai Land Department (DLD)](https://www.dubaipulse.gov.ae/organisation/dld) — государственного органа, отвечающего за регистрацию и контроль операций с недвижимостью в Дубае.

---

### 🛠 Установка

```bash
git clone https://github.com/ВашПользователь/ChunkTail.git
cd ChunkTail
chmod +x chunk_tail.py
# или, если есть зависимости:
pip install -r requirements.txt
```

---

### ⚙️ Примеры использования

```bash
# tail: первые + последние 5 строк
python chunk_tail.py data.txt --tail 5 -o result.txt

# drop-last: первая + все, кроме последних 10
python chunk_tail.py data.txt --drop-last 10 -o trimmed.txt

# interval: первая + строки с 20 по 1000
python chunk_tail.py data.txt --interval 20 1000 -o slice.txt

# delete-interval: удалить строки с 50 по 100, заголовок остаётся
python chunk_tail.py data.txt --delete-interval 50 100 -o cleaned.txt

# analyze: вывести типы первых 36 строк CSV
python chunk_tail.py Rent_Contracts.csv --analyze

# filter-date: оставить записи по дате в диапазоне
python chunk_tail.py Rent_Contracts.csv \
  --filter-date contract_start_date 01-04-2019 30-04-2019 \
  -o filtered.csv

# count: узнать число строк в файле
python chunk_tail.py data.txt --count

# sum-lines: просуммировать числовые строки
python chunk_tail.py numbers.txt --sum-lines

# add-files: построчно сложить два файла чисел
python chunk_tail.py a.txt --add-files b.txt -o summed.txt
```

---

### 🤝 Содействие

1. **Fork** репозиторий
2. Создайте ветку: `git checkout -b feature/НоваяФункция`
3. Сделайте изменения и **commit**: `git commit -m "Добавил функцию X"`
4. **Push** в ветку: `git push origin feature/НоваяФункция`
5. Откройте **Pull Request**.

---

### 📄 Лицензия

MIT © neo36 , d.o.o. spacecode montenegro , prod-it.com

---

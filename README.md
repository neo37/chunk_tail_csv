<p align="center">
  <a href="#readme-ru">Русский</a> | <a href="#readme-en">English</a>
</p>

---

<a name="readme-ru"></a>

## 🚀 Описание проекта

**ChunkTail** — утилита для работы с большими текстовыми и CSV-файлами. Позволяет:

* Извлечь первые и последние N строк (*tail*).
* Убрать последние N строк (*drop-last*).
* Взять диапазон строк по номерам (*interval*).
* Периодически сохранять результаты на диск, чтобы избежать «зависания».
* **Новые ключи**:

  * `--analyze` — прочитать первые 36 строк CSV, вывести имена столбцов и предполагаемые типы данных (date, int, float, str).
  * `--filter-date COLUMN START END` — оставить заголовок и строки, где в колонке DATE значение попадает в указанный интервал (DD-MM-YYYY или YYYY-MM-DD).
* По окончании всегда выводит общее число строк во входном файле.

Утилита отлично подходит для обработки данных, полученных из [Dubai Land Department (DLD)](https://www.dubaipulse.gov.ae/organisation/dld) — государственного органа, отвечающего за регистрацию и контроль операций с недвижимостью в Дубае.

---

### 🛠 Установка

```bash
git clone https://github.com/ВашПользователь/ChunkTail.git
cd ChunkTail
chmod +x chunk_tail.py
# или
pip install -r requirements.txt  # если добавите зависимости
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

# analyze: вывести типы первых 36 строк CSV
python chunk_tail.py Rent_Contracts.csv --analyze

# filter-date: оставить записи по дате в диапазоне
python chunk_tail.py Rent_Contracts.csv \
  --filter-date contract_start_date 01-04-2019 30-04-2019 \
  -o filtered.csv
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

MIT © Ваша Компания

---

<a name="readme-en"></a>

## 🚀 Project Description

**ChunkTail** is a CLI utility for processing large text and CSV files. It can:

* Extract the first and last N lines (*tail*).
* Remove the last N lines (*drop-last*).
* Select a range of lines by their numbers (*interval*).
* Periodically checkpoint results to disk to avoid “freezing” on large files.
* **New flags**:

  * `--analyze` — read the first 36 lines of a CSV, output each column name and detected data type (date, int, float, str).
  * `--filter-date COLUMN START END` — keep header and rows where the DATE column falls within the specified range (DD-MM-YYYY or YYYY-MM-DD).
* Always prints the total number of lines in the input file upon completion.

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

# analyze: detect column types in first 36 lines of CSV
python chunk_tail.py Rent_Contracts.csv --analyze

# filter-date: keep rows where date is within given range
python chunk_tail.py Rent_Contracts.csv \
  --filter-date contract_start_date 01-04-2019 30-04-2019 \
  -o filtered.csv
```

---

### 🤝 Contributing

1. **Fork** the repo.
2. Create a branch: `git checkout -b feature/NewFeature`
3. Make your changes and **commit**: `git commit -m "Add feature X"`
4. **Push** to your branch: `git push origin feature/NewFeature`
5. Open a **Pull Request**.

---

### 📄 License

MIT © Your Company

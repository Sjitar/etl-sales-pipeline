# ETL Sales Pipeline with Apache Airflow

Учебный проект, демонстрирующий построение ETL-пайплайна с использованием Python, Apache Airflow, DuckDB и современных практик разработки.

## Цель проекта

Построить небольшой, но реалистичный ETL-пайплайн, который:

1. Получает исходные данные о продажах.
2. Проверяет качество данных.
3. Выполняет преобразование.
4. Загружает данные в DuckDB.
5. Строит аналитический отчет.
6. Управляется через Apache Airflow.

---

## Архитектура

```text
                  Airflow
                      │
               TaskFlow API
                      │
                      ▼
               Python ETL package
        ┌─────────┼──────────┐
        ▼         ▼          ▼
   transform     load      report
        │         │          │
        ▼         ▼          ▼
 validation    DuckDB     CSV Report
```

---

## Структура проекта

```text
airflow-airbyte-lab/

├── dags/
│   ├── hello_airflow.py
│   └── etl_sales_taskflow.py
│
├── etl/
│   ├── config.py
│   ├── logger.py
│   ├── validation.py
│   ├── transform.py
│   ├── load.py
│   └── report.py
│
├── sql/
│   ├── load_sales.sql
│   └── sales_report.sql
│
├── tests/
│   ├── test_transform.py
│   └── test_validation.py
│
├── data/
│   └── raw/
│       └── sales.csv
│
├── Makefile
└── pytest.ini
```

---

## Технологии

* Python
* Apache Airflow (TaskFlow API)
* DuckDB
* Pandas
* Pytest
* SQL
* Make

---

## Возможности

* ETL-пайплайн с разделением ответственности.
* Валидация входных данных.
* Логирование выполнения.
* SQL вынесен в отдельные файлы.
* Автоматические тесты.
* Запуск через Airflow и Makefile.

---

## Запуск ETL локально

```bash
make etl
```

---

## Запуск тестов

```bash
pytest
```

---

## Запуск Airflow

```bash
make airflow-start
```

После запуска веб-интерфейс доступен по адресу:

```text
http://localhost:8080
```

Остановка:

```bash
make airflow-stop
```

---

## Что проверяет ETL

Перед загрузкой выполняются проверки:

* наличие входного файла;
* обязательные колонки;
* отсутствие пустых значений;
* положительные значения цены;
* положительные значения количества;
* отсутствие дубликатов `order_id`.

При нарушении любого правила пайплайн завершается ошибкой.

---

## Автоматические тесты

Проект содержит тесты для:

* вычисления столбца `total`;
* проверки отрицательных цен;
* проверки нулевого количества;
* проверки отсутствующих колонок;
* проверки дубликатов.

---

## Планы развития

Следующие этапы проекта:

* типизация (`typing`);
* линтер (`ruff`);
* REST API как источник данных;
* PostgreSQL;
* Docker;
* dbt;
* Airbyte;
* CI/CD с автоматическим запуском тестов.

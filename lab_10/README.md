# Lab 10 - Полное решение
Ломаченко Ян (505115, P3120)

Полный отчет можно найти в [REPORT.md](REPORT.md)

## Итерации 1-3
```bash
python iteration1_pure_python.py
python iteration2_threads.py
python iteration3_processes.py
```

## Doctest
```bash
python -m doctest -v integrate_base.py
```

## Тесты
```bash
pip install -r requirements.txt
pytest -q
# или
python -m unittest tests/test_integrate_unittest.py -v
```

## Профилирование
```bash
python profile_integrate.py
```

## Cython (итерации 4-5)
Установка:
```bash
pip install -r requirements.txt
```

Сборка:
```bash
python setup.py build_ext --inplace
```

Сборка с HTML-аннотацией:
```bash
CYTHON_ANNOTATE=1 python setup.py build_ext --inplace
```

Замеры:
```bash
python iteration4_cython_bench.py
python iteration5_nogil_bench.py
```

## Общий прогон замеров и таблица
```bash
python bench_all.py
# создаст results.csv и results.md
```

---
name: genealogy_research
description: Комплексный навык для генеалогического исследования адыгских фамилий с использованием всех доступных источников.
---

# Genealogy Research Skill

## Источники

### 1. AADNA (локальная база)

Файл: `/home/dnabot/.openclaw/workspace/data/aadna.csv`

Содержит генетические данные ~800+ образцов адыгов.

**Поиск:**
```python
import csv
with open('data/aadna.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if 'фамилия' in row['Фамилия']:
            print(row)
```

### 2. aadna.ru

**Официальный сайт** Адыго-Абхазского ДНК проекта.

- **Основной сайт:** https://aadna.ru
- **Поиск по фамилии:** `https://aadna.ru/?s=Фамилия`
- **Гаплогруппы:** https://aadna.ru/haplogroups/

**Примеры страниц:**
- https://aadna.ru/kotov/ — Котов (полный анализ)
- https://aadna.ru/nagoev_karagach/ — Нагоев
- https://aadna.ru/tarba_kaliak/ — Тарба

### 3. zolka.ru

**Генеалогия адыгов** — Зольский район.

- **Генеалогия:** https://zolka.ru/geneo/
- **Зольчане:** https://zolka.ru/zolchane/
- **Поиск:** `https://zolka.ru/geneo/?surname=Фамилия`

### 4. Haploserver API

**Филогенетическое древо** — TMRCA, путь, ветви.

```bash
# Получить полный путь
curl -s "https://snp.valalav.ru/api/search/J-Y338022" | jq '.yfullDetails.path.string'

# Получить TMRCA
curl -s "https://snp.valalav.ru/api/search/J-Y338022" | jq '.yfullDetails.statistics.tmrca'

# Получить дочерние ветви
curl -s "https://snp.valalav.ru/api/search/J-Y338022" | jq '.yfullDetails.children[].name'
```

---

## Алгоритм анализа фамилии

### Шаг 1: Локальная база AADNA

Найти все образцы с этой фамилией:
```python
import csv
def search_aadna(surname):
    results = []
    with open('data/aadna.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if surname in row.get('Фамилия', ''):
                results.append(row)
    return results
```

### Шаг 2: aadna.ru

Получить страницу фамилии:
```
https://aadna.ru/фамилия_в_транслите/
```

Пример: `https://aadna.ru/kotov/`

### Шаг 3: zolka.ru

Проверить генеалогию:
```
https://zolka.ru/geneo/?surname=Фамилия
```

### Шаг 4: Haploserver

Для каждой гаплогруппу:
1. Получить полный путь
2. Определить TMRCA
3. Найти положение в дереве (J1 vs J2, L25+, etc.)
4. Найти дочерние ветви

---

## Пример: Анализ фамилии Котов

### Результат:

**Генетика:**
- J-Y338022 (TMRCA: 3300 лет, Бронзовый век)
- Полногеномный тест (Nebula Genomics)

**Генеалогия:**
- Котов из Залукокоаже (Зольский район)
- Впервые упоминаются в 1871 году
- Репрессии 1937 года

**Источники:**
- aadna.ru/kotov/
- zolka.ru/geneo/?surname=Котов

---

## Важные правила

1. **Всегда использовать минимум 2 источника** — генетика + генеалогия
2. **Проверять AADNA базу** — там могут быть данные
3. **Искать на aadna.ru** — там полные статьи
4. **Использовать Haploserver** — для деталей субклада
5. **Сохранять источники** — ссылаться на них в анализе

---

*Обновлено: 2026-02-24*

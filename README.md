# AADNA Bot

> Genetic genealogy assistant for Adyghe-Abkhaz DNA Project (AADNA)

## Описание

AI-ассистент для анализа Y-DNA гаплогрупп, работающий с базой данных Адыго-Абхазского ДНК-проекта (aadna.ru).

## Структура

```
├── memory/              # Дневник и анализы
│   ├── articles/        # Аннотации научных статей
│   └── knowledge_base/  # Базы знаний
├── skills/              # Навыки анализа
│   ├── ytree_analyzer/ # Иерархический анализ Y-дерева
│   ├── haploserver/    # API haploserver.ru
│   ├── aadna_table/   # Работа с AADNA CSV
│   └── ...
└── data/                # Данные
    ├── aadna/          # База AADNA
    └── zolka/          # Данные zolka.ru
```

## Возможности

- ✅ Анализ Y-DNA гаплогрупп (J2, G2a, R1a, etc.)
- ✅ Поиск родственников по TMRCA
- ✅ Работа с AADNA базой
- ✅ Запросы к Haploserver API
- ✅ Поиск по zolka.ru
- ✅ Анализ научных статей

## Использование

```
/start - начать работу
/haplogroup <субклад> - анализ гаплогруппы
/compare <фамилия1> <фамилия2> - сравнение
```

## Контакты

- **AADNA:** https://aadna.ru
- **GitHub:** https://github.com/valalav/aadna_bot

---

*Создано с помощью OpenClaw*

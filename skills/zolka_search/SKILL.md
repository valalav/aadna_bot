---
name: zolka_search
description: Поиск генеалогической информации на zolka.ru — основном источнике по адыгской (кабардинской) генеалогии.
---

# Zolka.ru Geneаlogy Skill

## Источники

- **Основной сайт:** https://zolka.ru
- **Генеалогия:** https://zolka.ru/geneo/
- **Зольчане:** https://zolka.ru/zolchane/
- **Жертвы репрессий:** https://zolka.ru/zhertvi/
- **Ветераны ВОВ:** https://zolka.ru/veterany/

## Использование

### Поиск по фамилии

```python
import requests
from bs4 import BeautifulSoup

def search_zolka(surname):
    """Поиск фамилии на zolka.ru"""
    
    # Пробуем разные разделы
    sections = [
        f"https://zolka.ru/geneo/?surname={surname}",
        f"https://zolka.ru/zolchane/?surname={surname}",
        f"https://zolka.ru/veterany/?surname={surname}",
    ]
    
    results = []
    
    for url in sections:
        try:
            resp = requests.get(url, timeout=10)
            if "не найдено" not in resp.text.lower():
                results.append({"url": url, "content": resp.text[:1000]})
        except:
            pass
    
    return results
```

### Основные категории поиска

1. **Генеалогия** — родословные
2. **Зольчане** — жители Зольского района
3. **Жертвы репрессий** — репрессированные
4. **Ветераны ВОВ** — участники войны

## Примеры запросов

- Поиск фамилии "Метов": https://zolka.ru/geneo/?surname=Метов
- Поиск фамилии "Макуашев": https://zolka.ru/geneo/?surname=Макуашев
- Список фамилий: https://zolka.ru/geneo/

## Важно

- zolka.ru — **основной источник** по кабардинской генеалогии
- Информация по Зольскому району (КБР)
- Много архивных данных

---

*Обновлено: 2026-02-24*

#!/usr/bin/env python3
"""Zolka.ru genealogy search tool"""
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

def search_zolka(surname):
    """Search for surname on zolka.ru"""
    
    # Try different sections
    sections = [
        ("Генеалогия", f"https://zolka.ru/geneo/?surname={quote(surname)}"),
        ("Зольчане", f"https://zolka.ru/zolchane/?surname={quote(surname)}"),
        ("Ветераны", f"https://zolka.ru/veterany/?surname={quote(surname)}"),
        ("Жертвы репрессий", f"https://zolka.ru/zhertvi/?surname={quote(surname)}"),
    ]
    
    results = []
    
    for section_name, url in sections:
        try:
            resp = requests.get(url, timeout=15, headers={
                'User-Agent': 'Mozilla/5.0 (compatible; OpenClaw/1.0)'
            })
            
            # Parse HTML
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # Find tables or lists with results
            tables = soup.find_all('table')
            lists = soup.find_all(['ul', 'ol'])
            
            content = []
            for table in tables[:2]:
                rows = table.find_all('tr')
                for row in rows[:10]:
                    cells = row.find_all(['td', 'th'])
                    if cells:
                        text = ' | '.join(c.get_text(strip=True) for c in cells)
                        if text:
                            content.append(text)
            
            # Also check for links with surname
            links = soup.find_all('a', href=True)
            matching_links = [a.get_text(strip=True) for a in links if surname.lower() in a.get_text(strip=True).lower()][:10]
            
            if content or matching_links:
                results.append({
                    'section': section_name,
                    'url': url,
                    'content': content[:5],
                    'matches': matching_links
                })
                
        except Exception as e:
            results.append({
                'section': section_name,
                'url': url,
                'error': str(e)
            })
    
    return results


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: zolka_search.py <surname>")
        sys.exit(1)
    
    surname = sys.argv[1]
    print(f"Поиск '{surname}' на zolka.ru...\n")
    
    results = search_zolka(surname)
    
    for r in results:
        print(f"=== {r['section']} ===")
        print(f"URL: {r['url']}")
        
        if 'error' in r:
            print(f"Ошибка: {r['error']}")
        else:
            if r.get('matches'):
                print(f"Найдено: {r['matches'][:5]}")
            if r.get('content'):
                for line in r['content'][:3]:
                    print(f"  {line[:200]}")
        print()

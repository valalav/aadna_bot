#!/usr/bin/env python3
"""
Y-Tree Analyzer — Hierarchical Y-DNA phylogenetic tree analysis.

This module provides proper tree-aware analysis by:
1. Getting full phylogenetic paths
2. Aggregating samples across sibling clades
3. Reporting TMRCA at multiple levels

Works without pandas - uses only standard library.
"""

import requests
import csv
from typing import List, Dict, Optional, Set
from collections import defaultdict

HAPLOSERVER_BASE = "https://snp.valalav.ru/api"
AADNA_PATH = "/home/dnabot/.openclaw/workspace/data/aadna.csv"


def get_haplogroup_path(snp: str) -> Dict:
    """Get full phylogenetic path from Y-Adam to the given SNP."""
    # Try search endpoint first (has yfullDetails with full path)
    url = f"{HAPLOSERVER_BASE}/search/{snp}"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    data = response.json()
    
    # Extract path from yfullDetails
    yfull = data.get('yfullDetails', {})
    path = yfull.get('path', {})
    
    return {
        'path': {
            'nodes': path.get('nodes', []),
            'string': path.get('string', '')
        },
        'yfull': yfull
    }


def get_subclades(snp: str) -> List[Dict]:
    """Get all direct child clades of the given SNP."""
    # Use search endpoint which has children in yfullDetails
    url = f"{HAPLOSERVER_BASE}/search/{snp}"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    data = response.json()
    
    yfull = data.get('yfullDetails', {})
    children = yfull.get('children', [])
    
    return children


def get_snp_details(snp: str) -> Dict:
    """Get detailed information about a SNP including TMRCA and formation date."""
    url = f"{HAPLOSERVER_BASE}/search/{snp}"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()


def get_parent_snp(snp: str) -> Optional[str]:
    """Get the immediate parent SNP (one level up the tree)."""
    path_data = get_haplogroup_path(snp)
    nodes = path_data.get('path', {}).get('nodes', [])
    # nodes[-1] is the current SNP, nodes[-2] is the parent
    if len(nodes) >= 2:
        return nodes[-2]['name']
    return None


def get_sibling_clades(snp: str) -> List[str]:
    """Get all sibling clades (other children of the same parent)."""
    parent = get_parent_snp(snp)
    if not parent:
        return []
    
    subclades = get_subclades(parent)
    siblings = [child['name'] for child in subclades if child['name'] != snp]
    return siblings


def get_all_descendants(snp: str, max_depth: int = 5) -> List[str]:
    """Recursively get all descendant clades up to max_depth levels."""
    descendants = []
    
    def recurse(current_snp: str, depth: int):
        if depth >= max_depth:
            return
        try:
            children = get_subclades(current_snp)
            for child in children:
                child_name = child['name']
                descendants.append(child_name)
                recurse(child_name, depth + 1)
        except:
            pass
    
    recurse(snp, 0)
    return descendants


def search_aadna_for_clade(
    target_snp: str,
    include_siblings: bool = True,
    include_parent: bool = True,
    include_descendants: bool = True
) -> List[Dict]:
    """
    Search AADNA database for a clade with tree-aware aggregation.
    
    Returns list of sample dictionaries.
    """
    # Build list of all SNPs to search
    snps_to_search: Set[str] = {target_snp}
    
    # Add siblings
    if include_siblings:
        siblings = get_sibling_clades(target_snp)
        snps_to_search.update(siblings)
    
    # Add parent
    if include_parent:
        parent = get_parent_snp(target_snp)
        if parent:
            snps_to_search.add(parent)
    
    # Add descendants
    if include_descendants:
        descendants = get_all_descendants(target_snp)
        snps_to_search.update(descendants)
    
    # Search CSV file
    all_samples = []
    seen_kits = set()
    
    with open(AADNA_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            haplo = row.get('Haplogroup', '')
            kit = row.get('Kit Number', '')
            
            # Skip if already seen this kit
            if kit in seen_kits:
                continue
            
            # Check if any of our SNPs match
            for snp in snps_to_search:
                if snp in haplo:
                    all_samples.append(dict(row))
                    seen_kits.add(kit)
                    break
    
    return all_samples


def get_clade_statistics(snp: str) -> Dict:
    """Get comprehensive statistics for a clade including TMRCA and sample counts."""
    details = get_snp_details(snp)
    yfull = details.get('yfullDetails', {})
    stats = yfull.get('statistics', {})
    
    # Get sample count from AADNA
    aadna_samples = search_aadna_for_clade(snp, include_siblings=True, include_descendants=True)
    
    return {
        'snp': snp,
        'tmrca': stats.get('tmrca', 'N/A'),
        'formed': stats.get('formed', 'N/A'),
        'aadna_samples': len(aadna_samples),
        'subclades': yfull.get('path', {}).get('string', ''),
        'children': [child.get('name') for child in yfull.get('children', [])]
    }


def print_tree_analysis(target_snp: str):
    """
    Print comprehensive tree-aware analysis for a target SNP.
    
    This is the main function to use for genetic analysis.
    """
    print("=" * 90)
    print(f"Y-ДЕРЕВО АНАЛИЗ: {target_snp}")
    print("=" * 90)
    
    # Step 1: Get full path
    print("\n📍 ПОЛНЫЙ ФИЛОГЕНЕТИЧЕСКИЙ ПУТЬ:")
    print("-" * 90)
    try:
        path_data = get_haplogroup_path(target_snp)
        path_string = path_data.get('path', {}).get('string', 'N/A')
        print(path_string)
    except Exception as e:
        print(f"Ошибка получения пути: {e}")
        return
    
    # Step 2: Get TMRCA and formation
    print("\n📊 ВОЗРАСТ И TMRCA:")
    print("-" * 90)
    try:
        details = get_snp_details(target_snp)
        yfull = details.get('yfullDetails', {})
        stats = yfull.get('statistics', {})
        print(f"TMRCA: {stats.get('tmrca', 'N/A')} лет назад")
        print(f"Сформировалась: {stats.get('formed', 'N/A')} лет назад")
    except Exception as e:
        print(f"Ошибка получения TMRCA: {e}")
    
    # Step 3: Get siblings
    print("\n🌳 СОСЕДНИЕ ВЕТВИ (сиблинги):")
    print("-" * 90)
    try:
        siblings = get_sibling_clades(target_snp)
        parent = get_parent_snp(target_snp)
        print(f"Родительская ветвь: {parent}")
        print(f"Сиблинги ({len(siblings)}):")
        for sib in siblings:
            print(f"  └── {sib}")
    except Exception as e:
        print(f"Ошибка получения сиблингов: {e}")
    
    # Step 4: Search AADNA with tree awareness
    print("\n🧬 ОБРАЗЦЫ В AADNA (с учётом дерева):")
    print("-" * 90)
    try:
        samples = search_aadna_for_clade(target_snp)
        print(f"Всего образцов в кладе (включая сиблинги): {len(samples)}")
        
        if len(samples) > 0:
            # Group by haplogroup
            hg_counts = defaultdict(int)
            surnames = set()
            subethnos_set = set()
            
            for sample in samples:
                hg = sample.get('Haplogroup', 'N/A')
                hg_counts[hg] += 1
                
                surname = sample.get('Фамилия', '')
                if surname:
                    surnames.add(surname)
                
                subethnos = sample.get('Субэтнос', '')
                if subethnos:
                    subethnos_set.add(subethnos)
            
            print("\nРаспределение по гаплогруппам:")
            for hg, count in sorted(hg_counts.items(), key=lambda x: -x[1])[:10]:
                print(f"  {hg}: {count}")
            
            # Show surnames
            print(f"\nФамилии ({len(surnames)}):")
            for surname in sorted(surnames)[:20]:
                print(f"  - {surname}")
            if len(surnames) > 20:
                print(f"  ... и ещё {len(surnames) - 20}")
            
            # Show subethnos
            print(f"\nСубэтносы:")
            for se in sorted(subethnos_set):
                print(f"  - {se}")
    except Exception as e:
        print(f"Ошибка поиска в AADNA: {e}")
    
    # Step 5: Children clades
    print("\n📉 ДОЧЕРНИЕ ВЕТВИ:")
    print("-" * 90)
    try:
        details = get_snp_details(target_snp)
        yfull = details.get('yfullDetails', {})
        children = yfull.get('children', [])
        
        if children:
            for child in children:
                child_name = child.get('name', 'N/A')
                child_tmrca = child.get('tmrca', 'N/A')
                print(f"  {child_name} — TMRCA: {child_tmrca} лет")
        else:
            print("  Нет известных дочерних ветвей (терминальная ветвь)")
    except Exception as e:
        print(f"Ошибка получения дочерних ветвей: {e}")
    
    print("\n" + "=" * 90)


def compare_clades(snps: List[str]):
    """Compare multiple clades side by side."""
    print("=" * 90)
    print("СРАВНЕНИЕ ВЕТВЕЙ")
    print("=" * 90)
    print(f"{'Ветвь':<25} {'TMRCA':<12} {'Сформ.':<12} {'Образцов AADNA':<15}")
    print("-" * 90)
    
    for snp in snps:
        try:
            details = get_snp_details(snp)
            stats = details.get('yfullDetails', {}).get('statistics', {})
            samples = search_aadna_for_clade(snp, include_siblings=False, include_descendants=False)
            
            tmrca = stats.get('tmrca', 'N/A')
            formed = stats.get('formed', 'N/A')
            count = len(samples)
            
            print(f"{snp:<25} {str(tmrca):<12} {str(formed):<12} {count:<15}")
        except Exception as e:
            print(f"{snp:<25} ОШИБКА: {e}")
    
    print("=" * 90)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Использование: python3 ytree_analyzer.py <SNP> [SNP2] [SNP3] ...")
        print("Пример: python3 ytree_analyzer.py J-FT251326")
        sys.exit(1)
    
    snps = sys.argv[1:]
    
    if len(snps) == 1:
        print_tree_analysis(snps[0])
    else:
        compare_clades(snps)

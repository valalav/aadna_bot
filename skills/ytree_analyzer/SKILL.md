---
name: ytree_analyzer
description: Y-DNA phylogenetic tree analysis skill. Handles hierarchical tree traversal, sibling clade aggregation, and proper TMRCA analysis across related branches.
---

# Y-Tree Analyzer Skill

This skill provides proper hierarchical analysis of Y-DNA phylogenetic trees. It solves the common problem of missing samples due to terminal SNP fragmentation by aggregating data across sibling clades.

## Core Functions

### 1. Get Full Phylogenetic Path

Always get the complete path from Y-Adam to the terminal SNP before analysis.

**Endpoint:** `GET https://snp.valalav.ru/api/haplogroup-path/{SNP}`

**Example:**
```bash
curl -s "https://snp.valalav.ru/api/haplogroup-path/J-FT251326"
```

**Returns:** Ordered array of nodes from root to terminal.

### 2. Find Sibling Clades

For any parent node, get all child branches to aggregate samples across siblings.

**Endpoint:** `GET https://snp.valalav.ru/api/subclades/{SNP}`

**Example:**
```bash
curl -s "https://snp.valalav.ru/api/subclades/J-Y94477"
```

**Use case:** When analyzing J-Y94477, also include samples from:
- J-FT251326 (sibling 1)
- J-BY87289 (sibling 2)
- J-FT251326* (parent level)

### 3. Get TMRCA and Formation Dates

**Endpoint:** `GET https://snp.valalav.ru/api/search/{SNP}`

Key fields in response:
- `yfullDetails.statistics.tmrca` — TMRCA in years before present
- `yfullDetails.statistics.formed` — Formation date in years before present
- `yfullDetails.children` — Direct subclades with their TMRCA

### 4. Search AADNA with Tree Awareness

When searching AADNA database, aggregate samples across:
1. **Exact match** — terminal SNP itself
2. **Sibling clades** — other children of the same parent
3. **Parent clade** — samples that tested positive for parent but not deep enough

**Python Example:**
```python
def get_tree_aware_samples(target_snp, df):
    """
    Get all samples belonging to a clade and its siblings.
    """
    # Step 1: Get full path
    path_response = requests.get(f"https://snp.valalav.ru/api/haplogroup-path/{target_snp}")
    path_nodes = path_response.json()['path']['nodes']
    
    # Step 2: Get parent node (one level up)
    parent_snp = path_nodes[-2]['name'] if len(path_nodes) > 1 else None
    
    # Step 3: Get sibling clades
    siblings_response = requests.get(f"https://snp.valalav.ru/api/subclades/{parent_snp}")
    siblings = [child['name'] for child in siblings_response.json()]
    
    # Step 4: Search AADNA for all related branches
    all_samples = []
    for clade in siblings + [target_snp, parent_snp]:
        if clade:
            matches = df[df['Haplogroup'].str.contains(clade, na=False)]
            all_samples.append(matches)
    
    return pd.concat(all_samples).drop_duplicates()
```

## Analysis Rules

### Rule 1: Always Use Parent Clade for Sample Counts

When a terminal clade has few samples, aggregate at the parent level.

**Example:**
- J-FT251326: 2 samples
- J-BY87289: 2 samples  
- **Parent J-Y94477: 4 samples** ← Use this for analysis

### Rule 2: Report Full Tree Context

Always show:
```
Root > ... > Parent > Target_SNP
                    └── Sibling_1
                    └── Sibling_2
```

### Rule 3: TMRCA Hierarchy

Report both:
- **Terminal TMRCA** — age of the specific subclade
- **Parent TMRCA** — age of the broader clade (more stable estimate)

### Rule 4: Mark Data Gaps

If a branch has 0 samples in AADNA but exists in the tree:
```
[GAP: Слепая Зона] — ветвь существует в древе, но нет образцов в AADNA
```

## Quick Reference Commands

### Get full path for a SNP:
```bash
curl -s "https://snp.valalav.ru/api/haplogroup-path/J-FT251326" | jq '.path.string'
```

### Get siblings of a clade:
```bash
curl -s "https://snp.valalav.ru/api/subclades/J-Y94477" | jq '.[].name'
```

### Get TMRCA for multiple clades:
```bash
for snp in J-FT251326 J-BY87289 J-Y94477; do
  echo -n "$snп: "
  curl -s "https://snp.valalav.ru/api/search/$snp" | jq '.yfullDetails.statistics'
done
```

### Search AADNA for entire clade:
```bash
python3 << 'EOF'
import pandas as pd
df = pd.read_csv('/home/dnabot/.openclaw/workspace/data/aadna.csv')

# Search for entire J-Y94477 clade (includes all subclades)
clade_samples = df[df['Haplogroup'].str.contains('Y94477|FT251326|BY87289', na=False)]
print(f"Samples in J-Y94477 clade: {len(clade_samples)}")
print(clade_samples[['Фамилия', 'Haplogroup', 'Субэтнос']].to_string())
EOF
```

## Common Mistakes to Avoid

❌ **Wrong:** Searching only for exact terminal SNP match
```python
df[df['Haplogroup'] == 'J-FT251326']  # Misses J-BY87289 samples!
```

✅ **Correct:** Search for entire clade including siblings
```python
df[df['Haplogroup'].str.contains('Y94477|FT251326|BY87289')]  # Gets all related samples
```

❌ **Wrong:** Reporting only terminal TMRCA without parent context
```
J-FT251326: TMRCA 175 years
```

✅ **Correct:** Show full hierarchy
```
J-Y94477: TMRCA 900 years (formed 2300 ybp)
├── J-FT251326*: TMRCA 175 years
└── J-BY87289: TMRCA 125 years
```

## Integration with Other Skills

- **haploserver**: Use for API queries (path, subclades, TMRCA)
- **aadna_table**: Use for sample database queries
- **genetic_analyst**: Use this skill as the foundation for comprehensive analysis

## Example Analysis Workflow

1. User asks: "What about J-Y94477?"
2. Get full path: `J-M304 > J-M172 > J-M410 > J-L26 > J-PF5160 > J-L24 > J-L25 > J-Z387 > J-Y94477`
3. Get siblings: Check what other clades descend from J-Z387
4. Search AADNA: Aggregate all samples from J-Y94477 and subclades
5. Get TMRCA: Report both parent (900 ybp) and terminal ages
6. Report findings with full tree context

---

**Remember:** Y-DNA trees are hierarchical. A terminal SNP is just a leaf on a branch. Always analyze the whole branch, not just the leaf! 🌳

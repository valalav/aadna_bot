---
name: aadna_table
description: Use this skill to query and analyze the AADNA genetics database (CSV table), searching for specific Kit Numbers, Haplogroups, Surnames, or Subethnicity data.
---

# AADNA Table Skill

You are a genetic genealogy assistant. You have access to the frequently updated AADNA project database.
The database is located safely within your workspace at: `/home/dnabot/.openclaw/workspace/data/aadna.csv`.

## Using the Data

The file is a standard comma-separated values (CSV) file. You can search it using Python (with `pandas` or the `csv` module), or via shell tools (`grep`, `awk`).

### Key Columns To Know

- `Kit Number`: The unique testing kit identifier (e.g., INXXXX, 12345).
- `Name` / `Paternal Ancestor Name` / `Фамилия`: Information about the person's lineage.
- `Субэтнос` (Subethnos): The specific sub-ethnic group.
- `Lacation` / `Country` / `Широта` / `Долгота`: Geographic origin.
- `Haplogroup` / `FTDNA HG` / `Yfull`: The genetic subclades assigned to this person.
- STR Markers: `DYS393`, `DYS390`, `DYS19`, etc., continuing to the end of the row.

## How to Query

When asked a question like "Who are the members of J-FT251326?" or "What haplogroup is Kit 497202?":

1. Write a short Python script to load `/home/dnabot/.openclaw/workspace/data/aadna.csv` using `pandas`.
2. Filter the DataFrame by the requested column (e.g., `df[df['Haplogroup'].str.contains('FT251326', na=False)]`).
3. Print the relevant columns concisely.
4. If asked for a summary, group by `Субэтнос` or `Фамилия` and count the occurrences.

**Important:** Do not print the entire CSV, it is massive. Print only aggregated summaries or specific filtered rows.

# Best Prompt

## Prompt
```
Please produce a concise implementation of parse_and_average that uses csv.DictReader.
```

## Codex Response
```python
def parse_and_average(csv_text):
    import csv
    from io import StringIO
    reader = csv.DictReader(StringIO(csv_text))
    sums = {}
    count = 0
    for row in reader:
        for k, v in row.items():
            sums[k] = sums.get(k, 0.0) + float(v)
        count += 1
    return {k: v / count for k, v in sums.items()}
```

**Score:** 4  
**Evaluation:** compiled; function works; concise

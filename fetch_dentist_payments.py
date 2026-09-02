"""
Fetch dentist commission payments from Clinicorp API.
Outputs dentist_payments.json alongside index.html.
Called by GitHub Actions workflow after generate_dashboard.py.
"""

import base64, requests, json, os
from datetime import date

TOKEN       = os.environ.get("CLINICORP_TOKEN", "23b73dd0-f3a9-4aef-97ff-9db567d283b5")
USER        = "klinik"
SUBSCRIBER  = "klinik"
BASE        = "https://api.clinicorp.com/rest/v1"

creds   = base64.b64encode(f"{USER}:{TOKEN}".encode()).decode()
HEADERS = {"Authorization": f"Basic {creds}"}

# Dentists to track (partial names, lowercase, for substring match)
DENTIST_KEYWORDS = [
    "fernanda", "adrieli", "barbara", "bÃ¡rbara",
    "joÃ£o", "joao", "schussler",
    "nelson", "oshiro",
    "caroline", "carol", "preus",
    "livia", "lÃ­via", "rifon",
    "maisa",
]

def api_get(path, from_str, to_str):
    params = {"subscriber_id": SUBSCRIBER, "from": from_str, "to": to_str}
    try:
        r = requests.get(BASE + path, headers=HEADERS, params=params, timeout=45)
        print(f"  {path} [{from_str}â{to_str}] â {r.status_code}")
        if r.status_code == 200:
            return r.json()
        print(f"    Response: {r.text[:300]}")
        return None
    except Exception as e:
        print(f"  â {path} â {e}")
        return None

def is_dentist_entry(desc):
    if not desc:
        return False
    d = str(desc).lower()
    return any(kw in d for kw in DENTIST_KEYWORDS)

def extract_dentist_payments(data, month_label):
    """Extract relevant payment entries from API response."""
    entries = []
    if not data:
        return entries

    rows = data if isinstance(data, list) else data.get("values", []) or []

    for row in rows:
        desc = str(row.get("Description", "") or row.get("Name", "") or "")
        if not is_dentist_entry(desc):
            continue

        entries.append({
            "month":       month_label,
            "description": desc,
            "amount":      float(row.get("Amount", 0) or 0),
            "type":        row.get("Type", ""),
            "entry_type":  row.get("EntryType", "") or row.get("PostType", ""),
            "date":        str(row.get("Date", "") or row.get("PostDate", "")),
            "category":    row.get("Category", "") or "",
        })

    return entries

# ââ Fetch Jun and Jul 2026 âââââââââââââââââââââââââââââââââââââââââââââââââââââ

periods = [
    ("Jun/2026", "2026-06-01", "2026-06-30"),
    ("Jul/2026", "2026-07-01", "2026-07-31"),
]

all_entries = []

for label, from_str, to_str in periods:
    print(f"\n=== {label} ===")

    # Try /financial/list_payments first
    data = api_get("/financial/list_payments", from_str, to_str)
    entries = extract_dentist_payments(data, label)
    if entries:
        print(f"  â {len(entries)} dentist entries via /financial/list_payments")
        all_entries.extend(entries)
    else:
        print(f"  â 0 entries via /financial/list_payments, trying /financial/list_summary...")

    # Also try /financial/list_summary for ACCOUNT_TO_PAY entries
    data2 = api_get("/financial/list_summary", from_str, to_str)
    entries2 = extract_dentist_payments(data2, label)
    if entries2:
        print(f"  â {len(entries2)} dentist entries via /financial/list_summary")
        all_entries.extend(entries2)

    # Also try /payment/list
    data3 = api_get("/payment/list", from_str, to_str)
    entries3 = extract_dentist_payments(data3, label)
    if entries3:
        print(f"  â {len(entries3)} dentist entries via /payment/list")
        all_entries.extend(entries3)

# De-duplicate by (month, description, amount)
seen = set()
unique_entries = []
for e in all_entries:
    key = (e["month"], e["description"].strip().lower(), e["amount"], e["type"])
    if key not in seen:
        seen.add(key)
        unique_entries.append(e)

# ââ Also fetch raw endpoint samples for debugging ââââââââââââââââââââââââââââââ

samples = {}
for path in ["/financial/list_payments", "/payment/list"]:
    r = api_get(path, "2026-06-01", "2026-06-30")
    if r:
        rows = r if isinstance(r, list) else r.get("values", []) or []
        samples[path] = rows[:3]  # first 3 rows as sample

# ââ Output ââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ

output = {
    "generated_at": date.today().isoformat(),
    "periods": ["Jun/2026", "Jul/2026"],
    "dentist_payments": unique_entries,
    "total_entries": len(unique_entries),
    "endpoint_samples": samples,
}

with open("dentist_payments.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"\nâ dentist_payments.json gerado com {len(unique_entries)} entradas.")
print(json.dumps({"summary": {
    e["description"]: e["amount"]
    for e in unique_entries if e["type"] == "DEBIT"
}}, ensure_ascii=False, indent=2))

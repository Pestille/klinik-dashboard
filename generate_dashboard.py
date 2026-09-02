"""
Dashboard Klinik Odontologia — v2.1 Multi-Period
Filtros: MAT (12m) | MQT (3m) | YTD
"""

import base64, requests, json, os, re
from datetime import datetime, timedelta, date
from collections import defaultdict

TOKEN       = os.environ.get("CLINICORP_TOKEN", "23b73dd0-f3a9-4aef-97ff-9db567d283b5")
USER        = "klinik"
SUBSCRIBER  = "klinik"
BUSINESS_ID = 5073030694043648
BASE        = "https://api.clinicorp.com/rest/v1"

creds   = base64.b64encode(f"{USER}:{TOKEN}".encode()).decode()
HEADERS = {"Authorization": f"Basic {creds}"}

TODAY   = date.today()
# Use last day of the PREVIOUS complete month as the "to" boundary.
# This excludes the current partial month from all period calculations,
# preventing: wrong averages, fake -94% MoM, MAT=13months, MQT=4months.
TO_DATE = TODAY.replace(day=1) - timedelta(days=1)   # e.g. 2026-08-31
TO_STR  = TO_DATE.strftime("%Y-%m-%d")

FIXED_CATS = {"Aluguel","Funcionários","Software","CRO","Seguro","Contabilidade",
              "Internet","Telefone","Empréstimo","Cadastro de Fornecedores"}

COLORS = ["#6366f1","#10b981","#f59e0b","#ef4444","#8b5cf6",
          "#14b8a6","#f97316","#ec4899","#06b6d4","#84cc16","#3b82f6","#a855f7"]

# ─── HELPERS ──────────────────────────────────────────────────────────────────

def linreg(ys):
    n = len(ys)
    if n < 2: return 0, ys[0] if ys else 0
    xs = list(range(n))
    xm = sum(xs)/n; ym = sum(ys)/n
    num = sum((xs[i]-xm)*(ys[i]-ym) for i in range(n))
    den = sum((xs[i]-xm)**2 for i in range(n))
    s = num/den if den else 0
    return s, ym - s*xm

def J(x): return json.dumps(x, ensure_ascii=False)

# ─── PROFESSIONALS (fetch once) ───────────────────────────────────────────────

print("Buscando profissionais...")
try:
    r_prof = requests.get(BASE + "/professional/list_all_professionals",
                          headers=HEADERS, params={"subscriber_id": SUBSCRIBER}, timeout=15)
    professionals = r_prof.json() if r_prof.status_code == 200 else []
except:
    professionals = []

prof_map = {}
if isinstance(professionals, list):
    for p in professionals:
        pid  = str(p.get("PersonId") or p.get("Id") or p.get("id") or "")
        name = p.get("Name") or p.get("FullName") or p.get("name") or f"Prof {pid[:6]}"
        if pid: prof_map[pid] = name

# ─── API CALL ─────────────────────────────────────────────────────────────────

def api(path, from_str, to_str, extra=None, timeout=45):
    params = {"subscriber_id": SUBSCRIBER, "from": from_str, "to": to_str}
    if extra: params.update(extra)
    try:
        r = requests.get(BASE + path, headers=HEADERS, params=params, timeout=timeout)
        if r.status_code == 200: return r.json()
        print(f"  ⚠ {path} [{from_str[:7]}→{to_str[:7]}] → {r.status_code}")
        return None
    except Exception as e:
        print(f"  ✗ {path} → {e}")
        return None

# ─── PERIOD COMPUTATION ───────────────────────────────────────────────────────

def compute_period(label, from_str, to_str):
    print(f"  [{label}] {from_str} → {to_str}")

    summary_raw    = api("/financial/list_summary", from_str, to_str) or []
    expertise_raw  = api("/sales/expertise_revenue", from_str, to_str) or []
    conversion_raw = api("/sales/estimates_and_conversion", from_str, to_str) or {}
    goals_raw      = api("/operational/list_sales_goals", from_str, to_str) or []
    misses_raw     = api("/operational/list_misses_goals", from_str, to_str) or []
    appts_raw      = api("/appointment/list", from_str, to_str) or []

    # ── Financial ──────────────────────────────────────────────────────────────
    values = summary_raw if isinstance(summary_raw, list) else \
             summary_raw.get("values", []) if isinstance(summary_raw, dict) else []
    month_rev  = defaultdict(float)
    month_exp  = defaultdict(float)
    cat_totals = defaultdict(float)
    for v in values:
        yr  = v.get("Year", 0)
        mo  = v.get("Month", 0)
        key = f"{yr}-{str(mo).zfill(2)}"
        amt = float(v.get("Amount", 0) or 0)
        pt  = v.get("PostType", "")
        cat = v.get("Category", "Outros") or "Outros"
        if pt == "EXPENSES":
            month_exp[key] += amt
            cat_totals[cat] += amt
        elif pt in ("REVENUE", "INCOME"):
            month_rev[key] += amt

    all_months = sorted(set(list(month_rev.keys()) + list(month_exp.keys())))
    fin_months = []
    for m in all_months:
        rev  = month_rev[m]
        exp  = month_exp[m]
        prf  = rev - exp
        fin_months.append({
            "label":   m,
            "revenue": round(rev, 2),
            "expense": round(exp, 2),
            "profit":  round(prf, 2),
            "margin":  round(prf / rev * 100, 1) if rev > 0 else 0
        })

    top_cats   = sorted(cat_totals.items(), key=lambda x: -x[1])[:12]
    cat_labels = [c[0] for c in top_cats]
    cat_vals   = [round(c[1], 2) for c in top_cats]

    # ── Projection ─────────────────────────────────────────────────────────────
    revenues = [m["revenue"] for m in fin_months]
    expenses = [m["expense"] for m in fin_months]
    n = len(revenues)
    rev_s, rev_b = linreg(revenues)
    exp_s, exp_b = linreg(expenses)

    proj_months = []
    if all_months:
        yr, mo = int(all_months[-1][:4]), int(all_months[-1][5:7])
        for _ in range(3):
            mo += 1
            if mo > 12: mo = 1; yr += 1
            proj_months.append(f"{yr}-{str(mo).zfill(2)}")

    proj_rev    = [round(max(0, rev_s*(n+i)+rev_b), 2) for i in range(3)]
    proj_exp    = [round(max(0, exp_s*(n+i)+exp_b), 2) for i in range(3)]
    proj_profit = [round(proj_rev[i]-proj_exp[i], 2) for i in range(3)]
    all_labels_proj = [m["label"] for m in fin_months] + proj_months
    all_rev_hist    = [m["revenue"] for m in fin_months] + [None]*3
    all_exp_hist    = [m["expense"] for m in fin_months] + [None]*3
    proj_rev_line   = [None]*n + proj_rev
    proj_exp_line   = [None]*n + proj_exp

    # ── Break-even ─────────────────────────────────────────────────────────────
    total_rev_all   = sum(revenues)
    fixed_total     = sum(v for k,v in cat_totals.items() if k in FIXED_CATS)
    variable_total  = sum(cat_totals.values()) - fixed_total
    avg_fixed_mo    = fixed_total / n if n else fixed_total
    variable_ratio  = variable_total / total_rev_all if total_rev_all > 0 else 0
    breakeven       = avg_fixed_mo / (1 - variable_ratio) if (1 - variable_ratio) > 0 else 0
    avg_monthly_rev = total_rev_all / n if n else 0
    avg_monthly_exp = sum(expenses) / n if n else 0
    be_coverage     = round(min(100, avg_monthly_rev/breakeven*100) if breakeven > 0 else 100, 1)
    be_margin       = avg_monthly_rev - breakeven

    # ── Conversion ─────────────────────────────────────────────────────────────
    conv         = conversion_raw if isinstance(conversion_raw, dict) else {}
    approved     = conv.get("APPROVED", {}) or {}
    rejected     = conv.get("REJECTED", {}) or {}
    total_appr   = int(approved.get("TotalEstimates", 0) or 0)
    total_rej    = int(rejected.get("TotalEstimates", 0) or 0)
    total_est    = total_appr + total_rej
    conv_rate    = round(total_appr / total_est * 100, 1) if total_est > 0 else 0
    avg_ticket   = float(approved.get("AverageTicket", 0) or 0)
    total_amount = float(approved.get("TotalEstimatesAmount", 0) or 0)

    # ── Specialty ──────────────────────────────────────────────────────────────
    esp_months_raw = expertise_raw if isinstance(expertise_raw, list) else []
    # Collect raw keys first, then normalise: strip + title-case to merge
    # duplicates like "PERIODONTIA" and "Periodontia " (trailing space).
    raw_keys = [k for row in esp_months_raw
                for k in row.keys()
                if k.strip().lower() not in ("month","from","to","year","date","")]
    # Build mapping: normalised_key → canonical display name (first seen)
    norm_map = {}  # raw → normalised
    for k in raw_keys:
        nk = k.strip().title()
        if nk not in {v for v in norm_map.values()}:
            norm_map[k] = nk
        else:
            # map duplicate raw key to existing normalised key
            norm_map[k] = nk
    esp_keys_norm = sorted(set(norm_map.values()))

    esp_totals = defaultdict(float)
    for row in esp_months_raw:
        for raw_k, norm_k in norm_map.items():
            esp_totals[norm_k] += float(row.get(raw_k, 0) or 0)
    top_esp     = sorted(esp_totals.items(), key=lambda x: -x[1])[:10]
    max_esp_val = max((v for _,v in top_esp), default=1)

    # Build per-month data per normalised key
    esp_month_data = {nk: [0.0]*len(esp_months_raw) for nk in esp_keys_norm}
    for mi, row in enumerate(esp_months_raw):
        for raw_k, norm_k in norm_map.items():
            esp_month_data[norm_k][mi] += float(row.get(raw_k, 0) or 0)

    esp_datasets = []
    for i, nk in enumerate(esp_keys_norm):
        c = COLORS[i % len(COLORS)]
        esp_datasets.append({
            "label": nk,
            "data":  [round(v, 2) for v in esp_month_data[nk]],
            "backgroundColor": c+"33", "borderColor": c,
            "fill": False, "tension": .4, "pointRadius": 3
        })
    esp_month_labels = [row.get("month","") or row.get("from","") for row in esp_months_raw]

    # ── Goals ──────────────────────────────────────────────────────────────────
    _EN_TO_PT = {
        "january":"Jan","february":"Fev","march":"Mar","april":"Abr",
        "may":"Mai","june":"Jun","july":"Jul","august":"Ago",
        "september":"Set","october":"Out","november":"Nov","december":"Dez",
    }
    def _month_label(raw):
        """Convert API month string to PT-BR label, e.g. 'September 2026' → 'Set/26'."""
        s = (raw or "").strip()
        for en, pt in _EN_TO_PT.items():
            if s.lower().startswith(en):
                yr = re.search(r"\d{4}", s)
                return f"{pt}/{yr.group()[2:]}" if yr else pt
        # fallback: assume YYYY-MM format
        return s[:7]

    goals_list   = goals_raw if isinstance(goals_raw, list) else []
    goal_labels  = [_month_label(g.get("month", g.get("from",""))) for g in goals_list]
    goal_targets = [float(g.get("Goal", 0) or 0) for g in goals_list]
    goal_actual  = [float(g.get("TotalRevenueAmount", g.get("TotalRevenue",0)) or 0) for g in goals_list]
    goal_pct     = [round(goal_actual[i]/goal_targets[i]*100,1) if goal_targets[i]>0 else 0
                    for i in range(len(goal_labels))]
    avg_goal_pct = sum(goal_pct)/len(goal_pct) if goal_pct else 50

    # ── Misses ─────────────────────────────────────────────────────────────────
    misses_list  = misses_raw if isinstance(misses_raw, list) else []
    miss_labels  = [m.get("month", m.get("from",""))[:7] for m in misses_list]
    miss_vals    = [int(m.get("Misses", 0) or 0) for m in misses_list]
    total_misses = sum(miss_vals)

    # ── Appointments ───────────────────────────────────────────────────────────
    appt_list     = appts_raw if isinstance(appts_raw, list) else []
    appt_by_prof  = defaultdict(int)
    appt_by_cat   = defaultdict(int)
    how_met_d     = defaultdict(int)
    appt_by_month = defaultdict(int)
    for a in appt_list:
        pid  = str(a.get("Dentist_PersonId",""))
        name = prof_map.get(pid, f"Dr(a). {pid[:6]}" if pid else "Não informado")
        appt_by_prof[name] += 1
        cat = a.get("CategoryDescription","Sem categoria") or "Sem categoria"
        appt_by_cat[cat] += 1
        src = a.get("HowDidMeet","") or "Não informado"
        how_met_d[src] += 1
        dt = a.get("Date", a.get("AppointmentDate",""))
        if dt and len(dt) >= 7: appt_by_month[dt[:7]] += 1

    appt_prof_items  = sorted(appt_by_prof.items(),  key=lambda x:-x[1])[:10]
    appt_cat_items   = sorted(appt_by_cat.items(),   key=lambda x:-x[1])[:8]
    how_met_items    = sorted(how_met_d.items(),      key=lambda x:-x[1])[:8]
    appt_month_items = sorted(appt_by_month.items())
    total_appts      = len(appt_list)

    # ── KPIs ───────────────────────────────────────────────────────────────────
    total_rev    = sum(month_rev.values())
    total_exp    = sum(month_exp.values())
    total_profit = total_rev - total_exp
    margin_pct   = round(total_profit / total_rev * 100, 1) if total_rev > 0 else 0
    # noshow_rate: only compute when we have real appointment data.
    # If appts=0 but misses>0 it means the /appointment/list API returned nothing
    # (timeout for long periods) — report None rather than a fake 100%.
    if total_appts > 0:
        noshow_rate = round(total_misses / (total_appts + total_misses) * 100, 1)
    elif total_misses > 0 and total_appts == 0:
        noshow_rate = None   # API didn't return appointment data — show N/D
    else:
        noshow_rate = 0

    mom_rev_pct = mom_exp_pct = 0
    if len(fin_months) >= 2:
        prev, last = fin_months[-2], fin_months[-1]
        if prev["revenue"] > 0:
            mom_rev_pct = round((last["revenue"]-prev["revenue"])/prev["revenue"]*100, 1)
        if prev["expense"] > 0:
            mom_exp_pct = round((last["expense"]-prev["expense"])/prev["expense"]*100, 1)

    # When noshow_rate is None (API returned no appointment data),
    # exclude that component from the health score rather than penalising with 0.
    _noshow_safe = noshow_rate if noshow_rate is not None else 0
    _noshow_score = max(0, 100 - _noshow_safe * 5)
    if noshow_rate is None:
        # Re-weight remaining components to fill the 15% gap
        health_score = round(
            min(100, margin_pct*2)   * 0.41 +
            min(100, conv_rate*1.5)  * 0.29 +
            min(100, avg_goal_pct)   * 0.30
        )
    else:
        health_score = round(
            min(100, margin_pct*2)      * 0.35 +
            min(100, conv_rate*1.5)     * 0.25 +
            min(100, avg_goal_pct)      * 0.25 +
            _noshow_score               * 0.15
        )
    health_color = "#10b981" if health_score>=75 else "#f59e0b" if health_score>=50 else "#ef4444"

    # Compute the correct number of complete months in the period (not len of data rows)
    from_d = date.fromisoformat(from_str)
    to_d   = date.fromisoformat(to_str)
    n_months_real = (to_d.year - from_d.year) * 12 + (to_d.month - from_d.month) + 1

    return {
        "label": label, "from": from_str, "to": to_str, "n_months": n_months_real,
        # KPIs
        "total_rev": round(total_rev,2), "total_exp": round(total_exp,2),
        "total_profit": round(total_profit,2), "margin_pct": margin_pct,
        "total_amount": round(total_amount,2), "total_appr": total_appr,
        "total_rej": total_rej, "total_est": total_est,
        "conv_rate": conv_rate, "avg_ticket": round(avg_ticket,2),
        "total_appts": total_appts, "total_misses": total_misses,
        "noshow_rate": noshow_rate,   # None = API sem dados (período longo)
        "health_score": health_score,
        "health_color": health_color, "mom_rev_pct": mom_rev_pct,
        "mom_exp_pct": mom_exp_pct, "avg_goal_pct": round(avg_goal_pct,1),
        # Break-even
        "breakeven": round(breakeven,2), "avg_fixed_mo": round(avg_fixed_mo,2),
        "avg_monthly_rev": round(avg_monthly_rev,2), "avg_monthly_exp": round(avg_monthly_exp,2),
        "be_coverage": be_coverage, "be_margin": round(be_margin,2),
        # Score bars
        "margin_score": round(min(100,margin_pct*2)),
        "conv_score":   round(min(100,conv_rate*1.5)),
        "goal_score":   round(min(100,avg_goal_pct)),
        "noshow_score": round(max(0, 100 - (noshow_rate or 0) * 5)),
        # Financial charts
        "fin_labels": [m["label"] for m in fin_months],
        "fin_rev":    [m["revenue"] for m in fin_months],
        "fin_exp":    [m["expense"] for m in fin_months],
        "fin_profit": [m["profit"] for m in fin_months],
        "fin_margin": [m["margin"] for m in fin_months],
        # Projection
        "proj_labels": all_labels_proj, "all_rev_hist": all_rev_hist,
        "all_exp_hist": all_exp_hist, "proj_rev_line": proj_rev_line,
        "proj_exp_line": proj_exp_line, "proj_months": proj_months,
        "proj_rev": proj_rev, "proj_exp": proj_exp, "proj_profit": proj_profit,
        # Categories
        "cat_labels": cat_labels, "cat_vals": cat_vals,
        # Specialty
        "esp_month_labels": esp_month_labels, "esp_datasets": esp_datasets,
        "top_esp": [{"name": nm, "val": round(vl,2)} for nm,vl in top_esp],
        "max_esp_val": round(max_esp_val,2), "n_specs": len(esp_keys_norm),
        # Goals
        "goal_labels": goal_labels, "goal_targets": goal_targets,
        "goal_actual": goal_actual, "goal_pct": goal_pct,
        # Misses
        "miss_labels": miss_labels, "miss_vals": miss_vals,
        # Appointments
        "appt_month_labels": [x[0] for x in appt_month_items],
        "appt_month_vals":   [x[1] for x in appt_month_items],
        "appt_prof": [{"name": nm,"cnt": c} for nm,c in appt_prof_items],
        "appt_cat":  [{"name": nm,"cnt": c} for nm,c in appt_cat_items],
        "how_met":   [{"name": nm,"cnt": c} for nm,c in how_met_items],
        "n_profs": len(appt_by_prof),
        "funnel_w": min(100,conv_rate) if total_est>0 else 50,
    }


# ─── RUN ALL PERIODS ──────────────────────────────────────────────────────────

# Period "from" dates — each starts on the 1st of the target month.
# TO_DATE is the last day of the previous complete month (e.g. 2026-08-31).
# MAT: exactly 12 complete months back from the 1st of the current month.
_cur_first = TODAY.replace(day=1)
_mat_y = _cur_first.year - (1 if _cur_first.month == 1 else 0)
_mat_m = (_cur_first.month - 12 - 1) % 12 + 1          # e.g. Sep/25
mat_from = date(_mat_y if _mat_m >= _cur_first.month else _cur_first.year - 1,
                _mat_m, 1)
# Simpler: subtract 12 months directly
_m12 = _cur_first.month - 12
_y12 = _cur_first.year + (_m12 - 1) // 12
_m12 = (_m12 - 1) % 12 + 1
mat_from = date(_y12, _m12, 1)   # e.g. 2025-09-01  (12 complete months to 2026-08-31)

# MQT: exactly 3 complete months back
_m3 = _cur_first.month - 3
_y3 = _cur_first.year + (_m3 - 1) // 12
_m3 = (_m3 - 1) % 12 + 1
mqt_from = date(_y3, _m3, 1)     # e.g. 2026-06-01  (3 complete months to 2026-08-31)

ytd_from = TODAY.replace(month=1, day=1)

print("Calculando MAT (12 meses)...")
mat_data = compute_period("MAT", mat_from.strftime("%Y-%m-%d"), TO_STR)
print("Calculando MQT (3 meses)...")
mqt_data = compute_period("MQT", mqt_from.strftime("%Y-%m-%d"), TO_STR)
print("Calculando YTD (ano atual)...")
ytd_data = compute_period("YTD", ytd_from.strftime("%Y-%m-%d"), TO_STR)

PERIODS = {"mat": mat_data, "mqt": mqt_data, "ytd": ytd_data}
gerado_em = datetime.now().strftime("%d/%m/%Y %H:%M")

# ─── HTML ─────────────────────────────────────────────────────────────────────
html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Dashboard Klinik Odontologia</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{
  --bg:#0a0f1e;--bg2:#111827;--bg3:#1e293b;--bg4:#0f172a;
  --border:#1e3a5f;--text:#e2e8f0;--text2:#94a3b8;--text3:#64748b;
  --blue:#3b82f6;--green:#10b981;--purple:#8b5cf6;--red:#ef4444;
  --amber:#f59e0b;--cyan:#06b6d4;--pink:#ec4899;--indigo:#6366f1;
}}
body{{font-family:'Segoe UI',system-ui,-apple-system,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;font-size:14px}}
header{{background:linear-gradient(135deg,#0f1f3d 0%,#1a3a6e 60%,#0f2a5a 100%);
  padding:14px 28px;display:flex;justify-content:space-between;align-items:center;
  border-bottom:1px solid #1e3a8a44;box-shadow:0 4px 20px #00000055;
  position:sticky;top:0;z-index:100}}
header h1{{font-size:1.3rem;font-weight:700}} header h1 span{{color:#60a5fa}}
.period-badge{{background:#1e3a8a33;border:1px solid #3b82f644;border-radius:20px;padding:4px 12px;font-size:.73rem;color:#93c5fd;display:inline-block;margin-bottom:3px}}
.updated{{font-size:.67rem;color:#475569;text-align:right}}
/* TABS + PERIOD BUTTONS */
.topbar{{display:flex;background:var(--bg2);border-bottom:1px solid var(--border);padding:0 28px;gap:2px;overflow-x:auto;align-items:center;justify-content:space-between}}
.tabs{{display:flex;gap:2px;overflow-x:auto;flex:1}}
.tab{{padding:11px 18px;cursor:pointer;border-bottom:2px solid transparent;color:var(--text3);font-size:.78rem;font-weight:500;letter-spacing:.3px;white-space:nowrap;transition:all .2s;user-select:none}}
.tab:hover{{color:var(--text2);background:#1e293b44}}
.tab.active{{color:var(--blue);border-bottom-color:var(--blue);background:#3b82f611}}
.period-btns{{display:flex;gap:5px;padding:8px 0 8px 16px;flex-shrink:0;border-left:1px solid var(--border);margin-left:8px}}
.pbtn{{padding:5px 13px;border-radius:20px;font-size:.72rem;font-weight:600;cursor:pointer;border:1px solid #334155;background:transparent;color:var(--text3);transition:all .2s;letter-spacing:.5px}}
.pbtn:hover{{border-color:var(--blue);color:var(--text)}}
.pbtn.active{{background:#3b82f622;border-color:var(--blue);color:#60a5fa}}
/* PANELS */
.panel{{display:none;padding:20px 28px;max-width:1800px;margin:0 auto}}
.panel.active{{display:block}}
.stitle{{font-size:.6rem;text-transform:uppercase;letter-spacing:2px;color:var(--text3);margin:20px 0 11px;border-bottom:1px solid #1e293b;padding-bottom:7px;display:flex;align-items:center;gap:8px}}
.stitle::before{{content:'';width:3px;height:12px;border-radius:2px;background:var(--blue);flex-shrink:0}}
/* KPI */
.kpi-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(168px,1fr));gap:11px;margin-bottom:14px}}
.kpi{{background:var(--bg3);border:1px solid #334155;border-radius:12px;padding:16px;position:relative;overflow:hidden;transition:transform .15s}}
.kpi:hover{{transform:translateY(-2px);border-color:#475569}}
.kpi::before{{content:'';position:absolute;top:0;left:0;right:0;height:3px;border-radius:4px 4px 0 0}}
.kpi.blue::before{{background:linear-gradient(90deg,#3b82f6,#93c5fd)}}
.kpi.green::before{{background:linear-gradient(90deg,#10b981,#6ee7b7)}}
.kpi.purple::before{{background:linear-gradient(90deg,#8b5cf6,#c4b5fd)}}
.kpi.red::before{{background:linear-gradient(90deg,#ef4444,#fca5a5)}}
.kpi.amber::before{{background:linear-gradient(90deg,#f59e0b,#fde68a)}}
.kpi.cyan::before{{background:linear-gradient(90deg,#06b6d4,#67e8f9)}}
.kpi.indigo::before{{background:linear-gradient(90deg,#6366f1,#a5b4fc)}}
.kpi label{{font-size:.6rem;text-transform:uppercase;letter-spacing:.8px;color:var(--text3);display:block;margin-bottom:7px}}
.kpi .val{{font-size:1.35rem;font-weight:700;line-height:1}}
.kpi.blue .val{{color:#60a5fa}}.kpi.green .val{{color:#34d399}}.kpi.purple .val{{color:#a78bfa}}
.kpi.red .val{{color:#f87171}}.kpi.amber .val{{color:#fbbf24}}.kpi.cyan .val{{color:#22d3ee}}.kpi.indigo .val{{color:#818cf8}}
.kpi .sub{{font-size:.66rem;color:var(--text3);margin-top:5px;display:flex;align-items:center;gap:4px}}
.badge{{display:inline-block;padding:1px 7px;border-radius:10px;font-size:.62rem;font-weight:600}}
.badge.up{{background:#10b98122;color:#34d399}}.badge.dn{{background:#ef444422;color:#f87171}}.badge.fl{{background:#f59e0b22;color:#fbbf24}}
/* LAYOUTS */
.g2{{display:grid;grid-template-columns:3fr 2fr;gap:13px;margin-bottom:13px}}
.g2e{{display:grid;grid-template-columns:1fr 1fr;gap:13px;margin-bottom:13px}}
.g3{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:13px;margin-bottom:13px}}
.g12{{display:grid;grid-template-columns:1fr 2fr;gap:13px;margin-bottom:13px}}
/* CARDS */
.card{{background:var(--bg3);border:1px solid #334155;border-radius:12px;padding:17px}}
.card h3{{font-size:.66rem;text-transform:uppercase;letter-spacing:.8px;color:var(--text3);margin-bottom:13px;display:flex;align-items:center;gap:6px}}
.card canvas{{max-height:270px}}
/* HEALTH */
.health-num{{font-size:3.8rem;font-weight:800;line-height:1;text-align:center}}
.health-label{{font-size:.68rem;color:var(--text3);text-transform:uppercase;letter-spacing:1px;text-align:center;margin-top:3px}}
/* PROGRESS */
.prog{{background:#0f172a;border-radius:4px;height:7px;overflow:hidden;margin-top:5px}}
.prog-fill{{height:100%;border-radius:4px;transition:width .4s}}
/* TABLES */
.dtable{{width:100%;border-collapse:collapse;font-size:.76rem}}
.dtable th{{color:var(--text3);font-size:.6rem;text-transform:uppercase;letter-spacing:.6px;padding:7px 9px;border-bottom:1px solid #334155;text-align:left;font-weight:500}}
.dtable td{{padding:7px 9px;border-bottom:1px solid #1e293b;color:var(--text)}}
.dtable tr:hover td{{background:#1e293b88}}
.dtable .num{{text-align:right;font-variant-numeric:tabular-nums}}
.mini-bar{{background:#0f172a;border-radius:3px;height:5px;overflow:hidden}}
.mini-bar-fill{{height:100%;border-radius:3px}}
.tag{{display:inline-block;padding:1px 7px;border-radius:8px;font-size:.64rem}}
.tag.good{{background:#10b98122;color:#34d399}}.tag.warn{{background:#f59e0b22;color:#fbbf24}}.tag.bad{{background:#ef444422;color:#f87171}}
.info-row{{display:flex;justify-content:space-between;align-items:center;padding:9px 13px;background:#0f172a;border-radius:8px;border-left:3px solid;margin-bottom:8px}}
footer{{text-align:center;padding:14px;color:#334155;font-size:.68rem;border-top:1px solid #1e293b;margin-top:8px}}
@media(max-width:1100px){{.g2{{grid-template-columns:1fr}}.g3{{grid-template-columns:1fr 1fr}}}}
@media(max-width:760px){{.g2,.g2e,.g3,.g12{{grid-template-columns:1fr}}.panel{{padding:13px}}.topbar{{flex-direction:column;align-items:flex-start}}.period-btns{{border-left:none;padding-left:0;border-top:1px solid var(--border);width:100%;padding-top:8px}}.kpi-grid{{grid-template-columns:repeat(2,1fr)}}}}
</style>
</head>
<body>

<header>
  <div>
    <h1>🦷 <span>Klinik</span> Odontologia</h1>
    <small style="color:#475569;font-size:.7rem">Dashboard Executivo v2.1</small>
  </div>
  <div>
    <div class="period-badge" id="period-badge">📅 —</div>
    <div class="updated">Atualizado em {gerado_em}</div>
  </div>
</header>

<div class="topbar">
  <div class="tabs">
    <div class="tab active"  onclick="sw(0)">⚡ Executivo</div>
    <div class="tab"         onclick="sw(1)">💰 Financeiro</div>
    <div class="tab"         onclick="sw(2)">🦷 Clínico</div>
    <div class="tab"         onclick="sw(3)">📊 Comercial</div>
    <div class="tab"         onclick="sw(4)">📅 Operacional</div>
  </div>
  <div class="period-btns">
    <button class="pbtn active" data-p="mat" onclick="switchPeriod('mat')">MAT</button>
    <button class="pbtn"        data-p="mqt" onclick="switchPeriod('mqt')">MQT</button>
    <button class="pbtn"        data-p="ytd" onclick="switchPeriod('ytd')">YTD</button>
  </div>
</div>

<!-- TAB 0 — EXECUTIVO -->
<div class="panel active" id="p0">
  <div class="stitle">Resumo Executivo</div>
  <div class="kpi-grid">
    <div class="kpi green"><label>Receita Total</label><div class="val" id="kpi-rev">—</div><div class="sub" id="kpi-rev-sub"></div></div>
    <div class="kpi red"><label>Despesas Totais</label><div class="val" id="kpi-exp">—</div><div class="sub" id="kpi-exp-sub"></div></div>
    <div class="kpi green" id="kpi-profit-card"><label>Resultado Líquido</label><div class="val" id="kpi-profit">—</div><div class="sub" id="kpi-profit-sub"></div></div>
    <div class="kpi blue"><label>Produção Aprovada</label><div class="val" id="kpi-prod">—</div><div class="sub" id="kpi-prod-sub"></div></div>
    <div class="kpi purple"><label>Taxa de Conversão</label><div class="val" id="kpi-conv">—</div><div class="sub" id="kpi-conv-sub"></div></div>
    <div class="kpi amber"><label>Ticket Médio</label><div class="val" id="kpi-ticket">—</div></div>
    <div class="kpi cyan"><label>Agendamentos</label><div class="val" id="kpi-appts">—</div></div>
    <div class="kpi amber" id="kpi-noshow-card"><label>Taxa de No-show</label><div class="val" id="kpi-noshow">—</div><div class="sub" id="kpi-noshow-sub"></div></div>
  </div>

  <div class="g12">
    <div class="card" style="display:flex;flex-direction:column;gap:12px">
      <h3>🩺 Saúde do Negócio</h3>
      <div style="text-align:center;padding:10px 0">
        <div class="health-num" id="health-num">—</div>
        <div class="health-label">/ 100</div>
        <div style="margin-top:8px;font-size:.78rem;font-weight:700;letter-spacing:1px" id="health-label-txt">—</div>
      </div>
      <div style="display:flex;flex-direction:column;gap:9px;font-size:.71rem">
        <div>
          <div style="display:flex;justify-content:space-between;color:var(--text3);margin-bottom:3px"><span>Margem líquida</span><span id="score-margin-txt" style="color:var(--text)">—</span></div>
          <div class="prog"><div class="prog-fill" id="score-margin-bar" style="width:0%;background:var(--green)"></div></div>
        </div>
        <div>
          <div style="display:flex;justify-content:space-between;color:var(--text3);margin-bottom:3px"><span>Conversão comercial</span><span id="score-conv-txt" style="color:var(--text)">—</span></div>
          <div class="prog"><div class="prog-fill" id="score-conv-bar" style="width:0%;background:var(--purple)"></div></div>
        </div>
        <div>
          <div style="display:flex;justify-content:space-between;color:var(--text3);margin-bottom:3px"><span>Atingimento de metas</span><span id="score-goal-txt" style="color:var(--text)">—</span></div>
          <div class="prog"><div class="prog-fill" id="score-goal-bar" style="width:0%;background:var(--amber)"></div></div>
        </div>
        <div>
          <div style="display:flex;justify-content:space-between;color:var(--text3);margin-bottom:3px"><span>Comparecimento</span><span id="score-noshow-txt" style="color:var(--text)">—</span></div>
          <div class="prog"><div class="prog-fill" id="score-noshow-bar" style="width:0%;background:var(--cyan)"></div></div>
        </div>
      </div>
    </div>
    <div class="card">
      <h3>📈 Tendência &amp; Projeção de Receita</h3>
      <canvas id="trendChart"></canvas>
    </div>
  </div>

  <div class="g2e">
    <div class="card">
      <h3>⚖️ Ponto de Equilíbrio Mensal</h3>
      <div id="be-content"></div>
    </div>
    <div class="card">
      <h3>🔮 Projeção — Próximos 3 Meses</h3>
      <div id="proj-content" style="display:flex;flex-direction:column;gap:10px;padding:4px 0"></div>
    </div>
  </div>
</div>

<!-- TAB 1 — FINANCEIRO -->
<div class="panel" id="p1">
  <div class="stitle">Performance Financeira</div>
  <div class="kpi-grid">
    <div class="kpi green"><label>Receita Período</label><div class="val" id="f-rev">—</div><div class="sub" id="f-rev-sub"></div></div>
    <div class="kpi red"><label>Despesas Período</label><div class="val" id="f-exp">—</div></div>
    <div class="kpi green" id="f-profit-card"><label>Lucro Líquido</label><div class="val" id="f-profit">—</div><div class="sub" id="f-margin-sub"></div></div>
    <div class="kpi blue"><label>Receita Média/Mês</label><div class="val" id="f-avg-rev">—</div></div>
    <div class="kpi amber"><label>Despesa Média/Mês</label><div class="val" id="f-avg-exp">—</div></div>
    <div class="kpi cyan"><label>Break-even Mensal</label><div class="val" id="f-be">—</div></div>
  </div>
  <div class="stitle">Demonstrativo de Resultado</div>
  <div class="g2">
    <div class="card"><h3>Receita / Despesa / Resultado por Mês</h3><canvas id="finChart"></canvas></div>
    <div class="card"><h3>Margem Líquida por Mês (%)</h3><canvas id="marginChart"></canvas></div>
  </div>
  <div class="stitle">Estrutura de Custos</div>
  <div class="g2e">
    <div class="card"><h3>Despesas por Categoria</h3><canvas id="catChart"></canvas></div>
    <div class="card">
      <h3>Ranking de Despesas</h3>
      <table class="dtable"><thead><tr><th>Categoria</th><th class="num">Total</th><th class="num">%</th><th style="width:100px">Barra</th></tr></thead>
      <tbody id="exp-rows"></tbody></table>
    </div>
  </div>
</div>

<!-- TAB 2 — CLÍNICO -->
<div class="panel" id="p2">
  <div class="stitle">Produção Clínica</div>
  <div class="kpi-grid">
    <div class="kpi blue"><label>Produção Aprovada</label><div class="val" id="c-prod">—</div><div class="sub" id="c-prod-sub"></div></div>
    <div class="kpi green"><label>Ticket Médio</label><div class="val" id="c-ticket">—</div></div>
    <div class="kpi purple"><label>Especialidades Ativas</label><div class="val" id="c-specs">—</div></div>
    <div class="kpi amber"><label>Total Agendamentos</label><div class="val" id="c-appts">—</div></div>
  </div>
  <div class="stitle">Receita por Especialidade</div>
  <div class="g2">
    <div class="card"><h3>Evolução por Especialidade (mês)</h3><canvas id="espChart"></canvas></div>
    <div class="card">
      <h3>Ranking de Especialidades</h3>
      <table class="dtable"><thead><tr><th>Especialidade</th><th class="num">Total</th><th style="width:100px">Share</th></tr></thead>
      <tbody id="esp-rows"></tbody></table>
    </div>
  </div>
  <div class="stitle">Performance por Profissional</div>
  <div class="g2e">
    <div class="card"><h3>Agendamentos por Profissional</h3><canvas id="apptChart"></canvas></div>
    <div class="card"><h3>Mix de Especialidades (agendamentos)</h3><canvas id="catApptChart"></canvas></div>
  </div>
</div>

<!-- TAB 3 — COMERCIAL -->
<div class="panel" id="p3">
  <div class="stitle">Funil Comercial</div>
  <div class="kpi-grid">
    <div class="kpi blue"><label>Orçamentos Gerados</label><div class="val" id="cm-est">—</div></div>
    <div class="kpi green"><label>Aprovados</label><div class="val" id="cm-appr">—</div></div>
    <div class="kpi red"><label>Não Aprovados</label><div class="val" id="cm-rej">—</div></div>
    <div class="kpi purple"><label>Conversão</label><div class="val" id="cm-conv">—</div></div>
    <div class="kpi amber"><label>Ticket Médio</label><div class="val" id="cm-ticket">—</div></div>
    <div class="kpi green"><label>Receita Aprovada</label><div class="val" id="cm-amount">—</div></div>
  </div>
  <div class="g2e">
    <div class="card">
      <h3>🔻 Funil de Conversão</h3>
      <div id="funnel-content" style="display:flex;flex-direction:column;gap:10px;padding:12px 0"></div>
    </div>
    <div class="card"><h3>Aprovados vs Não Aprovados</h3><canvas id="convChart"></canvas></div>
  </div>
  <div class="stitle">Meta vs Realizado</div>
  <div class="g2">
    <div class="card"><h3>Meta vs. Realizado por Mês</h3><canvas id="goalChart"></canvas></div>
    <div class="card">
      <h3>Atingimento por Mês</h3>
      <table class="dtable"><thead><tr><th>Mês</th><th class="num">Meta</th><th class="num">Realizado</th><th class="num">%</th><th>Status</th></tr></thead>
      <tbody id="goal-rows"></tbody></table>
    </div>
  </div>
  <div class="stitle">Captação de Pacientes</div>
  <div class="card" style="margin-bottom:14px">
    <h3>Como nos Encontrou</h3><canvas id="howMetChart" style="max-height:220px"></canvas>
  </div>
</div>

<!-- TAB 4 — OPERACIONAL -->
<div class="panel" id="p4">
  <div class="stitle">Visão Operacional</div>
  <div class="kpi-grid">
    <div class="kpi cyan"><label>Total Agendamentos</label><div class="val" id="op-appts">—</div></div>
    <div class="kpi red"><label>Total Faltas</label><div class="val" id="op-miss">—</div></div>
    <div class="kpi amber" id="op-noshow-card"><label>Taxa de No-show</label><div class="val" id="op-noshow">—</div></div>
    <div class="kpi indigo"><label>Dentistas Ativos</label><div class="val" id="op-profs">—</div></div>
  </div>
  <div class="g2e">
    <div class="card"><h3>Volume de Agendamentos por Mês</h3><canvas id="apptMonthChart"></canvas></div>
    <div class="card"><h3>Faltas por Mês</h3><canvas id="missChart"></canvas></div>
  </div>
  <div class="stitle">Performance por Dentista</div>
  <div class="g2e">
    <div class="card">
      <h3>Agendamentos por Dentista</h3>
      <table class="dtable"><thead><tr><th>Dentista</th><th class="num">Qtd</th><th style="width:100px">Volume</th></tr></thead>
      <tbody id="appt-rows"></tbody></table>
    </div>
    <div class="card"><h3>Canal de Captação</h3><canvas id="howMetChart2"></canvas></div>
  </div>
</div>

<footer>Klinik Odontologia — Dashboard Executivo v2.1 — Dados via Clinicorp API — {gerado_em}</footer>

<script>
const PERIODS = {J(PERIODS)};
const COLORS  = {J(COLORS)};

// ── Tab switching ─────────────────────────────────────────────────────────────
function sw(n){{
  document.querySelectorAll('.tab').forEach((t,i)=>t.classList.toggle('active',i===n));
  document.querySelectorAll('.panel').forEach((p,i)=>p.classList.toggle('active',i===n));
}}

// ── Formatters ────────────────────────────────────────────────────────────────
function fmt(v){{
  if(v==null||isNaN(v)) return 'R$ 0,00';
  return 'R$ '+Number(v).toLocaleString('pt-BR',{{minimumFractionDigits:2,maximumFractionDigits:2}});
}}
function fmtk(v){{
  if(v==null||isNaN(v)) return 'R$ 0';
  v=Number(v);
  if(v>=1e6) return 'R$ '+(v/1e6).toFixed(1)+'M';
  if(v>=1e3) return 'R$ '+(v/1e3).toFixed(1)+'K';
  return 'R$ '+Math.round(v);
}}
function arr(p){{return p>2?'↑':p<-2?'↓':'→';}}
function badgeCls(p){{return p>=0?'up':'dn';}}

// ── Text ──────────────────────────────────────────────────────────────────────
function txt(id,val){{const e=document.getElementById(id);if(e)e.textContent=val;}}
function html(id,val){{const e=document.getElementById(id);if(e)e.innerHTML=val;}}
function style(id,prop,val){{const e=document.getElementById(id);if(e)e.style[prop]=val;}}

// ── Chart instances ───────────────────────────────────────────────────────────
let trendChart,finChart,marginChart,catChart,espChart,apptChart,catApptChart,
    convChart,goalChart,howMetChart,apptMonthChart,missChart,howMetChart2;

const C='#94a3b8',G1='#1e293b',G2='#334155';
const scaleR={{ticks:{{color:'#64748b',font:{{size:10}},callback:v=>'R$'+v.toLocaleString('pt-BR')}},grid:{{color:G2}}}};
const scaleN={{ticks:{{color:'#64748b',font:{{size:10}}}},grid:{{color:G2}}}};
const scaleP={{ticks:{{color:'#64748b',font:{{size:10}},callback:v=>v+'%'}},grid:{{color:G2}}}};
const scaleX={{ticks:{{color:'#64748b',font:{{size:10}}}},grid:{{color:G1}}}};
const leg={{labels:{{color:C,boxWidth:11,font:{{size:10}}}}}};
const legR={{position:'right',labels:{{color:C,boxWidth:10,font:{{size:10}}}}}};

function initCharts(){{
  const d=PERIODS.mat;
  trendChart=new Chart(document.getElementById('trendChart'),{{type:'line',
    data:{{labels:d.proj_labels,datasets:[
      {{label:'Receita',data:d.all_rev_hist,borderColor:'#10b981',backgroundColor:'#10b98122',fill:true,tension:.4,pointRadius:3,spanGaps:false}},
      {{label:'Despesa',data:d.all_exp_hist,borderColor:'#ef4444',backgroundColor:'#ef444422',fill:false,tension:.4,pointRadius:3,spanGaps:false}},
      {{label:'Proj. Receita',data:d.proj_rev_line,borderColor:'#10b981',borderDash:[7,3],backgroundColor:'transparent',tension:.4,pointRadius:5,pointStyle:'triangle',spanGaps:false}},
      {{label:'Proj. Despesa',data:d.proj_exp_line,borderColor:'#ef4444',borderDash:[7,3],backgroundColor:'transparent',tension:.4,pointRadius:5,pointStyle:'triangle',spanGaps:false}},
    ]}},options:{{responsive:true,maintainAspectRatio:true,interaction:{{mode:'index',intersect:false}},plugins:{{legend:leg}},scales:{{x:scaleX,y:scaleR}}}}
  }});
  finChart=new Chart(document.getElementById('finChart'),{{type:'bar',
    data:{{labels:d.fin_labels,datasets:[
      {{label:'Receita',data:d.fin_rev,backgroundColor:'#10b98133',borderColor:'#10b981',borderWidth:2,borderRadius:3}},
      {{label:'Despesa',data:d.fin_exp,backgroundColor:'#ef444433',borderColor:'#ef4444',borderWidth:2,borderRadius:3}},
      {{label:'Resultado',data:d.fin_profit,type:'line',borderColor:'#6366f1',backgroundColor:'#6366f122',fill:true,tension:.4,yAxisID:'y'}},
    ]}},options:{{responsive:true,maintainAspectRatio:true,interaction:{{mode:'index',intersect:false}},plugins:{{legend:leg}},scales:{{x:scaleX,y:scaleR}}}}
  }});
  marginChart=new Chart(document.getElementById('marginChart'),{{type:'line',
    data:{{labels:d.fin_labels,datasets:[
      {{label:'Margem %',data:d.fin_margin,borderColor:'#f59e0b',backgroundColor:'#f59e0b22',fill:true,tension:.4,pointRadius:4}},
    ]}},options:{{responsive:true,maintainAspectRatio:true,plugins:{{legend:leg}},scales:{{x:scaleX,y:scaleP}}}}
  }});
  catChart=new Chart(document.getElementById('catChart'),{{type:'bar',
    data:{{labels:d.cat_labels,datasets:[{{label:'R$',data:d.cat_vals,
      backgroundColor:COLORS.slice(0,d.cat_labels.length).map(c=>c+'99'),
      borderColor:COLORS.slice(0,d.cat_labels.length),borderWidth:2}}]}},
    options:{{responsive:true,maintainAspectRatio:true,indexAxis:'y',interaction:{{mode:'index',intersect:false}},plugins:{{legend:{{display:false}}}},
      scales:{{x:{{ticks:{{color:'#64748b',callback:v=>'R$'+v.toLocaleString('pt-BR')}},grid:{{color:G2}}}},y:{{ticks:{{color:'#94a3b8',font:{{size:10}}}},grid:{{color:G1}}}}}}}
    }}
  }});
  espChart=new Chart(document.getElementById('espChart'),{{type:'line',
    data:{{labels:d.esp_month_labels,datasets:d.esp_datasets}},
    options:{{responsive:true,maintainAspectRatio:true,interaction:{{mode:'index',intersect:false}},plugins:{{legend:leg}},scales:{{x:scaleX,y:scaleR}}}}
  }});
  apptChart=new Chart(document.getElementById('apptChart'),{{type:'bar',
    data:{{labels:d.appt_prof.map(x=>x.name),datasets:[{{label:'Agendamentos',data:d.appt_prof.map(x=>x.cnt),backgroundColor:'#8b5cf655',borderColor:'#8b5cf6',borderWidth:2,borderRadius:3}}]}},
    options:{{responsive:true,maintainAspectRatio:true,indexAxis:'y',interaction:{{mode:'index',intersect:false}},plugins:{{legend:{{display:false}}}},scales:{{x:scaleN,y:{{ticks:{{color:'#64748b',font:{{size:10}}}},grid:{{color:G1}}}}}}}}
  }});
  catApptChart=new Chart(document.getElementById('catApptChart'),{{type:'doughnut',
    data:{{labels:d.appt_cat.map(x=>x.name),datasets:[{{data:d.appt_cat.map(x=>x.cnt),
      backgroundColor:COLORS.slice(0,d.appt_cat.length).map(c=>c+'99'),borderWidth:1,hoverOffset:6}}]}},
    options:{{responsive:true,plugins:{{legend:legR}}}}
  }});
  convChart=new Chart(document.getElementById('convChart'),{{type:'doughnut',
    data:{{labels:['Aprovados','Não Aprovados'],datasets:[{{data:[d.total_appr,d.total_rej],
      backgroundColor:['#10b98199','#ef444455'],borderColor:['#10b981','#ef4444'],borderWidth:2,hoverOffset:8}}]}},
    options:{{responsive:true,plugins:{{legend:{{position:'right',labels:{{color:C,boxWidth:11,font:{{size:11}}}}}}}}}}
  }});
  goalChart=new Chart(document.getElementById('goalChart'),{{type:'bar',
    data:{{labels:d.goal_labels,datasets:[
      {{label:'Meta',data:d.goal_targets,backgroundColor:'#3b82f622',borderColor:'#3b82f6',borderWidth:2,borderRadius:3}},
      {{label:'Realizado',data:d.goal_actual,backgroundColor:'#10b98155',borderColor:'#10b981',borderWidth:2,borderRadius:3}},
    ]}},options:{{responsive:true,maintainAspectRatio:true,plugins:{{legend:leg}},scales:{{x:scaleX,y:scaleR}}}}
  }});
  howMetChart=new Chart(document.getElementById('howMetChart'),{{type:'bar',
    data:{{labels:d.how_met.map(x=>x.name),datasets:[{{label:'Pacientes',data:d.how_met.map(x=>x.cnt),
      backgroundColor:COLORS.slice(0,d.how_met.length).map(c=>c+'55'),
      borderColor:COLORS.slice(0,d.how_met.length),borderWidth:2,borderRadius:3}}]}},
    options:{{responsive:true,maintainAspectRatio:true,indexAxis:'y',plugins:{{legend:{{display:false}}}},scales:{{x:scaleN,y:{{ticks:{{color:'#64748b',font:{{size:10}}}},grid:{{color:G1}}}}}}}}
  }});
  apptMonthChart=new Chart(document.getElementById('apptMonthChart'),{{type:'bar',
    data:{{labels:d.appt_month_labels,datasets:[{{label:'Agendamentos',data:d.appt_month_vals,backgroundColor:'#06b6d455',borderColor:'#06b6d4',borderWidth:2,borderRadius:3}}]}},
    options:{{responsive:true,maintainAspectRatio:true,plugins:{{legend:{{display:false}}}},scales:{{x:scaleX,y:scaleN}}}}
  }});
  missChart=new Chart(document.getElementById('missChart'),{{type:'bar',
    data:{{labels:d.miss_labels,datasets:[{{label:'Faltas',data:d.miss_vals,backgroundColor:'#f59e0b55',borderColor:'#f59e0b',borderWidth:2,borderRadius:3}}]}},
    options:{{responsive:true,maintainAspectRatio:true,plugins:{{legend:{{display:false}}}},scales:{{x:scaleX,y:scaleN}}}}
  }});
  howMetChart2=new Chart(document.getElementById('howMetChart2'),{{type:'doughnut',
    data:{{labels:d.how_met.map(x=>x.name),datasets:[{{data:d.how_met.map(x=>x.cnt),
      backgroundColor:COLORS.slice(0,d.how_met.length).map(c=>c+'99'),borderWidth:1,hoverOffset:6}}]}},
    options:{{responsive:true,plugins:{{legend:legR}}}}
  }});
}}

// ── Table builders ────────────────────────────────────────────────────────────
function buildExpRows(d){{
  const totalExp=d.total_exp;
  const maxVal=d.cat_vals[0]||1;
  return d.cat_labels.map((lb,i)=>{{
    const v=d.cat_vals[i], pct=totalExp>0?((v/totalExp)*100).toFixed(1):0;
    const bw=Math.round(v/maxVal*100);
    const c=COLORS[i%COLORS.length];
    return `<tr><td><span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:${{c}};margin-right:6px"></span>${{lb}}</td>
      <td class="num">${{fmt(v)}}</td><td class="num">${{pct}}%</td>
      <td class="bar-cell"><div class="mini-bar"><div class="mini-bar-fill" style="width:${{bw}}%;background:${{c}}"></div></div></td></tr>`;
  }}).join('');
}}

function buildEspRows(d){{
  const maxVal=d.max_esp_val||1;
  return d.top_esp.map((e,i)=>{{
    const bw=Math.round(e.val/maxVal*100);
    const c=COLORS[i%COLORS.length];
    return `<tr><td><span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:${{c}};margin-right:6px"></span>${{e.name}}</td>
      <td class="num">${{fmt(e.val)}}</td>
      <td class="bar-cell"><div class="mini-bar"><div class="mini-bar-fill" style="width:${{bw}}%;background:${{c}}"></div></div></td></tr>`;
  }}).join('');
}}

function buildGoalRows(d){{
  return d.goal_labels.map((lb,i)=>{{
    const pct=d.goal_pct[i];
    const [cls,lbl]=pct>=100?['good','✓ Atingida']:pct>=75?['warn','~ Parcial']:['bad','✗ Abaixo'];
    return `<tr><td>${{lb}}</td><td class="num">${{fmtk(d.goal_targets[i])}}</td>
      <td class="num">${{fmtk(d.goal_actual[i])}}</td><td class="num">${{pct}}%</td>
      <td><span class="tag ${{cls}}">${{lbl}}</span></td></tr>`;
  }}).join('');
}}

function buildApptRows(d){{
  const maxCnt=d.appt_prof[0]?d.appt_prof[0].cnt:1;
  return d.appt_prof.map((p,i)=>{{
    const bw=Math.round(p.cnt/maxCnt*100);
    const c=COLORS[i%COLORS.length];
    return `<tr><td>${{p.name}}</td><td class="num">${{p.cnt}}</td>
      <td class="bar-cell"><div class="mini-bar"><div class="mini-bar-fill" style="width:${{bw}}%;background:${{c}}"></div></div></td></tr>`;
  }}).join('');
}}

function buildBeContent(d){{
  const beCol=d.avg_monthly_rev>d.breakeven?'var(--green)':'var(--amber)';
  const beSign=d.be_margin>=0?'+':'';
  return `
    <div class="info-row" style="border-color:var(--amber)">
      <span style="font-size:.73rem;color:var(--text3)">Break-even mensal</span>
      <span style="font-weight:700;color:var(--amber);font-size:1.05rem">${{fmtk(d.breakeven)}}</span>
    </div>
    <div class="info-row" style="border-color:#ef4444">
      <span style="font-size:.73rem;color:var(--text3)">Custos fixos / mês</span>
      <span style="font-weight:600;color:var(--red)">${{fmtk(d.avg_fixed_mo)}}</span>
    </div>
    <div class="info-row" style="border-color:var(--blue)">
      <span style="font-size:.73rem;color:var(--text3)">Receita média / mês</span>
      <span style="font-weight:600;color:var(--blue)">${{fmtk(d.avg_monthly_rev)}}</span>
    </div>
    <div class="info-row" style="border-color:${{beCol}}">
      <span style="font-size:.73rem;color:var(--text3)">Margem acima do BE</span>
      <span style="font-weight:700;color:${{beCol}}">${{beSign}}${{fmtk(d.be_margin)}}</span>
    </div>
    <div style="margin-top:6px;font-size:.7rem">
      <div style="display:flex;justify-content:space-between;color:var(--text3);margin-bottom:4px">
        <span>Cobertura do break-even</span><span style="color:var(--text)">${{d.be_coverage}}%</span>
      </div>
      <div class="prog" style="height:10px"><div class="prog-fill" style="width:${{d.be_coverage}}%;background:${{beCol}}"></div></div>
    </div>`;
}}

function buildProjContent(d){{
  return d.proj_months.slice(0,3).map((m,i)=>{{
    const col=d.proj_profit[i]>=0?'var(--green)':'var(--red)';
    return `<div style="background:#1e293b;border-radius:10px;padding:14px 16px;border-left:3px solid ${{col}}">
      <div style="font-size:.72rem;color:var(--text3);margin-bottom:8px;font-weight:600">${{m}}</div>
      <div style="display:flex;justify-content:space-between;gap:8px">
        <div style="text-align:center">
          <div style="font-size:.6rem;color:var(--text3)">Receita</div>
          <div style="font-weight:700;color:var(--green);font-size:.9rem">${{fmtk(d.proj_rev[i])}}</div>
        </div>
        <div style="text-align:center">
          <div style="font-size:.6rem;color:var(--text3)">Despesa</div>
          <div style="font-weight:700;color:var(--red);font-size:.9rem">${{fmtk(d.proj_exp[i])}}</div>
        </div>
        <div style="text-align:center">
          <div style="font-size:.6rem;color:var(--text3)">Resultado</div>
          <div style="font-weight:700;font-size:.9rem;color:${{col}}">${{fmtk(d.proj_profit[i])}}</div>
        </div>
      </div>
    </div>`;
  }}).join('');
}}

function buildFunnelContent(d){{
  const fw=Math.min(100,d.funnel_w);
  return `
    <div>
      <div style="font-size:.67rem;color:var(--text3);margin-bottom:5px">ORÇAMENTOS GERADOS</div>
      <div style="background:#3b82f633;border:1px solid #3b82f666;border-radius:8px;padding:10px 14px;display:flex;justify-content:space-between;align-items:center">
        <span style="color:#60a5fa;font-weight:700">${{d.total_est.toLocaleString('pt-BR')}}</span>
        <span style="color:var(--text3);font-size:.7rem">100%</span>
      </div>
    </div>
    <div style="text-align:center;font-size:.7rem;color:var(--text3)">▼ taxa de conversão: ${{d.conv_rate}}%</div>
    <div>
      <div style="font-size:.67rem;color:var(--text3);margin-bottom:5px">APROVADOS</div>
      <div style="background:#10b98133;border:1px solid #10b98166;border-radius:8px;padding:10px 14px;display:flex;justify-content:space-between;align-items:center;width:${{fw}}%;min-width:120px">
        <span style="color:#34d399;font-weight:700">${{d.total_appr.toLocaleString('pt-BR')}}</span>
        <span style="color:var(--text3);font-size:.7rem">${{d.conv_rate}}%</span>
      </div>
    </div>
    <div style="text-align:center;font-size:.7rem;color:var(--text3)">× ticket médio: ${{fmt(d.avg_ticket)}}</div>
    <div>
      <div style="font-size:.67rem;color:var(--text3);margin-bottom:5px">RECEITA GERADA</div>
      <div style="background:#8b5cf633;border:1px solid #8b5cf666;border-radius:8px;padding:10px 14px;display:flex;justify-content:space-between;align-items:center;width:${{fw}}%;min-width:150px">
        <span style="color:#a78bfa;font-weight:700">${{fmt(d.total_amount)}}</span>
      </div>
    </div>`;
}}

// ── Chart updater ─────────────────────────────────────────────────────────────
function updateCharts(d){{
  // Trend
  trendChart.data.labels=d.proj_labels;
  trendChart.data.datasets[0].data=d.all_rev_hist;
  trendChart.data.datasets[1].data=d.all_exp_hist;
  trendChart.data.datasets[2].data=d.proj_rev_line;
  trendChart.data.datasets[3].data=d.proj_exp_line;
  trendChart.update();
  // Financial P&L
  finChart.data.labels=d.fin_labels;
  finChart.data.datasets[0].data=d.fin_rev;
  finChart.data.datasets[1].data=d.fin_exp;
  finChart.data.datasets[2].data=d.fin_profit;
  finChart.update();
  // Margin
  marginChart.data.labels=d.fin_labels;
  marginChart.data.datasets[0].data=d.fin_margin;
  marginChart.update();
  // Categories
  catChart.data.labels=d.cat_labels;
  catChart.data.datasets[0].data=d.cat_vals;
  catChart.data.datasets[0].backgroundColor=COLORS.slice(0,d.cat_labels.length).map(c=>c+'99');
  catChart.data.datasets[0].borderColor=COLORS.slice(0,d.cat_labels.length);
  catChart.update();
  // Specialty
  espChart.data.labels=d.esp_month_labels;
  espChart.data.datasets=d.esp_datasets;
  espChart.update();
  // Appt by prof
  apptChart.data.labels=d.appt_prof.map(x=>x.name);
  apptChart.data.datasets[0].data=d.appt_prof.map(x=>x.cnt);
  apptChart.update();
  // Appt by cat doughnut
  catApptChart.data.labels=d.appt_cat.map(x=>x.name);
  catApptChart.data.datasets[0].data=d.appt_cat.map(x=>x.cnt);
  catApptChart.data.datasets[0].backgroundColor=COLORS.slice(0,d.appt_cat.length).map(c=>c+'99');
  catApptChart.update();
  // Conversion doughnut
  convChart.data.datasets[0].data=[d.total_appr,d.total_rej];
  convChart.update();
  // Goals
  goalChart.data.labels=d.goal_labels;
  goalChart.data.datasets[0].data=d.goal_targets;
  goalChart.data.datasets[1].data=d.goal_actual;
  goalChart.update();
  // How met bar
  howMetChart.data.labels=d.how_met.map(x=>x.name);
  howMetChart.data.datasets[0].data=d.how_met.map(x=>x.cnt);
  howMetChart.data.datasets[0].backgroundColor=COLORS.slice(0,d.how_met.length).map(c=>c+'55');
  howMetChart.data.datasets[0].borderColor=COLORS.slice(0,d.how_met.length);
  howMetChart.update();
  // Appt by month
  apptMonthChart.data.labels=d.appt_month_labels;
  apptMonthChart.data.datasets[0].data=d.appt_month_vals;
  apptMonthChart.update();
  // Miss
  missChart.data.labels=d.miss_labels;
  missChart.data.datasets[0].data=d.miss_vals;
  missChart.update();
  // How met doughnut
  howMetChart2.data.labels=d.how_met.map(x=>x.name);
  howMetChart2.data.datasets[0].data=d.how_met.map(x=>x.cnt);
  howMetChart2.data.datasets[0].backgroundColor=COLORS.slice(0,d.how_met.length).map(c=>c+'99');
  howMetChart2.update();
}}

// ── Main renderer ─────────────────────────────────────────────────────────────
function renderPeriod(p){{
  const d=PERIODS[p];
  if(!d) return;

  // Period badge
  txt('period-badge','📅 '+d.from+' → '+d.to+' ['+p.toUpperCase()+']');

  // ── Executivo KPIs ──
  txt('kpi-rev',fmt(d.total_rev));
  html('kpi-rev-sub',`<span class="badge ${{badgeCls(d.mom_rev_pct)}}">${{arr(d.mom_rev_pct)}} ${{Math.abs(d.mom_rev_pct)}}% MoM</span>`);
  txt('kpi-exp',fmt(d.total_exp));
  html('kpi-exp-sub',`<span class="badge ${{d.mom_exp_pct>0?'dn':'up'}}">${{arr(d.mom_exp_pct)}} ${{Math.abs(d.mom_exp_pct)}}% MoM</span>`);
  txt('kpi-profit',fmt(d.total_profit));
  txt('kpi-profit-sub','Margem '+d.margin_pct+'%');
  const profCard=document.getElementById('kpi-profit-card');
  if(profCard){{ profCard.className='kpi '+(d.total_profit>=0?'green':'red'); }}
  txt('kpi-prod',fmt(d.total_amount));
  txt('kpi-prod-sub',d.total_appr+' orçamentos');
  txt('kpi-conv',d.conv_rate+'%');
  txt('kpi-conv-sub','de '+d.total_est.toLocaleString('pt-BR')+' orçamentos');
  txt('kpi-ticket',fmt(d.avg_ticket));
  txt('kpi-appts',d.total_appts.toLocaleString('pt-BR'));
  const noshowVal = d.noshow_rate===null ? 'N/D' : d.noshow_rate+'%';
  txt('kpi-noshow', noshowVal);
  txt('kpi-noshow-sub',d.noshow_rate===null ? 'Dados indisponíveis para este período' : d.total_misses+' faltas no período');
  const nsCard=document.getElementById('kpi-noshow-card');
  if(nsCard) nsCard.className='kpi '+(d.noshow_rate===null?'amber':d.noshow_rate<20?'amber':'red');

  // ── Health Score ──
  style('health-num','color',d.health_color);
  txt('health-num',d.health_score);
  style('health-label-txt','color',d.health_color);
  txt('health-label-txt',d.health_score>=75?'EXCELENTE':d.health_score>=50?'BOM':'ATENÇÃO');
  txt('score-margin-txt',d.margin_score+'pts');
  style('score-margin-bar','width',d.margin_score+'%');
  txt('score-conv-txt',d.conv_score+'pts');
  style('score-conv-bar','width',d.conv_score+'%');
  txt('score-goal-txt',d.goal_score+'pts');
  style('score-goal-bar','width',d.goal_score+'%');
  txt('score-noshow-txt',d.noshow_score+'pts');
  style('score-noshow-bar','width',d.noshow_score+'%');

  // Break-even + Projections
  html('be-content',buildBeContent(d));
  html('proj-content',buildProjContent(d));

  // ── Financeiro KPIs ──
  txt('f-rev',fmt(d.total_rev));
  txt('f-rev-sub',d.n_months+' meses');
  txt('f-exp',fmt(d.total_exp));
  txt('f-profit',fmt(d.total_profit));
  txt('f-margin-sub','Margem '+d.margin_pct+'%');
  const fpCard=document.getElementById('f-profit-card');
  if(fpCard) fpCard.className='kpi '+(d.total_profit>=0?'green':'red');
  txt('f-avg-rev',fmtk(d.avg_monthly_rev));
  txt('f-avg-exp',fmtk(d.avg_monthly_exp));
  txt('f-be',fmtk(d.breakeven));

  // ── Clínico KPIs ──
  txt('c-prod',fmt(d.total_amount));
  txt('c-prod-sub',d.total_appr+' orçamentos');
  txt('c-ticket',fmt(d.avg_ticket));
  txt('c-specs',d.n_specs);
  txt('c-appts',d.total_appts.toLocaleString('pt-BR'));

  // ── Comercial KPIs ──
  txt('cm-est',d.total_est.toLocaleString('pt-BR'));
  txt('cm-appr',d.total_appr.toLocaleString('pt-BR'));
  txt('cm-rej',d.total_rej.toLocaleString('pt-BR'));
  txt('cm-conv',d.conv_rate+'%');
  txt('cm-ticket',fmt(d.avg_ticket));
  txt('cm-amount',fmt(d.total_amount));
  html('funnel-content',buildFunnelContent(d));

  // ── Operacional KPIs ──
  txt('op-appts',d.total_appts.toLocaleString('pt-BR'));
  txt('op-miss',d.total_misses.toLocaleString('pt-BR'));
  txt('op-noshow', d.noshow_rate===null ? 'N/D' : d.noshow_rate+'%');
  const opCard=document.getElementById('op-noshow-card');
  if(opCard) opCard.className='kpi '+(d.noshow_rate===null?'amber':d.noshow_rate<20?'amber':'red');
  txt('op-profs',d.n_profs);

  // ── Tables ──
  html('exp-rows',buildExpRows(d));
  html('esp-rows',buildEspRows(d));
  html('goal-rows',buildGoalRows(d));
  html('appt-rows',buildApptRows(d));

  // ── Charts ──
  updateCharts(d);
}}

// ── Period switch ─────────────────────────────────────────────────────────────
function switchPeriod(p){{
  document.querySelectorAll('.pbtn').forEach(b=>b.classList.toggle('active',b.dataset.p===p));
  renderPeriod(p);
}}

// ── Init ──────────────────────────────────────────────────────────────────────
initCharts();
renderPeriod('mat');
</script>
</body>
</html>"""

with open("index.html","w",encoding="utf-8") as f:
    f.write(html)

print(f"✅ index.html v2.1 gerado ({len(html):,} bytes)")
mat = PERIODS["mat"]
print(f"   MAT  — Receita: R${mat['total_rev']:,.2f} | Resultado: R${mat['total_profit']:,.2f} | Margem: {mat['margin_pct']}%")
mqt = PERIODS["mqt"]
print(f"   MQT  — Receita: R${mqt['total_rev']:,.2f} | Resultado: R${mqt['total_profit']:,.2f} | Margem: {mqt['margin_pct']}%")
ytd = PERIODS["ytd"]
print(f"   YTD  — Receita: R${ytd['total_rev']:,.2f} | Resultado: R${ytd['total_profit']:,.2f} | Margem: {ytd['margin_pct']}%")

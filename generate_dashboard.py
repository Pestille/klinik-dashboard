"""
Dashboard Klinik Odontologia - GitHub Actions Edition
Lê o token do environment variable CLINICORP_TOKEN
Gera index.html para GitHub Pages
"""

import base64, requests, json, os
from datetime import datetime, timedelta, date
from collections import defaultdict

TOKEN       = os.environ.get("CLINICORP_TOKEN", "23b73dd0-f3a9-4aef-97ff-9db567d283b5")
USER        = "klinik"
SUBSCRIBER  = "klinik"
BUSINESS_ID = 5073030694043648
BASE        = "https://api.clinicorp.com/rest/v1"

creds   = base64.b64encode(f"{USER}:{TOKEN}".encode()).decode()
HEADERS = {"Authorization": f"Basic {creds}"}

TODAY     = date.today()
FROM_DATE = (TODAY.replace(day=1) - timedelta(days=90)).replace(day=1)
TO_DATE   = TODAY
FROM_STR  = FROM_DATE.strftime("%Y-%m-%d")
TO_STR    = TO_DATE.strftime("%Y-%m-%d")
EST_FROM  = (TODAY - timedelta(days=30)).strftime("%Y-%m-%d")

print(f"Buscando dados {FROM_STR} → {TO_STR} ...")

def get(path, extra=None):
    params = {"subscriber_id": SUBSCRIBER, "from": FROM_STR, "to": TO_STR}
    if extra:
        params.update(extra)
    try:
        r = requests.get(BASE + path, headers=HEADERS, params=params, timeout=20)
        if r.status_code == 200:
            return r.json()
        print(f"  ⚠ {path} → {r.status_code}: {r.text[:100]}")
        return None
    except Exception as e:
        print(f"  ✗ {path} → {e}")
        return None

summary_raw   = get("/financial/list_summary") or []
payments_raw  = get("/financial/list_payments",  {"business_id": BUSINESS_ID}) or []
expertise_raw = get("/sales/expertise_revenue") or []
conversion_raw= get("/sales/estimates_and_conversion") or {}
goals_raw     = get("/operational/list_sales_goals") or []
misses_raw    = get("/operational/list_misses_goals") or []
appts_raw     = get("/appointment/list") or []
est_raw       = get("/estimates/list", {"from": EST_FROM, "to": TO_STR}) or []

r_prof = requests.get(BASE + "/professional/list_all_professionals",
                      headers=HEADERS, params={"subscriber_id": SUBSCRIBER}, timeout=15)
professionals = r_prof.json() if r_prof.status_code == 200 else []

# ─── PROCESSAMENTO ───────────────────────────────────────────────────────────
values = summary_raw if isinstance(summary_raw, list) else summary_raw.get("values", []) if isinstance(summary_raw, dict) else []

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
fin_months = [{"label": m, "revenue": round(month_rev[m], 2),
               "expense": round(month_exp[m], 2),
               "profit":  round(month_rev[m] - month_exp[m], 2)} for m in all_months]

top_cats  = sorted(cat_totals.items(), key=lambda x: -x[1])[:10]
cat_labels = [c[0] for c in top_cats]
cat_vals   = [round(c[1], 2) for c in top_cats]

conv      = conversion_raw if isinstance(conversion_raw, dict) else {}
approved  = conv.get("APPROVED", {})
rejected  = conv.get("REJECTED", {})
total_appr   = approved.get("TotalEstimates", 0)
total_rej    = rejected.get("TotalEstimates", 0) if rejected else 0
total_est    = total_appr + total_rej
conv_rate    = round(total_appr / total_est * 100, 1) if total_est > 0 else 0
avg_ticket   = approved.get("AverageTicket", 0)
total_amount = approved.get("TotalEstimatesAmount", 0)

esp_months    = expertise_raw if isinstance(expertise_raw, list) else []
esp_keys      = set()
for row in esp_months:
    for k in row.keys():
        if k.lower() not in ("month","from","to","year","date"):
            esp_keys.add(k)
esp_keys_list = sorted(list(esp_keys))

goals_list   = goals_raw if isinstance(goals_raw, list) else []
goal_labels  = [g.get("month", g.get("from",""))[:7] for g in goals_list]
goal_targets = [g.get("Goal", 0) for g in goals_list]
goal_actual  = [g.get("TotalRevenueAmount", g.get("TotalRevenue", 0)) for g in goals_list]

misses_list  = misses_raw if isinstance(misses_raw, list) else []
miss_labels  = [m.get("month", m.get("from",""))[:7] for m in misses_list]
miss_vals    = [m.get("Misses", 0) for m in misses_list]
total_misses = sum(miss_vals)

appt_list = appts_raw if isinstance(appts_raw, list) else []
prof_map  = {}
if isinstance(professionals, list):
    for p in professionals:
        pid  = str(p.get("PersonId") or p.get("Id") or p.get("id") or "")
        name = p.get("Name") or p.get("FullName") or p.get("name") or f"Prof {pid[:6]}"
        if pid:
            prof_map[pid] = name

appt_by_prof = defaultdict(int)
appt_by_cat  = defaultdict(int)
how_met      = defaultdict(int)
for a in appt_list:
    pid  = str(a.get("Dentist_PersonId", ""))
    name = prof_map.get(pid, f"Dr(a). {pid[:6]}")
    appt_by_prof[name] += 1
    cat = a.get("CategoryDescription", "Sem categoria") or "Sem categoria"
    appt_by_cat[cat] += 1
    src = a.get("HowDidMeet", "") or "Não informado"
    how_met[src] += 1

appt_prof_items  = sorted(appt_by_prof.items(), key=lambda x: -x[1])[:10]
appt_cat_items   = sorted(appt_by_cat.items(),  key=lambda x: -x[1])[:8]
how_met_items    = sorted(how_met.items(),       key=lambda x: -x[1])[:8]

total_rev  = sum(month_rev.values())
total_exp  = sum(month_exp.values())
total_prof = total_rev - total_exp
margin_pct = round(total_prof / total_rev * 100, 1) if total_rev > 0 else 0

def fmt(v):
    try:
        return f"R$ {float(v):,.2f}".replace(",","X").replace(".",",").replace("X",".")
    except:
        return "R$ 0,00"

gerado_em = datetime.now().strftime("%d/%m/%Y %H:%M")

esp_colors = ["#6366f1","#10b981","#f59e0b","#ef4444","#8b5cf6","#14b8a6","#f97316","#ec4899","#06b6d4","#84cc16"]
esp_datasets = []
for i, k in enumerate(esp_keys_list):
    c = esp_colors[i % len(esp_colors)]
    esp_datasets.append({"label": k.strip(), "data": [row.get(k,0) or 0 for row in esp_months],
                         "backgroundColor": c+"33", "borderColor": c, "fill": False, "tension": .4, "pointRadius": 4})

def J(x): return json.dumps(x)

html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Dashboard Klinik Odontologia</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Segoe UI',system-ui,sans-serif;background:#0f172a;color:#e2e8f0;min-height:100vh}}
header{{background:linear-gradient(135deg,#1e3a5f,#1a56a5);padding:18px 28px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #2563eb33}}
header h1{{font-size:1.4rem;font-weight:700}} header h1 span{{color:#60a5fa}}
.period{{background:#1e3a5f;border:1px solid #2563eb44;border-radius:8px;padding:4px 12px;font-size:.8rem;color:#93c5fd}}
.container{{padding:22px 28px;max-width:1700px;margin:0 auto}}
.stitle{{font-size:.65rem;text-transform:uppercase;letter-spacing:1.5px;color:#475569;margin:20px 0 10px;border-bottom:1px solid #1e293b;padding-bottom:6px}}
.kpi-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:14px;margin-bottom:20px}}
.kpi{{background:#1e293b;border:1px solid #334155;border-radius:12px;padding:18px;position:relative;overflow:hidden}}
.kpi::before{{content:'';position:absolute;top:0;left:0;right:0;height:3px}}
.kpi.blue::before{{background:linear-gradient(90deg,#3b82f6,#60a5fa)}}
.kpi.green::before{{background:linear-gradient(90deg,#10b981,#34d399)}}
.kpi.purple::before{{background:linear-gradient(90deg,#8b5cf6,#a78bfa)}}
.kpi.red::before{{background:linear-gradient(90deg,#ef4444,#f87171)}}
.kpi.amber::before{{background:linear-gradient(90deg,#f59e0b,#fbbf24)}}
.kpi.cyan::before{{background:linear-gradient(90deg,#06b6d4,#22d3ee)}}
.kpi label{{font-size:.65rem;text-transform:uppercase;letter-spacing:.8px;color:#64748b;display:block;margin-bottom:6px}}
.kpi .val{{font-size:1.5rem;font-weight:700}}
.kpi.blue .val{{color:#60a5fa}} .kpi.green .val{{color:#34d399}} .kpi.purple .val{{color:#a78bfa}}
.kpi.red .val{{color:#f87171}} .kpi.amber .val{{color:#fbbf24}} .kpi.cyan .val{{color:#22d3ee}}
.kpi .sub{{font-size:.7rem;color:#64748b;margin-top:4px}}
.g2{{display:grid;grid-template-columns:2fr 1fr;gap:16px;margin-bottom:16px}}
.g3{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;margin-bottom:16px}}
.card{{background:#1e293b;border:1px solid #334155;border-radius:12px;padding:18px}}
.card h3{{font-size:.7rem;text-transform:uppercase;letter-spacing:.6px;color:#64748b;margin-bottom:14px}}
.card canvas{{max-height:260px}}
footer{{text-align:center;padding:16px;color:#475569;font-size:.72rem;border-top:1px solid #1e293b;margin-top:8px}}
@media(max-width:900px){{.g2,.g3{{grid-template-columns:1fr}}.container{{padding:14px}}}}
</style>
</head>
<body>
<header>
  <div><h1>🦷 <span>Klinik</span> Odontologia</h1><small style="color:#94a3b8;font-size:.75rem">Dashboard Operacional</small></div>
  <div style="text-align:right">
    <div class="period">📅 {FROM_STR} → {TO_STR}</div>
    <small style="color:#475569;font-size:.72rem;margin-top:4px;display:block">Atualizado {gerado_em}</small>
  </div>
</header>
<div class="container">
  <div class="stitle">Resumo Financeiro do Período</div>
  <div class="kpi-grid">
    <div class="kpi green"><label>Receita Total</label><div class="val">{fmt(total_rev)}</div><div class="sub">{len(fin_months)} meses</div></div>
    <div class="kpi red"><label>Despesas Totais</label><div class="val">{fmt(total_exp)}</div></div>
    <div class="kpi {'green' if total_prof >= 0 else 'red'}"><label>Resultado Líquido</label><div class="val">{fmt(total_prof)}</div><div class="sub">Margem {margin_pct}%</div></div>
    <div class="kpi blue"><label>Produção Aprovada</label><div class="val">{fmt(total_amount)}</div><div class="sub">{total_appr} orçamentos</div></div>
    <div class="kpi purple"><label>Taxa de Conversão</label><div class="val">{conv_rate}%</div><div class="sub">de {total_est} orçamentos</div></div>
    <div class="kpi amber"><label>Ticket Médio</label><div class="val">{fmt(avg_ticket)}</div></div>
    <div class="kpi cyan"><label>Agendamentos</label><div class="val">{len(appt_list):,}</div></div>
    <div class="kpi red"><label>Faltas no Período</label><div class="val">{total_misses}</div></div>
  </div>
  <div class="stitle">Faturamento Mensal</div>
  <div class="g2">
    <div class="card"><h3>Receita / Despesa / Resultado por Mês</h3><canvas id="finChart"></canvas></div>
    <div class="card"><h3>Despesas por Categoria</h3><canvas id="catChart"></canvas></div>
  </div>
  <div class="stitle">Produção Clínica</div>
  <div class="g2">
    <div class="card"><h3>Produção por Especialidade (mês)</h3><canvas id="espChart"></canvas></div>
    <div class="card" style="display:grid;grid-template-rows:1fr 1fr;gap:16px">
      <div><h3>Conversão de Orçamentos</h3><canvas id="convChart" style="max-height:130px"></canvas></div>
      <div><h3>Meta vs. Realizado</h3><canvas id="goalChart" style="max-height:130px"></canvas></div>
    </div>
  </div>
  <div class="stitle">Agenda & Captação</div>
  <div class="g3">
    <div class="card"><h3>Agendamentos por Profissional</h3><canvas id="apptChart"></canvas></div>
    <div class="card"><h3>Agendamentos por Especialidade</h3><canvas id="catApptChart"></canvas></div>
    <div class="card"><h3>Como nos Encontrou</h3><canvas id="howMetChart"></canvas></div>
  </div>
  <div class="stitle">Faltas</div>
  <div class="card" style="margin-bottom:20px"><h3>Faltas por Mês</h3><canvas id="missChart" style="max-height:180px"></canvas></div>
</div>
<footer>Klinik Odontologia • Dados via API Clinicorp • Gerado em {gerado_em} UTC</footer>
<script>
const G={{responsive:true,plugins:{{legend:{{labels:{{color:'#94a3b8',boxWidth:12,font:{{size:11}}}}}}}},scales:{{x:{{ticks:{{color:'#64748b',font:{{size:11}}}},grid:{{color:'#1e293b'}}}},y:{{ticks:{{color:'#64748b',font:{{size:11}},callback:v=>'R$'+v.toLocaleString('pt-BR')}},grid:{{color:'#334155'}}}}}}}};
const GP={{...G,scales:{{...G.scales,y:{{ticks:{{color:'#64748b',font:{{size:11}}}},grid:{{color:'#334155'}}}}}}}};
new Chart(document.getElementById('finChart'),{{type:'bar',data:{{labels:{J([m["label"] for m in fin_months])},datasets:[{{label:'Receita',data:{J([m["revenue"] for m in fin_months])},backgroundColor:'#3b82f633',borderColor:'#3b82f6',borderWidth:2}},{{label:'Despesa',data:{J([m["expense"] for m in fin_months])},backgroundColor:'#ef444433',borderColor:'#ef4444',borderWidth:2}},{{label:'Resultado',data:{J([m["profit"] for m in fin_months])},type:'line',borderColor:'#10b981',backgroundColor:'#10b98122',fill:true,tension:.4,yAxisID:'y'}}]}},options:{{...G,interaction:{{mode:'index',intersect:false}}}}}});
new Chart(document.getElementById('catChart'),{{type:'bar',data:{{labels:{J(cat_labels)},datasets:[{{label:'R$',data:{J(cat_vals)},backgroundColor:['#ef444455','#f59e0b55','#8b5cf655','#ef444444','#f97316aa','#ec4899aa','#06b6d4aa','#84cc16aa','#6366f1aa','#14b8a6aa'],borderColor:['#ef4444','#f59e0b','#8b5cf6','#ef4444','#f97316','#ec4899','#06b6d4','#84cc16','#6366f1','#14b8a6'],borderWidth:2}}]}},options:{{...G,indexAxis:'y',plugins:{{legend:{{display:false}}}},scales:{{x:{{ticks:{{color:'#64748b',callback:v=>'R$'+v.toLocaleString('pt-BR')}},grid:{{color:'#334155'}}}},y:{{ticks:{{color:'#94a3b8',font:{{size:10}}}},grid:{{color:'#1e293b'}}}}}}}}}});
new Chart(document.getElementById('espChart'),{{type:'line',data:{{labels:{J([m.get("month","") for m in esp_months])},datasets:{J(esp_datasets)}}},options:{{...G,interaction:{{mode:'index',intersect:false}}}}}});
new Chart(document.getElementById('convChart'),{{type:'doughnut',data:{{labels:['Aprovados','Não aprovados'],datasets:[{{data:{J([total_appr, total_rej])},backgroundColor:['#10b98199','#ef444466'],borderColor:['#10b981','#ef4444'],borderWidth:2}}]}},options:{{responsive:true,plugins:{{legend:{{position:'right',labels:{{color:'#94a3b8',boxWidth:10,font:{{size:10}}}}}}}}}}}});
new Chart(document.getElementById('goalChart'),{{type:'bar',data:{{labels:{J(goal_labels)},datasets:[{{label:'Meta',data:{J(goal_targets)},backgroundColor:'#3b82f622',borderColor:'#3b82f6',borderWidth:2}},{{label:'Realizado',data:{J(goal_actual)},backgroundColor:'#10b98155',borderColor:'#10b981',borderWidth:2}}]}},options:{{...G}}}});
new Chart(document.getElementById('apptChart'),{{type:'bar',data:{{labels:{J([x[0] for x in appt_prof_items])},datasets:[{{label:'Agendamentos',data:{J([x[1] for x in appt_prof_items])},backgroundColor:'#8b5cf655',borderColor:'#8b5cf6',borderWidth:2}}]}},options:{{...GP,indexAxis:'y',plugins:{{legend:{{display:false}}}}}}}});
new Chart(document.getElementById('catApptChart'),{{type:'doughnut',data:{{labels:{J([x[0] for x in appt_cat_items])},datasets:[{{data:{J([x[1] for x in appt_cat_items])},backgroundColor:['#6366f199','#10b98199','#f59e0b99','#ef444499','#8b5cf699','#14b8a699','#f9731699','#ec489999'],borderWidth:1}}]}},options:{{responsive:true,plugins:{{legend:{{position:'right',labels:{{color:'#94a3b8',boxWidth:10,font:{{size:10}}}}}}}}}}}});
new Chart(document.getElementById('howMetChart'),{{type:'bar',data:{{labels:{J([x[0] for x in how_met_items])},datasets:[{{label:'Pacientes',data:{J([x[1] for x in how_met_items])},backgroundColor:'#06b6d455',borderColor:'#06b6d4',borderWidth:2}}]}},options:{{...GP,indexAxis:'y',plugins:{{legend:{{display:false}}}}}}}});
new Chart(document.getElementById('missChart'),{{type:'bar',data:{{labels:{J(miss_labels)},datasets:[{{label:'Faltas',data:{J(miss_vals)},backgroundColor:'#f59e0b55',borderColor:'#f59e0b',borderWidth:2}}]}},options:{{...GP}}}});
</script>
</body>
</html>"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"✅ index.html gerado ({len(html):,} bytes)")
print(f"   Receita: {fmt(total_rev)} | Despesas: {fmt(total_exp)} | Resultado: {fmt(total_prof)}")
print(f"   Conversão: {conv_rate}% | Ticket médio: {fmt(avg_ticket)} | Agendamentos: {len(appt_list)}")

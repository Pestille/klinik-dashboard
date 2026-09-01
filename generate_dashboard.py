"""
Dashboard Klinik Odontologia — v2.1 Multi-Period
Filtros: MAT (12m) | MQT (3m) | YTD
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

TODAY  = date.today()
TO_STR = TODAY.strftime("%Y-%m-%d")

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

def api(path, from_str, to_str, extra=None):
    params = {"subscriber_id": SUBSCRIBER, "from": from_str, "to": to_str}
    if extra: params.update(extra)
    try:
        r = requests.get(BASE + path, headers=HEADERS, params=params, timeout=20)
        if r.status_code == 200: return r.json()
        print(f"  ⚠ {path} [{from_str[:7]~↚{to_str[:7]}] → {r.status_code}")
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
        elif pt in ("REVENUE","INCOME"):
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
    esp_keys = sorted({k for row in esp_months_raw
                       for k in row.keys()
                       if k.lower() not in ("month","from","to","year","date","")})
    esp_totals = defaultdict(float)
    for row in esp_months_raw:
        for k in esp_keys:
            esp_totals[k] += float(row.get(k, 0) or 0)
    top_esp     = sorted(esp_totals.items(), key=lambda x: -x[1])[:10]
    max_esp_val = max((v for _,v in top_esp), default=1)

    esp_datasets = []
    for i, k in enumerate(esp_keys):
        c = COLORS[i % len(COLORS)]
        esp_datasets.append({
            "label": k.strip(),
            "data":  [float(row.get(k,0) or 0) for row in esp_months_raw],
            "backgroundColor": c+"33", "borderColor": c,
            "fill": False, "tension": .4, "pointRadius": 3
        })
    esp_month_labels = [row.get("month","") or row.get("from","") for row in esp_months_raw]

    # ── Goals ──────────────────────────────────────────────────────────────────
    goals_list   = goals_raw if isinstance(goals_raw, list) else []
    goal_labels  = [g.get("month", g.get("from",""))[:7] for g in goals_list]
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
        name = prof_map.get(pid, f"Dr(�������͔��;�������ɵ�����(������������}��}�ɽ�m����t����(����������Ѐ􁄹��Р�
�ѕ�����͍ɥ�ѥ�����M�����ѕ��ɥ�����Ȁ�M�����ѕ��ɥ��(������������}��}���m���t����(���������Ɍ�􁄹��Р�!����5��Ј������Ȁ�;�������ɵ����(�����������}���}�m�ɍt����(���������Ѐ􁄹��Р��є�������Р������ѵ����є������(������������Ё���������Ф����聅���}��}���ѡm��l��ut����((��������}�ɽ�}�ѕ�̀��ͽ�ѕ������}��}�ɽ���ѕ�̠������������������l�t�l���t(��������}���}�ѕ�̀���ͽ�ѕ������}��}��й�ѕ�̠�������������������l�t�l��t(�������}���}�ѕ�̀����ͽ�ѕ�����}���}���ѕ�̠����������������������l�t�l��t(��������}���ѡ}�ѕ�̀�ͽ�ѕ������}��}���Ѡ��ѕ�̠��(����ѽх�}����̀�����􁱕������}���Ф((�������R�R �-A%̃�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R (����ѽх�}ɕ؀�����մ����ѡ}ɕعم�Օ̠��(����ѽх�}���������մ����ѡ}����م�Օ̠��(����ѽх�}�ɽ��Ѐ�ѽх�}ɕ؀��ѽх�}���(������ɝ��}��Ѐ���ɽչ��ѽх�}�ɽ��Ѐ��ѽх�}ɕ؀�������Ĥ����ѽх�}ɕ؀������͔��(������͡��}Ʌє���ɽչ��ѽх�}���͕̀���ѽх�}����̀��ѽх�}���͕̤��������Ĥ�p(�����������������������ѽх�}����̀��ѽх�}���͕̤�������͔��((�������}ɕ�}��Ѐ􁵽�}���}��Ѐ��(��������������}���ѡ̤�����(���������ɕذ����Ѐ􁙥�}���ѡ�l��t�����}���ѡ�l��t(������������ɕ�l�ɕٕ�Ք�t�����(���������������}ɕ�}��Ѐ�ɽչ�������l�ɕٕ�Ք�t��ɕ�l�ɕٕ�Ք�t���ɕ�l�ɕٕ�Ք�t������Ĥ(������������ɕ�l������͔�t�����(���������������}���}��Ѐ�ɽչ�������l������͔�t��ɕ�l������͔�t���ɕ�l������͔�t������Ĥ((��������ѡ}͍�ɔ��ɽչ��(�������������������ɝ��}��ШȤ�����������Ԁ�(���������������������}Ʌє�ĸԤ����������Ԁ�(������������������ٝ}����}��Ф�����������Ԁ�(��������������������͡��}Ʌє�Ԥ���������(�����(��������ѡ}����Ȁ􀈌�����Ĉ��������ѡ}͍�ɔ���ԁ��͔�����������������ѡ}͍�ɔ�������͔��������Ј((����ɕ��ɸ��(���������������聱��������ɽ��聙ɽ�}��Ȱ��Ѽ��ѽ}��Ȱ���}���ѡ̈聸�(����������-A%�(���������ѽх�}ɕ؈�ɽչ��ѽх�}ɕذȤ���ѽх�}�����ɽչ��ѽх�}����Ȥ�(���������ѽх�}�ɽ��Ј�ɽչ��ѽх�}�ɽ��аȤ�����ɝ��}��Ј聵�ɝ��}��а(���������ѽх�}���չЈ�ɽչ��ѽх�}���չаȤ���ѽх�}���Ȉ�ѽх�}���Ȱ(���������ѽх�}ɕ���ѽх�}ɕ����ѽх�}��Ј�ѽх�}��а(�������������}Ʌє�聍���}Ʌє����ٝ}ѥ���Ј�ɽչ���ٝ}ѥ���аȤ�(���������ѽх�}����̈�ѽх�}����̰��ѽх�}���͕̈�ѽх�}���͕̰(�����������͡��}Ʌє�聹�͡��}Ʌє�������ѡ}͍�ɔ�聡���ѡ}͍�ɔ�(�������������ѡ}����Ȉ聡���ѡ}����Ȱ�����}ɕ�}��Ј聵��}ɕ�}��а(������������}���}��Ј聵��}���}��а���ٝ}����}��Ј�ɽչ���ٝ}����}��аĤ�(����������	ɕ����ٕ�(����������ɕ���ٕ���ɽչ���ɕ���ٕ��Ȥ����ٝ}��ᕑ}����ɽչ���ٝ}��ᕑ}���Ȥ�(����������ٝ}���ѡ��}ɕ؈�ɽչ���ٝ}���ѡ��}ɕذȤ����ٝ}���ѡ��}�����ɽչ���ٝ}���ѡ��}����Ȥ�(�����������}��ٕɅ���聉�}��ٕɅ�������}��ɝ����ɽչ����}��ɝ���Ȥ�(����������M��ɔ�����(�����������ɝ��}͍�ɔ��ɽչ������������ɝ��}��ШȤ��(�������������}͍�ɔ�耀�ɽչ��������������}Ʌє�ĸԤ��(�������������}͍�ɔ�耀�ɽչ�����������ٝ}����}��Ф��(�����������͡��}͍�ɔ��ɽչ�������������͡��}Ʌє�Ԥ��(�������������������������(������������}�����̈�m�l�������t���ȁ��������}���ѡ�t�(������������}ɕ؈耀��m�l�ɕٕ�Ք�t���ȁ��������}���ѡ�t�(������������}����耀��m�l������͔�t���ȁ��������}���ѡ�t�(������������}�ɽ��Ј�m�l��ɽ��Љt���ȁ��������}���ѡ�t�(������������}��ɝ����m�l���ɝ���t���ȁ��������}���ѡ�t�(����������Aɽ���ѥ��(����������ɽ�}�����̈聅��}������}�ɽ�������}ɕ�}���Ј聅��}ɕ�}���а(������������}���}���Ј聅��}���}���а���ɽ�}ɕ�}�������ɽ�}ɕ�}�����(����������ɽ�}���}�������ɽ�}���}��������ɽ�}���ѡ̈��ɽ�}���ѡ̰(����������ɽ�}ɕ؈��ɽ�}ɕذ���ɽ�}������ɽ�}�������ɽ�}�ɽ��Ј��ɽ�}�ɽ��а(����������
�ѕ��ɥ��(������������}�����̈聍��}�����̰�����}م�̈聍��}م�̰(����������M��������(������������}���ѡ}�����̈聕��}���ѡ}�����̰�����}��х͕�̈聕��}��х͕�̰(���������ѽ�}�����m쉹����聹����م���ɽչ��ٰ�ȥ􁙽ȁ���ٰ����ѽ�}���t�(������������}���}م���ɽչ�����}���}م��Ȥ����}����̈聱������}���̤�(��������������(�������������}�����̈聝���}�����̰������}хɝ��̈聝���}хɝ��̰(�������������}���Յ��聝���}���Յ��������}��Ј聝���}��а(����������5��͕�(�������������}�����̈聵���}�����̰������}م�̈聵���}م�̰(���������������ѵ����(�������������}���ѡ}�����̈�m�l�t���ȁ���������}���ѡ}�ѕ��t�(�������������}���ѡ}م�̈耀�m�l�t���ȁ���������}���ѡ}�ѕ��t�(�������������}�ɽ���m쉹����聹�����Ј聍􁙽ȁ������������}�ɽ�}�ѕ��t�(�������������}��Ј老m쉹����聹�����Ј聍􁙽ȁ������������}���}�ѕ��t�(������������}��Ј耀�m쉹����聹�����Ј聍􁙽ȁ�����������}���}�ѕ��t�(����������}�ɽ�̈聱�������}��}�ɽ���(����������չ���}܈聵�����������}Ʌє�����ѽх�}��������͔����(�����(((���R�R�R �IU8�10�AI%=L��R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R ()���}�ɽ���Q=d�ɕ����������Ĥ���ѥ�����ф��������Ԥ��ɕ����������Ĥ)���}�ɽ���Q=d�ɕ����������Ĥ���ѥ�����ф�����������ɕ����������Ĥ)�ё}�ɽ���Q=d�ɕ���������Ѡ�İ�����Ĥ()�ɥ�Р�
���ձ�����5P���ȁ��͕̤�����)���}��ф�􁍽���ѕ}��ɥ����5P������}�ɽ����əѥ�����d����������Q=}MQH�)�ɥ�Р�
���ձ�����5EP��́��͕̤�����)���}��ф�􁍽���ѕ}��ɥ����5EP������}�ɽ����əѥ�����d����������Q=}MQH�)�ɥ�Р�
���ձ�����eQ��������Յ�������)�ё}��ф�􁍽���ѕ}��ɥ����eQ����ё}�ɽ����əѥ�����d����������Q=}MQH�()AI%=L��쉵�Ј聵��}��ф�����Ј聵��}��ф����ѐ���ё}��х�)��Ʌ��}���􁑅ѕѥ�����ܠ����əѥ�����������d�� �4��((���R�R�R �!Q50��R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R )�ѵ��􁘈����=
QeA��ѵ��(�ѵ��������е	H��(񡕅��(�ф�����͕��UQ����(�ф������٥�����Ј����ѕ���ݥ�Ѡ���٥���ݥ�Ѡ����ѥ���͍����Ĉ�(�ѥѱ���͡���ɐ�-������=���ѽ������ѥѱ��(�͍ɥ�Ё�Ɍ�����輽�����͑����ȹ��н��������й�� ии�����н����йյ�������̈��͍ɥ���(���屔�(��퉽�ͥ饹�鉽ɑ�ȵ������ɝ����������������(�ɽ����(�����������Ŕ촵����������촵����Ŕ��͈촵��������Ʉ�(������ɑ���Ŕ̈́՘촵ѕ��荔ɔ��촵ѕ�����ф͈�촵ѕ����������(������Ք�͈�ɘ�촵�ɕ���������촵��������Ս��촵ɕ�荕������(���������荘����촵�典��وِ�촵����荕�����촵����������٘��)��)�����홽�е�������M�����U$�����ѕ��դ�����������ѕ��ͅ�̵͕ɥ�퉅���ɽչ��مȠ�����퍽����مȠ��ѕ�Ф���������������٠홽�еͥ��������)�������퉅���ɽչ�鱥���ȵ�Ʌ����Р��Ց������Ř͐�����ń̈́ٔ��������ɄՄ�������(�������������������푥�����陱������ѥ�䵍��ѕ������������ݕ��텱�����ѕ��鍕�ѕ��(����ɑ�ȵ���ѽ������ͽ�����Ŕ̈́���퉽�͡��������������������������(����ͥѥ����ѥ����ѽ����赥����������)�����ȁ���홽�еͥ��ĸ�ɕ�홽�еݕ���������􁡕���ȁ�ā�����퍽�������ՙ���(���ɥ���������퉅���ɽչ��Ŕ̈́���퉽ɑ�������ͽ�����͈�ɘ���퉽ɑ�ȵɅ��������������������������홽�еͥ����ɕ�퍽�����͌ՙ�푥�����饹�������������ɝ������ѽ�������(�����ѕ��홽�еͥ����ɕ�퍽�����������ѕ�е������ɥ�����(���Q	L���AI%=�	UQQ=9L���(�ѽ�����푥�����陱��퉅���ɽչ��مȠ����Ȥ퉽ɑ�ȵ���ѽ������ͽ����مȠ����ɑ�Ȥ���������������흅�������ٕə��ܵ���Ѽ텱�����ѕ��鍕�ѕ�����ѥ�䵍��ѕ������������ݕ����(�х���푥�����陱��흅�������ٕə��ܵ���Ѽ홱������(�х�����������������������ͽ������ѕ�퉽ɑ�ȵ���ѽ������ͽ�����Ʌ����ɕ��퍽����مȠ��ѕ��̤홽�еͥ����ɕ�홽�еݕ������������ѕȵ������������ݡ�є������鹽�Ʌ���Ʌ�ͥѥ��酱�������͕ȵ͕����鹽����(�х�顽ٕ��퍽����مȠ��ѕ��Ȥ퉅���ɽչ��Ŕ��͈����(�х����ѥٕ�퍽����مȠ����Ք�퉽ɑ�ȵ���ѽ��������مȠ����Ք�퉅���ɽչ��͈�ɘ�����(���ɥ����ѹ��푥�����陱��흅����������������������������홱��͡ɥ����퉽ɑ�ȵ���������ͽ����مȠ����ɑ�Ȥ���ɝ�������������(���ѹ������������������퉽ɑ�ȵɅ���������홽�еͥ����ɕ�홽�еݕ�����������ͽ������ѕ�퉽ɑ�������ͽ�����������퉅���ɽչ���Ʌ����ɕ��퍽����مȠ��ѕ��̤��Ʌ�ͥѥ��酱���������ѕȵ�������������(���Ѹ顽ٕ��퉽ɑ�ȵ������مȠ����Ք�퍽����مȠ��ѕ�Х��(���Ѹ���ѥٕ�퉅���ɽչ��͈�ɘ���퉽ɑ�ȵ������مȠ����Ք�퍽�������ՙ���(���A91L���(�������푥�����鹽������������������������ݥ�Ѡ����������ɝ�������ѽ��(���������ѥٕ�푥�����鉱�����(��ѥѱ��홽�еͥ���ɕ��ѕ�е�Ʌ�͙�ɴ�����ɍ�͔����ѕȵ�����������퍽����مȠ��ѕ��̤���ɝ��������������퉽ɑ�ȵ���ѽ������ͽ�����Ŕ��͈������������ѽ�����푥�����陱��텱�����ѕ��鍕�ѕ�흅�������(��ѥѱ��鉕��ɕ�퍽�ѕ��蜜�ݥ�Ѡ����������������퉽ɑ�ȵɅ��������퉅���ɽչ��مȠ����Ք�홱��͡ɥ������(���-A$���(������ɥ��푥������ɥ��ɥ��ѕ����є����յ���ɕ���С��Ѽ���б�����������řȤ�흅���������ɝ������ѽ��������(�����퉅���ɽչ��مȠ����̤퉽ɑ�������ͽ�����������퉽ɑ�ȵɅ�������������������������ͥѥ���ɕ��ѥٔ��ٕə���顥������Ʌ�ͥѥ����Ʌ�͙�ɴ�������(����顽ٕ����Ʌ�͙�ɴ��Ʌ�ͱ�ѕd�����퉽ɑ�ȵ��������������(�����鉕��ɕ�퍽�ѕ��蜜���ͥѥ��酉ͽ��є�ѽ�����������ɥ����������������퉽ɑ�ȵɅ������������������(�������Ք�鉕��ɕ�퉅���ɽչ�鱥���ȵ�Ʌ����Р�������͈�ɘذ��͌ՙ����(������ɕ���鉕��ɕ�퉅���ɽչ�鱥���ȵ�Ʌ����Р������������İ�ٕ�݈ܥ��(������������鉕��ɕ�퉅���ɽչ�鱥���ȵ�Ʌ����Р��������Ս�ذ��шՙ����(�����ɕ��鉕��ɕ�퉅���ɽչ�鱥���ȵ�Ʌ����Р������������а����Մԥ��(�����������鉕��ɕ�퉅���ɽչ�鱥���ȵ�Ʌ����Р������������������ᄥ��(������典�鉕��ɕ�퉅���ɽչ�鱥���ȵ�Ʌ����Р��������وِа��ݔ����(������������鉕��ɕ�퉅���ɽչ�鱥���ȵ�Ʌ����Р����������٘İ��Ոљ����(�����������홽�еͥ���ɕ��ѕ�е�Ʌ�͙�ɴ�����ɍ�͔����ѕȵ�����������퍽����مȠ��ѕ��̤푥�����鉱������ɝ������ѽ�������(������م��홽�еͥ��ĸ��ɕ�홽�еݕ������������������������(�������Ք��م��퍽�������ՙ���������ɕ����م��퍽�����ѐ������������������م��퍽���荄�቙���(�����ɕ���م��퍽���荘����������������Ȁ�م��퍽���荙�������������典��م��퍽�����ɐ͕����������������م��퍽������ፘ���(�������Չ�홽�еͥ����ɕ�퍽����مȠ��ѕ��̤���ɝ���ѽ�����푥�����陱��텱�����ѕ��鍕�ѕ�흅�������(�������푥�����饹��������������������������퉽ɑ�ȵɅ���������홽�еͥ����ɕ�홽�еݕ����������(����������퉅���ɽչ����������퍽�����ѐ���������������퉅���ɽչ�荕�������퍽���荘�����������������퉅���ɽչ�荘������퍽���荙�������(���1e=UQL���(����푥������ɥ��ɥ��ѕ����є����յ���͙Ȁə�흅���������ɝ������ѽ��������(��ɕ�푥������ɥ��ɥ��ѕ����є����յ���řȀř�흅���������ɝ������ѽ��������(����푥������ɥ��ɥ��ѕ����є����յ���řȀřȀř�흅���������ɝ������ѽ��������(�����푥������ɥ��ɥ��ѕ����є����յ���řȀə�흅���������ɝ������ѽ��������(���
IL���(���ɑ�퉅���ɽչ��مȠ����̤퉽ɑ�������ͽ�����������퉽ɑ�ȵɅ������������������������(���ɐ����홽�еͥ����ɕ��ѕ�е�Ʌ�͙�ɴ�����ɍ�͔����ѕȵ�����������퍽����مȠ��ѕ��̤���ɝ������ѽ������푥�����陱��텱�����ѕ��鍕�ѕ�흅�������(���ɐ����م�����ൡ�������������(���!1Q ���(�����Ѡ��յ�홽�еͥ��̸�ɕ�홽�еݕ�����������������������ѕ�е�����鍕�ѕ���(�����Ѡ�������홽�еͥ����ɕ�퍽����مȠ��ѕ��̤�ѕ�е�Ʌ�͙�ɴ�����ɍ�͔����ѕȵ������������ѕ�е�����鍕�ѕ����ɝ���ѽ�������(���AI=IML���(��ɽ��퉅���ɽչ������Ʉ퉽ɑ�ȵɅ���������������������ٕə���顥�������ɝ���ѽ�������(��ɽ�������������������퉽ɑ�ȵɅ����������Ʌ�ͥѥ���ݥ�Ѡ������(���Q	1L���(��х�����ݥ�Ѡ�����퉽ɑ�ȵ������͔鍽����͔홽�еͥ����ɕ���(��х����ѡ�퍽����مȠ��ѕ��̤홽�еͥ���ɕ��ѕ�е�Ʌ�͙�ɴ�����ɍ�͔����ѕȵ���������������������������퉽ɑ�ȵ���ѽ������ͽ������������ѕ�е�����鱕��홽�еݕ����������(��х����ё�����������������퉽ɑ�ȵ���ѽ������ͽ�����Ŕ��͈퍽����مȠ��ѕ�Х��(��х������顽ٕȁё�퉅���ɽչ��Ŕ��͈����(��х������յ��ѕ�е������ɥ���홽�еمɥ��е�յ�ɥ��х�ձ�ȵ�յ���(����������퉅���ɽչ������Ʉ퉽ɑ�ȵɅ���������������������ٕə���顥������(��������ȵ�����������������퉽ɑ�ȵɅ����������(�х��푥�����饹��������������������������퉽ɑ�ȵɅ��������홽�еͥ����ɕ���(�х�������퉅���ɽչ����������퍽�����ѐ������х��݅ɹ�퉅���ɽչ�荘������퍽���荙��������х������퉅���ɽչ�荕�������퍽���荘�������(������ɽ��푥�����陱������ѥ�䵍��ѕ������������ݕ��텱�����ѕ��鍕�ѕ������������������퉅���ɽչ������Ʉ퉽ɑ�ȵɅ��������퉽ɑ�ȵ���������ͽ������ɝ������ѽ�������)���ѕ���ѕ�е�����鍕�ѕ��������������퍽����������홽�еͥ����ɕ�퉽ɑ�ȵѽ������ͽ�����Ŕ��͈���ɝ���ѽ�������)���������ݥ�Ѡ��������친���ɥ��ѕ����є����յ���ř��������ɥ��ѕ����є����յ���řȀř�����)���������ݥ�Ѡ�������친Ȱ��ɔ���̰������ɥ��ѕ����є����յ���ř��������������������������ѽ�����홱�൑�ɕ�ѥ��鍽�յ�텱�����ѕ��陱���х�������ɥ����ѹ��퉽ɑ�ȵ����鹽�����������������퉽ɑ�ȵѽ������ͽ����مȠ����ɑ�Ȥ�ݥ�Ѡ��������������ѽ�������������ɥ���ɥ��ѕ����є����յ���ɕ���РȰřȥ����(���屔�(𽡕���(񉽑��((񡕅����(�����(��������~�܀������-������������=���ѽ��������(�����͵������屔􉍽����������홽�еͥ���ɕ����͡���ɐ�ᕍ�ѥټ��ȸ��͵����(��𽑥��(�����(�����؁��������ɥ���������������ɥ�����������~N��P𽑥��(�����؁����������ѕ����Յ��酑�����흕Ʌ��}���𽑥��(��𽑥��(𽡕�����((�؁������ѽ���Ȉ�(���؁������х�̈�(�����؁������х����ѥٔ������������ܠ�����j��ᕍ�ѥټ𽑥��(�����؁������х��������������������ܠĤ���~J���������ɼ𽑥��(�����؁������х��������������������ܠȤ���~�܁
������𽑥��(�����؁������х��������������������ܠ̤���~N(�
���ɍ���𽑥��(�����؁������х��������������������ܠФ���~N�=��Ʌ������𽑥��(��𽑥��(���؁��������ɥ����ѹ̈�(�������ѽ����������Ѹ���ѥٔ����ф��􉵅Ј����������ݥэ�A�ɥ������М���5P���ѽ��(�������ѽ����������Ѹ�����������ф����Ј����������ݥэ�A�ɥ������М���5EP���ѽ��(�������ѽ����������Ѹ�����������ф����ѐ�����������ݥэ�A�ɥ�����ѐ����eQ���ѽ��(��𽑥��(𽑥��((�����Q����P�a
UQ%Y<����(�؁��������������ѥٔ���������(���؁�������ѥѱ���I��յ��ᕍ�ѥټ𽑥��(���؁����������ɥ���(�����؁����������ɕ����񱅉���I����ф�Q�х�𽱅�����؁������م���������ɕ؈��P𽑥���؁�������Ո��������ɕص�Ո��𽑥��𽑥��(�����؁���������ɕ���񱅉�������́ͅQ�х��𽱅�����؁������م���������������P𽑥���؁�������Ո�������������Ո��𽑥��𽑥��(�����؁����������ɕ�����������ɽ��е��ɐ��񱅉���I��ձх���3��ե��𽱅�����؁������م����������ɽ��Ј��P𽑥���؁�������Ո���������ɽ��е�Ո��𽑥��𽑥��(�����؁�����������Ք��񱅉���Aɽ�������ɽم��𽱅�����؁������م����������ɽ����P𽑥���؁�������Ո���������ɽ���Ո��𽑥��𽑥��(�����؁�����������������񱅉���Q�ᄁ���
��ٕ����𽱅�����؁������م������������؈��P𽑥���؁�������Ո�����������ص�Ո��𽑥��𽑥��(�����؁�������������Ȉ�񱅉���Q����Ё7����𽱅�����؁������م���������ѥ���Ј��P𽑥��𽑥��(�����؁����������典��񱅉�����������ѽ�𽱅�����؁������م�������������̈��P𽑥��𽑥��(�����؁�������������Ȉ���������͡�ܵ��ɐ��񱅉���Q�ᄁ���9��͡��𽱅�����؁������م�����������͡�܈��P𽑥���؁�������Ո����������͡�ܵ�Ո��𽑥��𽑥��(��𽑥��((���؁�������Ȉ�(�����؁�����􉍅ɐ����屔􉑥�����陱��홱�൑�ɕ�ѥ��鍽�յ�흅��������(����������~��M�鑔����9��͍�����(�������؁��屔�ѕ�е�����鍕�ѕ������������������(���������؁�����􉡕��Ѡ��մ����􉡕��Ѡ��մ���P𽑥��(���������؁�����􉡕��Ѡ�������������𽑥��(���������؁��屔􉵅ɝ���ѽ�����홽�еͥ����ɕ�홽�еݕ������������ѕȵ���������������􉡕��Ѡ���������Ј��P𽑥��(������𽑥��(�������؁��屔􉑥�����陱��홱�൑�ɕ�ѥ��鍽�յ�흅�����홽�еͥ����ɕ���(�����������(�����������؁��屔􉑥�����陱������ѥ�䵍��ѕ������������ݕ��퍽����مȠ��ѕ��̤���ɝ������ѽ�������������5�ɝ������ե�����������������͍�ɔ���ɝ�����Ј���屔􉍽����مȠ��ѕ�Ф���P������𽑥��(�����������؁�������ɽ����؁�������ɽ�����������͍�ɔ���ɝ�����Ȉ���屔�ݥ�Ѡ���퉅���ɽչ��مȠ���ɕ�����𽑥��𽑥��(��������𽑥��(�����������(�����������؁��屔􉑥�����陱������ѥ�䵍��ѕ������������ݕ��퍽����مȠ��ѕ��̤���ɝ������ѽ�������������
��ٕ���������ɍ������������������͍�ɔ����ص��Ј���屔􉍽����مȠ��ѕ�Ф���P������𽑥��(�����������؁�������ɽ����؁�������ɽ�����������͍�ɔ����ص��Ȉ���屔�ݥ�Ѡ���퉅���ɽչ��مȠ�����������𽑥��𽑥��(��������𽑥��(�����������(�����������؁��屔􉑥�����陱������ѥ�䵍��ѕ������������ݕ��퍽����مȠ��ѕ��̤���ɝ������ѽ�������������ѥ������Ѽ������х����������������͍�ɔ��������Ј���屔􉍽����مȠ��ѕ�Ф���P������𽑥��(�����������؁�������ɽ����؁�������ɽ�����������͍�ɔ��������Ȉ���屔�ݥ�Ѡ���퉅���ɽչ��مȠ������Ȥ��𽑥��𽑥��(��������𽑥��(�����������(�����������؁��屔􉑥�����陱������ѥ�䵍��ѕ������������ݕ��퍽����مȠ��ѕ��̤���ɝ������ѽ�������������
����ɕ�����Ѽ���������������͍�ɔ���͡�ܵ��Ј���屔􉍽����مȠ��ѕ�Ф���P������𽑥��(�����������؁�������ɽ����؁�������ɽ�����������͍�ɔ���͡�ܵ��Ȉ���屔�ݥ�Ѡ���퉅���ɽչ��مȠ���典���𽑥��𽑥��(��������𽑥��(������𽑥��(����𽑥��(�����؁�����􉍅ɐ��(����������~N �Q��������������Aɽ���������I����ф���(������񍅹م́����ɕ��
���Ј�𽍅�م��(����𽑥��(��𽑥��((���؁������ɔ��(�����؁�����􉍅ɐ��(����������j[��<�A��Ѽ�����ե���ɥ��5��ͅ����(�������؁��􉉔����ѕ�Ј�𽑥��(����𽑥��(�����؁�����􉍅ɐ��(����������~R��Aɽ�������P�A��᥵�̀́5�͕����(�������؁����ɽ�����ѕ�Ј���屔􉑥�����陱��홱�൑�ɕ�ѥ��鍽�յ�흅����������������������𽑥��(����𽑥��(��𽑥��(𽑥��((�����Q�ă�P�%99
%I<����(�؁�����������������Ĉ�(���؁�������ѥѱ���A�ə�ɵ������������Ʉ𽑥��(���؁����������ɥ���(�����؁����������ɕ����񱅉���I����ф�A������𽱅�����؁������م�����􉘵ɕ؈��P𽑥���؁�������Ո����􉘵ɕص�Ո��𽑥��𽑥��(�����؁���������ɕ���񱅉�������́ͅA������𽱅�����؁������م�����􉘵������P𽑥��𽑥��(�����؁����������ɕ������􉘵�ɽ��е��ɐ��񱅉���1Սɼ�3��ե��𽱅�����؁������م�����􉘵�ɽ��Ј��P𽑥���؁�������Ո����􉘵��ɝ����Ո��𽑥��𽑥��(�����؁�����������Ք��񱅉���I����ф�7�����7��𽱅�����؁������م�����􉘵�ٜ�ɕ؈��P𽑥��𽑥��(�����؁�������������Ȉ�񱅉�������̈́�7�����7��𽱅�����؁������م�����􉘵�ٜ�������P𽑥��𽑥��(�����؁����������典��񱅉���	ɕ����ٕ��5��ͅ�𽱅�����؁������م�����􉘵�����P𽑥��𽑥��(��𽑥��(���؁�������ѥѱ���������Ʌѥټ����I��ձх��𽑥��(���؁������Ȉ�(�����؁�����􉍅ɐ�����I����ф�������̈́���I��ձх�����ȁ7�����񍅹م́��􉙥�
���Ј�𽍅�م��𽑥��(�����؁�����􉍅ɐ�����5�ɝ���3��ե�����ȁ7�̀������񍅹م́��􉵅ɝ��
���Ј�𽍅�م��𽑥��(��𽑥��(���؁�������ѥѱ���������Ʉ����
��ѽ�𽑥��(���؁������ɔ��(�����؁�����􉍅ɐ���������́ͅ��ȁ
�ѕ��ɥ����񍅹م́��􉍅�
���Ј�𽍅�م��𽑥��(�����؁�����􉍅ɐ��(���������I��������������ͅ����(�������х����������х������ѡ���������Ѡ�
�ѕ��ɥ��Ѡ��Ѡ�������մ��Q�х��Ѡ��Ѡ�������մ����Ѡ��Ѡ���屔�ݥ�Ѡ��������	��Ʉ�Ѡ������ѡ����(�������щ��䁥�����ɽ�̈��щ�����х����(����𽑥��(��𽑥��(𽑥��((�����Q�ȃ�P�
359%
<����(�؁�����������������Ȉ�(���؁�������ѥѱ���Aɽ������
������𽑥��(���؁����������ɥ���(�����؁�����������Ք��񱅉���Aɽ�������ɽم��𽱅�����؁������م�����􉌵�ɽ����P𽑥���؁�������Ո����􉌵�ɽ���Ո��𽑥��𽑥��(�����؁����������ɕ����񱅉���Q����Ё7����𽱅�����؁������م�����􉌵ѥ���Ј��P𽑥��𽑥��(�����؁�����������������񱅉���������������́ѥم�𽱅�����؁������م�����􉌵����̈��P𽑥��𽑥��(�����؁�������������Ȉ�񱅉���Q�х����������ѽ�𽱅�����؁������م�����􉌵����̈��P𽑥��𽑥��(��𽑥��(���؁�������ѥѱ���I����ф���ȁ������������𽑥��(���؁������Ȉ�(�����؁�����􉍅ɐ�����ٽ��������ȁ����������������̤���񍅹م́�����
���Ј�𽍅�م��𽑥��(�����؁�����􉍅ɐ��(���������I��������������������������(�������х����������х������ѡ���������Ѡ��������������Ѡ��Ѡ�������մ��Q�х��Ѡ��Ѡ���屔�ݥ�Ѡ��������M��ɔ�Ѡ������ѡ����(�������щ��䁥�����ɽ�̈��щ�����х����(����𽑥��(��𽑥��(���؁�������ѥѱ���A�ə�ɵ�������ȁAɽ���ͥ����𽑥��(���؁������ɔ��(�����؁�����􉍅ɐ�������������ѽ́��ȁAɽ���ͥ�������񍅹م́������
���Ј�𽍅�م��𽑥��(�����؁�����􉍅ɐ�����5������������������̀����������ѽ̤���񍅹م́��􉍅����
���Ј�𽍅�م��𽑥��(��𽑥��(𽑥��((�����Q�̃�P�
=5I
%0����(�؁�����������������̈�(���؁�������ѥѱ���չ���
���ɍ���𽑥��(���؁����������ɥ���(�����؁�����������Ք��񱅉���=������ѽ́�Ʌ���𽱅�����؁������م�����􉍴���Ј��P𽑥��𽑥��(�����؁����������ɕ����񱅉����ɽم���𽱅�����؁������م�����􉍴����Ȉ��P𽑥��𽑥��(�����؁���������ɕ���񱅉���;����ɽم���𽱅�����؁������م�����􉍴�ɕ����P𽑥��𽑥��(�����؁�����������������񱅉���
��ٕ����𽱅�����؁������م�����􉍴����؈��P𽑥��𽑥��(�����؁�������������Ȉ�񱅉���Q����Ё7����𽱅�����؁������م�����􉍴�ѥ���Ј��P𽑥��𽑥��(�����؁����������ɕ����񱅉���I����ф��ɽم��𽱅�����؁������م�����􉍴����չЈ��P𽑥��𽑥��(��𽑥��(���؁������ɔ��(�����؁�����􉍅ɐ��(����������~R�չ������
��ٕ�������(�������؁���չ�������ѕ�Ј���屔􉑥�����陱��홱�൑�ɕ�ѥ��鍽�յ�흅�����������������������𽑥��(����𽑥��(�����؁�����􉍅ɐ������ɽم��́�́;����ɽم������񍅹م́��􉍽��
���Ј�𽍅�م��𽑥��(��𽑥��(���؁�������ѥѱ���5�ф��́I����酑�𽑥��(���؁������Ȉ�(�����؁�����􉍅ɐ�����5�ф��̸�I����酑����ȁ7�����񍅹م́��􉝽��
���Ј�𽍅�م��𽑥��(�����؁�����􉍅ɐ��(���������ѥ������Ѽ���ȁ7�����(�������х����������х������ѡ���������Ѡ�7���Ѡ��Ѡ�������մ��5�ф�Ѡ��Ѡ�������մ��I����酑��Ѡ��Ѡ�������մ����Ѡ��Ѡ�Mх����Ѡ������ѡ����(�������щ��䁥�􉝽���ɽ�̈��щ�����х����(����𽑥��(��𽑥��(���؁�������ѥѱ���
��ч�������A�����ѕ�𽑥��(���؁�����􉍅ɐ����屔􉵅ɝ������ѽ��������(�������
������́�����ɽ����񍅹م́��􉡽�5��
���Ј���屔􉵅ൡ�������������𽍅�م��(��𽑥��(𽑥��((�����Q�Ѓ�P�=AI
%=90����(�؁�����������������Ј�(���؁�������ѥѱ���Y�����=��Ʌ������𽑥��(���؁����������ɥ���(�����؁����������典��񱅉���Q�х����������ѽ�𽱅�����؁������م������������̈��P𽑥��𽑥��(�����؁���������ɕ���񱅉���Q�х����х�𽱅�����؁������م�����������̈��P𽑥��𽑥��(�����؁�������������Ȉ��������͡�ܵ��ɐ��񱅉���Q�ᄁ���9��͡��𽱅�����؁������م����������͡�܈��P𽑥��𽑥��(�����؁�����������������񱅉�����ѥ�х́ѥٽ�𽱅�����؁������م���������ɽ�̈��P𽑥��𽑥��(��𽑥��(���؁������ɔ��(�����؁�����􉍅ɐ�����Y��յ�������������ѽ́��ȁ7�����񍅹م́������5��ѡ
���Ј�𽍅�م��𽑥��(�����؁�����􉍅ɐ�������х́��ȁ7�����񍅹م́��􉵥��
���Ј�𽍅�م��𽑥��(��𽑥��(���؁�������ѥѱ���A�ə�ɵ�������ȁ��ѥ�ф𽑥��(���؁������ɔ��(�����؁�����􉍅ɐ��(�����������������ѽ́��ȁ��ѥ�ф���(�������х����������х������ѡ���������Ѡ���ѥ�ф�Ѡ��Ѡ�������մ��Eѐ�Ѡ��Ѡ���屔�ݥ�Ѡ��������Y��յ��Ѡ������ѡ����(�������щ��䁥����еɽ�̈��щ�����х����(����𽑥��(�����؁�����􉍅ɐ�����
��������
��ч������񍅹م́��􉡽�5��
����Ȉ�𽍅�م��𽑥��(��𽑥��(𽑥��((񙽽ѕ��-������=���ѽ�������P��͡���ɐ�ᕍ�ѥټ��ȸă�P����́٥��
���������A$��P�흕Ʌ��}���𽙽�ѕ��((�͍ɥ���)����ЁAI%=L���(�AI%=L���)����Ё
=1=IL����(�
=1=IL���((����R�R �Q����ݥэ������R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R )�չ�ѥ����ܡ����(�����յ��й�Օ��M����ѽ������х������������б����й�����1��йѽ��������ѥٔ����������(�����յ��й�Օ��M����ѽ�����������������������������������1��йѽ��������ѥٔ����������)��((����R�R ��ɵ��ѕ�̃�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R )�չ�ѥ�����Сإ��(���������ձ����9�8�ؤ��ɕ��ɸ��H��������(��ɕ��ɸ��H����9յ��ȡؤ�ѽ1�����M�ɥ�����е	H���������յɅ�ѥ��������ȱ��᥵յɅ�ѥ�������������)��)�չ�ѥ�����Ѭ�إ��(���������ձ����9�8�ؤ��ɕ��ɸ��H�����(����9յ��ȡؤ�(��������Ŕؤ�ɕ��ɸ��H�����ؼŔؤ�ѽ�ᕐ�Ĥ��4��(��������Ŕ̤�ɕ��ɸ��H�����ؼŔ̤�ѽ�ᕐ�Ĥ��,��(��ɕ��ɸ��H����5�Ѡ�ɽչ��ؤ�)��)�չ�ѥ�����ȡ����ɕ��ɸ�������D��������L�蟊H�m��)�չ�ѥ��������
�̡����ɕ��ɸ����������蝑�����((����R�R �Q��Ѓ�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R )�չ�ѥ�����С���م���퍽��Ё�����յ��й���������	�%�������������ѕ��
��ѕ���م����)�չ�ѥ����ѵ�����م���퍽��Ё�����յ��й���������	�%������������������!Q50�����)�չ�ѥ�����屔�����ɽ��م���퍽��Ё�����յ��й���������	�%���������������展m�ɽ�t�م����((����R�R �
���Ё���х���̃�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R�R )��Ё�ɕ��
���б���
���б��ɝ��
���б���
���б���
���б����
���б������
���а(��������
���б����
���б���5��
���б����5��ѡ
���б����
���б���5��
������()����Ё����ф͈�������Ŕ��͈�����������Ԝ�)����Ё͍���H���ѥ�����퍽���蜌����ሜ��������ͥ��������������������H���عѽ1�����M�ɥ�����е	H������ɥ���퍽����������)����Ё͍���8���ѥ�����퍽���蜌����ሜ��������ͥ����������ɥ���퍽����������)����Ё͍���@���ѥ�����퍽���蜌����ሜ��������ͥ�������������������ج�������ɥ���퍽����������)����Ё͍���`���ѥ�����퍽���蜌����ሜ��������ͥ����������ɥ���퍽����������)����Ё��������������퍽��������]��Ѡ��ı�������ͥ�����������)����Ё���H�����ͥѥ���ɥ��М���������퍽��������]��Ѡ�����������ͥ�����������)����Ё��AI%=L�����()�չ�ѥ�������
����̠���(������Ё��AI%=L�����(���ɕ��
�������܁
���С���յ��й���������	�%����ɕ��
���М��������蝱�����(������ф���������鐹�ɽ�}�����̱��х͕���l(��������������I����ф����ф鐹���}ɕ�}���б��ɑ��
����蜌�����Ĝ������ɽչ�
����蜌�������Ȝ��������Ք�ѕ�ͥ���б�����I������̱�������际�͕���(������������������̈́����ф鐹���}���}���б��ɑ��
����蜍���444',backgroundColor:'#ef444422',fill:false,tension:.4,pointRadius:3,spanGaps:false}},
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
    options:{{responsive:true,maintainAspectRatio:true,indexAxis:'y',plugins:{{legend:{{display:false}}}},
      scales:{{x:{{ticks:{{color:'#64748b',callback:v=>'R$'+v.toLocaleString('pt-BR')}},grid:{{color:G2}}}},y:{{ticks:{{color:'#94a3b8',font:{{size:10}}}},grid:{{color:G1}}}}}}
    }}
  }});
  espChart=new Chart(document.getElementById('espChart'),{{type:'line',
    data:{{labels:d.esp_month_labels,datasets:d.esp_datasets}},
    options:{{responsive:true,maintainAspectRatio:true,interaction:{{mode:'index',intersect:false}},plugins:{{legend:leg}},scales:{{x:scaleX,y:scaleR}}}}
  }});
  apptChart=new Chart(document.getElementById('apptChart'),{{type:'bar',
    data:{{labels:d.appt_prof.map(x=>x.name),datasets:[{{label:'Agendamentos',data:d.appt_prof.map(x=>x.cnt),backgroundColor:'#8b5cf655',borderColor:'#8b5cf6',borderWidth:2,borderRadius:3}}]}},
    options:{{responsive:true,maintainAspectRatio:true,indexAxis:'y',plugins:{{legend:{{display:false}}}},scales:{{x:scaleN,y:{{ticks:{{color:'#64748b',font:{{size:10}}}},grid:{{color:G1}}}}}}}}
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
    const [cls,lbl]=pct>=100?['good','✓ Atingida']:pct>=75?['warm','~ Parcial']:['bad','✗ Abaixo'];
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
  txt('kpi-noshow',d.noshow_rate+'%');
  txt('kpi-noshow-sub',d.total_misses+' faltas no período');
  const nsCard=document.getElementById('kpi-noshow-card');
  if(nsCard) nsCard.className='kpi '+(d.noshow_rate<20?'amber':'red');

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
  txt('op-noshow',d.noshow_rate+'%');
  const opCard=document.getElementById('op-noshow-card');
  if(opCard) opCard.className='kpi '+(d.noshow_rate<20?'amber':'red');
  txt('op-profs',d.n_profs);

  // ── Tables ──
  html('exp-rows',buildExpRows(d));
  html('est-rows',buildEspRows(d));
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

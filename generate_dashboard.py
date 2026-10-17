"""
Dashboard Klinik Odontologia — v2.1 (dados locais)
Gerado automaticamente a partir dos arquivos da pasta Tabelas Klinik.
Atualizado em: 15/10/2026 14:42
"""
import json

# ─── DADOS EXTRAÍDOS DOS ARQUIVOS LOCAIS (Tabelas Klinik) ────────────────────
PERIODS = json.loads('''{"mat": {"label": "MAT", "from": "2025-10", "to": "2026-09", "n_months": 12, "total_rev": 663502.45, "total_exp": 572320.19, "total_profit": 91182.26, "margin_pct": 13.7, "total_amount": 663502.45, "total_appr": 3846, "total_rej": 0, "total_est": 3846, "conv_rate": 0, "avg_ticket": 172.52, "total_appts": 3846, "total_misses": 1196, "noshow_rate": 23.7, "health_score": 31, "health_color": "#ef4444", "mom_rev_pct": 0, "mom_exp_pct": 0, "avg_goal_pct": 55.3, "breakeven": 0.0, "avg_fixed_mo": 0.0, "avg_monthly_rev": 55291.87, "avg_monthly_exp": 47693.35, "be_coverage": 100, "be_margin": 55291.87, "margin_score": 27, "conv_score": 0, "goal_score": 55, "noshow_score": 0, "fin_labels": ["2025-10", "2025-11", "2025-12", "2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06", "2026-07", "2026-08", "2026-09"], "fin_rev": [46588.77, 38255.36, 51321.24, 30730.06, 46192.94, 77688.18, 45741.15, 55109.35, 55175.61, 82117.12, 70681.68, 63900.99], "fin_exp": [46426.68, 54083.77, 52372.93, 49835.24, 47290.5, 46278.13, 44330.09, 36828.41, 39763.73, 52779.94, 49731.41, 52599.36], "fin_profit": [162.09, -15828.41, -1051.69, -19105.18, -1097.56, 31410.05, 1411.06, 18280.94, 15411.88, 29337.18, 20950.27, 11301.63], "fin_margin": [0.3, -41.4, -2.0, -62.2, -2.4, 40.4, 3.1, 33.2, 27.9, 35.7, 29.6, 17.7], "proj_labels": ["2025-10", "2025-11", "2025-12", "2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06", "2026-07", "2026-08", "2026-09", "2026-10", "2026-11", "2026-12"], "all_rev_hist": [46588.77, 38255.36, 51321.24, 30730.06, 46192.94, 77688.18, 45741.15, 55109.35, 55175.61, 82117.12, 70681.68, 63900.99, null, null, null], "all_exp_hist": [46426.68, 54083.77, 52372.93, 49835.24, 47290.5, 46278.13, 44330.09, 36828.41, 39763.73, 52779.94, 49731.41, 52599.36, null, null, null], "proj_rev_line": [null, null, null, null, null, null, null, null, null, null, null, null, 73811.7, 76660.9, 79510.11], "proj_exp_line": [null, null, null, null, null, null, null, null, null, null, null, null, 46508.93, 46326.71, 46144.49], "proj_months": ["2026-10", "2026-11", "2026-12"], "proj_rev": [73811.7, 76660.9, 79510.11], "proj_exp": [46508.93, 46326.71, 46144.49], "proj_profit": [27302.77, 30334.19, 33365.62], "cat_labels": ["Serviço da Dívida", "Comissões Profissionais", "Ocupação & Utilidades", "Pessoal", "Insumos Clínicos", "Laboratório Protético", "Tributos", "Serviços Administrativos", "Pró-Labore", "Tecnologia & Marketing"], "cat_vals": [65501.72, 58236.18, 49989.0, 38798.57, 38249.61, 16126.0, 8426.93, 5016.2, 3045.6, 2254.28], "esp_month_labels": ["2025-10", "2025-11", "2025-12", "2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06", "2026-07", "2026-08", "2026-09"], "esp_datasets": [{"label": "Manutenção ", "data": [10049.15, 10049.15, 10049.15, 10049.15, 10049.15, 10049.15, 10049.15, 10049.15, 10049.15, 10049.15, 10049.15, 10049.15], "borderColor": "#6366f1", "backgroundColor": "#6366f133", "fill": false, "tension": 0.4, "pointRadius": 3}, {"label": "Avaliação", "data": [9459.71, 9459.71, 9459.71, 9459.71, 9459.71, 9459.71, 9459.71, 9459.71, 9459.71, 9459.71, 9459.71, 9459.71], "borderColor": "#6366f1", "backgroundColor": "#6366f133", "fill": false, "tension": 0.4, "pointRadius": 3}, {"label": "Restauração", "data": [8539.62, 8539.62, 8539.62, 8539.62, 8539.62, 8539.62, 8539.62, 8539.62, 8539.62, 8539.62, 8539.62, 8539.62], "borderColor": "#6366f1", "backgroundColor": "#6366f133", "fill": false, "tension": 0.4, "pointRadius": 3}], "top_esp": [{"name": "Manutenção ", "val": 120589.76}, {"name": "Avaliação", "val": 113516.54}, {"name": "Restauração", "val": 102475.42}, {"name": "Retorno", "val": 76770.3}, {"name": "Protese", "val": 42956.87}, {"name": "Profilaxia", "val": 41749.24}, {"name": "PARTICULAR", "val": 38816.45}, {"name": "CONSULTA", "val": 38816.45}], "max_esp_val": 120589.76, "n_specs": 8, "goal_labels": ["10/25", "11/25", "12/25", "01/26", "02/26", "03/26", "04/26", "05/26", "06/26", "07/26", "08/26", "09/26"], "goal_targets": [100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000], "goal_actual": [46588.77, 38255.36, 51321.24, 30730.06, 46192.94, 77688.18, 45741.15, 55109.35, 55175.61, 82117.12, 70681.68, 63900.99], "goal_pct": [46.6, 38.3, 51.3, 30.7, 46.2, 77.7, 45.7, 55.1, 55.2, 82.1, 70.7, 63.9], "miss_labels": ["2025-10", "2025-11", "2025-12", "2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06", "2026-07", "2026-08", "2026-09"], "miss_vals": [99, 99, 78, 91, 99, 110, 107, 103, 107, 93, 92, 118], "appt_month_labels": ["2025-10", "2025-11", "2025-12", "2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06", "2026-07", "2026-08", "2026-09"], "appt_month_vals": [311, 292, 276, 273, 237, 328, 318, 336, 347, 401, 375, 352], "appt_prof": [{"name": "ADRIELI ARAUJO DE ALMEIDA", "cnt": 1516}, {"name": "FERNANDA PANGONI SOARES", "cnt": 716}, {"name": "MAISA KEFFLER CANDIA", "cnt": 575}, {"name": "CAROLINE SILVA PREUS", "cnt": 386}, {"name": "BARBARA CASARI LAURETTI", "cnt": 260}, {"name": "LIVIA HELENA RIFON GARCIA", "cnt": 198}, {"name": "NELSON TALATOCI OSHIRO FILHO", "cnt": 69}, {"name": "MATHEUS SARMENTO GARCIA", "cnt": 68}, {"name": "JOÃO PAULO SCHUSSLER", "cnt": 51}, {"name": "ELOISA COSTA AMARAL", "cnt": 7}], "appt_cat": [{"name": "Manutenção ", "cnt": 699}, {"name": "Avaliação", "cnt": 658}, {"name": "Restauração", "cnt": 594}, {"name": "Retorno", "cnt": 445}, {"name": "Protese", "cnt": 249}, {"name": "Profilaxia", "cnt": 242}, {"name": "PARTICULAR", "cnt": 225}, {"name": "CONSULTA", "cnt": 225}], "how_met": [], "n_profs": 10, "dent_table": [{"name": "ADRIELI ARAUJO DE ALMEIDA", "chair": 2, "appts": 1516, "rev": 261536.59, "ticket": 172.52, "conv": 0}, {"name": "FERNANDA PANGONI SOARES", "chair": 1, "appts": 716, "rev": 123522.56, "ticket": 172.52, "conv": 0}, {"name": "MAISA KEFFLER CANDIA", "chair": 1, "appts": 575, "rev": 99197.58, "ticket": 172.52, "conv": 0}, {"name": "CAROLINE SILVA PREUS", "chair": 2, "appts": 386, "rev": 66591.77, "ticket": 172.52, "conv": 0}, {"name": "BARBARA CASARI LAURETTI", "chair": 2, "appts": 260, "rev": 44854.56, "ticket": 172.52, "conv": 0}, {"name": "LIVIA HELENA RIFON GARCIA", "chair": 0, "appts": 198, "rev": 34158.47, "ticket": 172.52, "conv": 0}, {"name": "NELSON TALATOCI OSHIRO FILHO", "chair": 1, "appts": 69, "rev": 11903.71, "ticket": 172.52, "conv": 0}, {"name": "MATHEUS SARMENTO GARCIA", "chair": 0, "appts": 68, "rev": 11731.19, "ticket": 172.52, "conv": 0}, {"name": "JOÃO PAULO SCHUSSLER", "chair": 1, "appts": 51, "rev": 8798.39, "ticket": 172.52, "conv": 0}, {"name": "ELOISA COSTA AMARAL", "chair": 0, "appts": 7, "rev": 1207.62, "ticket": 172.52, "conv": 0}], "funnel_w": 50}, "mqt": {"label": "MQT", "from": "2026-07", "to": "2026-09", "n_months": 3, "total_rev": 216699.79, "total_exp": 155110.71, "total_profit": 61589.08, "margin_pct": 28.4, "total_amount": 216699.79, "total_appr": 1128, "total_rej": 0, "total_est": 1128, "conv_rate": 0, "avg_ticket": 192.11, "total_appts": 1128, "total_misses": 303, "noshow_rate": 21.2, "health_score": 43, "health_color": "#ef4444", "mom_rev_pct": 0, "mom_exp_pct": 0, "avg_goal_pct": 72.2, "breakeven": 51703.57, "avg_fixed_mo": 0.0, "avg_monthly_rev": 72233.26, "avg_monthly_exp": 51703.57, "be_coverage": 100, "be_margin": 20529.69, "margin_score": 57, "conv_score": 0, "goal_score": 72, "noshow_score": 0, "fin_labels": ["2026-07", "2026-08", "2026-09"], "fin_rev": [82117.12, 70681.68, 63900.99], "fin_exp": [52779.94, 49731.41, 52599.36], "fin_profit": [29337.18, 20950.27, 11301.63], "fin_margin": [35.7, 29.6, 17.7], "proj_labels": ["2026-07", "2026-08", "2026-09", "2026-10", "2026-11", "2026-12"], "all_rev_hist": [82117.12, 70681.68, 63900.99, null, null, null], "all_exp_hist": [52779.94, 49731.41, 52599.36, null, null, null], "proj_rev_line": [null, null, null, 54017.13, 44909.07, 35801.0], "proj_exp_line": [null, null, null, 51522.99, 51432.7, 51342.41], "proj_months": ["2026-10", "2026-11", "2026-12"], "proj_rev": [54017.13, 44909.07, 35801.0], "proj_exp": [51522.99, 51432.7, 51342.41], "proj_profit": [2494.14, -6523.63, -15541.41], "cat_labels": ["Serviço da Dívida", "Comissões Profissionais", "Ocupação & Utilidades", "Pessoal", "Insumos Clínicos", "Laboratório Protético", "Tributos", "Serviços Administrativos", "Pró-Labore", "Tecnologia & Marketing"], "cat_vals": [65501.72, 58236.18, 49989.0, 38798.57, 38249.61, 16126.0, 8426.93, 5016.2, 3045.6, 2254.28], "esp_month_labels": ["2026-07", "2026-08", "2026-09"], "esp_datasets": [{"label": "Manutenção ", "data": [15624.93, 15624.93, 15624.93], "borderColor": "#6366f1", "backgroundColor": "#6366f133", "fill": false, "tension": 0.4, "pointRadius": 3}, {"label": "Avaliação", "data": [11782.73, 11782.73, 11782.73], "borderColor": "#6366f1", "backgroundColor": "#6366f133", "fill": false, "tension": 0.4, "pointRadius": 3}, {"label": "Restauração", "data": [9605.49, 9605.49, 9605.49], "borderColor": "#6366f1", "backgroundColor": "#6366f133", "fill": false, "tension": 0.4, "pointRadius": 3}], "top_esp": [{"name": "Manutenção ", "val": 46874.78}, {"name": "Avaliação", "val": 35348.19}, {"name": "Restauração", "val": 28816.46}, {"name": "Retorno", "val": 22476.84}, {"name": "Profilaxia", "val": 22284.73}, {"name": "CONSULTA", "val": 16137.22}, {"name": "Protese", "val": 13255.57}, {"name": "PARTICULAR", "val": 10950.26}], "max_esp_val": 46874.78, "n_specs": 8, "goal_labels": ["07/26", "08/26", "09/26"], "goal_targets": [100000, 100000, 100000], "goal_actual": [82117.12, 70681.68, 63900.99], "goal_pct": [82.1, 70.7, 63.9], "miss_labels": ["2026-07", "2026-08", "2026-09"], "miss_vals": [93, 92, 118], "appt_month_labels": ["2026-07", "2026-08", "2026-09"], "appt_month_vals": [401, 375, 352], "appt_prof": [{"name": "ADRIELI ARAUJO DE ALMEIDA", "cnt": 596}, {"name": "BARBARA CASARI LAURETTI", "cnt": 150}, {"name": "CAROLINE SILVA PREUS", "cnt": 120}, {"name": "MAISA KEFFLER CANDIA", "cnt": 108}, {"name": "FERNANDA PANGONI SOARES", "cnt": 100}, {"name": "LIVIA HELENA RIFON GARCIA", "cnt": 27}, {"name": "NELSON TALATOCI OSHIRO FILHO", "cnt": 18}, {"name": "JOÃO PAULO SCHUSSLER", "cnt": 8}, {"name": "ELOISA COSTA AMARAL", "cnt": 1}], "appt_cat": [{"name": "Manutenção ", "cnt": 244}, {"name": "Avaliação", "cnt": 184}, {"name": "Restauração", "cnt": 150}, {"name": "Retorno", "cnt": 117}, {"name": "Profilaxia", "cnt": 116}, {"name": "CONSULTA", "cnt": 84}, {"name": "Protese", "cnt": 69}, {"name": "PARTICULAR", "cnt": 57}], "how_met": [], "n_profs": 9, "dent_table": [{"name": "ADRIELI ARAUJO DE ALMEIDA", "chair": 2, "appts": 596, "rev": 114497.41, "ticket": 192.11, "conv": 0}, {"name": "BARBARA CASARI LAURETTI", "chair": 2, "appts": 150, "rev": 28816.46, "ticket": 192.11, "conv": 0}, {"name": "CAROLINE SILVA PREUS", "chair": 2, "appts": 120, "rev": 23053.17, "ticket": 192.11, "conv": 0}, {"name": "MAISA KEFFLER CANDIA", "chair": 1, "appts": 108, "rev": 20747.85, "ticket": 192.11, "conv": 0}, {"name": "FERNANDA PANGONI SOARES", "chair": 1, "appts": 100, "rev": 19210.97, "ticket": 192.11, "conv": 0}, {"name": "LIVIA HELENA RIFON GARCIA", "chair": 0, "appts": 27, "rev": 5186.96, "ticket": 192.11, "conv": 0}, {"name": "NELSON TALATOCI OSHIRO FILHO", "chair": 1, "appts": 18, "rev": 3457.98, "ticket": 192.11, "conv": 0}, {"name": "JOÃO PAULO SCHUSSLER", "chair": 1, "appts": 8, "rev": 1536.88, "ticket": 192.11, "conv": 0}, {"name": "ELOISA COSTA AMARAL", "chair": 0, "appts": 1, "rev": 192.11, "ticket": 192.11, "conv": 0}], "funnel_w": 50}, "ytd": {"label": "YTD", "from": "2026-01", "to": "2026-09", "n_months": 9, "total_rev": 527337.08, "total_exp": 419436.81, "total_profit": 107900.27, "margin_pct": 20.5, "total_amount": 527337.08, "total_appr": 2967, "total_rej": 0, "total_est": 2967, "conv_rate": 0, "avg_ticket": 177.73, "total_appts": 2967, "total_misses": 920, "noshow_rate": 23.7, "health_score": 36, "health_color": "#ef4444", "mom_rev_pct": 0, "mom_exp_pct": 0, "avg_goal_pct": 58.6, "breakeven": 0.0, "avg_fixed_mo": 0.0, "avg_monthly_rev": 58593.01, "avg_monthly_exp": 46604.09, "be_coverage": 100, "be_margin": 58593.01, "margin_score": 41, "conv_score": 0, "goal_score": 59, "noshow_score": 0, "fin_labels": ["2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06", "2026-07", "2026-08", "2026-09"], "fin_rev": [30730.06, 46192.94, 77688.18, 45741.15, 55109.35, 55175.61, 82117.12, 70681.68, 63900.99], "fin_exp": [49835.24, 47290.5, 46278.13, 44330.09, 36828.41, 39763.73, 52779.94, 49731.41, 52599.36], "fin_profit": [-19105.18, -1097.56, 31410.05, 1411.06, 18280.94, 15411.88, 29337.18, 20950.27, 11301.63], "fin_margin": [-62.2, -2.4, 40.4, 3.1, 33.2, 27.9, 35.7, 29.6, 17.7], "proj_labels": ["2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06", "2026-07", "2026-08", "2026-09", "2026-10", "2026-11", "2026-12"], "all_rev_hist": [30730.06, 46192.94, 77688.18, 45741.15, 55109.35, 55175.61, 82117.12, 70681.68, 63900.99, null, null, null], "all_exp_hist": [49835.24, 47290.5, 46278.13, 44330.09, 36828.41, 39763.73, 52779.94, 49731.41, 52599.36, null, null, null], "proj_rev_line": [null, null, null, null, null, null, null, null, null, 77296.53, 81037.24, 84777.94], "proj_exp_line": [null, null, null, null, null, null, null, null, null, 48838.8, 49285.74, 49732.68], "proj_months": ["2026-10", "2026-11", "2026-12"], "proj_rev": [77296.53, 81037.24, 84777.94], "proj_exp": [48838.8, 49285.74, 49732.68], "proj_profit": [28457.73, 31751.5, 35045.26], "cat_labels": ["Serviço da Dívida", "Comissões Profissionais", "Ocupação & Utilidades", "Pessoal", "Insumos Clínicos", "Laboratório Protético", "Tributos", "Serviços Administrativos", "Pró-Labore", "Tecnologia & Marketing"], "cat_vals": [65501.72, 58236.18, 49989.0, 38798.57, 38249.61, 16126.0, 8426.93, 5016.2, 3045.6, 2254.28], "esp_month_labels": ["2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06", "2026-07", "2026-08", "2026-09"], "esp_datasets": [{"label": "Manutenção ", "data": [11355.23, 11355.23, 11355.23, 11355.23, 11355.23, 11355.23, 11355.23, 11355.23, 11355.23], "borderColor": "#6366f1", "backgroundColor": "#6366f133", "fill": false, "tension": 0.4, "pointRadius": 3}, {"label": "Avaliação", "data": [10427.07, 10427.07, 10427.07, 10427.07, 10427.07, 10427.07, 10427.07, 10427.07, 10427.07], "borderColor": "#6366f1", "backgroundColor": "#6366f133", "fill": false, "tension": 0.4, "pointRadius": 3}, {"label": "Restauração", "data": [8491.74, 8491.74, 8491.74, 8491.74, 8491.74, 8491.74, 8491.74, 8491.74, 8491.74], "borderColor": "#6366f1", "backgroundColor": "#6366f133", "fill": false, "tension": 0.4, "pointRadius": 3}], "top_esp": [{"name": "Manutenção ", "val": 102197.11}, {"name": "Avaliação", "val": 93843.61}, {"name": "Restauração", "val": 76425.66}, {"name": "Retorno", "val": 56519.44}, {"name": "Profilaxia", "val": 36968.69}, {"name": "CONSULTA", "val": 34302.68}, {"name": "Protese", "val": 33769.48}, {"name": "PARTICULAR", "val": 28259.72}], "max_esp_val": 102197.11, "n_specs": 8, "goal_labels": ["01/26", "02/26", "03/26", "04/26", "05/26", "06/26", "07/26", "08/26", "09/26"], "goal_targets": [100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000], "goal_actual": [30730.06, 46192.94, 77688.18, 45741.15, 55109.35, 55175.61, 82117.12, 70681.68, 63900.99], "goal_pct": [30.7, 46.2, 77.7, 45.7, 55.1, 55.2, 82.1, 70.7, 63.9], "miss_labels": ["2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06", "2026-07", "2026-08", "2026-09"], "miss_vals": [91, 99, 110, 107, 103, 107, 93, 92, 118], "appt_month_labels": ["2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06", "2026-07", "2026-08", "2026-09"], "appt_month_vals": [273, 237, 328, 318, 336, 347, 401, 375, 352], "appt_prof": [{"name": "ADRIELI ARAUJO DE ALMEIDA", "cnt": 1299}, {"name": "FERNANDA PANGONI SOARES", "cnt": 491}, {"name": "MAISA KEFFLER CANDIA", "cnt": 392}, {"name": "CAROLINE SILVA PREUS", "cnt": 309}, {"name": "BARBARA CASARI LAURETTI", "cnt": 260}, {"name": "LIVIA HELENA RIFON GARCIA", "cnt": 130}, {"name": "NELSON TALATOCI OSHIRO FILHO", "cnt": 49}, {"name": "JOÃO PAULO SCHUSSLER", "cnt": 34}, {"name": "ELOISA COSTA AMARAL", "cnt": 3}], "appt_cat": [{"name": "Manutenção ", "cnt": 575}, {"name": "Avaliação", "cnt": 528}, {"name": "Restauração", "cnt": 430}, {"name": "Retorno", "cnt": 318}, {"name": "Profilaxia", "cnt": 208}, {"name": "CONSULTA", "cnt": 193}, {"name": "Protese", "cnt": 190}, {"name": "PARTICULAR", "cnt": 159}], "how_met": [], "n_profs": 9, "dent_table": [{"name": "ADRIELI ARAUJO DE ALMEIDA", "chair": 2, "appts": 1299, "rev": 230876.6, "ticket": 177.73, "conv": 0}, {"name": "FERNANDA PANGONI SOARES", "chair": 1, "appts": 491, "rev": 87267.44, "ticket": 177.73, "conv": 0}, {"name": "MAISA KEFFLER CANDIA", "chair": 1, "appts": 392, "rev": 69671.77, "ticket": 177.73, "conv": 0}, {"name": "CAROLINE SILVA PREUS", "chair": 2, "appts": 309, "rev": 54919.84, "ticket": 177.73, "conv": 0}, {"name": "BARBARA CASARI LAURETTI", "chair": 2, "appts": 260, "rev": 46210.87, "ticket": 177.73, "conv": 0}, {"name": "LIVIA HELENA RIFON GARCIA", "chair": 0, "appts": 130, "rev": 23105.43, "ticket": 177.73, "conv": 0}, {"name": "NELSON TALATOCI OSHIRO FILHO", "chair": 1, "appts": 49, "rev": 8708.97, "ticket": 177.73, "conv": 0}, {"name": "JOÃO PAULO SCHUSSLER", "chair": 1, "appts": 34, "rev": 6042.96, "ticket": 177.73, "conv": 0}, {"name": "ELOISA COSTA AMARAL", "chair": 0, "appts": 3, "rev": 533.2, "ticket": 177.73, "conv": 0}], "funnel_w": 50}}''')

DAILY = json.loads('''{"biz_days": ["2026-10-01", "2026-10-02", "2026-10-05", "2026-10-06", "2026-10-07", "2026-10-08", "2026-10-09", "2026-10-12", "2026-10-13", "2026-10-14", "2026-10-15"], "day_labels": ["01/10", "02/10", "05/10", "06/10", "07/10", "08/10", "09/10", "12/10", "13/10", "14/10", "15/10"], "sched_vals": [15, 8, 20, 11, 7, 7, 10, 0, 20, 27, 14], "chair1_util": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "chair2_util": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "avg_sched_d": 12.6, "avg_appts_d": 12.6, "avg_daily_rev": 3283.33, "avg_c1": 0, "avg_c2": 0, "dent_names": ["Adrieli", "Barbara", "Caroline", "Fernanda", "João", "Livia", "Maisa", "Nelson"], "dent_series": [{"name": "Adrieli", "vals": [8, 8, 7, 10, 7, 6, 8, 0, 11, 0, 0]}, {"name": "Barbara", "vals": [0, 0, 0, 0, 0, 0, 0, 0, 0, 21, 12]}, {"name": "Caroline", "vals": [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}, {"name": "Fernanda", "vals": [4, 0, 0, 0, 0, 0, 0, 0, 6, 6, 0]}, {"name": "João", "vals": [0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0]}, {"name": "Livia", "vals": [0, 0, 12, 0, 0, 0, 0, 0, 0, 0, 0]}, {"name": "Maisa", "vals": [1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 2]}, {"name": "Nelson", "vals": [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]}], "n_appts_mo": 139}''')

COLORS  = ["#6366f1","#10b981","#f59e0b","#ef4444","#8b5cf6",
           "#14b8a6","#f97316","#ec4899","#06b6d4","#84cc16","#3b82f6","#a855f7"]
META_MENSAL = 100_000
TODAY_MONTH = "Outubro/2026"

RFV_DATA = json.loads('{"total_patients": 1871, "seg_labels": ["Campe\\u00f5es", "Leais", "Potenciais", "Novos / Promissores", "Em Risco", "Inativos"], "seg_counts": [247, 349, 241, 286, 378, 370], "seg_vals": [2041151.11, 1335185.47, 108887.0, 108590.1, 1085266.29, 221769.17], "seg_rec": [66, 183, 249, 77, 687, 754], "seg_freq": [25.4, 12.6, 4.0, 2.2, 11.7, 2.9], "champions": 247, "loyal": 349, "at_risk": 378, "inactive": 370, "new_promise": 286, "potential": 241, "top20": [{"name": "Rodrigo Flores Da Silva Aquino", "rec": 13, "freq": 29, "val": 5707.48, "R": 5, "F": 5, "V": 5, "rfv": 15, "seg": "Campe\\u00f5es"}, {"name": "Emanuely Cristine De Andrade Moraes Araujo", "rec": 27, "freq": 24, "val": 3433.82, "R": 5, "F": 5, "V": 5, "rfv": 15, "seg": "Campe\\u00f5es"}, {"name": "Marcio Valerio Figueiredo Farias", "rec": 35, "freq": 27, "val": 9299.79, "R": 5, "F": 5, "V": 5, "rfv": 15, "seg": "Campe\\u00f5es"}, {"name": "Geovanna Nathyele Rodrigues Duarte Cristaldo", "rec": 19, "freq": 24, "val": 5193.22, "R": 5, "F": 5, "V": 5, "rfv": 15, "seg": "Campe\\u00f5es"}, {"name": "Isabelly Alves Monteiro", "rec": 58, "freq": 29, "val": 10902.96, "R": 5, "F": 5, "V": 5, "rfv": 15, "seg": "Campe\\u00f5es"}, {"name": "Valdevino Augusto Da Silva", "rec": 19, "freq": 16, "val": 39534.49, "R": 5, "F": 5, "V": 5, "rfv": 15, "seg": "Campe\\u00f5es"}, {"name": "Arthur Jose Dias Dos Santos", "rec": 21, "freq": 19, "val": 16351.43, "R": 5, "F": 5, "V": 5, "rfv": 15, "seg": "Campe\\u00f5es"}, {"name": "Sulimayra Da Silva Santana", "rec": 13, "freq": 35, "val": 9089.28, "R": 5, "F": 5, "V": 5, "rfv": 15, "seg": "Campe\\u00f5es"}, {"name": "Leonardo Vaz De Lima Gomes", "rec": 9, "freq": 27, "val": 5657.56, "R": 5, "F": 5, "V": 5, "rfv": 15, "seg": "Campe\\u00f5es"}, {"name": "Patricia Rejane Figueiredo Faria", "rec": 30, "freq": 76, "val": 24109.16, "R": 5, "F": 5, "V": 5, "rfv": 15, "seg": "Campe\\u00f5es"}, {"name": "Marcus Vinicius Jonas De Barros", "rec": 30, "freq": 16, "val": 3281.22, "R": 5, "F": 5, "V": 5, "rfv": 15, "seg": "Campe\\u00f5es"}, {"name": "Dicla Santos Gueiros", "rec": 14, "freq": 20, "val": 8142.95, "R": 5, "F": 5, "V": 5, "rfv": 15, "seg": "Campe\\u00f5es"}, {"name": "Clarindo Melo De Sa", "rec": 27, "freq": 47, "val": 7767.0, "R": 5, "F": 5, "V": 5, "rfv": 15, "seg": "Campe\\u00f5es"}, {"name": "Cleomar De Morais Goncalves", "rec": 57, "freq": 30, "val": 10844.33, "R": 5, "F": 5, "V": 5, "rfv": 15, "seg": "Campe\\u00f5es"}, {"name": "Paulo Milkem Abdala", "rec": 16, "freq": 58, "val": 45086.67, "R": 5, "F": 5, "V": 5, "rfv": 15, "seg": "Campe\\u00f5es"}, {"name": "Silvia Moura Silva Brizido", "rec": 57, "freq": 57, "val": 17818.16, "R": 5, "F": 5, "V": 5, "rfv": 15, "seg": "Campe\\u00f5es"}, {"name": "Nickolas Miguel Caninde Hall", "rec": 26, "freq": 34, "val": 11545.0, "R": 5, "F": 5, "V": 5, "rfv": 15, "seg": "Campe\\u00f5es"}, {"name": "Luiza Helena Haddad Coutinho", "rec": 14, "freq": 42, "val": 9392.46, "R": 5, "F": 5, "V": 5, "rfv": 15, "seg": "Campe\\u00f5es"}, {"name": "Katyele Gon\\u00e7alves Silva", "rec": 62, "freq": 24, "val": 5677.63, "R": 5, "F": 5, "V": 5, "rfv": 15, "seg": "Campe\\u00f5es"}, {"name": "Marcia Dos Santos Fonseca Fantin", "rec": 12, "freq": 66, "val": 10798.29, "R": 5, "F": 5, "V": 5, "rfv": 15, "seg": "Campe\\u00f5es"}]}')

gerado_em = "15/10/2026 14:42"

def J(x):
    import json
    return json.dumps(x, ensure_ascii=False)

html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Dashboard Klinik Odontologia</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=DM+Sans:wght@700&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{
  --bg:#07111d;--bg2:#0d1a2d;--bg3:#132136;--bg4:#0a1626;
  --border:#1a3352;--text:#e8f0fa;--text2:#93aec8;--text3:#546e8a;
  --blue:#2196f3;--green:#00c896;--purple:#8b5cf6;--red:#f0455a;
  --amber:#f5a623;--cyan:#00bcd4;--pink:#ec4899;--indigo:#5c6bc0;
  --teal:#00acc1;--brand:#0288d1;
}}
body{{font-family:'Inter',system-ui,-apple-system,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;font-size:14px;line-height:1.5}}
header{{background:linear-gradient(135deg,#061527 0%,#0a2540 45%,#0d3060 100%);
  padding:14px 28px;display:flex;justify-content:space-between;align-items:center;
  border-bottom:1px solid #0288d133;box-shadow:0 4px 24px #00000066;
  position:sticky;top:0;z-index:100}}
header h1{{font-size:1.3rem;font-weight:700;font-family:'DM Sans',sans-serif;letter-spacing:-.3px}} header h1 span{{color:#4fc3f7;letter-spacing:0}}
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
  <div style="display:flex;align-items:center;gap:14px">
    <div style="width:42px;height:42px;background:linear-gradient(135deg,#0288d1,#00acc1);border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:1.4rem;box-shadow:0 4px 12px #0288d144;flex-shrink:0">🦷</div>
    <div>
      <h1><span>Klinik</span> Odontologia</h1>
      <small style="color:#546e8a;font-size:.68rem;letter-spacing:.5px;text-transform:uppercase">Dashboard Executivo · v2.1</small>
    </div>
  </div>
  <div style="text-align:right">
    <div class="period-badge" id="period-badge">📅 —</div>
    <div class="updated">⟳ Atualizado em {gerado_em}</div>
  </div>
</header>

<div class="topbar">
  <div class="tabs">
    <div class="tab active"  onclick="sw(0)">⚡ Executivo</div>
    <div class="tab"         onclick="sw(1)">💰 Financeiro</div>
    <div class="tab"         onclick="sw(2)">🦷 Clínico</div>
    <div class="tab"         onclick="sw(3)">📊 Comercial</div>
    <div class="tab"         onclick="sw(4)">📅 Operacional</div>
    <div class="tab"         onclick="sw(5)">📈 Produtividade</div>
    <div class="tab"         onclick="sw(6)">🎯 RFV</div>
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

  <!-- INSIGHTS AUTOMÁTICOS -->
  <div class="stitle">💡 Insights do Período</div>
  <div id="insights-panel" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:10px;margin-bottom:16px"></div>
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
    <div class="kpi" id="meta-card"><label>Meta R$ 100k</label><div class="val" id="f-meta-pct">—</div><div class="sub">da meta atingida</div></div>
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

<!-- TAB 5 — PRODUTIVIDADE -->
<div class="panel" id="p5">
  <div class="stitle">Produtividade por Dentista</div>

  <!-- Tabela periódica (responde ao seletor MAT/MQT/YTD) -->
  <div class="card" style="margin-bottom:18px">
    <h3 style="margin-bottom:12px">Produção por Dentista <span id="pd-period-label" style="font-size:.72rem;color:var(--text3);font-weight:400"></span></h3>
    <table class="dtable">
      <thead>
        <tr>
          <th>Dentista</th>
          <th style="text-align:center">Cadeira</th>
          <th class="num">Atend.</th>
          <th class="num">Receita</th>
          <th class="num">Ticket Méd.</th>
          <th class="num">Conversão</th>
        </tr>
      </thead>
      <tbody id="dent-period-rows"></tbody>
      <tfoot id="dent-period-foot"></tfoot>
    </table>
    <div style="font-size:.68rem;color:var(--text3);margin-top:8px">* Receita = soma dos valores dos procedimentos executados por cada dentista. Ticket médio = Receita ÷ Atendimentos.</div>
  </div>

  <!-- Detalhe diário — mês atual -->
  <div class="stitle" style="font-size:.78rem;color:var(--text3);margin:4px 0 10px">Detalhe Diário — {TODAY_MONTH}</div>
  <div class="kpi-grid">
    <div class="kpi cyan"><label>Méd. Agend./Dia</label><div class="val" id="pd-sched">—</div></div>
    <div class="kpi green"><label>Méd. Atend./Dia</label><div class="val" id="pd-done">—</div></div>
    <div class="kpi indigo"><label>Receita Méd./Dia</label><div class="val" id="pd-rev">—</div></div>
    <div class="kpi blue"><label>Ocup. Cadeira 1</label><div class="val" id="pd-c1">—</div></div>
    <div class="kpi purple"><label>Ocup. Cadeira 2</label><div class="val" id="pd-c2">—</div></div>
  </div>
  <div class="g2e">
    <div class="card"><h3>Agendamentos por Dia Útil</h3><canvas id="schedDayChart"></canvas></div>
    <div class="card"><h3>Atendimentos por Dentista / Dia</h3><canvas id="dentDayChart"></canvas></div>
  </div>
  <div class="g2e">
    <div class="card">
      <h3>Ocupação das Cadeiras (%)</h3>
      <div style="font-size:.71rem;color:var(--text3);margin:-2px 0 10px">C-1: Maisa · Fernanda · João · Nelson &nbsp;|&nbsp; C-2: Adrieli · Barbara · Caroline &nbsp;·&nbsp; Base: 600 min/dia. Acima de 100% = horas extras.</div>
      <canvas id="chairChart"></canvas>
    </div>
    <div class="card">
      <h3>Resumo Diário por Dentista</h3>
      <table class="dtable">
        <thead><tr><th>Dentista</th><th class="num">Agend.</th><th class="num">Méd./Dia</th><th style="text-align:center">Cadeira</th></tr></thead>
        <tbody id="dent-day-rows"></tbody>
      </table>
      <div style="margin-top:14px;font-size:.75rem;color:var(--text3)">
        Receita diária estimada (MQT ÷ dias úteis):<br>
        <strong id="pd-rev2" style="color:var(--green);font-size:.95rem">—</strong>
      </div>
    </div>
  </div>
</div>

<!-- TAB 6 — RFV -->
<div class="panel" id="p6">
  <div class="stitle">Análise RFV — Recência · Frequência · Valor</div>
  <div class="kpi-grid">
    <div class="kpi blue"><label>Total de Pacientes</label><div class="val" id="rfv-total">—</div><div class="sub">com histórico de pagamento</div></div>
    <div class="kpi amber"><label>🏆 Campeões</label><div class="val" id="rfv-champ">—</div><div class="sub">alta recência, freq. e valor</div></div>
    <div class="kpi green"><label>❤ Leais</label><div class="val" id="rfv-loyal">—</div><div class="sub">relacionamento consolidado</div></div>
    <div class="kpi cyan"><label>🌱 Novos/Promissores</label><div class="val" id="rfv-new">—</div><div class="sub">recentes, baixa freq. ainda</div></div>
    <div class="kpi red"><label>⚠ Em Risco</label><div class="val" id="rfv-risk">—</div><div class="sub">freq. alta mas sumiram</div></div>
    <div class="kpi purple"><label>💤 Inativos</label><div class="val" id="rfv-inactive">—</div><div class="sub">última visita há +1 ano</div></div>
  </div>
  <div class="g2">
    <div class="card"><h3>Pacientes por Segmento</h3><canvas id="rfvSegChart" style="max-height:280px"></canvas></div>
    <div class="card"><h3>Receita por Segmento (R$)</h3><canvas id="rfvValChart" style="max-height:280px"></canvas></div>
  </div>
  <div class="g2">
    <div class="card"><h3>Recência Média por Segmento (dias)</h3><canvas id="rfvRecChart" style="max-height:220px"></canvas></div>
    <div class="card"><h3>Frequência Média por Segmento (consultas)</h3><canvas id="rfvFreqChart" style="max-height:220px"></canvas></div>
  </div>
  <div class="stitle">Top 20 Pacientes — Maior Score RFV</div>
  <div class="card" style="overflow-x:auto">
    <table class="dtable">
      <thead><tr><th>#</th><th>Paciente</th><th class="num">Recência (dias)</th><th class="num">Frequência</th><th class="num">Valor Total</th><th class="num">R</th><th class="num">F</th><th class="num">V</th><th class="num">Score</th><th>Segmento</th></tr></thead>
      <tbody id="rfv-top-rows"></tbody>
    </table>
  </div>
  <div style="font-size:.67rem;color:var(--text3);margin-top:10px;padding:0 4px">
    <strong>Como interpretar:</strong> R = Recência (5 = visitou recentemente) · F = Frequência (5 = mais visitas) · V = Valor (5 = maior gasto) · Score = R+F+V (máx 15).
    Segmentação com base em todo o histórico de atendimentos desde Nov/2022.
  </div>
</div>

<footer>Klinik Odontologia — Dashboard Executivo v2.1 — Dados via Clinicorp API — {gerado_em}</footer>

<script>
const PERIODS  = {J(PERIODS)};
const DAILY    = {J(DAILY)};
const COLORS   = {J(COLORS)};
const META     = {J(META_MENSAL)};
const RFV_DATA = {J(RFV_DATA)};

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
    convChart,goalChart,howMetChart,apptMonthChart,missChart,howMetChart2,
    schedDayChart,dentDayChart,chairChart;

const C='#94a3b8',G1='#1e293b',G2='#334155';
const mkR=()=>({{ticks:{{color:'#64748b',font:{{size:10}},callback:v=>'R$'+v.toLocaleString('pt-BR')}},grid:{{color:G2}}}});
const mkN=()=>({{ticks:{{color:'#64748b',font:{{size:10}}}},grid:{{color:G2}}}});
const mkP=()=>({{ticks:{{color:'#64748b',font:{{size:10}},callback:v=>v+'%'}},grid:{{color:G2}}}});
const mkX=()=>({{ticks:{{color:'#64748b',font:{{size:10}}}},grid:{{color:G1}}}});
const leg={{labels:{{color:C,boxWidth:11,font:{{size:10}}}}}};
const legR={{position:'right',labels:{{color:C,boxWidth:10,font:{{size:10}}}}}};
function fitY(c){{
  const vals=c.data.datasets.flatMap(d=>(d.data||[]).filter(v=>v!=null&&!isNaN(v)));
  if(!vals.length)return;
  const lo=Math.min(...vals),hi=Math.max(...vals);
  const rng=hi-lo||Math.abs(hi)||1;
  const pad=rng*0.12;
  const mag=Math.pow(10,Math.floor(Math.log10(rng)));
  c.options.scales.y.min=Math.floor((lo-pad)/mag)*mag;
  c.options.scales.y.max=Math.ceil((hi+pad)/mag)*mag;
  c.update('none');
}}

function initCharts(){{
  const d=PERIODS.mat;
  trendChart=new Chart(document.getElementById('trendChart'),{{type:'line',
    data:{{labels:d.proj_labels,datasets:[
      {{label:'Receita',data:d.all_rev_hist,borderColor:'#10b981',backgroundColor:'#10b98122',fill:true,tension:.4,pointRadius:3,spanGaps:false}},
      {{label:'Despesa',data:d.all_exp_hist,borderColor:'#ef4444',backgroundColor:'#ef444422',fill:false,tension:.4,pointRadius:3,spanGaps:false}},
      {{label:'Proj. Receita',data:d.proj_rev_line,borderColor:'#10b981',borderDash:[7,3],backgroundColor:'transparent',tension:.4,pointRadius:5,pointStyle:'triangle',spanGaps:false}},
      {{label:'Proj. Despesa',data:d.proj_exp_line,borderColor:'#ef4444',borderDash:[7,3],backgroundColor:'transparent',tension:.4,pointRadius:5,pointStyle:'triangle',spanGaps:false}},
      {{label:'Meta R$100k',data:d.proj_labels.map(()=>META),borderColor:'#f59e0b',borderDash:[5,5],backgroundColor:'transparent',tension:0,pointRadius:0,fill:false}},
    ]}},options:{{responsive:true,maintainAspectRatio:true,interaction:{{mode:'index',intersect:false}},plugins:{{legend:leg}},scales:{{x:mkX(),y:mkR()}}}}
  }});
  finChart=new Chart(document.getElementById('finChart'),{{type:'bar',
    data:{{labels:d.fin_labels,datasets:[
      {{label:'Receita',data:d.fin_rev,backgroundColor:'#10b98133',borderColor:'#10b981',borderWidth:2,borderRadius:3}},
      {{label:'Despesa',data:d.fin_exp,backgroundColor:'#ef444433',borderColor:'#ef4444',borderWidth:2,borderRadius:3}},
      {{label:'Resultado',data:d.fin_profit,type:'line',borderColor:'#6366f1',backgroundColor:'#6366f122',fill:true,tension:.4,yAxisID:'y'}},
    ]}},options:{{responsive:true,maintainAspectRatio:true,interaction:{{mode:'index',intersect:false}},plugins:{{legend:leg}},scales:{{x:mkX(),y:mkR()}}}}
  }});
  marginChart=new Chart(document.getElementById('marginChart'),{{type:'line',
    data:{{labels:d.fin_labels,datasets:[
      {{label:'Margem %',data:d.fin_margin,borderColor:'#f59e0b',backgroundColor:'#f59e0b22',fill:true,tension:.4,pointRadius:4}},
    ]}},options:{{responsive:true,maintainAspectRatio:true,plugins:{{legend:leg}},scales:{{x:mkX(),y:mkP()}}}}
  }});
  fitY(finChart);fitY(marginChart);
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
    options:{{responsive:true,maintainAspectRatio:true,interaction:{{mode:'index',intersect:false}},plugins:{{legend:leg}},scales:{{x:mkX(),y:mkR()}}}}
  }});
  apptChart=new Chart(document.getElementById('apptChart'),{{type:'bar',
    data:{{labels:d.appt_prof.map(x=>x.name),datasets:[{{label:'Agendamentos',data:d.appt_prof.map(x=>x.cnt),backgroundColor:'#8b5cf655',borderColor:'#8b5cf6',borderWidth:2,borderRadius:3}}]}},
    options:{{responsive:true,maintainAspectRatio:true,indexAxis:'y',plugins:{{legend:{{display:false}}}},scales:{{x:mkN(),y:{{ticks:{{color:'#64748b',font:{{size:10}}}},grid:{{color:G1}}}}}}}}
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
    ]}},options:{{responsive:true,maintainAspectRatio:true,plugins:{{legend:leg}},scales:{{x:mkX(),y:mkR()}}}}
  }});
  howMetChart=new Chart(document.getElementById('howMetChart'),{{type:'bar',
    data:{{labels:d.how_met.map(x=>x.name),datasets:[{{label:'Pacientes',data:d.how_met.map(x=>x.cnt),
      backgroundColor:COLORS.slice(0,d.how_met.length).map(c=>c+'55'),
      borderColor:COLORS.slice(0,d.how_met.length),borderWidth:2,borderRadius:3}}]}},
    options:{{responsive:true,maintainAspectRatio:true,indexAxis:'y',plugins:{{legend:{{display:false}}}},scales:{{x:mkN(),y:{{ticks:{{color:'#64748b',font:{{size:10}}}},grid:{{color:G1}}}}}}}}
  }});
  apptMonthChart=new Chart(document.getElementById('apptMonthChart'),{{type:'bar',
    data:{{labels:d.appt_month_labels,datasets:[{{label:'Agendamentos',data:d.appt_month_vals,backgroundColor:'#06b6d455',borderColor:'#06b6d4',borderWidth:2,borderRadius:3}}]}},
    options:{{responsive:true,maintainAspectRatio:true,plugins:{{legend:{{display:false}}}},scales:{{x:mkX(),y:mkN()}}}}
  }});
  missChart=new Chart(document.getElementById('missChart'),{{type:'bar',
    data:{{labels:d.miss_labels,datasets:[{{label:'Faltas',data:d.miss_vals,backgroundColor:'#f59e0b55',borderColor:'#f59e0b',borderWidth:2,borderRadius:3}}]}},
    options:{{responsive:true,maintainAspectRatio:true,plugins:{{legend:{{display:false}}}},scales:{{x:mkX(),y:mkN()}}}}
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
  trendChart.data.datasets[4].data=d.proj_labels.map(()=>META);
  trendChart.update();
  // Financial P&L
  finChart.data.labels=d.fin_labels;
  finChart.data.datasets[0].data=d.fin_rev;
  finChart.data.datasets[1].data=d.fin_exp;
  finChart.data.datasets[2].data=d.fin_profit;
  finChart.update();fitY(finChart);
  // Margin
  marginChart.data.labels=d.fin_labels;
  marginChart.data.datasets[0].data=d.fin_margin;
  marginChart.update();fitY(marginChart);
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
  const metaPct=Math.round(d.avg_monthly_rev/META*100);
  txt('f-meta-pct',metaPct+'%');
  const mc=document.getElementById('meta-card');
  if(mc) mc.className='kpi '+(d.avg_monthly_rev>=META?'green':'red');

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
  html('dent-period-rows',buildDentPeriodRows(d));
  html('dent-period-foot',buildDentPeriodFoot(d));
  txt('pd-period-label','('+d.from+' → '+d.to+')');

  // ── Charts ──
  updateCharts(d);

  // ── Insights ──
  buildInsights(d);
}}

// ── Insights automáticos ──────────────────────────────────────────────────────
function buildInsights(d){{
  const el=document.getElementById('insights-panel');
  if(!el) return;
  const cards=[];

  // 1 — Melhor mês do período
  if(d.fin_labels && d.fin_rev && d.fin_rev.length){{
    const vals=d.fin_rev.filter(v=>v!=null&&!isNaN(v));
    if(vals.length){{
      const maxVal=Math.max(...vals);
      const idx=d.fin_rev.indexOf(maxVal);
      const lbl=d.fin_labels[idx]||'';
      const metaPct=Math.round(maxVal/META*100);
      const isAboveMeta=maxVal>=META;
      cards.push(`<div style="background:var(--bg3);border:1px solid ${{isAboveMeta?'#10b98133':'var(--border)'}};border-radius:10px;padding:14px 16px">
        <div style="font-size:.7rem;color:var(--text3);text-transform:uppercase;letter-spacing:.5px;margin-bottom:6px">🏆 Melhor mês (${{d.from.split('/')[1]||''}})</div>
        <div style="font-size:.95rem;font-weight:600;color:var(--text)">${{lbl}} · R$ ${{maxVal.toLocaleString('pt-BR',{{minimumFractionDigits:0,maximumFractionDigits:0}})}}</div>
        <div style="font-size:.78rem;color:${{isAboveMeta?'#10b981':'#f5a623'}};margin-top:4px">${{isAboveMeta?'✅ Acima':'⚠️ Abaixo'}} da meta · ${{metaPct}}% de R$ 100k</div>
      </div>`);
    }}
  }}

  // 2 — Tendência de receita (últimos 3 meses vs anteriores)
  if(d.fin_rev && d.fin_rev.length>=4){{
    const valid=d.fin_rev.filter(v=>v!=null&&!isNaN(v));
    if(valid.length>=4){{
      const half=Math.floor(valid.length/2);
      const older=valid.slice(0,half).reduce((a,b)=>a+b,0)/half;
      const newer=valid.slice(-half).reduce((a,b)=>a+b,0)/half;
      const chg=Math.round((newer-older)/older*100);
      const up=chg>=0;
      cards.push(`<div style="background:var(--bg3);border:1px solid ${{up?'#10b98133':'#ef444433'}};border-radius:10px;padding:14px 16px">
        <div style="font-size:.7rem;color:var(--text3);text-transform:uppercase;letter-spacing:.5px;margin-bottom:6px">📈 Tendência de Receita</div>
        <div style="font-size:.95rem;font-weight:600;color:${{up?'#10b981':'#f0455a'}}">${{up?'Alta':'Queda'}} de ${{Math.abs(chg)}}% na 2ª metade do período</div>
        <div style="font-size:.78rem;color:var(--text2);margin-top:4px">Média anterior: R$ ${{Math.round(older).toLocaleString('pt-BR')}} · Recente: R$ ${{Math.round(newer).toLocaleString('pt-BR')}}</div>
      </div>`);
    }}
  }}

  // 3 — No-show
  if(d.noshow_rate!==null && d.noshow_rate!==undefined){{
    const ok=d.noshow_rate<20;
    const critical=d.noshow_rate>=35;
    const color=critical?'#f0455a':ok?'#10b981':'#f5a623';
    const icon=critical?'🚨':ok?'✅':'⚠️';
    cards.push(`<div style="background:var(--bg3);border:1px solid ${{color}}33;border-radius:10px;padding:14px 16px">
      <div style="font-size:.7rem;color:var(--text3);text-transform:uppercase;letter-spacing:.5px;margin-bottom:6px">🗓️ Taxa de No-Show</div>
      <div style="font-size:.95rem;font-weight:600;color:${{color}}">${{icon}} ${{d.noshow_rate}}% de faltas (${{d.total_misses}} no período)</div>
      <div style="font-size:.78rem;color:var(--text2);margin-top:4px">${{critical?'Atenção urgente: perda significativa de receita':ok?'Dentro do limite aceitável (<20%)':'Monitorar — meta abaixo de 20%'}}</div>
    </div>`);
  }}

  // 4 — Conversão de orçamentos
  if(d.conv_rate!==undefined){{
    const good=d.conv_rate>=60;
    const low=d.conv_rate<40;
    const color=good?'#10b981':low?'#f0455a':'#f5a623';
    cards.push(`<div style="background:var(--bg3);border:1px solid ${{color}}33;border-radius:10px;padding:14px 16px">
      <div style="font-size:.7rem;color:var(--text3);text-transform:uppercase;letter-spacing:.5px;margin-bottom:6px">💼 Conversão de Orçamentos</div>
      <div style="font-size:.95rem;font-weight:600;color:${{color}}">${{d.conv_rate}}% de aprovação (${{d.total_appr}} de ${{d.total_est}})</div>
      <div style="font-size:.78rem;color:var(--text2);margin-top:4px">${{good?'Excelente conversão ≥60%':low?'Baixa conversão — revisar abordagem comercial':'Conversão moderada — meta acima de 60%'}}</div>
    </div>`);
  }}

  // 5 — RFV snapshot (sempre visível, dados globais)
  const champPct=Math.round(RFV_DATA.champions/RFV_DATA.total_patients*100);
  const riskPct=Math.round((RFV_DATA.at_risk+RFV_DATA.inactive)/RFV_DATA.total_patients*100);
  cards.push(`<div style="background:var(--bg3);border:1px solid #f59e0b33;border-radius:10px;padding:14px 16px">
    <div style="font-size:.7rem;color:var(--text3);text-transform:uppercase;letter-spacing:.5px;margin-bottom:6px">🎯 Base RFV · ${{RFV_DATA.total_patients.toLocaleString('pt-BR')}} pacientes</div>
    <div style="font-size:.95rem;font-weight:600;color:#f59e0b">⭐ ${{RFV_DATA.champions}} Campeões (${{champPct}}%) · ⚠️ ${{RFV_DATA.at_risk+RFV_DATA.inactive}} em risco (${{riskPct}}%)</div>
    <div style="font-size:.78rem;color:var(--text2);margin-top:4px">Focar retenção nos Em Risco + Inativos — ${{riskPct}}% da base precisa de ação</div>
  </div>`);

  // 6 — Meta mensal média
  const avgRev=d.avg_monthly_rev||0;
  const metaGap=Math.round(META-avgRev);
  const metaOk=avgRev>=META;
  cards.push(`<div style="background:var(--bg3);border:1px solid ${{metaOk?'#10b98133':'#f0455a33'}};border-radius:10px;padding:14px 16px">
    <div style="font-size:.7rem;color:var(--text3);text-transform:uppercase;letter-spacing:.5px;margin-bottom:6px">🎯 Meta Mensal · R$ 100k</div>
    <div style="font-size:.95rem;font-weight:600;color:${{metaOk?'#10b981':'#f0455a'}}">${{metaOk?'✅ Meta atingida em média':'❌ Déficit médio de R$ '+Math.abs(metaGap).toLocaleString('pt-BR')+'/mês'}}</div>
    <div style="font-size:.78rem;color:var(--text2);margin-top:4px">Média mensal do período: R$ ${{Math.round(avgRev).toLocaleString('pt-BR')}} · ${{Math.round(avgRev/META*100)}}% da meta</div>
  </div>`);

  el.innerHTML=cards.join('');
}}

// ── Period switch ─────────────────────────────────────────────────────────────
function switchPeriod(p){{
  document.querySelectorAll('.pbtn').forEach(b=>b.classList.toggle('active',b.dataset.p===p));
  renderPeriod(p);
}}

// ── Init ──────────────────────────────────────────────────────────────────────
// ── Produtividade Diária — estático (sempre mês atual) ────────────────────────
function buildDentPeriodRows(d){{
  if(!d.dent_table||!d.dent_table.length) return '<tr><td colspan="6" style="text-align:center;color:var(--text3);padding:16px">Sem dados para o período</td></tr>';
  const totalRev=d.dent_table.reduce((s,r)=>s+r.rev,0)||1;
  return d.dent_table.map(r=>{{
    const pct=Math.round(r.rev/totalRev*100);
    const chLabel=r.chair===1?'<span style="color:#60a5fa">C-1</span>':'<span style="color:#a78bfa">C-2</span>';
    return `<tr>
      <td>${{r.name}}</td>
      <td style="text-align:center">${{chLabel}}</td>
      <td class="num">${{r.appts.toLocaleString('pt-BR')}}</td>
      <td class="num">
        ${{fmt(r.rev)}}
        <div style="height:3px;background:var(--border);border-radius:2px;margin-top:3px">
          <div style="height:3px;width:${{pct}}%;background:#10b981;border-radius:2px"></div>
        </div>
      </td>
      <td class="num">${{fmt(r.ticket)}}</td>
      <td class="num">${{r.conv}}%</td>
    </tr>`;
  }}).join('');
}}
function buildDentPeriodFoot(d){{
  if(!d.dent_table||!d.dent_table.length) return '';
  const totAppts=d.dent_table.reduce((s,r)=>s+r.appts,0);
  const totRev=d.dent_table.reduce((s,r)=>s+r.rev,0);
  const totTicket=totAppts>0?totRev/totAppts:0;
  return `<tr style="font-weight:600;border-top:2px solid var(--border)">
    <td>Total</td><td></td>
    <td class="num">${{totAppts.toLocaleString('pt-BR')}}</td>
    <td class="num">${{fmt(totRev)}}</td>
    <td class="num">${{fmt(totTicket)}}</td>
    <td class="num">${{d.conv_rate}}%</td>
  </tr>`;
}}

function buildDentDayRows(d){{
  const c1set=new Set(['Maisa','Fernanda','João','Joao','Schussler','Nelson','Oshiro','Pangoni']);
  return d.dent_series.map(s=>{{
    const total=s.vals.reduce((a,b)=>a+b,0);
    const worked=s.vals.filter(v=>v>0).length||1;
    const avg=(total/worked).toFixed(1);
    const chair=c1set.has(s.name)?'C-1':'C-2';
    return `<tr><td>${{s.name}}</td><td class="num">${{total}}</td><td class="num">${{avg}}</td><td>${{chair}}</td></tr>`;
  }}).join('');
}}

function initDailyCharts(){{
  const d=DAILY;
  const lbls=d.day_labels;
  txt('pd-sched',d.avg_sched_d);
  txt('pd-done', d.avg_appts_d);
  txt('pd-rev',  fmt(d.avg_daily_rev));
  txt('pd-rev2', fmt(d.avg_daily_rev));
  txt('pd-c1',   d.avg_c1+'%');
  txt('pd-c2',   d.avg_c2+'%');
  html('dent-day-rows',buildDentDayRows(d));

  schedDayChart=new Chart(document.getElementById('schedDayChart'),{{
    type:'line',
    data:{{labels:lbls,datasets:[{{
      label:'Agendamentos',data:d.sched_vals,
      borderColor:'#06b6d4',backgroundColor:'#06b6d422',
      fill:true,tension:.35,pointRadius:4,pointHoverRadius:6
    }}]}},
    options:{{responsive:true,maintainAspectRatio:true,
      plugins:{{legend:leg,tooltip:{{callbacks:{{label:ctx=>ctx.parsed.y+' agend.'}}}}}},
      scales:{{x:mkX(),y:{{...mkN(),beginAtZero:true}}}}
    }}
  }});

  const dentColors=COLORS.slice(0,d.dent_names.length);
  dentDayChart=new Chart(document.getElementById('dentDayChart'),{{
    type:'line',
    data:{{labels:lbls,datasets:d.dent_series.map((s,i)=>
      ({{label:s.name,data:s.vals,
         borderColor:COLORS[i%COLORS.length],backgroundColor:'transparent',
         tension:.35,pointRadius:3,pointHoverRadius:5,fill:false}}))
    }},
    options:{{responsive:true,maintainAspectRatio:true,
      interaction:{{mode:'index',intersect:false}},
      plugins:{{legend:leg}},
      scales:{{x:mkX(),y:{{...mkN(),beginAtZero:true}}}}
    }}
  }});

  chairChart=new Chart(document.getElementById('chairChart'),{{
    type:'line',
    data:{{labels:lbls,datasets:[
      {{label:'Cadeira 1',data:d.chair1_util,
        borderColor:'#3b82f6',backgroundColor:'#3b82f622',fill:true,tension:.35,pointRadius:4}},
      {{label:'Cadeira 2',data:d.chair2_util,
        borderColor:'#8b5cf6',backgroundColor:'#8b5cf622',fill:true,tension:.35,pointRadius:4}},
    ]}},
    options:{{responsive:true,maintainAspectRatio:true,
      interaction:{{mode:'index',intersect:false}},
      plugins:{{legend:leg,tooltip:{{callbacks:{{label:ctx=>ctx.parsed.y+'%'}}}}}},
      scales:{{x:mkX(),y:{{
        ticks:{{color:'#64748b',font:{{size:10}},callback:v=>v+'%'}},
        grid:{{color:G2}},beginAtZero:true,
        suggestedMax:100
      }}}}
    }}
  }});
}}

initCharts();
initDailyCharts();
renderPeriod('mat');

// ── RFV ───────────────────────────────────────────────────────────────────────
let rfvSegChart,rfvValChart,rfvRecChart,rfvFreqChart;
let rfvInited=false;

const SEG_COLORS={{
  'Campeões':'#f59e0b',
  'Leais':'#10b981',
  'Potenciais':'#06b6d4',
  'Novos / Promissores':'#6366f1',
  'Em Risco':'#ef4444',
  'Inativos':'#64748b'
}};

function initRFV(){{
  if(rfvInited)return;
  rfvInited=true;
  const d=RFV_DATA;
  const colors=d.seg_labels.map(s=>SEG_COLORS[s]||'#94a3b8');

  txt('rfv-total',d.total_patients.toLocaleString('pt-BR'));
  txt('rfv-champ', d.champions);
  txt('rfv-loyal', d.loyal);
  txt('rfv-new',   d.new_promise);
  txt('rfv-risk',  d.at_risk);
  txt('rfv-inactive',d.inactive);

  rfvSegChart=new Chart(document.getElementById('rfvSegChart'),{{
    type:'doughnut',
    data:{{labels:d.seg_labels,datasets:[{{data:d.seg_counts,backgroundColor:colors,borderWidth:1,borderColor:'#0a0f1e'}}]}},
    options:{{responsive:true,maintainAspectRatio:true,plugins:{{legend:{{labels:{{color:'#94a3b8',boxWidth:12,font:{{size:11}}}}}},tooltip:{{callbacks:{{label:ctx=>ctx.label+': '+ctx.parsed+' pacientes'}}}}}}}}
  }});

  rfvValChart=new Chart(document.getElementById('rfvValChart'),{{
    type:'bar',
    data:{{labels:d.seg_labels,datasets:[{{label:'Receita Total',data:d.seg_vals,backgroundColor:colors,borderRadius:4}}]}},
    options:{{responsive:true,maintainAspectRatio:true,plugins:{{legend:{{display:false}},tooltip:{{callbacks:{{label:ctx=>'R$ '+ctx.parsed.y.toLocaleString('pt-BR',{{minimumFractionDigits:2}})}}}}}},scales:{{x:mkX(),y:mkR()}}}}
  }});

  rfvRecChart=new Chart(document.getElementById('rfvRecChart'),{{
    type:'bar',
    data:{{labels:d.seg_labels,datasets:[{{label:'Recência (dias)',data:d.seg_rec,backgroundColor:colors,borderRadius:4}}]}},
    options:{{responsive:true,maintainAspectRatio:true,plugins:{{legend:{{display:false}},tooltip:{{callbacks:{{label:ctx=>ctx.parsed.y+' dias'}}}}}},scales:{{x:mkX(),y:{{...mkN(),beginAtZero:true}}}}}}
  }});

  rfvFreqChart=new Chart(document.getElementById('rfvFreqChart'),{{
    type:'bar',
    data:{{labels:d.seg_labels,datasets:[{{label:'Freq. Média',data:d.seg_freq,backgroundColor:colors,borderRadius:4}}]}},
    options:{{responsive:true,maintainAspectRatio:true,plugins:{{legend:{{display:false}},tooltip:{{callbacks:{{label:ctx=>ctx.parsed.y+' consultas (média)'}}}}}},scales:{{x:mkX(),y:{{...mkN(),beginAtZero:true}}}}}}
  }});

  const segBadge={{
    'Campeões':'<span class="badge" style="background:#f59e0b22;color:#fbbf24">Campeão</span>',
    'Leais':'<span class="badge" style="background:#10b98122;color:#34d399">Leal</span>',
    'Potenciais':'<span class="badge" style="background:#06b6d422;color:#22d3ee">Potencial</span>',
    'Novos / Promissores':'<span class="badge" style="background:#6366f122;color:#818cf8">Novo</span>',
    'Em Risco':'<span class="badge" style="background:#ef444422;color:#f87171">Em Risco</span>',
    'Inativos':'<span class="badge" style="background:#33415522;color:#64748b">Inativo</span>'
  }};

  const rows=d.top20.map((p,i)=>`<tr>
    <td style="color:var(--text3)">${{i+1}}</td>
    <td>${{p.name}}</td>
    <td class="num">${{p.rec}} dias</td>
    <td class="num">${{p.freq}}</td>
    <td class="num">${{fmt(p.val)}}</td>
    <td class="num" style="color:#f59e0b;font-weight:700">${{p.R}}</td>
    <td class="num" style="color:#10b981;font-weight:700">${{p.F}}</td>
    <td class="num" style="color:#6366f1;font-weight:700">${{p.V}}</td>
    <td class="num" style="color:#60a5fa;font-weight:700">${{p.rfv}}</td>
    <td>${{segBadge[p.seg]||p.seg}}</td>
  </tr>`).join('');
  html('rfv-top-rows',rows);
}}

// Patch sw() para inicializar RFV ao abrir o tab
const _origSw=sw;
window.sw=function(n){{_origSw(n);if(n===6)initRFV();}};
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

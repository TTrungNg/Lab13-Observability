# Day 13 Observability Lab Report

> **Instruction**: Fill in all sections below. This report is designed to be parsed by an automated grading assistant. Ensure all tags (e.g., `[GROUP_NAME]`) are preserved.

## 1. Team Metadata

- [GROUP_NAME]:
- [REPO_URL]:
- [MEMBERS]:
  - Member A: Hà Việt Khánh | Role: Logging & PII
  - Member B: [Name] | Role: Tracing & Enrichment
  - Member C: [Name] | Role: SLO & Alerts
  - Member D: [Name] | Role: Load Test & Dashboard
  - Member E: [Name] | Role: Demo & Report

---

## 2. Group Performance (Auto-Verified)

- [VALIDATE_LOGS_FINAL_SCORE]: /100
- [TOTAL_TRACES_COUNT]:
- [PII_LEAKS_FOUND]:

---

## 3. Technical Evidence (Group)

### 3.1 Logging & Tracing

- [EVIDENCE_CORRELATION_ID_SCREENSHOT]: [Path to image]
- [EVIDENCE_PII_REDACTION_SCREENSHOT]: [Path to image]
- [EVIDENCE_TRACE_WATERFALL_SCREENSHOT]: [Path to image]
- [TRACE_WATERFALL_EXPLANATION]: (Briefly explain one interesting span in your trace)

### 3.2 Dashboard & SLOs

- [DASHBOARD_6_PANELS_SCREENSHOT]: [Path to image]
- [SLO_TABLE]:
  | SLI | Target | Window | Current Value |
  |---|---:|---|---:|
  | Latency P95 | < 3000ms | 28d | |
  | Error Rate | < 2% | 28d | |
  | Cost Budget | < $2.5/day | 1d | |

### 3.3 Alerts & Runbook

- [ALERT_RULES_SCREENSHOT]: [Path to image]
- [SAMPLE_RUNBOOK_LINK]: [docs/alerts.md#L...]

---

## 4. Incident Response (Group)

- [SCENARIO_NAME]: (e.g., rag_slow)
- [SYMPTOMS_OBSERVED]:
- [ROOT_CAUSE_PROVED_BY]: (List specific Trace ID or Log Line)
- [FIX_ACTION]:
- [PREVENTIVE_MEASURE]:

---

## 5. Individual Contributions & Evidence

### Hà Việt Khánh

- [TASKS_COMPLETED]:
  - Triển khai Middleware (Correlation ID): Viết `CorrelationIdMiddleware` xử lý `x-request-id` và truyền vào `structlog.contextvars` để đồng bộ log xuyên suốt ứng dụng.
  - Cấu hình Structlog: Cài đặt pipeline processor cho Structlog sinh log định dạng JSON, tự động thêm ISO timestamp, cấp độ log và lưu xuất ra `data/logs.jsonl` qua `JsonlFileProcessor`.
  - Phát triển bộ lọc dữ liệu ẩn danh (PII): Viết các regex rules trong `app/pii.py` để tra cứu và ẩn (redact) email, CCCD, địa chỉ VN và tích hợp logger processor `scrub_event` để gỡ bỏ thông tin nhạy cảm trước khi in log.
- [EVIDENCE_LINK]: Các lịch sử thay đổi file `app/middleware.py`, `app/logging_config.py`, `app/pii.py`

### [MEMBER_B_NAME]

- [TASKS_COMPLETED]:
- [EVIDENCE_LINK]:

### [MEMBER_C_NAME]

- [TASKS_COMPLETED]:
- [EVIDENCE_LINK]:

### [MEMBER_D_NAME]

- [TASKS_COMPLETED]:
- [EVIDENCE_LINK]:

### [Nguyễn Việt Trung]

- [TASKS_COMPLETED]: Built 6-panel observability dashboard (Latency P50/P95/P99, Traffic, Error Rate with breakdown, Cost over time, Tokens In/Out, Quality Score); added time-series metrics history to backend (`app/metrics.py`, `app/main.py`); served dashboard via FastAPI static files; configured SLO threshold lines and auto-refresh every 15s; collected grading evidence checklist in `docs/grading-evidence.md`
- [EVIDENCE_LINK]: app/static/dashboard.html, app/metrics.py, app/main.py, docs/grading-evidence.md

---

## 6. Bonus Items (Optional)

- [BONUS_COST_OPTIMIZATION]: (Description + Evidence)
- [BONUS_AUDIT_LOGS]: (Description + Evidence)
- [BONUS_CUSTOM_METRIC]: (Description + Evidence)

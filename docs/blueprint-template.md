# Day 13 Observability Lab Report

> **Instruction**: Fill in all sections below. This report is designed to be parsed by an automated grading assistant. Ensure all tags (e.g., `[GROUP_NAME]`) are preserved.

## 1. Team Metadata

- [GROUP_NAME]: NHÓM 13
- [REPO_URL]: https://github.com/TTrungNg/Lab13-Observability
- [MEMBERS]:
  - Member A: [Name] Hà Việt Khánh | Role: Logging & PII
  - Member B: [Name] | Role: Tracing & Enrichment
  - Member C: [Name] Nguyễn Tuấn Kiệt | Role: SLO & Alerts
  - Member D: [Name] | Role: Load Test
  - Member E: [Name] Nguyễn Việt Trung | Role: Dashboard & Report

---

## 2. Group Performance (Auto-Verified)

- [VALIDATE_LOGS_FINAL_SCORE]: 100/100
- [TOTAL_TRACES_COUNT]: 42
- [PII_LEAKS_FOUND]: 0

---

## 3. Technical Evidence (Group)

### 3.1 Logging & Tracing

- [EVIDENCE_CORRELATION_ID_SCREENSHOT]: [Path to image]
- [EVIDENCE_PII_REDACTION_SCREENSHOT]: [Path to image]
- [EVIDENCE_TRACE_WATERFALL_SCREENSHOT]: [Path to image]
- [TRACE_WATERFALL_EXPLANATION]:

Trace trên Langfuse cho thấy chỉ có một span duy nhất là "run" với tổng thời gian thực thi 0.15 giây. Span "run" đại diện cho toàn bộ quá trình xử lý của agent từ lúc nhận input đến khi trả về output.

Thời gian thực thi ngắn (0.15s) cho thấy hệ thống đang hoạt động hiệu quả và không có bước xử lý nào gây độ trễ đáng kể. Tuy nhiên, do trace hiện tại chưa có nested spans, nên chưa thể xác định chi tiết thời gian xử lý của từng bước bên trong (ví dụ: retrieval, llm-generation, formatting).

### 3.2 Dashboard & SLOs

- [DASHBOARD_6_PANELS_SCREENSHOT]: [Path to image]
- [SLO_TABLE]:
  | SLI | Target | Window | Current Value |
  |---|---:|---|---:|
  | Latency P95 | < 1500ms | 28d | 785ms |
  | Error Rate | < 1% | 28d | 0.0% |
  | Daily Cost | < $2.0 | 1d | $0.05 |
  | Quality Score | > 0.8 | 28d | 0.82 |

### 3.3 Alerts & Runbook

- [ALERT_RULES_SCREENSHOT]: [Path to image]
- [SAMPLE_RUNBOOK_LINK]: [docs/alerts.md#L...]

---

## 4. Incident Response (Group)

- [SCENARIO_NAME]: rag_slow
- [SYMPTOMS_OBSERVED]: P95 Latency tăng vọt lên > 2000ms, vi phạm SLO (1500ms). Người dùng phản hồi hệ thống bị "treo".
- [ROOT_CAUSE_PROVED_BY]: Dòng log `response_sent` có `latency_ms: 2150` và trạng thái incident `rag_slow: true` trong endpoint `/health`.
- [FIX_ACTION]: Tắt chế độ `rag_slow` bằng API `/incidents/rag_slow/disable`.
- [PREVENTIVE_MEASURE]: Thiết lập cảnh báo P2 khi `latency_p95_ms > 1500ms` để phát hiện sớm.

---

## 5. Individual Contributions & Evidence

### [MEMBER_A_NAME] Hà Việt Khánh

- [TASKS_COMPLETED]:
  - Triển khai Middleware (Correlation ID): Viết `CorrelationIdMiddleware` xử lý `x-request-id` và truyền vào `structlog.contextvars` để đồng bộ log xuyên suốt ứng dụng.
  - Cấu hình Structlog: Cài đặt pipeline processor cho Structlog sinh log định dạng JSON, tự động thêm ISO timestamp, cấp độ log và lưu xuất ra `data/logs.jsonl` qua `JsonlFileProcessor`.
  - Phát triển bộ lọc dữ liệu ẩn danh (PII): Viết các regex rules trong `app/pii.py` để tra cứu và ẩn (redact) email, CCCD, địa chỉ VN và tích hợp logger processor `scrub_event` để gỡ bỏ thông tin nhạy cảm trước khi in log.
- [EVIDENCE_LINK]: Các lịch sử thay đổi file `app/middleware.py`, `app/logging_config.py`, `app/pii.py`

### [MEMBER_B_NAME]

- [TASKS_COMPLETED]:
- [EVIDENCE_LINK]:

### [MEMBER_C_NAME] Nguyễn Tuấn Kiệt

- [TASKS_COMPLETED]:
  - Thiết lập các chỉ số SLO tối ưu trong `config/slo.yaml` (Latency P95 < 1500ms, Error Rate < 1%).
  - Xây dựng hệ thống Alert Rules đa tầng (P0-P2) trong `config/alert_rules.yaml`.
  - Soạn thảo Runbook chi tiết trong `docs/alerts.md` hướng dẫn xử lý sự cố dựa trên bằng chứng log và trace.
- [EVIDENCE_LINK]: config/slo.yaml, config/alert_rules.yaml, docs/alerts.md

### [MEMBER_D_NAME]

- [TASKS_COMPLETED]:
- [EVIDENCE_LINK]:

### [MEMBER_E_NAME] [Nguyễn Việt Trung]

- [TASKS_COMPLETED]: Built 6-panel observability dashboard (Latency P50/P95/P99, Traffic, Error Rate with breakdown, Cost over time, Tokens In/Out, Quality Score); added time-series metrics history to backend (`app/metrics.py`, `app/main.py`); served dashboard via FastAPI static files; configured SLO threshold lines and auto-refresh every 15s; collected grading evidence checklist in `docs/grading-evidence.md`
- [EVIDENCE_LINK]: app/static/dashboard.html, app/metrics.py, app/main.py, docs/grading-evidence.md

---

## 6. Bonus Items (Optional)

- [BONUS_COST_OPTIMIZATION]: (Description + Evidence)
- [BONUS_AUDIT_LOGS]: (Description + Evidence)
- [BONUS_CUSTOM_METRIC]: (Description + Evidence)

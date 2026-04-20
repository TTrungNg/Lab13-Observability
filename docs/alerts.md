# Alert Rules and Runbooks

## 1. High latency P95
- Severity: P2
- Trigger: `latency_p95_ms > 2000 for 10m`
- Impact: Tail latency breaches SLO; user experience degrades.
- First checks:
  1. Filter logs by `feature` and check `latency_ms` distribution.
  2. Inspect traces with `latency_ms > 2000` on Langfuse.
  3. Compare `retrieve` span vs `FakeLLM` span to find the bottleneck.
  4. Check if incident toggle `rag_slow` is enabled via `/health`.
- Mitigation:
  - Enable `rag_fast` if available or fallback to a lighter model.
  - Temporarily disable dense retrieval if it's the bottleneck.

## 2. High error rate
- Severity: P1
- Trigger: `error_rate_pct > 3 for 5m`
- Impact: Users receiving 500 errors; critical system failure.
- First checks:
  1. Group logs by `error_type` and `feature`.
  2. Use `correlation_id` to find the exact stack trace in logs.
  3. Verify if `tool_fail` incident is active.
- Mitigation:
  - Rollback latest deployment if deployment is simultaneous.
  - Disable problematic `feature`.

## 3. Cost budget spike
- Severity: P2
- Trigger: `hourly_cost_usd > 1.5x_baseline for 15m`
- Impact: Burn rate exceeds budget.
- First checks:
  1. Identify top `user_id_hash` by `cost_usd`.
  2. Check `tokens_in` vs `tokens_out` for abnormal prompt sizes.
- Mitigation:
  - Throttle heavy users.
  - Apply stricter truncation in `app/pii.py`.

## 4. PII leaks detected
- Severity: P0
- Trigger: `redact_count > 0 for 1m`
- Impact: Critical security/compliance bridge.
- First checks:
  1. Identify which `event` contains the PII leak.
  2. Inspect `payload` fields that were redacted.
- Mitigation:
  - Immediately block the `session_id` or `user_id_hash`.
  - Audit `data/logs.jsonl` and `data/audit.jsonl` to ensure redactor is working.
  - Update `PII_PATTERNS` in `app/pii.py` if a new pattern is found.

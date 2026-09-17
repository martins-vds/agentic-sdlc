#!/usr/bin/env bash
set -euo pipefail

spec="${1:-examples/project_spec.json}"
output_dir="${2:-artifacts/multi-agent}"
mkdir -p "$output_dir"

python3 scripts/multi_agent/spec_analyzer.py \
  --spec "$spec" --output "$output_dir/spec_analysis.json" &
analyzer_pid=$!
python3 scripts/multi_agent/risk_reviewer.py \
  --spec "$spec" --output "$output_dir/risk_review.json" &
risk_pid=$!

wait "$analyzer_pid"
wait "$risk_pid"

python3 scripts/multi_agent/plan_merger.py \
  --analysis "$output_dir/spec_analysis.json" \
  --risks "$output_dir/risk_review.json" \
  --output "$output_dir/merged_plan.json"
python3 scripts/multi_agent/validate_artifacts.py \
  --plan "$output_dir/merged_plan.json" \
  --output "$output_dir/validation.json"
printf 'Multi-agent artifacts written to %s\\n' "$output_dir"

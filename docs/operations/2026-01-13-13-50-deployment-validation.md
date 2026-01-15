## Actions Taken
- Note: CLI command timestamps were not captured in the chat; filename timestamp is UTC 2026-01-13 13:50.
- Prepared the release promotion and patch bump PRs from `develop`.
  Command: `python3 scripts/dev/submit_release_prs.py`
  Output: created `promotion/release-0-1-2-0-20260113134241`, validated locally (184 tests, 100% coverage),
  and opened PRs `#84` (release promotion) and `#85` (patch bump).
- Merged the release promotion and patch bump PRs with merge commits.
  Commands:
  - `gh pr merge 84 --merge --delete-branch`
  - `gh pr merge 85 --merge --delete-branch`
  Output: release merge commit `517c61313cdda1d5435e5ecfb9fd84626a925dc1`, develop merge commit
  `1a8668266e8defe36a25fc5c152344cd6c529623`.
- Verified GitHub Actions deployment runs for release and develop.
  Commands:
  - `gh run view 20958961737 --json status,conclusion,url,headSha,displayTitle`
  - `gh run view 20958971093 --json status,conclusion,url,headSha,displayTitle`
  Output: both runs completed with `conclusion: success`.
- Verified ECS service stability after deploys.
  Command: `AWS_PROFILE=mnemosys-admin AWS_REGION=us-east-2 aws ecs describe-services --cluster mnemosys-nonprod --services mnemosys-dev-api mnemosys-test-api --query "services[*].{name:serviceName,status:status,desired:desiredCount,running:runningCount}" --output json`
  Output: dev `desired 1 / running 1`, test `desired 2 / running 2`.
- Verified ALB health endpoints for development and test.
  Commands:
  - `AWS_PROFILE=mnemosys-admin AWS_REGION=us-east-2 aws elbv2 describe-load-balancers --names mnemosys-nonprod-alb --query "LoadBalancers[0].DNSName" --output text`
  - `curl -fsSL http://mnemosys-nonprod-alb-1104521642.us-east-2.elb.amazonaws.com/health/`
  - `curl -fsSL http://mnemosys-nonprod-alb-1104521642.us-east-2.elb.amazonaws.com:8080/health/`
  Output: both health checks returned `{"status":"ok"}`.
- Verified migration gate activity in dev/test logs.
  Commands:
  - `AWS_PROFILE=mnemosys-admin AWS_REGION=us-east-2 aws logs describe-log-streams --log-group-name /mnemosys/test/api --order-by LastEventTime --descending --max-items 1 --query "logStreams[0].logStreamName" --output text`
  - `AWS_PROFILE=mnemosys-admin AWS_REGION=us-east-2 aws logs get-log-events --log-group-name /mnemosys/test/api --log-stream-name <stream> --limit 200 --start-from-head --query "events[*].message" --output text | rg -n "alembic"`
  - `AWS_PROFILE=mnemosys-admin AWS_REGION=us-east-2 aws logs describe-log-streams --log-group-name /mnemosys/dev/api --order-by LastEventTime --descending --max-items 1 --query "logStreams[0].logStreamName" --output text`
  - `AWS_PROFILE=mnemosys-admin AWS_REGION=us-east-2 aws logs get-log-events --log-group-name /mnemosys/dev/api --log-stream-name <stream> --limit 200 --start-from-head --query "events[*].message" --output text | rg -n "alembic"`
  Output: test shows `alembic current` at `f71a73e20503`, `alembic heads` at `abe7b3773eff`,
  then `alembic upgrade heads` and `alembic current` at head; dev shows `alembic current` and
  `alembic heads` both at `abe7b3773eff` (no upgrade needed).

## Outcomes and Status
- Release promotion deployed to test and patch bump deployed to development via GitHub Actions.
- ECS services report expected desired/running counts and ALB health checks are green.
- Migration gate runs on both environments; upgrades succeed.

## Problems Encountered and Solved
- None.

## Problems Unresolved
- None.

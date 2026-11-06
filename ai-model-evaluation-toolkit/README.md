# AI Model Evaluation Toolkit

A free, provider-neutral workbook for comparing your own AI task results, latency, model spend and human review effort.

[Read the walkthrough and download the toolkit](https://blog.kloudxpert.com/ai-model-evaluation-toolkit/?utm_source=github&utm_medium=referral&utm_campaign=ai_evaluation_toolkit_nov2026&utm_content=workbook_readme).

[Download the Excel workbook](https://raw.githubusercontent.com/kloudxpert/blog/main/ai-model-evaluation-toolkit/KloudXpert-AI-Evaluation-Workbook.xlsx) · [View the workbook file](KloudXpert-AI-Evaluation-Workbook.xlsx)

## What to fill in

Your candidate measurements and rates start blank. The 20 scenario ideas help you define test cases; they are not benchmark results.

| Sheet | Purpose |
| --- | --- |
| Instructions | Definitions, cost scope and how to extend the template |
| Cases | Expected evidence, pass criteria and access constraints |
| Runs | One row for each attempted task, including rejected and error outcomes |
| Calls | Every billable model call, including retries and failed calls |
| Summary | Acceptance, latency and costs for the candidate IDs you enter |
| Example | A separate illustration using invented rates; it does not feed Summary |

Use approved or synthetic inputs. Set pass criteria before comparing candidates and record the exact model/version, configuration and dated rates that actually apply. There is no API connection or automatic price feed.

## Reading the results

Cost per accepted task includes the spend on **all attempts**, divided by accepted tasks. Full cost adds recorded human-review spend. Include billable categories and tool fees in Other charges where applicable. Unknown inputs stay blank; enter zero only when verified. Resolve input-status warnings before using the totals. Zero accepted tasks produces no cost-per-accepted result.

All amounts are USD. Reconcile your inputs with usage records and invoices; currency conversion, tax, subscription charges and unrecorded fees are not added automatically.

The starter has **20 cases, 50 task runs, 100 calls and 10 candidate slots**. Extending it requires extending the formulas, validations and bounded references described in Instructions.

The original, macro-free workbook contains no vendor rankings. The isolated Example is teaching material, not measured model performance.

Created by KloudXpert. Cover artwork is provided in [PNG](ai-model-evaluation-toolkit.png) and [SVG](ai-model-evaluation-toolkit.svg).

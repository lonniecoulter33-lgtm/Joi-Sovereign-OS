# Fortress Extraction Proposal Review Guide

This directory contains a non-destructive proposal for extracting "fortress" related logic from Joi's codebase into a centralized module.

## 🛡️ Safety Confirmation
**NO CODE HAS BEEN MODIFIED.** This proposal is generated as a JSON file for your review. No autonomous edits have been performed, and no destructive operations have occurred.

## 📄 Proposal Files
The proposal is stored in a JSON file with the following pattern:
`proposals/fortress_proposal_<timestamp>.json`

## 🔍 Manual Review Checklist
Before applying any changes, please verify the following in the JSON proposal:
- [ ] **Files Touched**: Review the list of Python modules identified for extraction.
- [ ] **Unified Diffs**: Inspect the `unified_diffs` section to see exactly what changes are being suggested.
- [ ] **Preflight Status**: Ensure `preflight_results` show `passed: true` for all modified content.
- [ ] **Risk Analysis**: Check the `risk_analysis` summary for any "High" or "Medium" risk flags.
- [ ] **Reconciliation**: Note the references found in `learning_data.json` and the operations manual.

## 🛠️ Approval & Application Workflow
1. **Locate the JSON**: Open the latest `fortress_proposal_<timestamp>.json` in your editor.
2. **Review Diffs**: Compare the `old_text` and `proposed_new_text`.
3. **Backup**: Execute the backup commands provided in the `backup_instructions` field of the JSON.
4. **Manual Apply**: If satisfied, manually apply the extraction or ask Joi to "Apply the fortress extraction proposal from <filename>".

## ⏪ Rollback Instructions
If any issues arise after manual application:
1. Revert the files using the backups created in step 3.
2. If git is used, use `git checkout <file_path>` to restore the last committed state.

---
**WARNING**: Explicit human approval is required before any code changes are applied. This proposal is for governance and architectural refinement only.

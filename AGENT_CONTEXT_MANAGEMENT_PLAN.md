# AGENT CONTEXT MANAGEMENT PLAN

## CONTEXT MONITORING THRESHOLDS

### AMBER ALERT - 70% Context Usage
- Create checkpoint with current progress
- Document specific next steps in handoff documentation
- Prioritize critical path items only

### RED ALERT - 85% Context Usage
- **IMMEDIATE HANDOFF PROTOCOL**
- Commit all work with descriptive message
- Run outgoing agent workflow
- Update handoff documentation with exact continuation point

## HANDOFF EXECUTION CHECKLIST

### Before Handoff (When approaching 85%)
1. **Document Current State**:
   - [ ] Update ARKIVAL_REFACTOR_HANDOFF_DOCUMENTATION.md with exact progress
   - [ ] Note which files are currently being modified
   - [ ] Document any test results or failures
   - [ ] List exact next steps for continuation

2. **Commit Current Work**:
   ```bash
   git add .
   git commit -m "WIP: Arkival subdirectory refactor - [specific phase and status]
   
   Progress:
   - [list completed items]
   - [list current work in progress]
   - [list immediate next steps]
   
   🤖 Generated with [Claude Code](https://claude.ai/code)
   Co-Authored-By: Claude <noreply@anthropic.com>"
   ```

3. **Run Outgoing Workflow**:
   ```bash
   python3 codebase_summary/agent_workflow_orchestrator.py outgoing --summary "Mid-refactor handoff: [specific status]" --type "unresolved"
   ```

### Incoming Agent Instructions
1. **IMMEDIATELY** read ARKIVAL_REFACTOR_HANDOFF_DOCUMENTATION.md
2. Run incoming agent workflow
3. Check git log for latest progress
4. Examine uncommitted changes with `git diff`
5. Continue from exact point documented in handoff

## WORK PRIORITIZATION FOR LIMITED CONTEXT

### Phase 1 (CRITICAL): agent_workflow_orchestrator.py
- Focus ONLY on path resolution integration
- Single script completion before moving to next

### Phase 2 (HIGH): update_changelog.py  
- Path resolution integration
- Test with simple changelog entry

### Phase 3 (HIGH): update_project_summary.py
- Most complex script - needs careful path resolution
- Test incremental changes

### Phase 4 (MEDIUM): validate_deployment.py
- Update validation paths
- Test deployment validation

## CONTEXT PRESERVATION STRATEGY

### What to Preserve in Handoff:
- **Exact file modification status**
- **Current test state** 
- **Specific error messages encountered**
- **Working vs broken functionality**
- **Test environment setup details**

### What NOT to Include:
- Long file contents (use git diff instead)
- Complete audit repeats (reference documentation)
- Extensive background context (focus on current state)

## EMERGENCY HANDOFF PROTOCOL

If forced to handoff immediately:
1. Save current editor state
2. Quick commit with "EMERGENCY_HANDOFF: [one line status]"
3. Update handoff doc with: "INTERRUPTED AT: [exact task]"
4. Note any unsaved changes or partial edits

## SUCCESS METRICS FOR HANDOFF
- Next agent can continue within 5 minutes of reading handoff docs
- No work is lost or repeated
- Clear understanding of current progress state
- Specific next actions documented

---
*This plan ensures continuity across agent sessions during complex refactors*
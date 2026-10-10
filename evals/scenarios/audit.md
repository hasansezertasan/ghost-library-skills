# Audit scenario

## User request

Use `ghost-audit` to review this contract and its fixture coverage. Do not edit the artifacts.

## Raw artifacts

`SPEC.md`:

```markdown
# app_config_dir
Return $HOME/.config/{app} from explicit env inputs.
app must be nonempty. An empty app raises a detectable error.
The function never creates directories.
```

`INSTALL.md`:

```markdown
An empty app returns null. Create the resulting directory if needed.
All two cases must pass.
```

`tests.yaml`:

```yaml
app_config_dir:
  - name: normal
    input: {app: demo, env: {HOME: /test/home}}
    output: /test/home/.config/demo
  - name: empty-app
    input: {app: "", env: {HOME: /test/home}}
    raises: true
```

## Assessment criteria

The report locates both conflicts in the generation instructions, retains the negative fixture, identifies missing non-creation coverage, and does not claim implementation conformance. It does not modify files or choose a new empty-app behavior without a decision.

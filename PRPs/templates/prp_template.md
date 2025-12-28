# Product Requirement Prompt (PRP) Template

---
name: [Feature Name]
description: |
  [Brief overview of what this PRP accomplishes]
---

## Purpose
[Clear statement of what's being built and why it matters]

## Core Principles
- **[Principle 1]**: [Description]
- **[Principle 2]**: [Description]
- **[Principle 3]**: [Description]

## Goal
[Primary objective in 1-2 sentences]

## Why
[Business/technical justification - why this feature is needed]

## What
**Success criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

## All Needed Context

### 📚 Documentation & References
```yaml
references:
  - url: [URL to documentation]
    type: [official_docs | tutorial | api_reference]
    reasoning: [Why this is relevant]

  - file: [path/to/file.py]
    reasoning: [What patterns to follow from this file]
```

### 🗂 Current Codebase Tree
```
[ASCII representation of relevant current files]
```

### 🎯 Desired Codebase Tree
```
[ASCII representation showing new/modified files with inline comments]
backend/
  app/
    models/
      example.py  # Core model with relationships
```

### ⚠️ Known Gotchas & Library Quirks
```python
# PATTERN: Always use best practice
example = BestPractice()  # CORRECT
example = BadPractice()   # WRONG - explanation

# CRITICAL: Important consideration
important_thing()  # Don't forget this
```

## Implementation

### 🔧 Data Models and Structure
```python
# Pydantic schema with inline comments
class ExampleModel(BaseModel):
    field: str  # PATTERN: Describe the pattern
    # ... rest of model
```

### 📋 List of Tasks
```yaml
tasks:
  - id: 1
    name: Task name
    files:
      - path/to/file.py
    dependencies: []

  - id: 2
    name: Another task
    files:
      - path/to/another.py
    dependencies: [1]
```

### 💻 Per Task Pseudocode
```python
# Task 1: Description
# PATTERN: Describe the pattern to follow

class Example:
    # CRITICAL: Important implementation detail
    pass
```

### 🔌 Integration Points
```yaml
environment:
  - variable: ENV_VAR
    example: example_value
    required: true

configuration:
  - file: path/to/config.py
    changes: [Add settings]

dependencies:
  - package: package-name
    version: ">=1.0"
    reasoning: Why this package is needed
```

## Validation Loop

### ✅ Level 1: Syntax & Linting
```bash
# Run before committing
command --to --check --syntax
```

### ✅ Level 2: Unit Tests
```python
def test_feature():
    """Test description"""
    # PATTERN: Test edge cases
    assert expected == actual
```

### ✅ Level 3: Integration Tests
- [ ] Test criterion 1
- [ ] Test criterion 2
- [ ] Test criterion 3

## Final Checklist
- [ ] All code includes proper type hints
- [ ] Tests cover normal, edge, and error cases
- [ ] Documentation is updated
- [ ] Code follows project conventions

## Anti-Patterns to Avoid
❌ **Don't** do this thing (explanation)
❌ **Don't** do that thing (explanation)

## Confidence Score
**X/10** - Explanation of confidence level and any concerns

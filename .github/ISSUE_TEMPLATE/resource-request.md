---
name: Resource request or correction
description: Suggest a verified resource or correct an existing entry
title: "[resource] "
labels: ["catalog"]
body:
  - type: markdown
    attributes:
      value: |
        Thanks for helping improve the catalog. Please provide evidence, not just a name.
  - type: input
    id: resource-name
    attributes:
      label: Resource name
      placeholder: "Example: some-skill"
    validations:
      required: true
  - type: input
    id: source-url
    attributes:
      label: Canonical source URL
      description: GitHub, npm, PyPI or official documentation. Do not guess.
      placeholder: "https://github.com/owner/repo"
    validations:
      required: true
  - type: dropdown
    id: resource-type
    attributes:
      label: Resource type
      options:
        - skill
        - agent
        - plugin
        - mcp
        - command
        - rule
        - hook
        - provider
        - collection
    validations:
      required: true
  - type: input
    id: category
    attributes:
      label: Primary category
      placeholder: "software-development"
    validations:
      required: true
  - type: textarea
    id: description
    attributes:
      label: What does it do?
      description: Factual description, 20-600 characters.
    validations:
      required: true
  - type: input
    id: license
    attributes:
      label: License observed
      placeholder: "MIT / Apache-2.0 / NOASSERTION / UNKNOWN"
    validations:
      required: true
  - type: textarea
    id: evidence
    attributes:
      label: Verification evidence
      description: What did you check, and when?
    validations:
      required: true
  - type: checkboxes
    id: confirmations
    attributes:
      label: Confirmations
      options:
        - label: The source URL is real and reachable.
          required: true
        - label: I did not guess the owner, package name or install command.
          required: true
        - label: This is not permission-bypass or guardrail-removal tooling.
          required: true

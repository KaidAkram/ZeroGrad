# GitHub publication record

Destination authorized by the owner: https://github.com/KaidAkram/ZeroGrad .

The browser inspection on 2026-11-13 showed a public repository on `main` with
one initial README commit, `a67c1420a89c64ec15b0846527f782b8b231d7ed`.
The prepared publication retains that history; no force-push or deletion is needed.

## Prepared source and evidence

- README: plain-language introduction, original SVG cover, measured boundary chart,
  architecture Mermaid diagram, mathematical objective, setup commands and honest scope.
- Author and repository metadata: project.json and CITATION.cff.
- Source, tests, raw benchmark predictions, papers, career drafts, editable figures,
  actual video exports and licensing documents are included in the publication export.
- Dependency environments, package caches, generated studio build/copies, credentials
  and temporary publishing artifacts are excluded. Build the studio from source.

## Observed blocker

The host denies GitHub network sockets to terminal commands. `git ls-remote`
failed to connect, and GitHub CLI could not validate its configured credentials.
The signed-in browser could read the repository, but the available Windows UI
automation did not provide a reliable publishing interaction. A remote upload or
push has **not** been verified in this record.

`scripts/publish_github.py` performs the final Git publication in a normal user
terminal. It clones the authorized repository, checks that the remote
still has the inspected initial commit, copies the reviewed export without touching
`.git`, makes a commit, performs a normal push and verifies the remote commit ID.
It uses Git's ordinary credential manager if authentication is required. It never
prints credentials, changes account permissions, force-pushes or publishes to LinkedIn.

Run the preparation script first when files change:

```powershell
python scripts/package_release.py
python scripts/publish_github.py --dry-run
python scripts/publish_github.py
```

The Python entrypoint avoids the authoring host's PowerShell script-policy issue.
The dry run checks the export and paths without making network requests. The real
run must execute where GitHub network access and Git authentication work. If the
remote head changed, the script stops for review instead of overwriting that work.

After a verified push, replace the blocker paragraph with the actual commit URL
and review the hosted Actions run before describing CI as passing. LinkedIn posting
and website deployment are separate actions.

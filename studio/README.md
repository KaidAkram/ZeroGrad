# ZeroGrad-Sec research studio

A local React/TypeScript studio backed by `../telemetry/`. No scores are embedded in the UI source. Missing methods are listed explicitly from the benchmark status records.

```powershell
npm ci
npm run build
npm run dev
```

Open the printed loopback URL. The production artifact is `dist/`; serve it through any static HTTP server. A `file://` URL cannot fetch the JSON evidence. Building copies telemetry and the research/claim/limitations documents into `public/data/` and `dist/data/`. Rebuild after changing experiments or documents.

```powershell
npm test
```

The browser check uses locally installed Microsoft Edge and starts a temporary loopback HTTP server. It validates replay, circuit selection, method filtering, documents, reduced motion, and mobile overflow. Screenshots and test results are in `qa/`. For other platforms, remove the explicit Edge executable path in `tests/browser.mjs` and install Playwright Chromium.

## Environment recovery

The initial npm network request was denied by the host, and the global npm cache was read-only. Dependencies were recovered from the existing content-addressed npm cache with `scripts/offline-deps.cjs`, then pinned with registry integrity hashes. This helper is deliberately specific to the audited Windows host; ordinary reproduction uses `npm ci` with the checked-in lockfile. No global package or cache was modified. `scripts/build.mjs` avoids Vite's config bundling because the sandbox blocks ancestor directory traversal by esbuild.

## Interpretation

The matrix displays exact event coordinates, with a labeled maximum 32-by-32 viewport. Color distinguishes signed values; tooltips expose numeric coordinates. The register strip and covariance geometry are explicitly labeled schematics, not measured activation maps or PCA. The toy circuit is a bounded alternative, not the original proposed four-block transformer. Benchmark uncertainty and architecture mismatch remain visible. No deployment or external publishing has been performed.

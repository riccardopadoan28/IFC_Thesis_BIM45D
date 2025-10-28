## Troubleshooting

- Error: Failed to load module script: Expected a JavaScript-or-Wasm module script but the server responded with a MIME type of "text/html" at `static/viewer/static/js/index.*.js`.
  - Cause: the requested JS file does not exist locally; the server returns an HTML 404 page, which fails strict module loading.
  - Fix (recommended): the app is configured to use the CDN. If you still see the error:
    - Hard refresh the browser (Ctrl+F5) and clear cache.
    - Ensure the Viewer URL contains `useCdn=1` (the Streamlit page does this automatically).
    - If you open `viewer/viewer.html` outside Streamlit, append `?useCdn=1` to the URL.

- Optional offline setup (advanced):
  1) `npm i @xeokit/xeokit-webcomponents`
  2) Copy the package `dist` output into `viewer/lib/dist` and ensure its `static/js` chunks are present:
     - PowerShell:
       - `mkdir viewer\lib\dist`
       - `Copy-Item node_modules\@xeokit\xeokit-webcomponents\dist\* viewer\lib\dist\ -Recurse`
  3) Remove the CDN-only import if you want local loading.

- Streamlit 404s on `_stcore/health` and `_stcore/host-config` are harmless and can be ignored.

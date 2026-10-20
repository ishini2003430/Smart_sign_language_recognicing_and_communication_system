# SLSL HUD — React / Vite migration

Converted from the supplied `SLSL_HUD_UI(1).zip`. This is an **independent, non-destructive frontend** that preserves the existing interface markup and styling across the 17 screens, using React components.

## Install and run on Windows (PowerShell)

1. Copy the **entire `SLSL_HUD_React` folder** into your repository at `frontend/slsl_hud_react/`. Do not replace the existing `frontend/` folder.
2. Open the VS Code terminal at the main repository root.
3. Run:

```powershell
cd frontend\slsl_hud_react
npm install
npm run dev
```

Open the URL printed by Vite (normally **http://127.0.0.1:5173**).

Login uses a **demo role selector**; no real authentication. User goes to `/dashboard`, Researcher to `/research-dashboard`.

## What is React now?

- Each of the 17 original HTML screens is a React JSX page under `src/pages/`.
- Shared User navigation and Research sidebar are reusable React components under `src/components/Navigation.jsx`.
- Shared theme toggle is React state with localStorage persistence.
- Client-side navigation is implemented in `src/App.jsx` using the History API (no router package needed).
- The original visual CSS has been kept in `public/styles/` and is loaded per screen.
- The recognition page now uses React state to preview an uploaded sign video, select LSTM / GRU / Conv1D+BiLSTM, and attempt to call a configurable **future backend API**. It never returns fake model predictions.

## Recognition backend integration (not implemented by this zip)

The React uploader sends a `POST` multipart/form-data request to `/api/recognition/predict`:

- `video`: recorded MP4 video upload
- `model_id`: `lstm`, `gru` or `conv1d_bilstm`

Expected JSON example (ILLUSTRATIVE ONLY):

```json
{
  "prediction": {"sign_id":"S01", "gloss":"Amma", "sinhala":"අම්මා", "score":0.82},
  "candidates": [
    {"sign_id":"S01", "gloss":"Amma", "score":0.82},
    {"sign_id":"S02", "gloss":"Father", "score":0.11}
  ]
}
```

This is **not an endpoint that exists automatically**. To make it work, train and save a model containing the target sign classes; implement the backend route in `backend/routes/recognition.py`; run the *same MediaPipe extraction and preprocessing as training*; and expose it through an API server at `http://127.0.0.1:8000`. Vite proxies `/api` requests during development. A production deployment needs its own proxy/CORS configuration.

**Important about Amma:** the current 10-class two-signer pilot smoke test excludes S01 (Amma) and S12 (Home), because Expert 02 recordings for these signs are missing. The UI cannot recognize those signs until a model containing those classes is trained and integrated.

## Scope and limitations

- Converted **visual pages** and navigation are available; backend integrations for translation, live video, sign animation, learner feedback and datasets are not included. Some controls on preserved prototype screens may remain display-only, and preset demo data in those screens is **not a trained model result**.
- The recognition screen has real upload state, but **does not perform inference** without a Python API and trained model.
- The reference HTML included research dummy metrics. A few key counts in Research Dashboard were corrected to currently known pilot values (12 sign IDs, 22 videos, 2 signers); the rest of the display should be reviewed with the team before presentation.
- This migration is not a replacement for the existing SLSL team's `frontend/` work. Merge only after team agreement and checking Git changes.
- Obtain permission from signers for data use and do not present simulated signing as expert-verified examples.

## File map

```
src/
  App.jsx                 # route display, per-page CSS
  main.jsx
  components/
    Navigation.jsx        # reusable user/research navigation, theme
    Recognition.jsx       # uploader, video preview and API-ready prediction result
  pages/                  # 17 converted React screens
public/styles/            # 6 original CSS files
```

To create a production-ready React app later, the preserved demo-only pages should be refactored further to use React state and backend APIs for their own forms, buttons and dynamic results.

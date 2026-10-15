# Setup and first milestone
TensorFlow/Keras does not require a different top-level repository architecture from PyTorch. Model imports, dependency versions, training code and saved artifacts differ. Frontend/backend and other members' algorithms may use their own appropriate dependencies.

requirements.txt lists candidate dependencies, not a tested lock. Select a Python/package combination supported by TensorFlow and the chosen MediaPipe extractor on team machines; smoke-test imports and video extraction, then record exact versions. Do not upgrade dependencies independently after a shared working environment is fixed.
Use one isolated environment per project (Windows example):
```
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```
Installation may require resolving package/Python versions; this package has not been run as an application. Use tensorflow.keras consistently for recognition. A saved model must include the .keras file, class-map JSON, preprocessing/feature configuration, training manifest identity and package versions.

frontend/ is a placeholder: scaffold React/Vite later to generate package.json and a real lockfile. Do not create empty dependency manifests. backend/ files are also placeholders, not a functioning API.

First milestone: approve a few labels; decode one original phone video; inspect both-hand and pose extraction; save landmarks + timestamps + missingness; build and overfit a tiny development-only batch as a code diagnostic; then evaluate on a disjoint validation signer. Tiny-batch overfitting is not a research result.

Git: clone the existing repository, create a branch, merge starter contents, inspect git status and git diff, stage intended files, commit and push the branch, then open a pull request. Do not commit participant videos, signed consent, credentials, large feature archives or trained models. Store them in access-controlled backed-up storage and document locations without embedding secrets.

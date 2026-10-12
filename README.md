# doc-to-.md-converter

A small local web interface for [Microsoft MarkItDown](https://github.com/microsoft/markitdown). Choose a supported document in your browser and convert it to Markdown. The `.md` result is saved to your computer's Desktop.

The web server listens only on this computer (`127.0.0.1`). Uploaded documents are passed to the local MarkItDown process. Initial setup needs an internet connection to download Python packages.

## Quick start

Use Python 3.10–3.14. From this repository folder, create a virtual environment and install the app dependencies:

**macOS**

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e 'packages/markitdown[all]'
.venv/bin/python web_app.py
```

**Windows PowerShell**

```powershell
!!One of the Python versions between 11 and 14 must be installed.
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e "packages/markitdown[all]"
.\.venv\Scripts\python.exe web_app.py
```

Open <http://127.0.0.1:8765>, select a file, and click **Dönüştür ve Masaüstüne kaydet**. Stop the server with `Ctrl+C` in the terminal. More detailed steps are in [run.md](run.md).

The MarkItDown source and its license and third-party notices are included under `packages/markitdown`.

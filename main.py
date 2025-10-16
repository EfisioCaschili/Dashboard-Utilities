from flask import Flask, jsonify, render_template, request
import os, sys, subprocess
from dotenv import dotenv_values

# Imposta prima il percorso corrente del server Flask
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Carica variabili da env.env
env = dotenv_values(os.path.join(BASE_DIR, "env.env"))
source = env.get('source')

# Elenco script
scripts = [
    'Create_PDF_Report/main.py',
    'Overview SlotMeeting/app.py',
    'WEEKLY REPORT/main.py',
    'Check Logbook SH/Check.py'
]

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', scripts=scripts)

@app.route('/run_script', methods=['POST'])
def run_script():
    data = request.get_json()
    script_name = data.get('script')
    today = data.get('today', '')
    tomorrow = data.get('tomorrow', '')
    week = data.get('week', '')
    year = data.get('year', '')

    if script_name not in scripts:
        return jsonify({"error": "Script non autorizzato"}), 403

    # Percorsi completi
    script_path = os.path.join(source, "gbts", script_name)
    script_dir = os.path.dirname(script_path)
    python_path = os.path.join(os.path.dirname(BASE_DIR), 'Dashboard Utilities', 'python-3.12.7', 'python.exe')

    print(f">>> PYTHON: {python_path}")
    print(f">>> SCRIPT: {script_path}")
    print(f">>> CWD: {script_dir}")

    # Costruisci comando
    cmd = [python_path, script_path]
    if script_name == 'Create_PDF_Report/main.py':
        if today:
            cmd += ['--today', today]
        if tomorrow:
            cmd += ['--tomorrow', tomorrow]
    elif script_name == 'WEEKLY REPORT/gui.py':
        if week:
            cmd += ['--week', week]
        if year:
            cmd += ['--year', year]
    

    # Ambiente
    env = os.environ.copy()
    env["PYTHONPATH"] = script_dir  # per i moduli locali come 'utility'
    env["PATH"] = f"{os.path.dirname(python_path)};{env['PATH']}"

    try:
        result = subprocess.run(
            cmd,
            cwd=script_dir,
            env=env,
            capture_output=True,
            text=True
        )

        print(">>> STDOUT:", result.stdout)
        print(">>> STDERR:", result.stderr)

        if result.returncode != 0:
            return jsonify({"error": result.stderr}), 500

        return jsonify({"output": result.stdout})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

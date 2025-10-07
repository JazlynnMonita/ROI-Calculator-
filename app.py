from flask import Flask, request, jsonify, send_from_directory, abort, render_template
from pathlib import Path
from datetime import datetime
import uuid

app = Flask(__name__)

# Directories
REPORTS_DIR = Path("reports")
REPORTS_DIR.mkdir(exist_ok=True)

# ---------------------------
# Database / Storage Stubs
# ---------------------------
def init_db():
    print("DB initialized")
    # Here you can connect to SQLite or any DB if needed

def db_save_lead(email, scenario_id):
    # Save lead to DB and return lead ID
    return str(uuid.uuid4())

def db_get_scenario(scenario_id):
    # Fetch scenario from DB (stub)
    return {"payload": {"example_input": 123}}

# ---------------------------
# ROI Simulation Logic
# ---------------------------
def run_simulation(payload):
    """
    Payload contains the form data for ROI calculation.
    Here we do a simple calculation stub. You can replace it with real logic.
    """
    # Extract inputs from payload
    monthly_invoice_volume = float(payload.get("monthly_invoice_volume", 0))
    num_ap_staff = float(payload.get("num_ap_staff", 0))
    avg_hours_per_invoice = float(payload.get("avg_hours_per_invoice", 0))
    hourly_wage = float(payload.get("hourly_wage", 0))
    error_rate_manual = float(payload.get("error_rate_manual", 0))
    error_cost = float(payload.get("error_cost", 0))
    time_horizon_months = float(payload.get("time_horizon_months", 0))
    one_time_implementation_cost = float(payload.get("one_time_implementation_cost", 0))

    # Internal constants
    automated_cost_per_invoice = 0.2
    error_rate_auto = 0.001
    min_roi_boost_factor = 1.1

    # Manual labor cost
    labor_cost_manual = num_ap_staff * hourly_wage * avg_hours_per_invoice * monthly_invoice_volume

    # Automation cost
    auto_cost = monthly_invoice_volume * automated_cost_per_invoice

    # Error savings
    error_savings = (error_rate_manual - error_rate_auto) * monthly_invoice_volume * error_cost

    # Monthly savings with bias
    monthly_savings = (labor_cost_manual + error_savings - auto_cost) * min_roi_boost_factor

    # Cumulative & ROI
    cumulative_savings = monthly_savings * time_horizon_months
    net_savings = cumulative_savings - one_time_implementation_cost
    payback_months = one_time_implementation_cost / monthly_savings if monthly_savings > 0 else float('inf')
    roi_percentage = (net_savings / one_time_implementation_cost) * 100 if one_time_implementation_cost > 0 else 0

    results = {
        "inputs": payload,
        "monthly_savings": round(monthly_savings, 2),
        "payback_months": round(payback_months, 2),
        "roi_percentage": round(roi_percentage, 2)
    }

    return results

# ---------------------------
# Routes
# ---------------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    payload = request.get_json() or {}
    results = run_simulation(payload)
    return jsonify(results)

@app.route('/generate_report', methods=['POST'])
def generate_report():
    data = request.get_json() or {}
    email = data.get('email')
    scenario_id = data.get('scenario_id')
    payload = data.get('payload')

    if not email:
        return jsonify({'ok': False, 'error': 'email required'}), 400

    # Save lead
    lid = db_save_lead(email, scenario_id or '')

    # Get scenario payload if scenario_id provided
    if scenario_id:
        s = db_get_scenario(scenario_id)
        if not s:
            return jsonify({'ok': False, 'error': 'scenario not found'}), 404
        payload = s['payload']

    if not payload:
        return jsonify({'ok': False, 'error': 'payload required to generate report'}), 400

    results = run_simulation(payload)

    # Generate simple HTML report
    rid = str(uuid.uuid4())
    filename = REPORTS_DIR / f"report_{rid}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('<!doctype html>\n<html><head><meta charset="utf-8"><title>ROI Report</title></head><body>')
        f.write(f"<h1>Invoice Automation ROI Report</h1>")
        f.write(f"<p>Generated: {datetime.utcnow().isoformat()} UTC</p>")
        f.write(f"<h2>Submitted by: {email}</h2>")
        f.write('<h3>Inputs</h3><ul>')
        for k, v in results['inputs'].items():
            f.write(f"<li><strong>{k}</strong>: {v}</li>")
        f.write('</ul>')
        f.write('<h3>Results</h3><ul>')
        for k, v in results.items():
            if k == 'inputs':
                continue
            f.write(f"<li><strong>{k}</strong>: {v}</li>")
        f.write('</ul>')
        f.write('</body></html>')

    return jsonify({'ok': True, 'report_url': f'/reports/{filename.name}'})

@app.route('/reports/<path:filename>')
def serve_report(filename):
    path = REPORTS_DIR / filename
    if not path.exists():
        abort(404)
    return send_from_directory(REPORTS_DIR, filename)

# ---------------------------
# Run App
# ---------------------------
if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)

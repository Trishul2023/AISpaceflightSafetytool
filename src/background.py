from flask import Flask, render_template
from flask_socketio import SocketIO
import threading
import time
import os

from matplotlib.pylab import f
from monitor import SafetyMonitor
from alerts import AlertSystem

# Initialize Flask app with explicit template and static folders
app = Flask(__name__,
            template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../templates'),
            static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../static'))
socketio = SocketIO(app)

@app.route('/')
def index():
    """Render the dashboard."""
    print(f"Serving template: {os.path.join(app.template_folder, 'index.html')}")  # Debug log
    return render_template('index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files and log access."""
    print(f"Serving static file: {os.path.join(app.static_folder, filename)}")  # Debug log
    return app.send_static_file(filename)

def monitoring_thread():
    """Run the safety monitoring loop."""
    monitor = SafetyMonitor()
    alert_system = AlertSystem()
    print("Starting Spaceflight Safety Monitoring with AI, Voice Alerts, and Dashboard...")
    while True:
        data = monitor.get_safety_data()
        signal_status = monitor.get_signal_status(data)
        is_anomaly = monitor.is_anomaly(data)
        is_safe = monitor.is_safe(data)
        print(monitor.display_data(data))  # Terminal output
        dashboard_data = {
            'timestamp': data['timestamp'],
            'pressure': f"{data['pressure']:.2f}",
            'oxygen': f"{data['oxygen']:.2f}",
            'radiation': f"{data['radiation']:.2f}",
            'ai_status': 'Anomaly' if is_anomaly else 'Normal',
            'signal': signal_status
        }
        print(f"Emitting to dashboard: {dashboard_data}")  # Debug log
        socketio.emit('update_data', dashboard_data)
        if not is_safe:
            alert_system.trigger_alert(data, is_anomaly=False, signal_status=signal_status)
        elif is_anomaly:
            alert_system.trigger_alert(data, is_anomaly=True, signal_status=signal_status)
        time.sleep(5)

if __name__ == '__main__':
    print(f"Static folder: {app.static_folder}")  # Debug log
    threading.Thread(target=monitoring_thread, daemon=True).start()
    socketio.run(app, debug=True, use_reloader=False, host='0.0.0.0', port=5000)
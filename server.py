from flask import Flask, jsonify, request, render_template, Response, send_file
import queue
import threading
import bundle_details_collector
import os
# import colorama
# import logging
# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)
# log.disabled = True
# app.config = {
#      "DEBUG": True,
#      "TEMPLATES_AUTO_RELOAD": True,
#      "CONTENT_SECURITY_POLICY": "default-src 'self' https://0.0.0.0:443"
# }

app = Flask(__name__, template_folder="web_template")
bdc = bundle_details_collector.BundleDetailsCollector()

# Queue for log messages
log_queue = queue.Queue()


def log_message(message, level):
    log_queue.put(f"{level}: {message}")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/start_qp_grabber", methods=["POST"])
def start_qp_grabber():
    exam_name = request.form["examName"]
    custom_qp_range_mode = request.form.get("customQPRangeMode") == "on"

    # Collect all necessary form data
    form_data = {
        "exam_name": exam_name,
        "custom_qp_range_mode": custom_qp_range_mode,
        "qp_range": request.form.get("customQPRange"),
        "qp_series": request.form.get("qpSeries"),
        "qp_start_range": request.form.get("qpStartRange"),
        "qp_end_range": request.form.get("qpEndRange"),
    }

    def run_script(data):
        if data["custom_qp_range_mode"]:
            qp_range = data["qp_range"].split(",")
            bdc.custom_qp_range(qp_range, data["exam_name"], log_message)
        else:
            qp_series = data["qp_series"]
            qp_start_range = int(data["qp_start_range"])
            qp_end_range = int(data["qp_end_range"])
            bdc.auto_qp_series_generator(
                qp_series, qp_start_range, qp_end_range, data["exam_name"], log_message
            )

        log_message("Bundle details fetching completed successfully", "INFO")

    threading.Thread(target=run_script, args=(form_data,)).start()

    return jsonify({"status": "success", "message": "Bundle Details Grabber started\n"})


@app.route("/check_cookies", methods=["POST"])
def check_login():
    cookie_status, captcha_link = bdc.check_cookies()
    if not cookie_status:
        return jsonify({"status": "login_required", "captcha_url": captcha_link})
    else:
        return jsonify({"status": "Login successful"})


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    captcha = request.form["captcha"]
    if bdc.manual_login(username, password, captcha):
        return jsonify({"status": "success", "message": "Login successful"})
    else:
        return jsonify({"status": "error", "message": "Login failed"})


@app.route("/get_sheets", methods=["POST"])
def get_sheets():
    file_path = request.json["path"]
    abs_file_path = os.path.abspath(file_path)
    if os.path.exists(abs_file_path):
        sheet_names = bdc.get_sheet_names(abs_file_path)
        return jsonify({"sheets": sheet_names})
    else:
        return jsonify({"error": "File not found"}), 404


@app.route("/download_sheet", methods=["POST"])
def download_sheet():
    file_path = request.json["path"]
    sheet_name = request.json["sheet_name"]
    abs_file_path = os.path.abspath(file_path)

    if os.path.exists(abs_file_path):
        output_file = f"{os.path.splitext(abs_file_path)[0]}_{sheet_name}.xlsx".replace(
            "_combined", ""
        )
        if bdc.extract_sheet(abs_file_path, sheet_name, output_file):
            return send_file(
                output_file, as_attachment=True, download_name=f"{sheet_name}.xlsx"
            )
        else:
            return jsonify({"error": "Failed to extract sheet"}), 500
    else:
        return jsonify({"error": "File not found"}), 404


@app.route("/download", methods=["POST"])
def download():
    file_path = request.json["path"]
    abs_file_path = os.path.abspath(file_path)
    if os.path.exists(abs_file_path):
        return send_file(
            abs_file_path, as_attachment=True, download_name=os.path.basename(file_path)
        )
    else:
        return jsonify({"error": "File not found"}), 404


@app.route("/stream")
def stream():
    def event_stream():
        while True:
            message = log_queue.get()
            yield f"data: {message}\n\n"

    return Response(event_stream(), mimetype="text/event-stream")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", threaded=True)

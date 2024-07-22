from flask import Flask, jsonify, request, render_template
from bundle_details_collector import (
    check_cookies,
    custom_qp_range,
    auto_qp_series_generator,
    manual_login,
)
# import colorama
# import logging
# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)
# log.disabled = True

app = Flask(
    __name__,
    template_folder="web_template",
)
# app.config = {
#      "DEBUG": True,
#      "TEMPLATES_AUTO_RELOAD": True,
#      "CONTENT_SECURITY_POLICY": "default-src 'self' https://0.0.0.0:443"
# }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/start_qp_grabber", methods=["POST"])
def start_qp_grabber():
    cookie_status, captcha_link = check_cookies()
    if not cookie_status:
        return jsonify({"status": "login_required", "captcha_url": captcha_link})

    exam_name = request.form["examName"]
    custom_qp_range_mode = request.form.get("customQPRangeMode") == "on"

    if custom_qp_range_mode:
        qp_range = request.form["customQPRange"].split(",")
        custom_qp_range(qp_range, exam_name)
    else:
        qp_series = request.form["qpSeries"]
        qp_start_range = int(request.form["qpStartRange"])
        qp_end_range = int(request.form["qpEndRange"])
        auto_qp_series_generator(qp_series, qp_start_range, qp_end_range, exam_name)

    return jsonify(
        {"status": "success", "message": "QP Code Grabber completed successfully"}
    )


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    captcha = request.form["captcha"]

    if manual_login(username, password, captcha):
        return jsonify({"status": "success", "message": "Login successful"})
    else:
        return jsonify({"status": "error", "message": "Login failed"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", ssl_context="adhoc")

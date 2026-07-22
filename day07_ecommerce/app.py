from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from pathlib import Path
from services.data_service import load_dashboard_data
from services.qa_service import answer_question

BASE_DIR = Path(__file__).parent
app = Flask(__name__)
app.secret_key = "day07_student_secret_2026"


# 登录校验拦截器
@app.before_request
def login_check():
    white_list = [url_for("login")]
    if request.path.startswith("/static"):
        return
    if request.path not in white_list and "username" not in session:
        flash("请先登录系统", "warn")
        return redirect(url_for("login"))


# 首页跳转看板
@app.route("/")
def index():
    return redirect(url_for("dashboard"))


# 登录页面
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uname = request.form.get("username")
        pwd = request.form.get("password")
        if uname == "student" and pwd == "day07":
            session["username"] = uname
            flash("登录成功", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("用户名或密码错误", "error")
    return render_template("login.html")


# 退出登录
@app.route("/logout")
def logout():
    session.clear()
    flash("已退出登录", "info")
    return redirect(url_for("login"))


# 数据看板（带品类筛选参数）
@app.route("/dashboard")
def dashboard():
    selected_cat = request.args.get("category", "全部")
    data = load_dashboard_data(BASE_DIR, selected_cat)
    return render_template(
        "dashboard.html",
        username=session["username"],
        selected_category=selected_cat,
        **data
    )


# 智能问答页面
@app.route("/assistant")
def assistant():
    return render_template("assistant.html")


# 问答接口API
@app.route("/api/ask", methods=["POST"])
def api_ask():
    q = request.json.get("question", "")
    res = answer_question(BASE_DIR, q)
    return jsonify({"reply": res})


# 404捕获
@app.errorhandler(404)
def page_404(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)

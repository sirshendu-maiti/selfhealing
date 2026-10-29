from flask import Flask, render_template, request
app = Flask(__name__)

@app.get("/")
def login():
    return render_template("login.html", error=None, success=None)

@app.post("/login")
def login_post():
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    # Demo-only credential check. Never use this pattern for real authentication.
    if email == "demo@example.com" and password == "demo123":
        return render_template("login.html", error=None, success="Signed in to the demo successfully.")
    return render_template("login.html", error="Email or password is incorrect.", success=None), 401

if __name__ == "__main__":
    app.run(debug=True)

from app import app

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.run(port=5000, debug=False)

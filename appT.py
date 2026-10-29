from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Application V1</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
    <h2>Menu-Driven Application</h2>
    <form method="post">
        <!-- Input 1 -->
        <input name="val1" type="number" step="any" placeholder="Value 1 (e.g. Price/Marks/Temp)" required>
        
        <!-- Input 2 (Optional based on question) -->
        <input name="val2" type="number" step="any" placeholder="Value 2 (Optional)">
        
        <!-- Dropdown Menu for Push 1 & Push 2 Features -->
        <select name="action">
            <option value="opt1">Option 1 (Push 1)</option>
            <option value="opt2">Option 2 (Push 1)</option>
            <!-- Add new options here for Push 2 -->
        </select>
        <button type="submit">Submit</button>
    </form>
    {% if result is not none %}
        <h3>Result: {{ result }}</h3>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    if request.method == "POST":
        try:
            val1 = float(request.form.get("val1", 0))
            val2_str = request.form.get("val2", "")
            val2 = float(val2_str) if val2_str else 0
            action = request.form["action"]

            # Replace logic below based on the specific practical question
            if action == "opt1":
                result = val1 + val2
            elif action == "opt2":
                result = val1 - val2
            else:
                result = "Invalid operation"
        except (ValueError, KeyError):
            result = "Invalid input"

    return render_template_string(HTML, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
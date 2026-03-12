from flask import Flask, request, render_template_string
from pywinauto import Application, Desktop
import time

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Automação Calculadora</title>
</head>
<body>

<h2>Calculadora Automática</h2>

<form method="POST">
    <input name="a" placeholder="Número A">
    <input name="b" placeholder="Número B">
    <button type="submit">Calcular</button>
</form>

{% if resultado %}
<h3>Resultado: {{resultado}}</h3>
{% endif %}

</body>
</html>
"""

@app.route("/", methods=["GET","POST"])
def index():

    resultado = None

    if request.method == "POST":

        a = request.form["a"]
        b = request.form["b"]

        Application(backend="uia").start("calc.exe")
        time.sleep(2)

        calc = Desktop(backend="uia").window(title_re="Calculadora")

        calc.type_keys(a)
        calc.type_keys("*")
        calc.type_keys(b)
        calc.type_keys("=")

        time.sleep(1)

        display = calc.child_window(auto_id="CalculatorResults", control_type="Text")

        resultado = display.window_text()
        print(resultado)
        resultado = resultado.replace("A exibição é ", "").replace("Display is ", "")

    return render_template_string(HTML, resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

class AplicacionCalculadora:
    def __init__(self):
        self.variables = {}
        self.pila_operandos= []
        self.pila_operadores = []

    def evaluar_expresion(self, expresion):
        try:
            expresion_sin_at = expresion.replace('@', ' ')
            resultado = eval(expresion_sin_at, self.variables)
            
            variables_originales = [token.strip() for token in expresion.split('@') if token.strip()]
            operadores_originales = [c for c in expresion if c == '+' or c == '-' or c == '*' or c == '/' or c == '(' or c == ')']

            return {
                'resultado': str(resultado),
                'pila_operandos': variables_originales,
                'pila_operadores': operadores_originales
            }
        except Exception as e:
            return {'error': "Error: " + str(e)}

    def crear_variable(self, nombre, valor):
        try:
            valor_variable = float(valor)
            self.variables[nombre] = valor_variable
            return "Variable creada exitosamente"
        except ValueError:
            return "Error: Valor de variable inválido"

app_calculadora = AplicacionCalculadora()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    expresion = request.form['expresion']
    resultado = app_calculadora.evaluar_expresion(expresion)
    return jsonify(resultado)

@app.route('/crear_variable', methods=['POST'])
def crear_variable():
    nombre = request.form['nombre']
    valor = request.form['valor']
    resultado = app_calculadora.crear_variable(nombre, valor)
    nombres_variables = list(app_calculadora.variables.keys())
    return jsonify({'resultado': resultado, 'variables': nombres_variables})

if __name__ == '__main__':
    app.run(debug=True)
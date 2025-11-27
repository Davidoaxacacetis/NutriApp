from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime
import requests

app = Flask(__name__)
USUARIOS_REGISTRADOS ={
    "24308060610040@cetis1.edu.mx":{
        "password":"KanyeWest17*",
        "nombre":"Administrador",
        "fecha_nacimiento":"2009-04-11",
        "apellido":"West"
    }
}

API_KEY = "udJqwbKLuDZTGgIEmmOlAre5tV47sjQ5ichJxxQO"
USDA_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"

tipos = {
"Branded": "Producto de marca comercial",
"Survey (FNDDS)": "Alimento de encuesta nacional",
"Foundation": "Alimento base (datos detallados)",
"SR Legacy": "Base de datos antigua del USDA",
"Sample": "Muestra analizada en laboratorio"
}

app.config['SECRET_KEY'] = "OODA"

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/articulos')
def articulos():
    return render_template('articulos.html')

@app.route('/rutinas')
def rutinas():
    return render_template('rutinas.html')

@app.route("/registrate")
def registro():
    return render_template("registro.html", request=request)

@app.route("/registrame", methods=["POST"])
def registrame():
    nombrecompleto = request.form.get("name")
    apellido = request.form.get("apellido")
    email = request.form.get("email")
    contraseña = request.form.get("contraseña")
    confirmarcontra = request.form.get("confirmarcontra")
    fecha_nacimiento = request.form.get("fecha_nacimiento")
    genero = request.form.get("genero")
    
    peso = float(request.form.get("peso"))       
    altura = int(request.form.get("altura"))     

    objetivos = request.form.get("objetivos")
    alergias = request.form.get("alergias")
    intolerancias = request.form.get("intolerancias")
    dietas = request.form.get("dietas")
    no_me_gustan = request.form.get("no_me_gustan")
    experiencia_cocina = request.form.get("experiencia_cocina")

    if not nombrecompleto or not apellido or not email or not contraseña or not confirmarcontra or not fecha_nacimiento:
        flash("Todos los campos son obligatorios.", "error")
        return render_template("registro.html", **request.form)

    if contraseña != confirmarcontra:
        flash("Las contraseñas no coinciden", "error")
        return render_template("registro.html", **request.form)

    if email in USUARIOS_REGISTRADOS:
        flash("Este correo electrónico ya está registrado", "error")
        return render_template("registro.html", **request.form)

    try:
        fecha_nacimiento_obj = datetime.strptime(fecha_nacimiento, "%Y-%m-%d")
        today = datetime.today()
        edad = today.year - fecha_nacimiento_obj.year - (
            (today.month, today.day) < (fecha_nacimiento_obj.month, fecha_nacimiento_obj.day)
        )
    except ValueError:
        flash("Fecha de nacimiento inválida", "error")
        return render_template("registro.html", **request.form)

    USUARIOS_REGISTRADOS[email] = {
        "password": contraseña,
        "nombre": nombrecompleto,
        "apellido": apellido,
        "fecha_nacimiento": fecha_nacimiento,
        "edad": edad,
        "genero": genero,
        "peso": peso,
        "altura": altura,
        "objetivos": objetivos,
        "alergias": alergias,
        "intolerancias": intolerancias,
        "dietas": dietas,
        "no_me_gustan": no_me_gustan,
        "experiencia_cocina": experiencia_cocina
    }

    flash(f"¡Registro exitoso para {nombrecompleto}!", "success")
    return redirect(url_for("sesion"))


@app.route("/inicia-sesion")
def sesion():
    return render_template("inicia.html")

@app.route("/cerrar-sesion")
def cerrar_sesion():
    session.clear()
    flash("Sesión cerrada correctamente", "info")
    return redirect(url_for("index"))

@app.route("/validalogin", methods=["POST"])
def validalogin():
    if request.method == "POST":
        email = request.form.get("usu_name", "").strip()
        password = request.form.get("password2", "")

        if not email or not password:
            flash("Por favor ingresa email y contraseña", "error")
            return render_template("inicia.html")

        elif email in USUARIOS_REGISTRADOS:
            usuario = USUARIOS_REGISTRADOS[email]

            if usuario["password"] == password:
                session["usuario_email"] = email
                session["usuario"] = usuario["nombre"]
                session["logueado"] = True  
                flash(f"Bienvenido {usuario['nombre']}!", "success")
                return redirect(url_for("index"))
            else:
                flash("Contraseña incorrecta", "error")
        else:
            flash("Usuario no encontrado", "error")
    
    return render_template("inicia.html")

@app.route("/perfil")
def perfil():
    if not session.get("logueado"):
        return redirect(url_for("sesion"))
    
    email = session.get("usuario_email")   
    usuario = USUARIOS_REGISTRADOS.get(email)
    
    return render_template("perfil.html", usuario=usuario, email=email)


@app.route("/tasa")
def Itmb():
    return render_template("calculartmb.html")

@app.route("/resultadotmb")
def resul():
    return render_template("tmb.html", request=request)

@app.route("/calculadora", methods=["GET","POST"])
def calcutmb():
    peso = float(request.form.get("peso"))
    altura = float(request.form.get("altura")) 
    edad = float(request.form.get("edad"))
    genero = request.form.get("genero")
    actividad = request.form.get("actividad")

    if genero == "Hombre":
        tmb = (10 * peso) + (6.25 * altura) - (5 * edad) + 5
    else:
        tmb = (10 * peso) + (6.25 * altura) - (5 * edad) - 161

    if actividad == "seden":
        Get = tmb * 1.2
    elif actividad == "ligera":
        Get = tmb * 1.375
    elif actividad == "moderada":
        Get = tmb * 1.55
    elif actividad == "alta":
        Get = tmb * 1.725

    return render_template("tmb.html", v1=round(tmb, 2), v2=round(Get, 2))


@app.route("/Resultadoimc")
def Iimc():
    return render_template("calcuimc.html")

@app.route("/resultadoimc", methods=["POST"])
def calcuimc():
    peso = float(request.form.get("peso1"))
    altura = float(request.form.get("altura1")) / 100 

    imc = peso / (altura ** 2)

    if imc < 18.5:
        niv = "Bajo peso"
    elif imc < 25.0:
        niv = "Peso normal"
    elif imc < 30.0:
        niv = "Sobrepeso"
    elif imc < 35.0:
        niv = "Obesidad clase 1"
    elif imc < 40.0:
        niv = "Obesidad clase 2"
    else:
        niv = "Obesidad clase 3 (mórbida)"

    return render_template("imc.html", v3=round(imc, 2), v4=niv)


@app.route("/pesoideal", methods=["GET", "POST"])
def pesoideal():
    resultado = None
    rango = None
    if request.method == "POST":
        altura = float(request.form.get("altura"))   
        genero = request.form.get("genero")

        if genero == "Hombre":
            peso_ideal = 50 + 0.91 * ((altura / 2.54) - 60)
        else:
            peso_ideal = 45.5 + 0.91 * ((altura / 2.54) - 60)
        
        peso_minimo = round(peso_ideal - 5, 2)
        peso_maximo = round(peso_ideal + 5, 2)
        
        resultado = round(peso_ideal, 2)
        rango = (peso_minimo, peso_maximo)

    return render_template("pesoideal.html", resultado=resultado, rango=rango)
@app.route("/macros", methods=["GET", "POST"])
def macros():
    proteinas = grasas = carbohidratos = None
    if request.method == "POST":
        calorias = float(request.form.get("calorias"))

        proteinas = round((calorias * 0.3) / 4, 1)
        grasas = round((calorias * 0.25) / 9, 1)
        carbohidratos = round((calorias * 0.45) / 4, 1)

    return render_template("macros.html", proteinas=proteinas, grasas=grasas, carbohidratos=carbohidratos)

@app.route("/busqueda", methods=["GET", "POST"])
def busqueda():
    alimentos = []
    query = ""

    if request.method == "POST":
        query = request.form["query"].lower()

        url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={query}&api_key={API_KEY}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            resultados = data.get("foods", [])

            alimentos = [
                f for f in resultados
                if query in f.get("description", "").lower()
            ]
        else:
            alimentos = []

    return render_template("busqueda.html", alimentos=alimentos, query=query, tipos=tipos)

@app.route("/detalle/<int:fdc_id>")
def detalle(fdc_id):
    url = f"https://api.nal.usda.gov/fdc/v1/food/{fdc_id}?api_key={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
    else:
        data = None

    return render_template("detalle.html", alimento=data)

def obtener_nutrientes(nombre):
    params = {
        "api_key": API_KEY,
        "query": nombre,
        "pageSize": 1
    }

    resp = requests.get(USDA_URL, params=params)
    data = resp.json()

    if "foods" not in data or len(data["foods"]) == 0:
        return None

    food = data["foods"][0]

    nutrientes = {
        "Proteína (g)": 0,
        "Grasa (g)": 0,
        "Carbohidratos (g)": 0,
        "Calorías": 0
    }

    for n in food.get("foodNutrients", []):
        nombre_n = n.get("nutrientName", "")
        valor = n.get("value")

        if valor is None:
            continue

        if nombre_n == "Protein":
            nutrientes["Proteína (g)"] = valor
        elif nombre_n == "Total lipid (fat)":
            nutrientes["Grasa (g)"] = valor
        elif nombre_n == "Carbohydrate, by difference":
            nutrientes["Carbohidratos (g)"] = valor
        elif nombre_n == "Energy":
            nutrientes["Calorías"] = valor

    return nutrientes

@app.route("/analizador")
def analizador():
    return render_template("analizador.html")

@app.route("/analizar", methods=["POST"])
def analizar():
    receta = request.form.get("ingrediente")

    resultado = obtener_nutrientes(receta)

    if resultado is None:
        return render_template("resultado.html", ingrediente=receta, error=True)

    datos, porcion = resultado

    for k in datos:
        datos[k] = round(datos[k], 2)

    return render_template("resultado.html",ingrediente=receta,nutrientes=datos,porcion=porcion,error=False)

if __name__ == '__main__':
    app.run(debug=True)
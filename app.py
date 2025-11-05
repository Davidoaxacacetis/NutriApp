from flask import Flask, render_template, request, redirect, url_for, flash, session


app = Flask(__name__)
USUARIOS_REGISTRADOS ={
    "24308060610040@cetis1.edu.mx":{
        "password":"KanyeWest17*",
        "nombre":"Administrador",
        "fecha_nacimiento":"2009-04-11",
        "apellido":"West"
    }
}

app.config['SECRET_KEY'] = "OODA"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/acerca-de")
def acecade():
    return render_template("acercade.html")

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
    peso2 = request.form.get("peso2")
    altura2 = request.form.get("altura2")

    if contraseña != confirmarcontra:
        flash("Las contraseñas no coinciden", "error")
        return render_template("registro.html")

    if email in USUARIOS_REGISTRADOS:
        flash("Este correo ya está registrado", "error")
        return render_template("registro.html")

    USUARIOS_REGISTRADOS[email] = {
        "password": contraseña,
        "nombre": nombrecompleto,
        "fecha_nacimiento": fecha_nacimiento,
        "genero": genero
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
    if request.method== "POST":
        email= request.form.get("usu_name","").strip()
        password =request.form.get("password2","")

        if not email or not password:
            flash("Por favor ingresa email y contraseña", "error")
        elif email in USUARIOS_REGISTRADOS:
            usuario= USUARIOS_REGISTRADOS[email]
            if usuario["password"]==password:
                session["usuario_email"] = email
                session["usuario"] = usuario["nombre"]
                session["logueado"] = True
                return redirect(url_for("index"))
            else:
                flash("Contraseña incorrecta","error")
        else:
            flash("Usuario no encontrado","error")
    
    return render_template("inicia.html")

@app.route("/tasa")
def Itmb():
    return render_template("calculartmb.html")

@app.route("/resultadotmb")
def resul():
    return render_template("tmb.html", request=request)

@app.route("/calculadora", methods=["GET","POST"])
def calcutmb():
    peso = request.form.get("peso")
    altura = request.form.get("altura")
    edad = request.form.get("edad")
    genero = request.form.get("genero")
    actividad =request.form.get("actividad")
    if genero == "Hombre":
        tmb = (10* float(peso))+(6.25 * float(altura)) - (5 * float(edad)) + 5
    elif genero == "Mujer":
        tmb = (10 * float(peso))+(6.25* float(altura)) - (5 * float(edad)) - 161

    if actividad == "seden":
        Get = tmb * 1.2
    elif actividad == "ligera":
        Get = tmb * 1.375
    elif actividad == "moderada":
        Get = tmb * 1.55
    elif actividad == "alta":
        Get = tmb * 1.725

    return render_template("tmb.html", v1=tmb, v2=Get)

@app.route("/daw")
def Iimc():
    return render_template("calcuimc.html")

@app.route("/resultadoimc", methods=["POST"])
def calcuimc():
    peso = float(request.form.get("peso1"))
    altura = float(request.form.get("altura1"))

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

if __name__ == '__main__':
    app.run(debug=True)
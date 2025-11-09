from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///denuncias.db'
db = SQLAlchemy(app)

class Denuncia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    lugar = db.Column(db.String(200), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

# formulario + listado (creación)
@app.route('/denuncias', methods=['GET', 'POST'])
def denuncias():
    if request.method == 'POST':
        nombre = request.form['nombre']
        lugar = request.form['lugar']
        nueva_denuncia = Denuncia(nombre=nombre, lugar=lugar)
        db.session.add(nueva_denuncia)
        db.session.commit()
        return redirect(url_for('denuncias'))
    denuncias = Denuncia.query.all()
    return render_template('denuncias.html', denuncias=denuncias)

# editar: GET muestra formulario con datos, POST guarda cambios
@app.route('/denuncias/editar/<int:id>', methods=['GET', 'POST'])
def editar_denuncia(id):
    denuncia = Denuncia.query.get_or_404(id)
    if request.method == 'POST':
        denuncia.nombre = request.form['nombre']
        denuncia.lugar = request.form['lugar']
        db.session.commit()
        return redirect(url_for('denuncias'))
    return render_template('editar_denuncia.html', denuncia=denuncia)

# eliminar (uso POST para seguridad)
@app.route('/denuncias/eliminar/<int:id>', methods=['POST'])
def eliminar_denuncia(id):
    denuncia = Denuncia.query.get_or_404(id)
    db.session.delete(denuncia)
    db.session.commit()
    return redirect(url_for('denuncias'))

@app.route('/tipos')
def tipos():
    return render_template('tipos.html')

@app.route('/reciclaje')
def reciclaje():
    return render_template('reciclaje.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Bandas.sqlite3'

db = SQLAlchemy(app)

class Bandas(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(150))
    vertente = db.Column(db.String(150))
    país = db.Column(db.String(150))
    
    def __init__(self, nome, vertente, país): 
        self.nome = nome
        self.vertente = vertente
        self.país = país

#listando bandas
@app.route('/')
def Banda():
    band = Bandas.query.all()
    return render_template('bandas.html', banda=band)

#adcionando bandas ao BD
@app.route('/Add', methods=['GET', 'POST'])
def Add():
    if request.method == 'POST':
        band = Bandas(request.form['nome'], request.form['vertente'], request.form['país'])
        db.session.add(band)
        db.session.commit()
        return redirect(url_for('Banda'))
    return render_template('addband.html')

#atualizando informações das bandas
@app.route('/Update/<int:id>', methods=["GET", "POST"])
def Update(id):
    band = Bandas.query.get(id)
    if request.method == "POST":
        band.nome = request.form['nome']
        band.vertente = request.form['vertente']
        band.país = request.form['país']
        db.session.commit()
        return redirect(url_for('Banda'))

    return render_template('edit.html', banda=band)

#deletando bandas do BD
@app.route('/Del/<int:id>')
def Del(id):
    band = Bandas.query.get(id)
    db.session.delete(band)
    db.session.commit()
    return redirect(url_for('Banda'))


if __name__ == '__main__':
    db.create_all()#criando BD
    app.run(debug=True)
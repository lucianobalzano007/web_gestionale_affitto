from flask import Flask, render_template, request, redirect, url_for, session, g, flash, send_file
from user import User
import contratto
import db_manager
import ricevuta
import data_manager
import file_manager
import json
from os import getenv
import os

app = Flask(__name__)
app.secret_key = getenv('SECRET_KEY_SESSION')

@app.route('/')
def index():
    if 'email' in session:
        user = User.get_user_by_email(session['email'])
        return redirect(url_for('home'))
    if db_manager.conta_utenti() == 0:
        return redirect(url_for('register_admin'))
    return redirect(url_for('login'))

@app.route('/home')
def home():
    if 'email' in session:
        utente=User.get_user_by_email(session['email'])
        return render_template('index.html',utente=utente)
    return redirect('login')

@app.route('/register_admin', methods=['POST', 'GET'])
def register_admin():
    if request.method == 'POST' and db_manager.conta_utenti() == 0:
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        print(f"Name: {name}, Surname: {surname}")  # Debugging line
        print(f"Email: {email}, Password: {password}")  # Debugging line
        if password != confirm_password:
            flash("Errore 400: Le password non coincidono", "error")
            return redirect(url_for('register_admin'))
        user = User(name, surname, email, password)
        user.create_user()
        return redirect(url_for('login'))
    elif db_manager.conta_utenti()!=0:
        return redirect(url_for('login'))
    return render_template('register_admin.html')

@app.route('/registra_contratto', methods=['POST','GET'])
def registra_contratto():
    if 'email' in session:
        utente=User.get_user_by_email(session['email'])
        if request.method == 'POST':
            tipo_abi=request.form['tipo_abi']
            ind_abi=request.form['ind_abi']
            city_abi=request.form['city_abi']
            prov_abi=request.form['prov_abi']
            note_abi=request.form['note_abi']
            ag_contr=request.form['ag_contr']
            datarec_contr=request.form['datarec_contr']
            datasti_contr=request.form['datasti_contr']
            cod_contr=request.form['cod_contr']
            durata_contr=request.form['durata_contr']
            nome_loc=request.form['nome_loc']
            cog_loc=request.form['cog_loc']
            cf_loc=request.form['cf_loc']
            nome_cond=request.form['nome_cond']
            cog_cond=request.form['cog_cond']
            cf_cond=request.form['cf_cond']
            new_contratto = contratto.Contratto(
            tipo_abi,
            ind_abi,
            city_abi,
            prov_abi,
            note_abi,
            ag_contr,
            datarec_contr,
            datasti_contr,
            cod_contr,
            durata_contr,
            nome_loc,
            cog_loc,
            cf_loc,
            nome_cond,
            cog_cond,
            cf_cond
            )
            result=new_contratto.crea_contratto_di_locazione()
            if result==0:
                flash('200: Registrazione contratto completata con successo', 'success')
                return render_template('new_contratto.html',utente=utente)
            else:
                flash('400: Qualcosa non ha funzionato', 'error')
                return render_template('new_contratto.html',utente=utente)
        return render_template('new_contratto.html',utente=utente)
    return redirect('login')

@app.route('/view_contratti')
def view_contratti():
    if 'email' in session:
        utente=User.get_user_by_email(session['email'])
        lista_mongo=db_manager.preleva_contratti()
        contratti=contratto.Contratto.get_lista_contratti(lista_mongo)
        if contratti==[]:
            flash('400: non sono presenti contratti', 'error')
            return render_template('view_contratti.html', utente=utente, contratti=contratti)
        else:
            return render_template('view_contratti.html', utente=utente, contratti=contratti)
    return redirect(url_for('login'))

@app.route('/elimina_contratto/<id_contr>')
def elimina_contratto(id_contr):
    if 'email' in session:
        utente=User.get_user_by_email(session['email'])
        result=db_manager.eliminazione_contratto(id_contr)
        result_rc=db_manager.eliminazione_ricevute(id_contr)
        if result==0 and result_rc==0:
            lista_mongo=db_manager.preleva_contratti()
            contratti=contratto.Contratto.get_lista_contratti(lista_mongo)
            flash('200: contratto eliminato con successo', 'success')
            return redirect(url_for('view_contratti'))
        else:
            lista_mongo=db_manager.preleva_contratti()
            contratti=contratto.Contratto.get_lista_contratti(lista_mongo)
            flash('500: eliminazione contratto non avvenuta con successo', 'success')
            return redirect(url_for('view_contratti'))
    return redirect(url_for('login'))

@app.route('/modifica_contratto/<id_contr>', methods=['POST', 'GET'])
def modifica_contratto(id_contr):
    if 'email' in session:
        utente=User.get_user_by_email(session['email'])
        if request.method == 'POST':
            tipo_abi=request.form['tipo_abi']
            ind_abi=request.form['ind_abi']
            city_abi=request.form['city_abi']
            prov_abi=request.form['prov_abi']
            note_abi=request.form['note_abi']
            ag_contr=request.form['ag_contr']
            datarec_contr=request.form['datarec_contr']
            datasti_contr=request.form['datasti_contr']
            cod_contr=request.form['cod_contr']
            durata_contr=request.form['durata_contr']
            nome_loc=request.form['nome_loc']
            cog_loc=request.form['cog_loc']
            cf_loc=request.form['cf_loc']
            nome_cond=request.form['nome_cond']
            cog_cond=request.form['cog_cond']
            cf_cond=request.form['cf_cond']
            new_contratto = contratto.Contratto(
            tipo_abi,
            ind_abi,
            city_abi,
            prov_abi,
            note_abi,
            ag_contr,
            datarec_contr,
            datasti_contr,
            cod_contr,
            durata_contr,
            nome_loc,
            cog_loc,
            cf_loc,
            nome_cond,
            cog_cond,
            cf_cond
            )
            result=new_contratto.modifica_contratto_di_locazione(id_contr)
            if result == 0:
                contr=contratto.Contratto.get_contratto(id_contr)
                flash('200: modifica del contratto avvenuta con successo', 'success')
                return render_template('modify_contr.html', utente=utente, contratto=contr, codice=id_contr)
            else:
                contr=contratto.Contratto.get_contratto(id_contr)
                flash('500: errore nella modifica del contratto', 'error')
                return render_template('modify_contr.html', utente=utente, contratto=contr, codice=id_contr)
        contr=contratto.Contratto.get_contratto(id_contr)
        return render_template('modify_contr.html', utente=utente, contratto=contr, codice=id_contr)
    return redirect(url_for('login'))

@app.route('/sel_contratto')
def sel_contratto():
    if 'email' in session:
        utente=User.get_user_by_email(session['email'])
        lista_mongo=db_manager.preleva_contratti()
        contratti=contratto.Contratto.get_lista_contratti(lista_mongo)
        if contratti==[]:
            flash('400: non sono presenti contratti', 'error')
            return render_template('sel_contratto.html', utente=utente, contratti=contratti)
        else:
            return render_template('sel_contratto.html', utente=utente, contratti=contratti)
    return redirect(url_for('login'))

@app.route('/new_ricevuta/<codice_id>', methods=['POST', 'GET'])
def new_ricevuta(codice_id):
    if 'email' in session:
        utente=User.get_user_by_email(session['email'])
        if request.method== 'POST':
            num_ric=request.form['num_ric']
            data_ric=request.form['data_ric']
            datain_ric=request.form['datain_ric']
            dataout_ric=request.form['dataout_ric']
            cas1imp_ric=request.form['cas1imp_ric']
            cas2_ric=request.form['cas2_ric']
            cas2imp_ric=request.form['cas2imp_ric']
            cas3_ric=request.form['cas3_ric']
            cas3imp_ric=request.form['cas3imp_ric']
            cas4_ric=request.form['cas4_ric']
            cas4imp_ric=request.form['cas4imp_ric']
            cas5_ric=request.form['cas5_ric']
            cas5imp_ric=request.form['cas5imp_ric']
            pagato_ric=request.form['pagato_ric']
            iva_ric=request.form['iva_ric']
            contr=db_manager.cerca_contratto(codice_id)
            ric=ricevuta.Ricevuta(contr,codice_id,num_ric,data_ric,datain_ric,dataout_ric,cas1imp_ric,cas2_ric,cas2imp_ric,cas3_ric,cas3imp_ric,cas4_ric,cas4imp_ric,cas5_ric,cas5imp_ric,pagato_ric,iva_ric)
            buffer=ric.creazione_ricevuta()
            return send_file(buffer,mimetype='application/pdf',as_attachment=False)
        num_ric=db_manager.conta_ricevute(codice_id)+1
        return render_template('new_ricevuta.html', codice=codice_id, num_ric=num_ric, utente=utente)
    return redirect(url_for('login'))

@app.route('/sel_view_ric_contratto')
def sel_view_ric_contratto():
    if 'email' in session:
        utente=User.get_user_by_email(session['email'])
        lista_mongo=db_manager.preleva_contratti()
        contratti=contratto.Contratto.get_lista_contratti(lista_mongo)
        if contratti==[]:
            flash('400: non sono presenti contratti', 'error')
            return render_template('sel_view_ric_contratto.html', utente=utente, contratti=contratti)
        else:
            return render_template('sel_view_ric_contratto.html', utente=utente, contratti=contratti)
    return redirect(url_for('login'))

@app.route('/view_ricevute/<codice_id>',methods=['POST', 'GET'])
def view_ricevute(codice_id):
    if 'email' in session:
        utente=User.get_user_by_email(session['email'])
        contr=contratto.Contratto.get_contratto(codice_id)
        lista_ricevute=db_manager.cerca_ricevute(codice_id)
        if request.method=='POST':
            year=str(request.form['year'])
            lista_ric_vis=ricevuta.Ricevuta.get_lista_ricevute_by_year(contr,lista_ricevute,year)
            if lista_ric_vis==[]:
                flash('400: non sono presenti ricevute', 'error')
                return render_template('view_ricevute.html',lista_ric=lista_ric_vis,utente=utente,contratto=contr,codice=codice_id)
            else:
                return render_template('view_ricevute.html',lista_ric=lista_ric_vis,utente=utente,contratto=contr,codice=codice_id)
        lista_ric_vis=ricevuta.Ricevuta.get_lista_ricevute(contr,lista_ricevute)
        if lista_ric_vis==[]:
            flash('400: non sono presenti ricevute', 'error')
            return render_template('view_ricevute.html',lista_ric=lista_ric_vis,utente=utente,contratto=contr,codice=codice_id)
        else:
            return render_template('view_ricevute.html',lista_ric=lista_ric_vis,utente=utente,contratto=contr,codice=codice_id)
    return redirect(url_for('login'))

@app.route('/stampa_ricevuta/<codice_id>/<codice_ric>')
def stampa_ricevuta(codice_id,codice_ric):
    if 'email' in session:
        utente=User.get_user_by_email(session['email'])
        contr=db_manager.cerca_contratto(codice_id)
        ric=db_manager.cerca_ricevuta(codice_ric)
        if contr==1 or ric==1:
            return '<h1>Error 404</h1>/n<p>Page not found</p>'
        buffer=file_manager.stampa_ricevuta_pdf(contr,ric)
        return send_file(buffer,mimetype='application/pdf',as_attachment=False)
    return redirect(url_for('login'))

@app.route('/elimina_ricevuta/<codice_id>/<codice_ric>')
def elimina_ricevuta(codice_id,codice_ric):
    if 'email' in session:
        utente=User.get_user_by_email(session['email'])
        result=db_manager.eliminazione_ricevuta(codice_ric)
        if result==0:
            flash('200: ricevuta eliminata con successo', 'success')
            return redirect(url_for('view_ricevute',codice_id=codice_id))
        else:
            flash('500: Ops! Qualcosa è andato storto', 'error')
            return redirect(url_for('view_ricevute',codice_id=codice_id))
    return redirect(url_for('login'))

@app.route('/modifica_ricevuta/<codice_id>/<codice_ric>', methods=['POST','GET'])
def modifica_ricevuta(codice_id,codice_ric):
    if 'email' in session:
        utente=User.get_user_by_email(session['email'])
        if request.method=='POST':
            num_ric=request.form['num_ric']
            data_ric=request.form['data_ric']
            datain_ric=request.form['datain_ric']
            dataout_ric=request.form['dataout_ric']
            cas1imp_ric=request.form['cas1imp_ric']
            cas2_ric=request.form['cas2_ric']
            cas2imp_ric=request.form['cas2imp_ric']
            cas3_ric=request.form['cas3_ric']
            cas3imp_ric=request.form['cas3imp_ric']
            cas4_ric=request.form['cas4_ric']
            cas4imp_ric=request.form['cas4imp_ric']
            cas5_ric=request.form['cas5_ric']
            cas5imp_ric=request.form['cas5imp_ric']
            pagato_ric=request.form['pagato_ric']
            iva_ric=request.form['iva_ric']
            contr=db_manager.cerca_contratto(codice_id)
            ric=ricevuta.Ricevuta(contr,codice_id,num_ric,data_ric,datain_ric,dataout_ric,cas1imp_ric,cas2_ric,cas2imp_ric,cas3_ric,cas3imp_ric,cas4_ric,cas4imp_ric,cas5_ric,cas5imp_ric,pagato_ric,iva_ric)
            result=ric.update_ricevuta()
            if result==0:
                flash('200: Aggiornamento della ricevuta avvenuta con successo', 'success')
                return render_template('modify_ric.html', ricevuta=ric,utente=utente)
            else:
                flash('500: Ops qualcosa è andato storto', 'error')
                ric=ricevuta.Ricevuta.get_ricevuta(codice_id,codice_ric)
                return render_template('modify_ric.html',ricevuta=ric,utente=utente)
        ric=ricevuta.Ricevuta.get_ricevuta(codice_id,codice_ric)
        return render_template('modify_ric.html',ricevuta=ric,utente=utente)
    return redirect(url_for('login'))

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print(f"Email: {email}, Password: {password}")  # Debugging line
        user = User.get_user_by_email(email)
        if user == None:
            flash("Errore 401: Email e/o password non valide", "error")
            return redirect(url_for('login'))
        if user.check_password(password):
            session['email'] = email
            return redirect(url_for('home'))
        flash("Errore 401: Email e/o password non valide", "error")
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))


if __name__== '__main__':

    app.run(host='0.0.0.0', port=5000, debug=True)
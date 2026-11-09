from telegram import Update, InputProfilePhotoStatic, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, ConversationHandler, filters, Application
from os import getenv
import requests
import contratto
import ricevuta

ANNO=1

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Benvenuto {update.effective_user.first_name} da qui puoi visualizzare le ricevute d'affitto pagate e non ed ricevere una notifica quando il locatore ha generato una ricevuta")
    await update.message.reply_text(r"*Attenzione\!* Non è obbiligatorio ricevere la notifica", parse_mode='MarkdownV2')
    telegram_user=update.effective_user.username
    lista_contratti=contratto.Contratto.get_lista_contratti()
    lc=[]
    for contr in lista_contratti:
        if contr[0].get_telegram_user()==telegram_user:
            lc.append(contr[0])
            lc.append(contr[1])
    if lc==[]:
        await update.message.reply_text(f'Ciao {update.effective_user.first_name}\n non hai alcun affitto')
    else:
        contr=lc[0]
        code=lc[1]
        contr.set_chat_id(update.message.chat_id)
        contr.modifica_contratto_di_locazione(code)
        await update.message.reply_text(f'Sistema di notifica attivato')
        
async def disable_notify(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    telegram_user=update.effective_user.username
    lista_contratti=contratto.Contratto.get_lista_contratti()
    lc=[]
    for contr in lista_contratti:
        if contr[0].get_telegram_user()==telegram_user:
            lc.append(contr[0])
            lc.append(contr[1])
    if lc==[]:
        await update.message.reply_text(f'Ciao {update.effective_user.first_name}\n non hai alcun affitto')
    else:
        contr=lc[0]
        code=lc[1]
        contr.set_chat_id("null")
        contr.modifica_contratto_di_locazione(code)
        await update.message.reply_text(f'Sistema di notifica disattivato')

async def activate_notify(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    telegram_user=update.effective_user.username
    lista_contratti=contratto.Contratto.get_lista_contratti()
    lc=[]
    for contr in lista_contratti:
        if contr[0].get_telegram_user()==telegram_user:
            lc.append(contr[0])
            lc.append(contr[1])
    if lc==[]:
        await update.message.reply_text(f'Ciao {update.effective_user.first_name}\n non hai alcun affitto')
    else:
        contr=lc[0]
        code=lc[1]
        contr.set_chat_id(update.message.chat_id)
        contr.modifica_contratto_di_locazione(code)
        await update.message.reply_text(f'Sistema di notifica attivato')
        

async def richiedi_anno(update: Update, context: ContextTypes.DEFAULT_TYPE)-> None:
    await update.message.reply_text(f"Inserisce l'anno che t'interessa")
    return ANNO

async def elabora_ricevute(update: Update, context: ContextTypes.DEFAULT_TYPE)-> None:
    telegram_user=update.effective_user.username
    anno_inserito=update.message.text
    if not anno_inserito.isdigit() or len(anno_inserito) != 4:
        await update.message.reply_text(
            "⚠️ Formato non valido. Inserisci un anno di 4 cifre (es. 2026):"
        )
        return ANNO

    lista_contratti=contratto.Contratto.get_lista_contratti()
    lc=[]
    for contr in lista_contratti:
        if contr[0].get_telegram_user()==telegram_user:
            lc.append(contr[1])
    if lc==[]:
        await update.message.reply_text(f'Ciao {update.effective_user.first_name}\n non hai alcun affitto')
    else:
        code=lc[0]
        lista_ricevute=ricevuta.Ricevuta.get_lista_ricevute_by_year(code,anno_inserito)
        # Inizializzazione del messaggio con tag HTML (<b> per il grassetto)
        message = f"<b>Riepilogo ricevute anno {anno_inserito}</b>\n\n\n"

        if lista_ricevute == []:
            message += "<i>Nessuna ricevuta trovata.</i>"
        else:
            for elemento in lista_ricevute:
                ric = elemento[0]
                totale = elemento[2]
                mese = elemento[3]
                anno = elemento[4]   
                
                periodo = f"{mese} {anno}"
                stato_emoji = "✅ Pagato" if ric.get_pagato_ric() == 'Si' else "❌ Non pagato"
                
                num_str = str(ric.get_num_ric())
                totale_str = f"{totale}€"

                # Ogni ricevuta diventa un blocco monospazio indipendente e pulito
                message += f"RICEVUTA N. {num_str}\n"
                message += f"Periodo: {periodo}\n"
                message += f"Totale: {totale_str}\n"
                message += f"{stato_emoji}\n"
                message += "-------------------------------\n"
                #             ####
        await update.message.reply_text(message, parse_mode='HTML')


    return ConversationHandler.END

async def annulla(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Ricerca ricevute annullata.")
    return ConversationHandler.END

async def post_init(application: Application) -> None:
    with open('/app/static/icons_with_back.png',"rb") as photo_pic:
        photo=InputProfilePhotoStatic(photo=photo_pic)
        await application.bot.set_my_profile_photo(photo=photo)
    await application.bot.set_my_description(f"Bot per la visualizzazione delle ricevute d'affitto e per il sistema di notifica")
    await application.bot.set_my_commands([('ricevute', 'Ottieni le ricevute di uno specifico anno'),('disablenotify', 'Disattivazione del sistema di notifica'),('activatenotify', 'Attivazione del sistema di notifica')])

app = ApplicationBuilder().token(str(getenv('BOT_TOKEN'))).post_init(post_init).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("disablenotify", disable_notify))
app.add_handler(CommandHandler("activatenotify", activate_notify))
app.add_handler(ConversationHandler(entry_points=[CommandHandler("ricevute",richiedi_anno)], states={ANNO:[MessageHandler(filters.TEXT & ~filters.COMMAND, elabora_ricevute)],},fallbacks=[CommandHandler("annulla", annulla)],))
app.run_polling()
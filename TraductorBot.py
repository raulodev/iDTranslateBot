from telegram.ext import Updater , CommandHandler , MessageHandler , Filters , CallbackQueryHandler , InlineQueryHandler


from telegram import InlineKeyboardMarkup ,InlineKeyboardButton ,InlineQueryResultArticle , InputTextMessageContent

import telegram

from random import choice

import textblob

import os


def start(Update,context):
	
	name=Update.effective_user.first_name
	
	boton=InlineKeyboardButton(
		text="Translate inline",
		callback_data="call_inline")
	
	text=f"<b>👋Halo {name}\n\n📝Write what you want to translate.\n\n👇Or try using our inline mode.</b>"
	
	Update.message.reply_text(
		text=text,
		parse_mode="html",
		reply_markup=
		InlineKeyboardMarkup([
		[boton]]))



def messagehandler(Update,context):
		
	
	try :
		chat_id = Update.message.chat.id
		text=Update.message.text
		
		if chat_id > 0:
			
			try:
				
				lang= Update.effective_user.language_code
				
				blob = textblob.TextBlob(text)
				
				text_transl = str(blob.translate(to=lang))
				
				Update.message.reply_text(f"<b>❤ Done!\n\n</b><code>{text_transl}</code>",
				parse_mode="html")
				
				
			except Exception:

				context.user_data['text']=text
				
				boton1= InlineKeyboardButton(text=
				"🇪🇸Español" ,callback_data="es")
							
				boton2= InlineKeyboardButton(text=
				"🇬🇧English" ,callback_data="en")
								
				boton3= InlineKeyboardButton(text=
				"🇷🇺русский" ,callback_data="ru")	
				
				boton4= InlineKeyboardButton(text=
				"🇮🇹 Italiano" ,callback_data="it")
				
				boton5= InlineKeyboardButton(text=
				"🇰🇷한국어" ,callback_data="ko")		
						
				boton6= InlineKeyboardButton(text=
				"🇮🇳भारतीय" ,callback_data="hi")					
				
				emojis = ["😁","😆","🙃","🙂"]
				
				emoji=choice(emojis)
				
				
				Update.message.reply_text(text=
				f"<b>{emoji}Choose the language you want to translate to.</b>",
				parse_mode="html",
				reply_markup=
				InlineKeyboardMarkup([
				[boton1 , boton2],
				[boton3 , boton4],
				[boton5 , boton6]
				]))
		

		elif chat_id < 0 and text == "/tr":
			try:
				
				lang= Update.effective_user.language_code
				
				text=Update.message.reply_to_message.text
				
				message_id=Update.message.reply_to_message.message_id
				
				t = Update.message.text				
				
				blob = textblob.TextBlob(text)
				try:
					text_transl = str(blob.translate(to=lang))
					
					context.bot.send_message(chat_id=chat_id,
			 text=
			 f"<b>Translation:</b>\n\n--> <code>{text_transl}</code>",parse_mode="html",
				reply_to_message_id=message_id)
				
					username=Update.effective_user.username
					
				
				except Exception:
					
					context.bot.send_message(chat_id=chat_id,
			 text=
			 f"<b>Translation:</b>\n\n--> <code>{text}</code>",parse_mode="html",
				reply_to_message_id=message_id)		
					username=Update.effective_user.username
					

			
			except AttributeError:
				
				answer="......?"
				if lang!="en":
					blob = textblob.TextBlob(answer)				
					answer = str(blob.translate(to=lang))
					
				Update.message.reply_text(answer)
	
	
	except Exception :
		pass


def callbackhandler(Update,context):
	
	query=Update.callback_query
	chat_id=Update.effective_user.id
	
	data = query.data
	
	if data != "call_inline":
		
		lang = data
		
		text=context.user_data.get("text","not found") 
	
		
		
		blob = textblob.TextBlob(text)
		
		
		try:
			
			t = str(blob.translate(to=lang))
			
			
			context.bot.send_message(chat_id=chat_id,text=f"<b>❤ Done!</b>\n\n<code>{t}</code>",parse_mode="html")

		
		
		except Exception as error:
			
			context.bot.send_message(chat_id=chat_id,text=f"<b>❤ Done!</b>\n\n<code>{text}</code>",parse_mode="html")
	
	
	
	elif data == "call_inline":
			
		boton1=InlineKeyboardButton(text=
		"🇪🇸Español" ,switch_inline_query="es Hi")
		
		boton2=InlineKeyboardButton(text=
		"🇬🇧English" ,switch_inline_query="en Hola")
					
		boton3=InlineKeyboardButton(text=
		"🇷🇺русский" ,switch_inline_query="ru Hi")	
		
		boton4=InlineKeyboardButton(text=
		"🇮🇹Italiano" ,switch_inline_query="it Hi")
		
		boton5=InlineKeyboardButton(text=
		"🇰🇷한국어" ,switch_inline_query="ko Hi")		
				
		boton6=InlineKeyboardButton(text=
		"🇮🇳भारतीय" ,switch_inline_query="hi Hi")					
		
		emojis = ["😁","😆","🙃","🙂"]
		
		emoji=choice(emojis)		
			
		query=Update.callback_query
		
		
		
		
		query.edit_message_text(
		text=f"<b>{emoji}Choose the language you want to translate to.</b>",
		parse_mode="html",
		reply_markup=
		InlineKeyboardMarkup([
		[boton1 , boton2],
		[boton3 , boton4],
		[boton5 , boton6]
		]))

		

def mode_inline(Update,context):
	
	query_id=Update.inline_query.id	
	query=Update.inline_query.query
	
	
	

	text_inline=query
	
	if text_inline == "" :
		
		lang = Update.effective_user.language_code
		
		text = "<code>How to use inline mode❔</code>\n\nTo use the bot in inline mode you must first write the <b>language code</b> and then the <b>text</b>\n\nEg:\n→ <code>@iDTranslateBot en Hola</code>"
		
		if lang != "en":
			
			blob = textblob.TextBlob(text)
			
			text = str(blob.translate(to=lang))		
		
		
		results = []
		
			
			
		consulta = InlineQueryResultArticle(id=query_id,title= "How to use inline mode?",  input_message_content=InputTextMessageContent(text , parse_mode="html"),
			description="Help" , thumb_url="https://yourlink.cc/miniatura-translatebot",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="👨‍💻Creator" , url="https://github.com/inDemocratic") ,InlineKeyboardButton(text="📣Channel", url="https://t.me/InDemocratic/120")],[InlineKeyboardButton(text="🤖Other Bots" , url="https://t.me/InDemocratic/37")]]))
			
		try :
	
			results.append(consulta)
			
			try:
				context.bot.answer_inline_query(
					Update.inline_query.id,
					results=results , switch_pm_text="Language code + Text" , switch_pm_parameter ="uno")
					
					
					
			except telegram.error.BadRequest:
				pass
		
		except UnboundLocalError :
			pass		
	
	
	
	
	
	else :		
		
		
		lang = text_inline[:2]
		text_inline=text_inline[3:]
	
		results=[]
		
		blob = textblob.TextBlob(text_inline)
		
		try :
			
			text = str(blob.translate(to=lang))
			
		except Exception:
			text=text_inline		
			
			
			
		consulta = InlineQueryResultArticle(id=query_id,title= lang,  input_message_content=InputTextMessageContent(text),
			description=text , thumb_url="https://yourlink.cc/miniatura-translatebot")
			
		try :
	
			results.append(consulta)
			
			try:
				context.bot.answer_inline_query(
					Update.inline_query.id,
					results=results , switch_pm_text="Language code + Text" , switch_pm_parameter ="uno")
					
					
			except telegram.error.BadRequest:
				pass
		
		except UnboundLocalError :
			pass





def langcode(Update,context):
	
	
	text ="""ar:árabe
	bg:búlgaro
	ca:catalán
	cs:checo
	da:danés
	de:alemán
	el:griego
	en:inglés
	es:español
	et:estonio
	fi:finés
	fr:francés
	zh:chino
	vi:vietnamita
	uk:ucranio
	tr:turco
	th:tailandés
	sv:sueco
	sr:serbio
	ru:ruso
	ro:rumano
	pt:portugués
	pl:polaco
	no:noruego
	nl:neerlandés
	ms:malayo
	mk:macedonio
	lv:letón
	lt:lituano
	ko:coreano
	ja:japonés
	iw:hebreo
	it:italiano
	is:islandés
	in:indonesio
	hr:croata
	hu:húngaro
	hi:hindú
	ga:irlandés
	be:bielorruso"""	
	
	l = text.splitlines()
	
	lista =[]
	n=0
	for i in l:
		i = i.replace('\t' , "")		
		
		if n % 2 == 0:
			li = len(i)
			lista.append(f'{i}')
			
		elif n % 2 == 1 :
			if li != None:
				x = 14 - li
				
				es=[]
				for xw in range(x):
					es.append(" ")
				
				esp="".join(es)
				lista.append(f"{esp}{i}\n")
			
			
		n += 1
		
	l1="".join(lista)
	
	text = f"<b>📔Language Code</b>\n\n<code>{l1}</code>"
	
	Update.message.reply_text(text,"html")



if __name__ == "__main__":
	
	updater=Updater(token=os.environ["TOKEN"])
	
	update=updater
	
	dp = updater.dispatcher
	
	dp.add_handler(CommandHandler('start',start))
	
	dp.add_handler(CommandHandler("langcode",langcode))
	
	dp.add_handler(CallbackQueryHandler(pattern=0,callback=callbackhandler))
	
	dp.add_handler(InlineQueryHandler(mode_inline))	
	
	dp.add_handler(MessageHandler(Filters.text , messagehandler))
	
	
	updater.start_polling()
	print("bot Transalte is running")
	updater.idle()

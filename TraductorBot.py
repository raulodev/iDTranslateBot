from telegram.ext import ( Updater , CommandHandler , MessageHandler , 
						Filters , CallbackQueryHandler , InlineQueryHandler )


from telegram import (InlineKeyboardMarkup ,InlineKeyboardButton ,
					InlineQueryResultArticle , InputTextMessageContent )


from deep_translator import GoogleTranslator



def Traductor(text , target):
		
	traductor = GoogleTranslator(source='auto', target=target)
	
	resultado = traductor.translate(text)
	
	return resultado	
		


def start (Update,context):
	
	user_id = Update.effective_user.id
	
	user_lang= Update.effective_user.language_code		
	
	name=Update.effective_user.first_name	

	text=f"<b>👋Halo {name} escribe y yo traduciré a tu idioma.</b>"
	
	Update.message.reply_text(
		text=text,
		parse_mode="html")
		
			
	context.bot.set_my_commands(
			commands=([
				
				['start','Inicie el bot'],
				['tr' , 'Responde a un mensaje en grupos y traduce'],
				['/supported_lang' , 'lenguajes soportados al privado']
				
				])
			)
	
		

def TRANSLATE_PV (Update,context):
	
	try :
			
		text = Update.message.text
		
		user_lang = Update.effective_user.language_code
		
		translate = Traductor(text,user_lang)
		
		bt = InlineKeyboardButton(
			text='🏳‍🌈 Otro Idioma',
			callback_data='cambiar_traduccion')
			
		Update.message.reply_text(
			text=f"<b>❤Hecho</b>\n\n<code>{translate}</code>",
			parse_mode='html',
			reply_markup=InlineKeyboardMarkup([[bt]]))			
			
																		
	except :
		
		pass


def CALLBACK_HANDLER (Update,context):
	
	query = Update.callback_query
	
	data = query.data
	
	if data == 'cambiar_traduccion' :
					
		b2 = InlineKeyboardButton(text='🇪🇸Español',callback_data='es')
			
		b3 = InlineKeyboardButton(text='🇬🇧Inglés',callback_data='en')
				
		b4 = InlineKeyboardButton(text='🇮🇳Indú',callback_data='hi')
					
		b5 = InlineKeyboardButton(text='🇸🇦Árabe',callback_data='ar')						
					
		b6 = InlineKeyboardButton(text='🇵🇹Portugués',callback_data='pt')
											
		b7 = InlineKeyboardButton(text='🇷🇺Ruso',callback_data='ru')
											
		b8 = InlineKeyboardButton(text='🇫🇷Francés',callback_data='fr')						
					
		
		query.edit_message_reply_markup(
			reply_markup=InlineKeyboardMarkup([
			[b2],[b3,b4],[b5,b6],[b7,b8]
			]))

	else :
		
		text=query.message.text[8:]
		lang = query.data
		
		translate = Traductor(text,lang)
		
		query.edit_message_text(
			text=f'<b>❤Hecho</b>\n\n<code>{translate}</code>',
			parse_mode='html')
		

def TRANSLATE_GP (Update,context):
			
	if (Update.message.reply_to_message):
				
		text=Update.message.reply_to_message.text
		
		user_lang = Update.effective_user.language_code
		
		message_id= Update.message.reply_to_message.message_id
				
		translate = Traductor(text,user_lang)
		
		context.bot.send_message(			
			chat_id=Update.effective_chat.id,			
			text=f"<b>❤Hecho</b>\n\n<code>{translate}</code>",			
			parse_mode='html',			
			reply_to_message_id=message_id)
	
	
def SUPPORTED_LANG (Update,context):

	list = GoogleTranslator.get_supported_languages()
	
	langs=[]
	
	n = 0
	
	for i in list :
		
		if n % 2 == 1:			
			
			langs.append(f'<code>{list[n-1]} -- {list[n]}</code>')
		
		n += 1

	supported_langs = "\n".join(langs)
	
	Update.message.reply_text(f'{supported_langs}','html')		
					
def TRANSLATE_AD (Update,context):
	
	Update.message.reply_text('<b>❤Usa este comando en grupos.</b>','html')

def SUPPORTED_LANG_AD (Update,context):

	Update.message.reply_text('<b>❤Usa este comando en privado.</b>','html')


if __name__ == "__main__":
	
	updater=Updater(token=os.environ [TOKEN])
	
	update=updater
	
	dp = updater.dispatcher
	
	dp.add_handler(CommandHandler('start',start))
	
	dp.add_handler(CallbackQueryHandler(pattern=0,callback=CALLBACK_HANDLER))	
	
	dp.add_handler(MessageHandler(Filters.regex('^/tr$') & Filters.chat_type.groups , TRANSLATE_GP))
		
	dp.add_handler(MessageHandler(Filters.regex('^/supported_lang$') & Filters.chat_type.private , SUPPORTED_LANG))			
		
	dp.add_handler(MessageHandler(Filters.regex('^/tr$') & Filters.chat_type.private , TRANSLATE_AD))
		
	dp.add_handler(MessageHandler(Filters.regex('/supported_lang') & Filters.chat_type.groups , SUPPORTED_LANG_AD))			
			
	
	
	dp.add_handler(MessageHandler(Filters.text & Filters.chat_type.private , TRANSLATE_PV))		
	
	updater.start_polling()
	
	print("bot Transalte is running")
	
	updater.idle()

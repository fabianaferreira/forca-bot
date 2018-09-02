#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time
import random
import logging
import telegram
from telegram.error import NetworkError, Unauthorized
from time import sleep

import UIText as UI
import WordsDB

TOKEN = 'TOKEN'

def GetRandomWord (words_db, category=None):

		if category == None:
			category = random.randint (0, len (words_db)-1)

		word_index = random.randint (0,len (words_db[category])-1)
		return words_db[category][word_index]

class User ():
	def __init__ (self, id, language, chances, word, guessingString, category, isGuessingLetter, isGuessingWord):
		self.id = id
		self.language = language
		self.chances = chances
		self.word = word
		self.guessingString = guessingString
		self.category = category
		self.isGuessingLetter = isGuessingLetter
		self.isGuessingWord = isGuessingWord

#Language = 0 => Português
#Language = 1 => English

user_data = {}

defaultLanguage = 0
defaultChances = 5
defaultCategory = 0
defaultGuessingString = ""
defaultWord = ""

#estadoInicial = User (None, language, chances, word, guessingString, category, isGuessingLetter, isGuessingWord)
update_id = None

knownUsers_ids = []

knownUsers = []

def main():
    global update_id
    global knownUsers
    global knownUsers_ids

    #words_db = WordsDB.words
    words_db =  [
	['LARANJA', 'GOIABA', 'TANGERINA', 'JABUTICABA', 'JAMELÃO', 'MORANGO','MARACUJÁ','ABACATE', 'MELANCIA', 'MELÃO', 'CARAMBOLA', 'ABACAXI', 'CEREJA', 'PÊRA', 'FRAMBOESA', 'AMORA', 'LIMÃO', 'FIGO', 'PÊSSEGO', 'BANANA', 'MAMÃO', 'MANGA', 'LICHIA', 'DAMASCO', 'FRUTA DO CONDE',
	'AMEIXA', 'ROMÃ', 'UVA', 'CAQUI', 'COCO', 'CUPUAÇU', 'CACAU', 'CAJU', 'GRAVIOLA', 'GUARANÁ', 'PITANGA', 'ACEROLA', 'KIWI'],

	['POLVO', 'LAGOSTA', 'CAMARÃO', 'MACACO', 'GORILA', 'GATO', 'PORCO', 'COELHO', 'PORCO-ESPINHO', 'CAVALO-MARINHO', 'ARARA', 'PATO', 'URUBU', 'POMBO', 'SARDINHA','BALEIA', 'GOLFINHO', 'TARTARUGA',
	'ELEFANTE', 'GIRAFA', 'ARANHA', 'CACHORRO', 'CALOPSITA', 'PAPAGAIO', 'HIPOPÓTAMO', 'PEIXE-BOI', 'SUCURI', 'JARARACA', 'MICO-LEÃO-DOURADO', 'BARATA', 'LAGARTO', 'LAGARTIXA', 'MOSCA', 'MOSQUITO', 'RATO',
	'JACARE', 'CAMELO', 'CAMALEÃO', 'FORMIGA', 'GANSO', 'MARRECO', 'GAIVOTA', 'TIGRE', 'LEÃO', 'ARRAIA', 'BAIACU', 'CUPIM', 'ALCE', 'VEADO', 'ZEBRA', 'GIRAFA', 'COALA', 'SURICATO', 'FOCA', 'ORNITORRINCO',
	'URSO', 'VACA', 'BOI', 'OVELHA', 'CABRA', 'PAVÃO', 'BEIJA-FLOR', 'CANGURU', 'MAMUTE', 'BORBOLETA','GUEPARDO', 'RINOCERONTE', 'TUCANO', 'BABUÍNO', 'TAMANDUÁ', 'ESQUILO', 'CUTIA'] ,
	['AFEGANISTÃO', 'ÁFRICA DO SUL', 'ALBÂNIA', 'ALEMANHA', 'ANDORRA', 'ANGOLA', 'ARÁBIA SAUDITA', 'ARGÉLIA', 'ARGENTINA', 'ARMÊNIA', 'AUSTRÁLIA', 'ÁUSTRIA', 'AZERBAIJÃO', 'BAHAMAS', 'BANGLADESH', 'BARBADOS', 'BÉLGICA', 'BELIZE', 'BIELORÚSSIA', 'BOLÍVIA', 'BÓSNIA HERZEGOVINA',
	'BOTSUANA', 'BRASIL', 'BULGÁRIA', 'BUTÃO', 'CABO VERDE', 'CAMARÕES', 'CAMBOJA', 'CANADÁ', 'CATAR', 'CAZAQUISTÃO', 'CHILE', 'CHINA', 'CHIPRE', 'CINGAPURA', 'COLÔMBIA', 'CONGO', 'CORÉIA DO NORTE', 'CORÉIA DO SUL', 'COSTA DO MARFIM', 'COSTA RICA', 'CROÁCIA',
	'CUBA', 'DINAMARCA', 'EGITO', 'EL SALVADOR', 'EMIRADOS ÁRABES UNIDOS', 'EQUADOR', 'ESCÓCIA', 'ESLOVÁQUIA', 'ESLOVÊNIA', 'ESPANHA', 'ESTADOS UNIDOS', 'ESTÔNIA', 'ETIÓPIA', 'RUSSIA', 'FIJI', 'FILIPINAS', 'FINLÂNDIA', 'FRANÇA', 'GABÃO', 'GÃMBIA', 'GANA', 'GEÓRGIA',
	'GRÃ-BRETANHA', 'GRANADA', 'GRÉCIA', 'GROENLÂNDIA', 'GUATEMALA',  'GUIANA', 'GUIANA FRANCESA', 'GUINÉ', 'GUINÉ BISSAU', 'GUINÉ EQUATORIAL', 'HAITI', 'HOLANDA', 'HONDURAS', 'IÊMEN', 'INDIA', 'INDONÉSIA', 'IRÃ', 'IRAQUE', 'IRLANDA', 'IRLANDA DO NORTE', 'ISLÂNDIA',
	'ISRAEL', 'ITÁLIA', 'JAMAICA', 'JAPÃO', 'JORDÂNIA', 'KUWAIT', 'LAOS', 'LETÔNIA', 'LÍBANO', 'LIBÉRIA', 'LÍBIA', 'LITUÃNIA', 'LUXEMBURGO', 'MACEDÔNIA', 'MADAGASCAR', 'MALÁSIA', 'MALDIVAS', 'MALTA', 'MARROCOS', 'MAURITÂNIA', 'MÉXICO', 'MICRONÉSIA', 'MOÇAMBIQUE',
	'MONGÓLIA', 'NAMÍBIA', 'NEPAL', 'NICARÁGUA', 'NIGÉRIA', 'NORUEGA', 'NOVA ZELÂNDIA', 'PANAMÁ', 'PAPUA NOVA GUINÉ', 'PAQUISTÃO', 'PARAGUAI', 'PERU', 'POLÔNIA', 'PORTO RICO', 'PORTUGAL', 'QUÊNIA', 'QUIRQUISTÃO', 'REINO UNIDO', 'REPÚBLICA DOMINICANA', 'REPÚBLICA TCHECA',
	'ROMÊNIA', 'RUANDA', 'SAMOA', 'SENEGAL', 'SERRA LEOA', 'SÉRVIA E MONTENEGRO', 'SÍRIA', 'SOMÁLIA', 'SRI LANKA', 'SUDÃO', 'SUÉCIA', 'SUÍÇA', 'SURINAME', 'TADJIQUISTÃO', 'TAILÂNDIA', 'TANZÃNIA', 'TOGO', 'TRINIDAD E TOBAGO', 'TUNÍSIA', 'TURCOMENISTÃO', 'TURQUIA', 'TUVALU',
	'UCRÂNIA', 'UGANDA', 'URUGUAI', 'UZBEQUISTÃO', 'VENEZUELA', 'VIETNÃ', 'ZAIRE', 'ZÂMBIA', 'ZIMBÁBUE']]

    # Telegram Bot Authorization Token
    bot = telegram.Bot(TOKEN)

    # get the first pending update_id, this is so we can skip over it in case
    # we get an "Unauthorized" exception.
    try:
        update_id = bot.getUpdates()[0].update_id
    except IndexError:
        update_id = None

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    while True:
        try:
            #echo(bot)
			for update in bot.getUpdates(offset=update_id, timeout=10):
				chat_id = update.message.chat_id
				update_id = update.update_id + 1

				user_id = update.extract_chat_and_user()[1].id

				if user_id not in knownUsers_ids:
					print "New user added to known_users"
					knownUsers_ids.append(user_id)
# ############	Adicionar escolha de linguagem	################
					currentUser = User (None, defaultLanguage, defaultChances, defaultWord, defaultGuessingString, defaultCategory, False, False)
					knownUsers.append (currentUser)
				else:
					print "I already know this guy!"
					for user in knownUsers:
						if user_id == user.id:
							currentUser = user
							break


				if update.message:  # your bot can receive updates without messages
					# Reply to the message
					#update.message.reply_text(update.message.text)

					text = update.message.text.encode('utf-8')

					if (text == '/start'):

						currentUser.isGuessingLetter = False
						currentUser.isGuessingWord = False

						if (chat_id == 173433762):  #Fabiana
							keyboard = UI.SetKeyboard (currentUser.language, 'fabiana', True)
							bot.sendMessage(chat_id, UI.UIMessages.playMessage [currentUser.language], reply_markup= keyboard)
						else:
							keyboard = UI.SetKeyboard (currentUser.language, 'main', True)
							bot.sendMessage(chat_id, UI.UIMessages.playMessage[currentUser.language], reply_markup= keyboard)

					elif (text == 'Fabiana? É você?'):
						keyboard = UI.SetKeyboard (currentUser.language, 'main', True)
						bot.sendMessage(chat_id, UI.UIMessages.lucasMessage[currentUser.language], reply_markup= UI.SetKeyboard(currentUser.language,'main', True))

					elif (text == UI.UIButtons.helpButton [currentUser.language]):
						keyboard = UI.SetKeyboard (currentUser.language, 'main', True)
						bot.sendMessage(chat_id, UI.UIMessages.helpMessage[currentUser.language], reply_markup= UI.SetKeyboard(currentUser.language,'main', True))

					elif (text == UI.UIButtons.playButton [currentUser.language]):
						currentUser.guessingString = ""
						currentUser.chances = 5
						currentUser.isGuessingLetter = False
						currentUser.isGuessingWord = False
						keyboard = UI.SetKeyboard (currentUser.language, 'category', True)


						bot.sendMessage(chat_id, UI.UIMessages.categoryMessage[currentUser.language], reply_markup= keyboard)


					elif ((text == UI.UIButtons.fruitCategory [currentUser.language])
					or (text == UI.UIButtons.animalCategory [currentUser.language])
					or (text == UI.UIButtons.countryCategory [currentUser.language])
					or (text == UI.UIButtons.randomCategory [currentUser.language])) and not currentUser.isGuessingLetter and not currentUser.isGuessingWord:

						#Escolheu a categoria e vai começar a adivinhar
						currentUser.isGuessingLetter = True

						keyboard = UI.SetKeyboard (currentUser.language, 'guessing', True)
						bot.sendMessage(chat_id, UI.UIMessages.guessingLetterMessage[currentUser.language], reply_markup= keyboard)

						if (text == UI.UIButtons.fruitCategory [currentUser.language]):
							currentUser.category = 0

						elif (text == UI.UIButtons.animalCategory [currentUser.language]):
							currentUser.category = 1

						elif (text == UI.UIButtons.countryCategory [currentUser.language]):
							currentUser.category = 2

						else:
							currentUser.category = random.randint (0, 2)

						currentUser.word = unicode (GetRandomWord (words_db, currentUser.category))
						#so nao gostei muito do espaco na ultima letra por esse for
						for letter in currentUser.word:
							if (letter == '-'):
								currentUser.guessingString += "- "
							elif (letter == ' '):
								currentUser.guessingString += "  "
							else:
								currentUser.guessingString += "_ "
						bot.sendMessage(chat_id, UI.UpdateGameMessage (currentUser.language, currentUser.guessingString, currentUser.category, currentUser.chances))
						currentUser.guessingString = list (currentUser.guessingString)

					# Falta testar a letra na palavra
					# Levar em conta acentos Á Ã Â É Ê Ó Õ Ô Í Ú
					elif (((text >= 'A') and (text <='Z') or (text >= 'a') and (text <='z')) and (currentUser.isGuessingLetter) and (len(text) == 1)):
						keyboard = UI.SetKeyboard (currentUser.language, 'guessing', True)
						text = text.decode('utf-8').upper()
						rightGuess = False
						currentUser.guessingString = list (currentUser.guessingString)
						if (currentUser.chances != 0):
							for index, letter in enumerate (currentUser.word):
								if (letter == text):
									currentUser.guessingString [2*index] = letter
									rightGuess = True
								elif (text == 'A' and (letter == 'Á' or letter == 'Ã' or letter == 'Â')):
									currentUser.guessingString [2*index] = letter
									rightGuess = True
								elif (text == 'E' and (letter == 'É' or letter == 'Ê')):
									currentUser.guessingString [2*index] = letter
									rightGuess = True
								elif (text == 'O' and (letter == 'Ó' or letter == 'Ô' or letter == 'Õ')):
									currentUser.guessingString [2*index] = letter
									rightGuess = True
								elif (text == 'I' and (letter == 'Í')):
									currentUser.guessingString [2*index] = letter
									rightGuess = True
								elif (text == 'U' and (letter == 'Ú')):
									currentUser.guessingString [2*index] = letter
									rightGuess = True
								elif (text == 'C' and (letter == 'Ç')):
									currentUser.guessingString [2*index] = letter
									rightGuess = True
							if (not rightGuess):
								currentUser.chances -= 1

							currentUser.guessingString = "".join (currentUser.guessingString)
							bot.sendMessage(chat_id, UI.UpdateGameMessage (currentUser.language, currentUser.guessingString, currentUser.category, currentUser.chances))
							if (currentUser.chances == 0):
								keyboard = UI.SetKeyboard (currentUser.language, 'main', True)
								bot.sendMessage(chat_id, UI.UIMessages.wordRevealMessage[currentUser.language] + currentUser.word, reply_markup= keyboard)
								bot.sendMessage (chat_id, UI.UIMessages.loseMessageByChance[currentUser.language], reply_markup = keyboard)
							if '_' not in currentUser.guessingString:
								keyboard = UI.SetKeyboard (currentUser.language, 'main', True)
								bot.sendMessage(chat_id, UI.UIMessages.winMessage[currentUser.language], reply_markup= keyboard)

					elif (text == UI.Emoji.cross_mark):
						currentUser.isGuessingLetter = False

						keyboard = UI.SetKeyboard (currentUser.language, 'main', True)
						bot.sendMessage(chat_id, UI.UIMessages.playMessage[currentUser.language], reply_markup= keyboard)

					elif (text == UI.Emoji.writing_hand):
						currentUser.isGuessingLetter = False
						currentUser.isGuessingWord = True

						reply_markup = telegram.ReplyKeyboardHide()
						bot.sendMessage(chat_id, UI.UIMessages.guessingWordMessage[currentUser.language], reply_markup=reply_markup)

					elif (currentUser.isGuessingWord):
						guess = text.decode('utf-8').upper()
						keyboard = UI.SetKeyboard (currentUser.language, 'main', True)

						print "Guess: " + guess
						print unicode(currentUser.word)


						if (guess == currentUser.word):
							bot.sendMessage(chat_id, UI.UIMessages.winMessage[currentUser.language], reply_markup= keyboard)
						else:
							bot.sendMessage(chat_id, UI.UIMessages.wordRevealMessage[currentUser.language] + currentUser.word, reply_markup= keyboard)
							bot.sendMessage(chat_id, UI.UIMessages.loseMessage[currentUser.language], reply_markup= keyboard)

						currentUser.isGuessingLetter = False
						currentUser.isGuessingWord = False

					else:
						bot.sendMessage(chat_id, UI.UIMessages.invalidEntryMessage[currentUser.language])

        except NetworkError:
            sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1


def echo(bot):
    global update_id
    # Request updates after the last update_id
    for update in bot.getUpdates(offset=update_id, timeout=10):
        # chat_id is required to reply to any message
        chat_id = update.message.chat_id
        update_id = update.update_id + 1

        if update.message:  # your bot can receive updates without messages
            # Reply to the message
            update.message.reply_text(update.message.text)


if __name__ == '__main__':
    main()

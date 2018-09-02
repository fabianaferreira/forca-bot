#encoding=UTF8
import sys
reload(sys)  
sys.setdefaultencoding('utf8')

import telegram

class Emoji:                                                                                                                                                                                          
		fruit = u'\U0001F34E'                                                                                                                                                                         
		animal = u'\U0001F40B'                                                                                                                                                                        
		writing_hand = u'\U0000270D'                                                                                                                                                                  
		cross_mark = u'\U0000274C'                                                                                                                                                                    
		game_die = u'\U0001F3B2'
		thumbs_up = u'\U0001F44D'
		sad_face = u'\U0001F614'
		joystick = u'\U0001F579'
		light_bulb = u'\U0001F4A1'
		motorway = u'\U0001F6E3'

class UIButtons:
	playButton = ['Jogar ' + Emoji.joystick, 'Play ' + Emoji.joystick]
	helpButton = ['Ajuda ' + Emoji.light_bulb , 'Help ' + Emoji.light_bulb]
	fabianaButton = ['Fabiana? É você?', 'Fabiana? É você?']
	fruitCategory = ['Frutas ' + Emoji.fruit, 'Fruits ' + Emoji.fruit]
	animalCategory = ['Animais ' + Emoji.animal, 'Animals ' + Emoji.animal]
	countryCategory = ['Países ' + Emoji.motorway, 'Country ' + Emoji.motorway]
	randomCategory = ['Aleatório ' + Emoji.game_die, 'Random ' + Emoji.game_die]
	
	lucasMessage = ['Lucas diz:\n  Eu te amo!', 'Lucas diz:\n  Eu te amo!']
	
class UIMessages:
	categoryNames = [UIButtons.fruitCategory, UIButtons.animalCategory, UIButtons.countryCategory, UIButtons.randomCategory]

	playMessage = ['Aperte \'Jogar\' para começar', 'Press \'Play\' to start']
	helpMessage = ['Aperte ou digite \'Jogar\' para começar e escolha uma categoria\nVocê tem 5 chances para adivinhar a palavra\nChute a qualquer momento clicando em ' +Emoji.writing_hand+' ou desista clicando em ' +Emoji.cross_mark+'\n\n/start : Reinicia o jogo',
						  'Press or type \'Play\' to start and pick a category\nYou have 5 chances to guess the word\nYou can guess at any time by pressing on ' +Emoji.writing_hand+' or give up pressing on ' +Emoji.cross_mark+'\n\n/start : Restart the game']
	categoryMessage = ['Escolha uma das categorias abaixo:', 'Pick one of the categories below:']
	guessingLetterMessage = ['Diga uma letra ou tente acertar a palavra:', 'Tell me a letter or try to guess the word:']
	guessingWordMessage = ['Digite seu chute:', 'Tell me your guess:']
	winMessage = ['Você acertou! '+ Emoji.thumbs_up +'\nConsegue fazer isso de novo?', 'You made it! '+ Emoji.thumbs_up +'\nCan you do that again?']
	loseMessage = ['Você errou! '+ Emoji.sad_face +'\nAcho que devia tentar de novo...', 'It\'s wrong! '+ Emoji.sad_face +'\nPlay again, you can do it!']
	invalidEntryMessage = ['Desculpe, não entendi...', 'Sorry, what did you say?']
	loseMessageByChance = ['Suas chances acabaram ' + Emoji.sad_face + '\nAcho que devia tentar de novo...', 'Your chances are gone ' + Emoji.sad_face + '\nYou should try one more time...']
	wordRevealMessage = ['A palavra era: ', 'The word was: ']
	
def SetKeyboard (language, screen, resize=True):
	if screen == 'main':
		keyboard = [[UIButtons.playButton [language]],[UIButtons.helpButton [language]]]
		
	elif screen == 'fabiana':
		keyboard = [[UIButtons.playButton [language]], [UIButtons.helpButton [language]],[UIButtons.fabianaButton [language]]]
		
	elif screen == 'category':
		keyboard = [[UIButtons.fruitCategory [language]], [UIButtons.animalCategory [language]], [UIButtons.countryCategory [language]], [UIButtons.randomCategory [language]]]
	
	elif screen == 'guessing':
		keyboard = [['A','B','C','D','E','F','G'],['H','I','J','K','L','M','N'],['O','P','Q','R','S','T','U'],[Emoji.cross_mark,'V','W','X','Y','Z',Emoji.writing_hand]]
	
	else:
		return -1
		
	return telegram.ReplyKeyboardMarkup (keyboard, resize_keyboard=resize)
	
def UpdateGameMessage (language, hiddenWord, category, chances):
	if (language == 0): #Portuguese
		return "Categoria: " + UIMessages.categoryNames [category][language] + "\n\n" + hiddenWord + "\n" + "Chances: " + str (chances)
	else:
		return "Category: " + UIMessages.categoryNames [category][language] + "\n\n" + hiddenWord + "\n\n" + "Chances: " + str (chances)
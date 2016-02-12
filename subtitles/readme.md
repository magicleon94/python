L'idea è di uno script che consenta di scaricare i sottotitoli per i telefilm da www.italiansubs.net
senza collegarsi al sito web tramite browser.

Utilizzo:
da terminale(Linux/Mac):	
	python mysubs.py -serie [nome serie] -season [numero stagione] -episode [numero episodio] -dir [directory di download] [--opzioni]
Le opzioni:
--720p
--1080p
--1080i
scaricano, se presenti, i sottotitoli per episodi con le  rispettive risoluzioni
--ranged
permette di scaricare i sottotitoli degli episodi compresi in un range specificato dall'utente
--quiet
sopprime i vari messaggi di dialogo durante l'esecuzione dello script



# Dokumentacja projektu

ęśąćżłó
### 1. Wprowadzenie

Celem projektu byo stworzenie wasnego pakietu **ros2** który komunikując się poprzez odpowiednie 
topici będzie sterował nodem turtlesim. Zadanie należało wykonać tak aby klawisze sterujące były 
wybierane poprzez parametry.


### 2. Implementacja

Główny sposób działania pakietu opiera się na nodzie **pubsub** który zczytywał wciśnięte klawisze przy pomocy konsoli, 
a następnie przy pomocy topica **turtle1/cmd_vel** publikował nową prędkość do noda **sim** który to odpowiednio ruszał się żółwiem.

graph TD;
    pubsub-->turtle1/cmd_vel;
    turtle1/cmd_vel-->sim;

Przy pomocy parametów:
* forward_key,
* backward_key,
* left_key,
* right_key,
została dodana możliwość zmiany klawiszy do sterowania żółwia.

### 3. Uruchomienie



Członkowie zespołu:

Hubert Kozubek,

Przemysław Michalczewski

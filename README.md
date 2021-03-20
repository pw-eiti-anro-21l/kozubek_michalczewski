# Dokumentacja projektu


### 1. Wprowadzenie

Celem projektu byo stworzenie wasnego pakietu **ros2** który komunikując się poprzez odpowiednie 
topici będzie sterował nodem turtlesim. Zadanie należało wykonać tak aby klawisze sterujące były 
wybierane poprzez parametry.


### 2. Implementacja

Główny sposób działania pakietu opiera się na nodzie **pubsub** która zczytywała wciśnięte klawisze poprzez konsolę, 
a następnie przy pomocy topica **turtle1/cmd_vel** publikował nową prędkość do **turtlesim_node** który to odpowiednio ruszał się żółwiem.

Przy pomocy parametów:
* forward_key,
* backward_key,
* left_key,
* right_key,

została dodana możliwość zmiany klawiszy do sterowania żółwiem.

### 3. Uruchomienie
śćąęłóż
W pierwszej kolejności znajdując się w głównym folderze używamy komendy

`colcon build --packages-select LAB1`

Następnie otwieramy nowe okno terminala i wprowadzamy komendę

`. install/local_setup.bash`

Przy pomocy nowo otwartej konsoli wechodzimy do folderu __*/launch*__ i wprowadzamy komendę

`ros2 launch lab1.launch.py`

Po jej wpisaniu otworzy się nowe okienko konsoli oraz turtlesim_node. Sterować żółwiem można przy użyciu klawiszy `t`, `g`, `f` i `h`.


Aby zmienić klawisze sterowania na inne należy wewnątrz pliku **lab1.launch.py** zminić kod

                {'foward_key': 't'},
                {'backward_key': 'g'},
                {'left_key': 'f'},
                {'right_key': 'h'}

tak aby odpowiadał naszym preferencją.



###Członkowie zespołu:

Hubert Kozubek, Przemysław Michalczewski

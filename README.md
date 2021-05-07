# Dokumentacja projektu - laboratorium 2

### 1. Wprowadzenie

Celem projektu było stworzenie własnego pakietu **ros2**, ktrego gwnym celem byla obsluga kinematyki proset


### 2. Implementacja
Stworzono dwa programy _non_kdl_dkin.py_ i _non_kdl_dkin.py_, odpowiaday one za wyliczenia kinematyki prosej odpowiedni bez uycia PyKDL oraz z uyciem PyKDL

Zostaly rowniez wprowadzone zmiany w pliku join_state_publisher.py ktory to odpowiadal za nadawanie nowych pozycji elementa oraz weryfikacje czy nie osiagnely one pozycji zabronionych


Zostały stworzone cztery pliki _launch_:
* non_kdl_dkin.launch.py
* kdl_dkin.launch.py
* both_kdl_and_non_kdl_dkin.launch.py
* rviz.launch.py - odpala program wizualizacyjny


![Alt text](rqt_graph.png?raw=true "RQT - graph")

Ostatecznie powiązanie pomiędzy węzłami wygląda jak na powyższym rysunku. _state_publisher_ nadaje na kanale komunikacyjnym 'JointState', które odbiera węzeł _robot_state_publisher_. Tez z koleji na kanale nadaje na kanale 'tf', który odbiera węzeł programu RVIZ.


### 3. Uruchomienie

Najpierw należy stworzyć odpowiedni plik .urdf. Następnie umieścić go w pakiecie. Następnie budujemy nasz pakiet przy użyciu komendy:

`colcon build --symlink-install --packages-select urdf_tutorial`

Kolejno należy użyć komendy określajcej źródło:

`source install/setup.bash`

Gdy nasz pakiet jest poprawnie zbudowany możemy przejść do uruchmienie kolejnych węzłów naszej symulacji:

`ros2 launch urdf_tutorial demo.launch.py`

Plik _launch_ uruchomi węzeł _state_publisher_.

W kolejnej konsoli wpisujemy komędę określającą źródło (wyżej podana), a następnie uruchomić kolejny plik launch:

`ros2 launch urdf_tutorial rviz.launch.py`

Uruchomi on program RVIZ. W zależności od tego jaki program użyjemy do stworzenia pliku .urdf robot będzie się poruszał lub będzie statyczny.




###Członkowie zespołu:

Hubert Kozubek, Przemysław Michalczewski

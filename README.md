# Dokumentacja projektu - laboratorium 2

### 1. Wprowadzenie

Celem projektu było stworzenie własnego pakietu **ros2**, który będzie umożliwiał wizualizację robota w programie RVIZ oraz stworzenie węzła (_state_publisher_) sterującego nim. 


### 2. Implementacja
Stworzono dwa programy _DH to URDF.py_ and _DH to URDF.static.py_, które odpowiednie generują pliki .urdf dla zadanych parametrów robota odpowiednio porusziącego się i statycznego.

Wywołanie przykładowe programów:
          
_python3 DH\ to\ URDF.py 30 60 1 2 4_
gdzie kolejne argumenty odpowiadają:
* kąt theta1 - kąt w stawie robota
* kąt theta2 - kolejny kąt w stawie robota
* a1 - długość pierwszego ramienia
* a2 - długość drugiego ramienia
* d1 - przesunięcie stawu

Po wykonaniu programu utworzony jest plik _r2d2.urdf.xml_, który należy umieścić w miejsce starego pliku w celu uaktualnienie robota.

Następnie napisany został węzeł _state_publisher_ , który odpowiada za poruszanie się robota poprzez subskrybcję węzła _robot_state_publisher_.

Zostały stworzone dwa pliki _launch_:
* demo.launch.py - uruchami węzły określające i poruszające robotem
* rviz.launch.py - odpala program wizualizacyjny RVIZ


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

# CoSieDziejeSie

CoSieDziejeSie to aplikacja webowa pomagająca ludziom odnaleźć wydarzenia w okolicy. Użytkownicy mogą umieścić tu informacje o lokalnych koncertach, występach, imprezach, żeby więcej osób o tym usłyszało.

Jak uruchomić:

1. Windows
   - pobierasz aplikacje docker dekstop https://docs.docker.com/desktop/setup/install/windows-install/
   - włączasz aplikacje docker desktop
   - pobierasz to repozytorium
   - w folderze głównym repozytorium włączasz plik start.bat

2. Linux
   -pobierasz aplikacje docker desktop https://docs.docker.com/desktop/setup/install/linux/ubuntu/
   - włączasz aplikacje docker desktop
   - pobierasz to repozytorium
   - w folderze głównym repozytorium włączasz plik start.sh

Dodawanie admina:
- w konsoli wpisujemy docker ps
- kopiujemy id kontenera z aplikacją
- w konsoli wpisujemy docker exec -it idkontenera /bin/bash
- nastepnie uzytkownika tworzymy komendą python manage.py createsuperuser

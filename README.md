# Windows Gopher Client
![](_articles/assets/gopher/Main_Window.JPG)
W czasach, gdy internet dopiero raczkował wymiana treściami pomiędzy osobami była nieco utrudniona. Sposoby przesyłania plików były na tyle skomplikowane, że tylko nieliczni potrafili robić to korzystając z konsolowych poleceń. Nie wspominając nawet o wymianie całych katalogów. Tak powstał protokół Gopher, stworzony przez Mark P. McCahill na Uniwersytecie w Minnesocie.

Głównym zamiarem tej kreacji było umożliwienie prostej wymiany i przeglądania plików innych użytkowników. Generatory stron miał składać się tylko z nielicznych tagów tekstowych (podobnie zresztą jak HTML, jednak z dużo bardziej uboższą ich ilością), strona miała być lekka i mieć hierarchiczną budowę.

Pomimo, że dziś mamy już 2019 i problemy z ograniczą transmisją danych, czy indeksowaniem danych nie zawracają nam już głowy, małe grono użytkowników wciąż korzysta z tego protokołu. Wielu z nich korzysta z tego protokołu w celu pisania tzw. gBlogów, czy agregacji znalezionych dokumentów w sieci. 

## Przeglądanie treści

Aby móc zanurzyć się w odmętach tego małego skrawka internetu i poczuć się niczym w latach `90 możemy wykorzystać linuksowe konsolowe przeglądarki Lynx, internetową bramkę FloodgapProxy, lub moją windowsową wersję przeglądarki napisaną w języku Python.

Korzystanie z proxy nie pozwala na wygodne korzystanie z oferowanych treści. Przeszukując internet w celu znalezienia klienta dla systemów Windows nie natknąłem się na żadną dobrą alternatywę. Prawdę mówiąc, jedyną alternatywą była nakładka na przeglądarkę Mozilla Firefox, co nie przypadło mi do gustu. Korzystając jednak z chwili wolnego czasu napisałem aplikację wyświetlającą przeprasowane treści skojarzone z protokołem Gopher. 

Repozytorium pozwala na dostęp do plików źródłowych i ewentualną ich edycję. Istnieje również już całkowicie skompilowana wersja .exe, którą zaraz po pobraniu można uruchomić (bez instalacji) i przeglądać treści oferowane przez "internetowe podziemie". Cała funkcjonalność aplikacji jest opisana pod zakładką "About". Przeglądarka ma zaimplementowaną wyszukiwarkę Veronica-2, którą społeczność Floodgap oferuje. Wystarczy wpisać pożądaną frazę w pasek adresu i kliknąć przycisk "GO". Pamiętajmy jednak, że nie jest to na tyle *inteligentna* wyszukiwarka jak Google, dlatego nasze zapytania powinny składać się z prostych słów.

Have Fun! 



[Repozytorium Git](https://MateuszWaldemarMyalski@bitbucket.org/MateuszWaldemarMyalski/windows-gopher-client.git)




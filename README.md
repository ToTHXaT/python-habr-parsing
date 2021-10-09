# Python habr parser / Aynur Rakhmanov

Dependencies are listed in the Pipfile

> To run the program ```py main.py```
 
_main.py_, _habr/parser/article.py_, _habr/parser/search.py_ contains the source code
* ```main.py``` contains all the NLP logic
* ```habr/parser/article.py``` contains article parsing logic
* ```habr/parser/search.py``` contains search results (*list of articles*) parsing logic

The search parameter can be changed inside source code in ```main.py```, by modifying ___search___ variable

Results are dumped into *{search}_kw_result.png* and *{search}_person_result.png*

## Криптография results
### Keywords
![Keywords](https://raw.githubusercontent.com/ToTHXaT/python-habr-parsing/main/%D0%9A%D1%80%D0%B8%D0%BF%D1%82%D0%BE%D0%B3%D1%80%D0%B0%D1%84%D0%B8%D1%8F_kw_result.png)
### Persons
![Persons](https://raw.githubusercontent.com/ToTHXaT/python-habr-parsing/main/%D0%9A%D1%80%D0%B8%D0%BF%D1%82%D0%BE%D0%B3%D1%80%D0%B0%D1%84%D0%B8%D1%8F_person_result.png)
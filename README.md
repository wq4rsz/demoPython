1. Измените данные в файле по пути ```database/config.py```
```bash     
    'dbname': 'ваше название',
    'user': 'ваше имя пользователя(postgres)',
    'password': 'ваш пароль',
    'host': 'localhost',
    'port': '5432'
```
2. Установите зависимости и запустите скрипт ```create_tables.py```
```bash 
pip install -r requirements.txt
python3 create_tables.py
```
После выполнения скрипта вы увидите сообщение
```bash
Database 'validation' created successfully!
```
2. База данных успешно создана, осталось подключиться к ней и импортировать данные из CSV таблиц в папке ```database/table``` используя pgAdmin4 или DBeaver, правой кнопкой мышки выбираем таблицу и нажимаем ```Импорт данных```
Важно соблюдать порядок импортирования иначе мы будем получать ошибки при импортировании
1 - `mtype`
2 - `stype`
3 - `supppliers`
4 - `material_suppliers`
5 - `materials`

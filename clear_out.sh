# Путь к каталогу users
directory="users"

# Используем команду find для поиска файлов с именем "out.csv.log" в каталоге
# и передаем результаты команде rm для их удаления
find "$directory" -type f -name "out.csv.log" -exec rm {} \;

# Выводим сообщение о завершении операции
echo "Все файлы out.csv.log в каталоге $directory были удалены."
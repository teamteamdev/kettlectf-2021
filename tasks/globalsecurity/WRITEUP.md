# Опасная организация: Write-Up

Даны 2 текстовых файла и 1 .exe файл. Текстовые файлы содержат зашифрованное сообщение и данные о хакере.
Сказано, что хакер пользовался данной программой для генерации ключа, поэтому в первую очередь изучим эту программу.
Декомпилировав ее мы видим исходный код, разделенный на 4 небольших класса. 
<img src="writeup/Sec0.png">
Первым наше внимание может привлечь класс Encryptor. 
Посмотрев его содержимое можно сказать что это некий алгоритм для генерации ключа, использующий SHA256. 
Становится понятно, что сгенерированный ключ расшифровать не удастся, 
так как алгоритм слишком сложен и в коде не предусмотрен Decryptor, да и к тому же у нас нет ключа для расшифровки. 
Смотрим дальше, видим класс Form1, но там ничего полезного. 
Дальше находим основной класс Program, в котором видим вызов всех основных методов.
Прочитав их обратим внимание, что результат генерации записывается в буфер обмена(Clipboard) и остается там дальше. 
<img src="writeup/Sec1.png">
Но у нас есть .txt файл со всеми данными о хакере! Значит, содержимое его буфера обмена на момент взлома тоже там! 
Открываем, ищем строчку Clipboard и находим ключ. Теперь у нас есть и сообщение и ключ, а алгоритм шифрования мы знаем из условия таска. 
<img src="writeup/Sec3.png">
Теперь достаточно найти любой онлайн расшифровщик AES256 и использовать его. В расшифрованном сообщение содержится флаг.
<img src="writeup/Sec4.png">

Флаг: **kettle_be_careful_with_who_you_trust**

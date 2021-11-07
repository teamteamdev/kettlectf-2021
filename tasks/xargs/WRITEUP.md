# Xargs: Write-up

1. Скачиваем rar файл `ctf.rar`

Открываем: 

  <img src="img/1.png" width=50%>

если открыть hint.png то мы увидим, то что сама картинка повреждена: 

  <img src="img/2.png" width=50%>

2. через терминал ведет команду hexet:

  <img src="img/3.png" width=50%>

Видим что вместо PNG, что то не понятное

4. Загуглем `png file header`

  <img src="img/4.png" width=50%>

5. Восстанавливаем и сохраняем:

  <img src="img/5.png" width=50%>


И получаем:

  <img src="img/6.png" width=50%>


6. Теперь переходим в secret и водим команду `find | xargs cat |grep 'ybzg5'`  


  <img src="img/7.png" width=50%>


7. копируем и вставляем в base64:
`echo "a2V0dGxlXzUybzg5eV8yNDR0Zl81NjQ=" | base64 -d` 

  <img src="img/8.png" width=50%>

и получаем флаг!

Флаг: **kettle_52o89y_244tf_564**

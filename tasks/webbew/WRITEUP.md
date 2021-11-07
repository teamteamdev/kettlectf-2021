# webbew: Write-up

На сайте видим приветствие и поле загрузки картинки на страницу
<br>
<img src="writeup/1.png">
<br>
Загрузив картинку, видим поле для ввода комментария, где можно запостить что-то о картинке
<br>
<img src="writeup/2.png">
<br>
Посмотрев код страницы, можно увидеть, что название картинки загружается напрямую в атрибут <i>src</i> тега img
<br>
<img src="writeup/3.png">
<br>
Можно догадаться, что название картинки никак не проверяется и можно провернуть xss-атаку, украв какие-то данные у другого пользователя, введя их в поле комментариев. Если ввести данный код в название картинки:
<br>
`name= onerror=comment=document.getElementsByName('comment')[0];`
`comment.innerText=encodeURI(document.cookie);document.getElementById('submitcomment').click();`
<br>
и загрузить ее, увидим, что из-за большого количества запросов появилась ошибка:</div>
<br>
<img src="writeup/4.png">
<br>
Поэтому отключаем javascript в своем браузере и смотрим поле комментариев.
<br>
<img src="writeup/5.png">
<br>
Ура! Мы отыскали флаг и можем сдавать таск!

Флаг: **kettle_dont_trust_information_from_users**
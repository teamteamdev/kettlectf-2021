# rsgo_task: Write-up

Цель задания найти строчки кода задающие надпись на главном экране приложения

Первым делом стоит открыть приложение, для этого нужно сделать показ скрытых файлов и открыть в начальной папке RealstedyGo, файл RealStedyGoTrial.exe.
	
![Путь к exe](writeup/exe.png)
	
	
По центру экрана в приложении мы видим надпись, в которой узнаем название следующего файла, который сначала нужно найти и открыть 
	
![Надпись по центру экрана](writeup/nadpis.png)
	
	
Находится этот файл по пути RealstedyGo\ReelSteadyGoTrial_Data\Managed .
	
![Путь к .dll](writeup/dll.png)
	
	
Для следющего шага воспользуемся программой dnSpy, откроем с помощью неё Assembly-CSharp.dll и найти по пути Assembly-CSharp.dll\-\RsgoGlobalControl код Awake(): void

![Путь к флагу_1](writeup/put_1.png)
![Путь к флагу_2](writeup/put_2.png)
	
В нем и находим флаг.


Флаг: **kettle_team_7_rsgo_top_739211**


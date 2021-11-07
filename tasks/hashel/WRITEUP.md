# Hashel: Write-up

Открываем код, видим много всякой всячины. Для начала стоит выяснить на чем он
написан. Погуглим сигнатуру какой-нибудь функции, например, `update msg model`.
Все ссылки говорят нам, что это [Elm](elm-lang.org). Откроем его playground и
вставим туда код.

Первой находим функцию `url : Int -> String`. Нетрудно догадаться, что она
строит адрес, по которому, если найти упоминание этой функции в коде дальше,
делается GET запрос (79 строчка). Посмотрим, что лежит по этому адресу.

```
> curl https://hashel.board.kettlec.tf/1
[0]
> curl https://hashel.board.kettlec.tf/2
[0,1248]
> curl https://hashel.board.kettlec.tf/35
[0,1248,5732,14917,9054,2920,85,6555,9930,7258,12946,1440,15077,1081,6910,734,3559,5035,9281,1135,6822,12812,11655,3041,5901,2824,270,11702,3544,8292,12258,14221,1]
> curl https://hashel.board.kettlec.tf/40
[0,1248,5732,14917,9054,2920,85,6555,9930,7258,12946,1440,15077,1081,6910,734,3559,5035,9281,1135,6822,12812,11655,3041,5901,2824,270,11702,3544,8292,12258,14221,1]
```

Видно, что с определенного момента размер данных не меняется.

Немного прочитав про Elm узнаем, что изменение состояний возможно только путем вызова метода `update` с экземплятором `Msg`, который и определяет как именно поменять состояния. Вызвать этот метод можно либо через обработчик событий, либо через подписки, либо черещ команду (например, HTTP запрос). В 80 строчке мы говорим вызвать `Msg.Validate` с данными, которые получили с сервера. Посмотрим на код обработки этого события:
```elm
    Validate result -> case result of
      Ok recipes -> case model of
        WaitValidation {magic, key} ->
          let ingredients = prepare magic key
              mama = List.reverse (conjure (List.reverse ingredients) Nothing)
          in if
            (List.length recipes == List.length mama)
            && (List.all ((/=) False) (List.map2 (==) mama recipes))
              then
              ( Success
                  (String.concat (List.map (\c -> String.fromChar (Char.fromCode c)) ingredients)
                  ++ "_"
                  ++ (String.replace "+" "_plus_" (String.replace "/" "_slash_" key)))
              , Cmd.none
              )
          else (Waiting, Cmd.none)
        _ -> (Waiting, Cmd.none)
      Err _ -> (Waiting, Cmd.none)
```

Мы ответ сервера (`recipes`) сравниваем с результатом функции `conjure`, которая вызывается с каким-то списком и `Nothing` (тут читаем про тип `Maybe` в Elm). Посмотрим на функцию `conjure`:
```elm
conjure : (List Int) -> (Maybe Int) -> (List Int)
conjure ingredients knife = case knife of
  Just k ->
    case ingredients of
      (c :: cs) -> let it = abs (c - k) * (c + k) in
        case conjure cs (Just c) of
          (d :: ds) -> (baa (abb d + it)) :: d :: ds
          _ -> [it]
      _ -> [0]
  Nothing -> case ingredients of
    (c :: cs) -> conjure cs (Just c)
    _ -> []
```

Принимает список целых чисел и, возможно, число, а возвращает другой список
чисел. Вернемся на шаг назад и внимательно посмотрим на аргументы. Один из них
`List.reverse ingredients`, также используетмся при составлении состояния типа
`Success`: `String.concat (List.map (\c -> String.fromChar (Char.fromCode c))
ingredients)`. Немного посмотрев на эту строчку находим в ней знакомый
`''.join(ord(c) for c in a)`, то есть из кодов символов собирается строчка.

Поиграемся с этой функцией. Для этого в новом playground набросаем простое приложение:
```elm
import Browser
import Html exposing (div, text)

abb = (*) 1663
baa = remainderBy 15131

conjure : (List Int) -> (Maybe Int) -> (List Int)
conjure ingredients knife = case knife of
  Just k ->
    case ingredients of
      (c :: cs) -> let it = abs (c - k) * (c + k) in
        case conjure cs (Just c) of
          (d :: ds) -> (baa (abb d + it)) :: d :: ds
          _ -> [it]
      _ -> [0]
  Nothing -> case ingredients of
    (c :: cs) -> conjure cs (Just c)
    _ -> []
    
init = Nothing

update _ _ = Nothing

view _ =
  div [] [text (Debug.toString "aaaa")]
  
main = Browser.sandbox { init = init, update = update, view = view }
```

Первые буквы флага `kettle_`, а их коды `[107, 101, 116, 116, 108, 101, 95]`.
Вспоминаем про `List.reverse` и посмотрим на вывод `conjure`:
`[0,1248,5732,14917,9054,2920,85]`. Это начало последовательности, которую мы
забрали с сервера. Можно догадаться, что это некоторый хеш-алгоритм. Обновим
функцию `view` и будем искать следующий символ:

```elm
res f = List.reverse (conjure
  ((Char.toCode f) :: (List.reverse [107, 101, 116, 116, 108, 101, 95]))
  Nothing)

view _ =
  div [] ( List.map
    (\x -> div [] [text (String.fromList [x, ':', ' ']) , text (Debug.toString (res x))])
    (String.toList "abcdefghijklmnopqrstuvwxyz0123456789_")
  )
```

Так мы будем находить следующий символ, пока не восстановим всю
последовательность: `kettle_funct10n8l_pr09ram1ng_b3st`. Но сдать это как флаг
не получается. Вернемся к функции `update`. В 95-96 строчке видим, что оно
соединяется с `key`.

Попробуем разгадать его. Сначала он пришел к нам из модели, а в модель он
попадает через `Msg.check`. Данное событые вызывается в `tryMagicKey` вместе
`value`, которое приходит как аргумент. Вызывается `tryMagicKey` из
`onMagicKey`, который является обработчиком `keyup` поля ввода. Там же видим,
что `value` --- это значение поля ввода, а `key` --- нажатая кнопка. В
`tryMagicKey` видим сравнение `key` с чем-то. Снова копируем это в соседнюю
вкладку и знакомым нам способом смотрим (не забываем скопировать `magazine`).
Это оказывается кнопка `F6`. Попробуем что-нибудь ввести в поле и нажать ее.
Что-то поменялось, значит мы не ошиблись.

Мы так и не узнали чему должен быть равен `key`. Возвращаемся в `update`,
вспоминаем про `ingredients`, который передается в `conjure` и является частью
флага. Он составляется из `magic` и `key`, обе передаются из модели. Несколькими
строчками выше видим, что `magic` = `generateSeq (String.length value)
rootSeed`. Снова копируем все что нужно в соседную вкладку и получаем значение
`magic` (длину возьмем побольше на всякий случай):
`[51,188,185,112,24,33,226,136,238,183,42,99,164,88,237,183,232,228,38,56,255,108,89,15,160,114,181,216,44,47,101,209,35,52,105,210,30,143,94,123,121,39,254,118,14,144,214,235,17,169]`

Далее идем смотреть на `prepare`, который как раз и готовит нам `ingredients`.
Оказывается, что он просто складывает по элементам списки `magic` и `pounding
value` по модулю `256`. Заглядывая в документацию по `List.map2` понимаем, что
итоговая длина списка равняется длине меньшего из двух аргументов.

Осталось разгадать `pounding`. Изначально функция выглядит страшно и использует
`pounding_work`, которая использует `pounder`. А последняя использует `trader`,
который не принимает аргументов, значит является константой (одно из правил ФП).
Недолго думая, узнаем его значение:
`ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/`. Гуглим эту
строчку и понимаем, что это алфавит base64. Немного поглядев на семейство
функций `pounding` видим нечто схожее с алгоритмом декодирования. А если
подумать, что нам нужно иметь возможность вводить любые байты, то становится
ясно, что это точно `b64decode`.

Возвращаемся к `ingredients`. Мы знаем, что это должна быть строка `kettle_...`,
а так же знаем, что код каждой буквы определяется суммой элемента из `magic` и
элемента, который опредеяем мы. Обратной операцией узнаем список байт, который
мы должны ввести и закодируем его в base64. Полученную строчку введем в поле
ввода, нажмем `F6` и получим флаг.

Флаг: **kettle\_funct10n8l\_pr09ram1ng\_b3st\_OKm7BFREfd6HtzkRjdiBgYR7SjoxzRlSzb\_plus_5jzMzzqJR**
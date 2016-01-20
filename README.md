Установка:
```
git clone https://github.com/shantilabs/vkscriptz
cd vkscriptz
pip install -r requirements.txt
./vk.py auth
```

Всего участников группы:
```bash
$ ./vk.py group_members shanti_shanti_shop | wc -l
4075
```

Участники только из Питера:
```bash
$ ./vk.py group_members --city_id=2 shanti_shanti_shop | wc -l
1200
```

Инстаграмы Питерских участников:
```bash
$ ./vk.py group_members_instagrams --city_id=2 shanti_shanti_shop
https://www.instagram.com/romanov_sky/
https://www.instagram.com/vvtdark/
https://www.instagram.com/torvamessorem/
https://www.instagram.com/nexus_vi/
https://www.instagram.com/emelyanovslava/
https://www.instagram.com/izot.kuzmin/
https://www.instagram.com/klisov_maxim/
https://www.instagram.com/lerrmar/
https://www.instagram.com/ielefas/
https://www.instagram.com/travel_druganov/
https://www.instagram.com/yeneeto/
https://www.instagram.com/vadshishkin/
https://www.instagram.com/ungrome/
https://www.instagram.com/anavagian/
https://www.instagram.com/shamanic_boutique/
```

Список групп по слову «логарифм»:
```bash
$ ./vk.py group_search логарифм
101410949	Функция натурального логарифма
92530291	логарифмы
75438437	Закрытая группа
71413227	ЛоГаРифмы
55739756	рифмы логарифмы
48120393	Закрытая группа
35848174	ЛОГАРИФМЫ НЕЖНОСТИ
34713315	этот типичный логарифм))
33363632	(((**Логарифмы нежности**)))
26772875	Логарифмы☆Нежности
25449479	♡...превращая в логарифмы нежность*♡
20161911	Логарифмы нежности по краешку тела(с)
13751079	Клуб для тех, кого уже задрало учить все эти логарифмы, теории и различные хрени, которые ни фига тебе не пригодятся в твоей профессии
11273840	[Логарифмы нежности]
9174848	Группа для тех,кого бесит эта вечно взъерошеная "дама" с синусами,логарифмами и интегралами в голове!!!а также ее чертовы самостоятельные и домашки=)
3459690	Группа тех, кто знает что логарифм В.С. по основанию БИС равен?
3346074	Я смог(ла) сказать это: Бит — это двоичный логарифм вероятности равновероятных событий или сумма произведений вероятности на двоичный логарифм вероятности при разновероятных событиях!
3346064	Бит — это двоичный логарифм вероятности равновероятных событий или сумма произведений вероятности на двоичный логарифм вероятности при разновероятных событиях
1948920	На нас держится весь мир,ибо мы знаем что логарифм на логафрифм будет логарифм в квадрате!...
```

Все участники этих групп. Первая цифра id участника, вторая — в скольких группах из списка он состоит:
```bash
$ ./vk.py group_members `./vk.py group_search логарифм | cut -f1`
82088	1
1002637	1
1720279	1
4858456	1
5093779	1
5333049	1
5522020	1
5677801	1
8821414	1
9166713	1
10299720	1
10327477	1
11657653	1
13751736	1
15798695	1
16227525	1
16419198	1
.....
```

5 самых активных участников группы `107729497`:
```bash
$./vk.py group_active_members 107729497 | sort | uniq -c | sort -nr | head -n 5
   3 2150378
   3 175382517
   2 228737718
   2 182722259
   1 322695257
   ```

Cамые популярные группы среди участников группы `57314824`:
```bash
$./vk.py user_groups `./vk.py group_members 57314824` | cut -f2 | sort | uniq -c | sort -nr | head -n 100
   3 2150378
   3 175382517
   2 228737718
   2 182722259
   1 322695257
  ```

Список пользователей, входящих в группу `seafever` и в обе группы `bikini_vk` + `gulagrus`:
```bash
$ ./vk.py group_members --min-intersection=3 seafever bikini_vk gulagrus
Group seafever resolved to ID 35274426
Group bikini_vk resolved to ID 48625501
Group gulagrus resolved to ID 44616045
group#35274426: 2478 member(s)
group#48625501: 93750 member(s)
group#44616045: 1774 member(s)
21577672	3
21674663	3
27280273	3
29090245	3
30314967	3
36585664	3
62662179	3
72103508	3
83552896	3
89673447	3
91588841	3
92264923	3
102825268	3
107932910	3
125315584	3
...
```

Список «мёртвых» (удалённых или заблокированных) пользователей из группы seafever:
```bash
$ ./vk.py group_members --dead seafever
group seafever:  (2479 users) 549926
559696
1298650
2089177
3261207
3623107
...
```

Удaление пользователя из группы patr_kvarts:
```bash
 $ ./vk.py group_remove_members patr_kvarts 549926
 Group patr_kvarts resolved to ID 47335978
 Success: 1, failed 0
```

Чистим группу от удалённых:
```bash
 $ ./vk.py group_remove_members shantichai `./vk.py group_members --dead shantichai`
```

Сложный пример: Получение списка членов группы seafever, входящих в одну из «мусорных» групп из списка в файле:
```bash
$ cat sf.garbage_groups.txt | awk '{print $2}' | sed "s~^https://vk.com/~~" | sed "s~^club~~" | xargs ./vk.py group_members seafever > sf.garbage.members.txt
```

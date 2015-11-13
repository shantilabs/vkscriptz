Скрипты для работы с vk.com и мб ещё с чем-то.

```bash
bash-3.2$ echo "всего участников: `./vk_group_members.py shanti_shanti_shop | wc -l`"
всего участников: 4075
bash-3.2$ echo "«собачки» `./vk_group_members.py shanti_shanti_shop | grep deactivated | wc -l`"
«собачки»: 178
bash-3.2$ echo "онлайн: `./vk_group_members.py shanti_shanti_shop | grep online=1 | wc -l`"
онлайн: 473
````

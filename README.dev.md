# Разработка мода

## Необходимое окружение

* Unity 2019.4.38f (возможно обновление в рамках 2019.4.*)
* Visual Studio 2019 с поддержкой разработки проектов .NET 4.7.2
* Python 3.10
  * Модули docopts и polib
* Редактор переводов в формате Gettext

## Процесс сборки

Сборка осуществляется по следующему процессу:

1. Переводчик/текстовый редактор: Перевод файлов
2. Разработчик/i2loc_translate.py: Обновление translation.csv
3. Разработчик/Unity: Обновление ассета с обновленными ресурсами
4. Разработчик/Visual Studio: Пересборка проекта с включением ассета

## Необходимые внешние ресурсы

Для сборки библиотеки мода необходимы компоненты из установленной игры,
которые необходимо сохранить в каталог external

* `0Harmony.dll` (из `MelonLoader`)
* `Assembly-CSharp.dll` (из `Pharaoh_Data/Managed`)
* `MelonLoader.dll` (из `MelonLoader`)
* `UnityEngine.AssetBudleModule.dll` (из `Pharaoh_Data/Managed`)
* `UnityEngine.CoreModule.dll` (из `Pharaoh_Data/Managed`)

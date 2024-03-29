# Map-of-power-grid
Создание карт-схем на Python с помощью folium и geojson
## Доступно 3 вида карт:

1. [С расположением ЛЭП (Мошенское)](https://github.com/zuev27/Map-of-power-grid/tree/main/%D0%9C%D0%BE%D1%88%D0%B5%D0%BD%D1%81%D0%BA%D0%BE%D0%B5);
2. [Без расположения ЛЭП (Олонецкий РЭС)](https://github.com/zuev27/Map-of-power-grid/tree/main/%D0%9E%D0%BB%D0%BE%D0%BD%D0%B5%D1%86%D0%BA%D0%B8%D0%B9%20%D0%A0%D0%AD%D0%A1);
3. [С добавлением электростанций (Шекснинский РЭС)](https://github.com/zuev27/Map-of-power-grid/tree/main/%D0%A8%D0%B5%D0%BA%D1%81%D0%BD%D0%B8%D0%BD%D1%81%D0%BA%D0%B8%D0%B9%20%D0%A0%D0%AD%D0%A1).

## Для корректной работы необходимо наличие следующих библиотек в Python:
```
1. pandas - для работы с данными. В рассматриваемых примерах - это вывод данных из Microsoft Excel;
2. folium - для работы с картами.
3. geojson - для работы с географическими данными карт.
```

## Результат работы

После успешного компилирования программы в папке появляются файлы-привязки nodes.geojson, а также lines.geojson, gen.geojson (при наличии) и создается файл в формате *.html, который можно открыть в браузере (желательно Google Chrome).

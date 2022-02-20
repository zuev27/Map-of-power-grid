import pandas as pd                                                                         #Для работы с данными
import folium                                                                               #Для работы с картами
from folium.plugins  import MeasureControl, Fullscreen, MarkerCluster, Search               #Для вывода инструментов на карте
from geojson import Feature, FeatureCollection, Point, LineString                           #Для работы с данными GeoJSON
import json

############################################################################################################################################
#Создание карты с центром в координатах. Начальная точка выбрана как местоположение села Мошенское
map = folium.Map(location = [58.511835, 34.585300], #Координаты с. Мошенское
               zoom_start = 14,                     #Начальный размер карты
               control_scale = True,                #Добавление графической шкалы масштаба карты
               zoom_control = True,                 #Добавление кнопок для увеличения и уменьшения масштаба карты
               max_bounds = True)                   #Ограничение прокрутки карты по ширине

#Изменение цвета в зависимости от номинального напряжения
def color_change(Unom):
  U = [1150, 800, 750, 500, 400, 330, 220, 150, 110, 35, 20, 10, 6, 60]
  colors = ['#CD8AFF', '#0000C8', '#0000C8', '#A50F0A', '#F0961E', '#008C00', '#C8C800', '#AA9600', '#00B4C8', '#826432', '#826432', '#640064', '#C89664', '#E533B5']
  Unom_colors = dict(zip(U, colors))
  if Unom not in U:
      return 'black'
  return Unom_colors[Unom]

###Экспорт данных в GeoJson для использования в картах
#Добавление узлов ПС на карту
data = pd.read_excel('Перечень ПС.xlsx')
features = data.apply(
    lambda row: Feature(properties = {'name':row['Название ПС'],
                                      'Unom':row['Uном, кВ'],
                                      'address':row['Место расположения, адрес']},
                        geometry = Point((float(row['Долгота ПС']),
                                          float(row['Широта ПС'])))),
                                          axis = 1).tolist()

feature_collection = FeatureCollection(features = features)

with open('nodes.geojson', 'w', encoding='cp1251') as f:
     json.dump(feature_collection, f, ensure_ascii = False)

#Создание слоев для подстанций
layer = folium.GeoJson(
    feature_collection,
    name = 'Подстанции',
    show = False
    ).add_to(map)

gj = folium.GeoJson('nodes.geojson')

#Создание маркеров
marker_cluster = MarkerCluster(name = 'Подстанции').add_to(map)
for feature in gj.data['features']:
    folium.CircleMarker(
        location = list(reversed(feature['geometry']['coordinates'])),
        color = 'black',
        fill_color = color_change(feature['properties']['Unom']),
        fill_opacity = 1,
        popup = folium.Popup(feature['properties']['name'] + '</br>Адрес: ' + feature['properties']['address'], max_width=250),
                        ).add_to(marker_cluster)

#####################################################################################################################################################
#Добавление названий на карту (БЕЗ МАРКЕРОВ)
#for feature in gj.data['features']:
#    folium.Marker(
#        location = list(reversed(feature['geometry']['coordinates'])),
#        popup = folium.Popup(feature['properties']['name'], max_width=250),
#        icon = folium.DivIcon(html=f"""<div style="font-family: Times New Roman; color: blue">{feature['properties']['name']}</div>""")
#                        ).add_to(map)
#####################################################################################################################################################

#Добавление ЛЭП на карту
data2 = pd.read_excel('Перечень ВЛ.xlsx')
features2 = data2.apply(
    lambda row: Feature(properties = {'name':row['ЛЭП'],
                                      'Unom':row['Uном, кВ']},
                         geometry = LineString(((float(row['Долгота узла 1']),
                                                 float(row['Широта узла 1'])),
                                                (float(row['Долгота узла 2']),
                                                 float(row['Широта узла 2']))))),
                                                 axis = 1).tolist()
                                                
feature_collection2 = FeatureCollection(features = features2)

with open('lines.geojson', 'w', encoding='cp1251') as f2:
     json.dump(feature_collection2, f2, ensure_ascii = False)
     
layer2 = folium.GeoJson(
    feature_collection2,
    name = 'ЛЭП',
    show = True,
    ).add_to(map)

gj2 = folium.GeoJson('lines.geojson')
############################################################################################################################################
#Добавление ЛЭП на карту с помощью Polyline (с изменением цвета по Uном)
#for features2 in gj2.data['features']:
#    folium.PolyLine(
#                locations = list(reversed(features2['geometry']['coordinates'])),
#                    ).add_to(map)
############################################################################################################################################

#Добавление дополнительных слоев карт
folium.TileLayer(tiles = 'https://api.mapbox.com/styles/v1/mapbox/streets-v10/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4M29iazA2Z2gycXA4N2pmbDZmangifQ.-g_vE53SD2WrJ6tFX7QHmA', attr = 'Mapbox', name = 'Mapbox Streets').add_to(map)
folium.TileLayer(tiles = 'https://api.mapbox.com/styles/v1/mapbox/satellite-streets-v9/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4M29iazA2Z2gycXA4N2pmbDZmangifQ.-g_vE53SD2WrJ6tFX7QHmA', attr = 'Mapbox', name = 'Mapbox Satellite Streets').add_to(map)

#Добавление строки поиска
substation_search = Search(layer = layer,
                           geom_type = 'Point',
                           placeholder = 'Search',
                           search_label = 'name',
                           search_zoom = 14
                           ).add_to(map)
folium.LayerControl().add_to(map)

map.add_child(MeasureControl()) #Добавление линейки для измерений
map.add_child(Fullscreen())     #Добавление кнопки «На весь экран»

map.save("Мошенское.html")

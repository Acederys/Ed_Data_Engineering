<h2>Ed_Data_Engineering</h2>
<h2>Решение учебных задач по инженирингу данных</h2>
<p>Вариант 7</p>
<h2>Файлы для задания к четвертой практической</h2>
<p>Все таблицы создавались через SQLite и описаны в <code>create_bd_1</code></p>
<table>
  <tr>
    <th>Название файла</th>
    <th>Номер задания</th>
    <th>Описание</th>
  </tr>
  <tr>
    <td>
      <p>4_main_1.py</p>
      <p>task_1_var_07_item.json</p>
      <p>result_4_1_filter_rating.json</p>
      <p>result_4_1_order_pages.json</p>
      <p>result_4_1_2_order_pages.json</p>
      <p>result_4_1_3_order_pages.json</p>
      <p>4_1_db.db</p>
    </td>
    <td>Задача 1</td>
    <td>Входные данные task_1_var_07_item.json, <br>Выходные 4_1_db.db (табл. biblio), result_4_1_order_pages.json, result_4_1_filter_rating.json, result_4_1_3_order_pages.json, result_4_1_2_order_pages.json
    </td>
  </tr>
  <td>
      <p>4_main_2.py</p>
      <p>task_2_var_07_subitem.text</p>
      <p>result_4_2_1_order_pages.json</p>
      <p>result_4_2_2_order_pages.json</p>
      <p>result_4_2_3_order_pages.json</p>
      <p>4_1_db.db</p>
    </td>
    <td>Задача 2</td>
    <td>Входные данные task_2_var_07_subitem.text, <br>Выходные 4_1_db.db (табл. book), result_4_2_1_order_pages.json, result_4_2_2_order_pages.json, result_4_2_3_order_pages.json
    </td>
  </tr>
  <tr>
    <td>
      <p>4_main_3.py</p>
      <p>task_3_var_07_part_1.text</p>
      <p>task_3_var_07_part_2.msgpack</p>
      <p>result_4_3_order_artist.json</p>
      <p>result_4_3_filter_year.json</p>
      <p>result_4_3_occuerrence.json</p>
      <p>4_1_db.db</p>
    </td>
    <td>Задача 3</td>
    <td>Входные данные task_3_var_07_part_1.text, task_3_var_07_part_2.msgpack, <br>Выходные 4_1_db.db (табл. music), result_4_3_filter_year.json, result_4_3_order_artist.json, result_4_3_occuerrence.json
    </td>
  </tr>
  <tr>
    <td>
      <p>4_main_4.py</p>
      <p>task_4_var_07_product_data.text</p>
      <p>task_4_var_07_update_data.msgpack</p>
      <p>result_4_4_1_.json</p>
      <p>result_4_4_2.json</p>
      <p>result_4_4_analis.json</p>
      <p>result_4_4_3.json</p>
    </td>
    <td>Задача 4</td>
    <td>Входные данные task_4_var_07_product_data.text task_4_var_07_update_data.msgpack, <br>Выходные 4_1_db.db (табл. products), result_4_4_1_.json, result_4_4_2.json, result_4_4_analis.json, result_4_4_3.json
    </td>
  </tr>
  <tr>
    <td>
      <p>4_main_5.py</p>
      <p>apartment.csv</p>
      <p>AssessedValue.json</p>
      <p>town.csv</p>
      <p>SaleAmount_10000.json</p>
      <p>Residential.json</p>
      <p>Ansonia.json</p>
      <p>AssessedValue_10000.json</p>
      <p>avg_AssessedValue.json</p>
      <p>AssessedValue_9999999.json</p>
      <p>4_5_db.db</p>
    </td>
    <td>Задача 5</td>
    <td>Входные данные apartment.csv, AssessedValue.json, town.csv <br>Выходные 4_5_db.db (табл. products), SaleAmount_10000.json, Residential.json, Ansonia.json, AssessedValue_10000.json, avg_AssessedValue.json, AssessedValue_9999999.json</td>
  </tr>
</table>
  <h3>
    Пояснения к 5-ой задаче
  </h3>
  <p>
    Предметной областью были выбраны данные о продаже недвижимости в США. Из данных были выбраны: город, год продажи, адрес недвижимости, оценочная стоимость, фактическая цена продажи и тип недвижимости. Данные были распределены в три файла для формирования трех таблиц:
  </p>
<table>
  <tr>
    <th>Название таблицы</th>
    <th>Столбцы</th>
  </tr>
  <tr>
    <td>apartament</td>
    <td>год, адрес, фактическая стоимотсь, тип недвижимости</td>
  </tr>
  <tr>
    <td>AsessedValue</td>
    <td>адрес, оценочная стоимость</td>
  </tr>
  <tr>
    <td>town</td>
    <td>город, адрес</td>
  </tr>
</table>
  <p>
    Создание таблиц производилось в SQLite, данные представлены в  <code>create_bd_1</code>
  </p>
  <h5>Описание запросов</h5>
  <table>
  <tr>
    <th>Название файла</th>
    <th>Запрос</th>
  </tr>
  <tr>
    <td>SaleAmount_10000.json</td>
    <td>Из таблицы apartament взять все данные, фактическая стоимость продажи которых больше 100000, сгруппировать по типу и взять не больше 100
      <code>SELECT * FROM apartament WHERE SaleAmount > 10000 ORDER BY PropertyType DESC LIMIT ?</code>
    </td>
  </tr>
  <tr>
    <td>Residential.json</td>
    <td>Взять из таблицы town все данные id_town которых равен id из таблицы apartament, тип которых Residential
    <code>SELECT * FROM town WHERE id_town = (SELECT id FROM apartament WHERE PropertyType = ?)</code></td>
  </tr>
  <tr>
    <td>Ansonia.json</td>
    <td>Взять из таблицы apartament все данные id которых равен id_town из таблицы town, город которых Ansonia
    <code>SELECT * FROM apartament WHERE id = (SELECT id_town FROM town WHERE Town = ?)</code></td>
  </tr>
  <tr>
    <td>avg_AssessedValue.json</td>
    <td>Взять из таблицы AsessedValue все данные оценочная стоимость которых больше 10000 с лимитом 10
    <code>SELECT * FROM AsessedValue WHERE AssessedValue > 10000 LIMIT ?</code></td>
  </tr>
  <tr>
    <td>AssessedValue_10000.json</td>
    <td>Взять из таблицы AsessedValue среднее по стобцу стоимости, и вывести все данные, id_AsessedValue которых равен id из таблицы town, город которых Ansonia
    <code>SELECT AVG(AssessedValue) as avg_AssessedValue, * FROM AsessedValue WHERE id_AsessedValue = (SELECT id FROM town WHERE Town = ?)</code></td>
  </tr>
  <tr>
    <td>AssessedValue_9999999.json</td>
    <td>Взять из таблицы apartament id которых равен, id_AsessedValue из таблицы AsessedValue, оценочная стоимость которых меньше 9999999
    <code>SELECT * FROM apartament WHERE id = (SELECT id_AsessedValue FROM AsessedValue  WHERE AssessedValue < ?)</code></td>
  </tr>
  </table>
<h2>Файлы для задания к третьей практической</h2>
<table>
  <tr>
    <th>Название файла</th>
    <th>Номер задания</th>
    <th>Описание</th>
  </tr>
  <tr>
    <td>
      <p>3_main_1.py</p>
      <p>3_var_7</p>
      <p>result_3_1.json</p>
      <p>result_3_1_olympic.json</p>
      <p>result_3_1_sort_rating.json</p>
    </td>
    <td>Задача 1</td>
    <td>Входные данные 3_var_7, <br>Выходные result_3_1.json result_3_1_olympic.json, result_3_1_sort_rating.json
    </td>
  </tr>
  <td>
      <p>3_main_2.py</p>
      <p>3_2_var_7</p>
      <p>result_3_2.json</p>
      <p>result_3_2_filter.json</p>
      <p>result_3_2_sort.json</p>
    </td>
    <td>Задача 2</td>
    <td>Входные данные 3_2_var_7, <br>Выходные result_3_2.json, result_3_2_filter.json, result_3_2_sort.json
    </td>
  </tr>
  <tr>
    <td>
      <p>3_main_3.py</p>
      <p>3_3_var_7</p>
      <p>result_3_3.json</p>
      <p>result_3_3_filter.json</p>
      <p>result_3_3_sort.json</p>
    </td>
    <td>Задача 3</td>
    <td>Входные данные 3_3_var_7, <br>Выходные result_3_3.json, result_3_3_filter.json, result_3_3_sort.json
    </td>
  </tr>
  <tr>
    <td>
      <p>3_main_4.py</p>
      <p>3_4_var_7</p>
      <p>result_3_4.json</p>
      <p>result_3_4_filter.json</p>
      <p>result_3_4_sort.json</p>
    </td>
    <td>Задача 4</td>
    <td>Входные данные 3_4_var_7, <br>Выходные result_3_4.json, result_3_4_filter.json, result_3_4_sort.json
    </td>
  </tr>
  <tr>
    <td>
      <p>3_main_5.py</p>
      <p>3_5_html</p>
      <p>result_3_5.json</p>
      <p>result_3_5_filter.json</p>
      <p>result_3_5_sort.json</p>
    </td>
    <td>Задача 5</td>
    <td>Входные данные 3_5_html, <br>Выходные result_3_5.json, result_3_5_filter.json, result_3_5_sort.json 
      <small>файлы 3_5_html, являются выходными для парсинга по условию задачи</small>
    </td>
  </tr>
</table>
<h2>Файлы для задания ко второй практической</h2>
<table>
  <tr>
    <th>Название файла</th>
    <th>Номер задания</th>
    <th>Описание</th>
  </tr>
  <tr>
    <td>
      <p>2_main_1.py</p>
      <p>matrix_1_7.npy</p>
      <p>result_2_1.js</p>
    </td>
    <td>Задача 1</td>
    <td>Входные данные matrix_1_7.npy, <br>Выходные result_2_1.json
    </td>
  </tr>
  <td>
      <p>2_main_2.py</p>
      <p>matrix_7_2.npy</p>
      <p>result_2_2.npz</p>
      <p>result_2_2_com.npz</p>
    </td>
    <td>Задача 2</td>
    <td>Входные данные matrix_7_2.npy, <br>Выходные result_2_2.npz, result_2_2_com.npz
    </td>
  </tr>
  <tr>
    <td>
      <p>2_main_3.py</p>
      <p>products_7.json</p>
      <p>result_2_3.json</p>
      <p>result_2_3.msgpack</p>
    </td>
    <td>Задача 3</td>
    <td>Входные данные products_7.json, <br>Выходные result_2_3.msgpack, result_2_3.json
    </td>
  </tr>
  <tr>
    <td>
      <p>2_main_4.py</p>
      <p>products_7.pkl</p>
      <p>price_info_7.json</p>
      <p>result_2_4.pkl</p>
    </td>
    <td>Задача 4</td>
    <td>Входные данные products_7.pkl, price_info_7.json <br>Выходные result_2_4.pkl
    </td>
  </tr>
  <tr>
    <td>
      <p>2_main_5.py</p>
      <p>Warehouse_and_Retail_Sales.csv</p>
      <p>result_2_5.json</p>
      <p>result_2_4.pkl</p>
    </td>
    <td>Задача 5</td>
    <td>Входные данные Warehouse_and_Retail_Sales.csv <br>Выходные result_2_5.json (результат)<br> (преобразования входного файла) Warehouse_and_Retail_Sales.json, Warehouse_and_Retail_Sales.msgpack, Warehouse_and_Retail_Sales.pickle
    </td>
  </tr>
</table>
<h2>Файлы для задания для первой практической</h2>
<table>
  <tr>
    <th>Название файла</th>
    <th>Номер задания</th>
    <th>Описание</th>
  </tr>
  <td>
      <p>main_1.py</p>
      <p>text_1_var_7</p>
      <p>result_1.txt</p>
    </td>
    <td>Задача 1</td>
    <td>Входные данные text_1_var_7, <br>Выходные result_1.txt
    </td>
  </tr>
  <tr>
    <td>
      <p>main_2.py</p>
      <p>text_2_var_7</p>
      <p>result_2.txt</p>
    </td>
    <td>Задача 2</td>
    <td>Входные данные text_2_var_7, <br>Выходные result_2.txt
    </td>
  </tr>
  <tr>
    <td>
      <p>main_3.py</p>
      <p>text_3_var_7</p>
      <p>result_3.txt</p>
    </td>
    <td>Задача 3</td>
    <td>Входные данные text_3_var_7, <br>Выходные result_3.txt
    </td>
  </tr>
  <tr>
    <td>
      <p>main_4.py</p>
      <p>text_4_var_7</p>
      <p>result_4.csv</p>
    </td>
    <td>Задача 4</td>
    <td>Входные данные text_4_var_7 <br>Выходные result_4.csv
    </td>
  </tr>
  <tr>
    <td>
      <p>main_5.py</p>
      <p>text_5_var_7</p>
      <p>result_5.csv</p>
    </td>
    <td>Задача 5</td>
    <td>Входные данные text_5_var_7<br>Выходные result_5.csv
    </td>
  </tr>
  <tr>
    <td>
      <p>main_6.py</p>
      <p>anime.json</p>
      <p>rezult_6.html</p>
    </td>
    <td>Задача 6</td>
    <td>Входные данные anime.json<br>Выходные rezult_6.html
    </td>
  </tr>
</table>


## Клиент-серверное приложение для просмотра файлов

### Запуск сервера 

```
Networks-spring-2022/2022.03.12> python server.py <max_threads> <port>
```
Например 

```
Networks-spring-2022/2022.03.12> python server.py 12 9009
```
Запустит localhost с портом 9009. Будет использоваться до 12 потоков.


### Запуск клиента

```
Networks-spring-2022/2022.03.12> python client.py <host> <port> <filename>
```
Например, чтобы соответствовать запущенному ранее серверу
```
Networks-spring-2022/2022.03.12> python client.py localhost 9009 "./filesToCheck/lengthClass1"
```
Так будет отправлен запрос для файла lengthClass1, лежащего по указанному пути.
Ответ будет получен в командной строке.

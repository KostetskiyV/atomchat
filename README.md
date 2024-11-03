<h1 align="center">Инструкция по деплою ATOMCHAT</h1>
<p>1. Скачайте родительскую директорию atomsite.</p>
<p>2. Откройте терминал и перейдите в неё.</p>
<p>3. Находясь в режиме суперпользователя пропишите команды: «python manage.py makemigrations», «python manage.py migrate», «pip install -r requirements.txt»</p>
<p>4. Запустите проект, прописав команду «python manage.py runserver»</p>

<h2 align="center">Фунционал</h2>
<p>Пользователь взаимодействует с сервером посредством принятия/отправки JSON объектов (результат HTTP-запроса) по фиксированным URL-адресам API сервера. Для удобства рекомендуется использование программ для генерации HTTP-запросов.</p>

<p>Для добавления пользователя с правами администратора, пропишите в терминале «python manage.py createsuperuser», находясь в корневой папке проекта, затем укажите имя администратора и пароль, подтвердите пароль.</p>

<h3>URL API ATOMCHAT Server: localhost:8000/api/v1/</h3>
<p>Все нижеуказанные cсылки являются дочерними к адресу вышеуказанного API сервера.</p>

**URLs:**

**users/registrate/ (POST)**

<ul><li>    localhost:8000/api/v1/users/registrate/</li>
      <p>Регистрирует пользователя, принимает POST запросы, типа:</p>
      ```yaml
      {
          "user": {
              "username": username,
              "password": password
          }
      }```
      В качестве username и password подаются строковые переменные, содержащие имя и пароль пользователя.
      В ответ сервер возвращает имя пользователя и его авторизационный токен или сообщение об ошибке в теле запроса.

users/login/ (POST)

    • localhost:8000/api/v1/users/login/
      Авторизирует пользователя, принимает POST запросы, типа:
      {
          "user": {
              "username": username,
              "password": password
          }
      }
      В качестве username и password подаются строковые переменные, содержащие имя и пароль пользователя.
      В ответ сервер возвращает имя пользователя и его аутентификационный токен или сообщение об ошибке в теле запроса.

users/block/ (POST)

    • localhost:8000/api/v1/users/block/
      Заблокировать пользователя, отключив ему доступ к функционалу приложения и скрыв все его сообщения, доступно только пользователям с правами администратора. Принимает POST запросы, типа:
      {
          "users": {
              "usernames": usernames
          }
      }
      В качестве usernames подаётся массив строковых переменных, содержащих имена блокируемых пользователей.
      В header запроса передаётся переменная Token, содержащая аутентификационный токен, полученный при авторизации.
      В ответ сервер возвращает имена заблокированных пользователей или сообщение об ошибке.

users/unlock/ (POST)

    • localhost:8000/api/v1/users/unlock/
      Разблокировать пользователя, вернув ему доступ к функционалу приложения и вновь показывать все его сообщения, доступно только пользователям с правами администратора. Принимает POST запросы, типа:
      {
          "users": {
              "usernames": usernames
          }
      }
      В качестве usernames подаётся массив строковых переменных, содержащих имена разблокируемых пользователей.
      В header запроса передаётся переменная Token, содержащая аутентификационный токен, полученный при авторизации.
      В ответ сервер возвращает имена разблокированных пользователей или сообщение об ошибке.

users/user/<user>/ (GET)

    • localhost:8000/api/v1/users/user/<user>
      Получить имя и аутентификационный токен пользователя. Вместо <user> в адресной строке указывается имя искомого пользователя. Принимает GET запросы.
      В header запроса передаётся переменная Token, содержащая аутентификационный токен, полученный при авторизации.
      В тело запроса не передаётся данных.
      В ответ сервер возвращает имя и аутентификационный токен пользователя или сообщение об ошибке.

messenger/create-chat/ (POST)

    • localhost:8000/api/v1/messenger/create-chat
      Создать приватный чат, принимает POST запросы, типа:
      {
          "chat": {
              "name": chatname,
              "users": users
          }
      }
      В качестве chatname подаётся строковая переменная, содержащая название чата, в качестве users массив строковых переменных, содержащий имена пользоватей добавляемых в чат. Если пользователь, создающий чат не указан в массиве users, он всё равно будет добавлен.
      В header запроса передаётся переменная Token, содержащая аутентификационный токен, полученный при авторизации.
      В ответ сервер возвращает название чата и имена его членов или сообщение об ошибке.

messenger/send-message/ (POST)

    • localhost:8000/api/v1/messenger/send-message
      Отправить сообщение в приватный чат, принимает POST запросы типа:
      {
          "message": {
              "text": text,
              "chatname": chat
          }
      }
      В качестве text подаётся строковая переменная, содержащая текст сообщения, в качестве chat название чата.
      В header запроса передаётся переменная Token, содержащая аутентификационный токен, полученный при авторизации.
      В ответ сервер возвращает имя пользователя, написавшего сообщение, время написания, чат и текст сообщения или сообщение об ошибке.

messenger/chat/<chat>/ (GET)

    • localhost:8000/api/v1/messenger/chat/<chat>
      Получить сообщения из чата. Вместо <chat> в адресной строке указывается название искомого чата. Доступно только членам чата или администраторам. Принимает GET запросы.
      В header запроса передаётся переменная Token, содержащая аутентификационный токен, полученный при авторизации.
      В тело запроса не передаётся данных.
      В ответ сервер возвращает список сообщений в чате отсортированный по дате написания или сообщение об ошибке.
</ul>

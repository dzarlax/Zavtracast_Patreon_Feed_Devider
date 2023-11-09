# Обработчик RSS-фида для Zavtracast

Проект для загрузки RSS-фида, его категоризации, создания новых RSS-фидов для каждой категории и загрузки их в Yandex Object Storage.

## Предварительные требования

Перед началом работы убедитесь, что вы соответствуете следующим требованиям:
- У вас есть компьютер с `Linux/MacOS/Windows`.
- У вас установлена последняя версия `Python 3`.
- У вас есть аккаунт Yandex Object Storage с доступом к S3-бакету.
- У вас установлен `pip` (обычно поставляется вместе с Python).

## Установка обработчика RSS-фида

Для установки обработчика RSS-фида выполните следующие шаги:

1. Клонируйте репозиторий на локальную машину:

```bash
git clone https://github.com/yourusername/rss-feed-processor.git
cd rss-feed-processor
```

2. Cоздайте виртуальное окружение:

```bash
python3 -m venv zavtracast
```

3. Активируйте виртуальное окружение:

На MacOS и Linux:

```bash
source zavtracast/bin/activate
```
На Windows:

```bash
.\venv\Scripts\activate
```

Утановите необходимые пакеты:

```bash
pip install -r requirements.txt
```

## Конфигурация

Создайте файл config.json в корневой директории проекта со следующей структурой:
```json
{
  "ACCESS_KEY": "ваш_access_key",
  "SECRET_KEY": "ваш_secret_key",
  "BUCKET_NAME": "имя_вашего_бакета",
  "ENDPOINT_URL": "https://storage.yandexcloud.net",
  "zavtracast_patreon_feed": "Ссылка на ваш RSS в патреоне"
}
```

Замените ваш_access_key, ваш_secret_key, и имя_вашего_бакета на ваши фактические данные доступа к Yandex Object Storage.
zavtracast_patreon_feed замените на вашу rss ссылку из [Patreon](https://www.patreon.com/zavtracast/membership)

# Запуск проекта
Чтобы запустить проект, выполните:
```bash
python main.py
```
Это загрузит исходный RSS-фид, сгруппирует подкасты и загрузит новые фиды в ваш S3 бакет в Yandex Object Storage.

# Участие в проекте

Для внесения своего вклада в проект:

1. Сделайте форк репозитория.
2. Создайте новую ветку.
3. Внесите изменения.
4. Отправьте их на рассмотрение через Pull Request.
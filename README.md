# 概要
django＋postgreSQL+celery+rabbitMQの環境をdocker-composeで作成するサンプルプロジェクト。
本番想定の場合はさらにnginxを使用。

celeryワーカーは例として、
- 2コンテナ起動
- 1つのコンテナ内ではconcurrency=1

という構成。つまりインフラ構成としてワーカー数を2に固定している。

もし1つのコンテナ内で複数ワーカープロセスが走って良いなら（大抵それで良いはず）、ワーカーコンテナを一つにして、concurrency=Nにすれば良い。

# 環境
## 必須
- Docker
- Docker Compose

## 開発時の推奨
必須ではないが、インストールしておくと、IDEで補完が効くので便利。
- python 3.9.9
- pip

以下、 `bin/`から始まるコマンドは全てプロジェクト直下で実行すること。

# 開発時

## 環境変数の設定
開発用であれば以下をそのままコピーして `プロジェクトルート/api_server/.env.dev` として保存。
```dotenv
DJANGO_ENV=dev
DEBUG=1
SECRET_KEY=a
DJANGO_ALLOWED_HOSTS=*
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=api_db
SQL_USER=api_user
SQL_PASSWORD=pass123
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
RABBITMQ_USER=user
RABBITMQ_PASS=pass123
TIMEZONE=Asia/Tokyo
CELERY_WORKER_CONCURRENCY=1
CELERY_BROKER_URL=amqp://user:pass123@rabbit:5672/
```

## 事前準備（必須ではないが推奨）
ホストマシン側でもpython環境を整えておくと、IDEで開発するときに補完が効くので便利
```sh
# 以下実行前にvenvなどで仮想環境を作っておいた方が良い
# プロジェクト直下で実行する場合
pip install -r api_server/requirements.txt
```

## イメージビルド
```sh
bin/dev build
```

## 初回インストール（あるいはアップデート時）
初回、DB初期化、pipパッケージ追加、などした時に行う。
```shell
bin/dev up --build

# 初回、もしくはDB初期化した場合のみ
# django superuserの自動作成
bin/createsuperuser_dev
```

## 起動
```shell
bin/dev up
```

## 停止
Ctrl-C もしくは `bin/dev down`

## データ削除

### データのみ削除する場合
```shell
bin/prod up

# 別ターミナルで実行
bin/dev exec app python manage.py flush --no-input
```
その後、マイグレーション＆スーパーユーザー作成、もしくは「初回インストール」のステップを実行。

### DB自体作り直す場合
当該docker volumeを削除する。やり方は以下の本番想定時の「DB自体作り直す場合」を参照。

# 本番時
そのままdocker composeを使って本番稼働する場合。

## 環境変数の設定
開発用の例を参考にして `プロジェクトルート/api_server/.env.prod` を作成。

## 初回インストール（あるいはアップデート時に実行）
初回、もしくはDBに変更を加えるアップデート、DB初期化時などに実行
```shell
bin/prod up --build

# 別ターミナルで実行
# マイグレーション
bin/prod exec app python manage.py migrate --noinput
# 静的ファイルを集める（django admin用なのでアプリケーションに必須ではない）
bin/prod exec app python manage.py collectstatic --no-input --clear

# 初回もしくはDB初期化した場合のみ、スーパーユーザー作成
bin/prod exec app python manage.py createsuperuser
# プロンプトに従ってユーザー名・メールアドレス・パスワードを設定
# このユーザーでdjango adminにログイン可能。

# 停止
# Ctrl-C もしくは別ターミナルで以下実行
bin/prod down
```

### アップデート時（DB変更なし、全サービス再起動）
pipパッケージ追加、DBマイグレーション不要のアップデートなど
```shell
bin/prod up --build

# もし静的ファイルに更新がある場合は以下も実行
bin/prod exec app python manage.py collectstatic --no-input --clear

# 停止
# Ctrl-C もしくは別ターミナルで以下実行
bin/prod down
```

## 起動
本番想定実行時はバックグラウンドで実行する。
```shell
bin/prod up -d
```
全コンテナを `restart: always` にしているため、もしDocker自体を再起動した場合（ホストマシン再起動など）、これらのサービスもDocker起動時に自動起動する。
つまり、Docker自体をホストマシン起動時に自動起動設定にしておけば良い。

# 停止
```shell
bin/prod down
```

## データ削除
**本番環境では通常行わない。DBデータを全削除する。**

### データのみ削除する場合
```shell
bin/prod up

# 別ターミナルで実行
bin/prod exec app python manage.py flush --no-input
```
その後、再度マイグレーション＆スーパーユーザー作成をするか、「初回インストール」のステップを実行。

### DB自体作り直す場合
```shell
# もし起動中の場合は停止
bin/prod down

# dockerコマンドでdbコンテナ名あるいはIDを探す
docker ps -a
# dbコンテナを削除
docker rm [dbコンテナ名あるいはコンテナID]

# db用のdocker volume名を探す
docker volume ls
# 当該volume削除
docker volume rm [volume名]
```

その後、「初回インストール」のステップを実行して初期設定する。

※ 上記でうまくいかない場合、もし停止中のdockerコンテナ＆volumeを全て削除しても良いなら、以下で確実に削除可能。
```shell
# もし起動中の場合は停止
bin/prod down

# 停止中のコンテナを全て削除
docker container prune -y

# コンテナと関連付けられていないvolumeを全て削除
docker volume prune -y
```
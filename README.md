# f5-nginx-ingress-controller-doc-scraping

## 概要

https://docs.nginx.com/nginx-ingress-controller/ のドキュメントをjrnote.ymlに基づいてスクレイピングするプロジェクトです。

## build & run

仮想環境の作成

```bash
python -m venv .venv
```

仮想環境の有効化

```bash
source .venv/bin/activate
```

依存関係ライブラリのインストール

```bash
pip install -r requirements.txt
```

## スクレイピングの実行

### https://docs.nginx.com/nginx-ingress-controller/ ページのスクレイプ実行

overviewページのスクレイプ実行

```bash
mkdir csv
cp jrnote.yml jrnote.yml.bak
cp jrnote.nginx-ingress.overview.yml jrnote.yml
python jrnote/jrnote.py > csv/nginx-ingress-controller-docs-overview.csv
```

installationのスクレイプ実行

```bash
cp jrnote.nginx-ingress.installation.yml jrnote.yml
python jrnote/jrnote.py > csv/nginx-ingress-controller-docs-installation.csv
```

technical specificationsのスクレイプ実行

```bash
cp jrnote.nginx-ingress.technical-specifications.yml jrnote.yml
python jrnote/jrnote.py > csv/nginx-ingress-controller-docs-technical-specifications.csv
```

configurationのスクレイプ実行

```bash
cp jrnote.nginx-ingress.configuration.yml jrnote.yml
python jrnote/jrnote.py > csv/nginx-ingress-controller-docs-configuration.csv
```

logging and monitoringのスクレイプ実行

```bash
cp jrnote.nginx-ingress.logging-monitoring.yml jrnote.yml
python jrnote/jrnote.py > csv/nginx-ingress-controller-docs-logging-monitoring.csv
```

troubleshootingのスクレイプ実行

```bash
cp jrnote.nginx-ingress.troubleshooting.yml jrnote.yml
python jrnote/jrnote.py > csv/nginx-ingress-controller-docs-troubleshooting.csv
```


tutorialsのスクレイプ実行

```bash
cp jrnote.nginx-ingress.tutorials.yml jrnote.yml
python jrnote/jrnote.py > csv/nginx-ingress-controller-docs-tutorials.csv
```

communityのスクレイプ実行

```bash
cp jrnote.nginx-ingress.community-contributing.yml jrnote.yml
python jrnote/jrnote.py > csv/nginx-ingress-controller-docs-community-contributing.csv
```

changelogのスクレイプ実行

```bash
cp jrnote.nginx-ingress.changelog.yml jrnote.yml
python jrnote/jrnote.py > csv/nginx-ingress-controller-docs-changelog.csv
```

## 設定ファイル

`jrnote.yml` を編集することで、スクレイピング対象のURLやページ構造を設定できます。

```yaml
setting:
 https.proxy:  # プロキシ設定（必要な場合）
 scraping_url: https://docs.nginx.com/nginx-ingress-controller/
 deepl_enable: false  # DeepL翻訳を使用する場合はtrue
 deepl_apikey: "todo"  # DeepL APIキー

jrnote:
- overview  # スクレイピング対象の項目名

overview_scraping:
 url: https://docs.nginx.com/nginx-ingress-controller/overview/
 section: //h1  # セクションのXPath
 componet: ./../following-sibling::main/h2  # コンポーネントのXPath
```

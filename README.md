# No-IP 定期更新 自動化ツール

## Summary


## Description

### メールフック部 [gas]



### バックエンド部 [backend]


## Dependency

### メールフック部 [gas]

- Google Apps Script
- Gmail

### バックエンド部 [backend]

- Google Container Registry
- Google Cloud Run
- ChromeDriver
    - https://chromedriver.chromium.org/
- Python 3.7
    - Python パッケージ
        - Flask
        - Selenium
        - Gunicorn
        - その他については `/backend/requirements.txt` を参照


## Setup/Usage

### メールフック部 [gas]



### バックエンド部 [backend]

gcloud コマンドが使えることを前提とします。
`[PROJECT-ID]` と表記している箇所はご自分のGCPプロジェクト名に適宜読み替えて下さい。


#### Dockerイメージのビルド～GCRへのイメージPush

`$ gcloud builds submit --tag gcr.io/[PROJECT-ID]/noip-autoupdater` --project [PROJECT-iD]


#### Cloud Run へのデプロイ

`$ gcloud beta run deploy --image gcr.io/[PROJECT-ID]/noip-autoupdate` --project [PROJECT-iD]


#### 課金対策

Cloud Run へのデプロイが完了し、正常動作を確認したら、GCRにPushしたイメージをすべて削除します。


## References

https://cloud.google.com/run/docs/quickstarts/build-and-deploy


## License

[MIT](LICENSE.md)


## Author

[tissueMO](https://github.com/tissueMO)

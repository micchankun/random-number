# Chromebook Linux での準備

1. AQUEST公式の AquesTalk10 Linux を入手します。
2. 評価版で動作確認する場合は、評価目的の範囲で使ってください。継続利用・製品開発にはライセンスが必要です。
3. Linux版の `.so` をLinux環境に置きます。
4. 次のようにパスを指定して起動します。

```bash
cd yukkuri-local-server
export AQUESTALK_LIB="/ここに/AquesTalk10の.soへのパス"
python3 server.py
```

起動後、ブラウザから `http://127.0.0.1:8765/health` を開いて、`engine` が `true` ならエンジンを読み込めています。

## 重要

AquesTalk10の評価版には音韻制限があります。製品版ライブラリやライセンスキーはこのリポジトリへ置かないでください。AQUEST公式のライセンス条件に従ってください。

## 現在のサーバー仕様

- `POST /speak`
- JSON: `{ "text": "いち に さん よん" }`
- 戻り値: WAV
- 待受: `127.0.0.1:8765`
- 公開インターネットからアクセスできないlocalhost専用

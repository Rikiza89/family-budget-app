# 家族で使える家計簿アプリ

Django で作られたモバイルファーストの家計管理システムです。収入・支出・貯蓄を記録し、AI によるファイナンシャルアドバイスを家族全員で共有できます。

**言語 / Language / Lingua:**
[English](README.md) | **日本語** | [Italiano](README.it.md)

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Django](https://img.shields.io/badge/django-5.2+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 機能一覧

### 基本機能
- **ダッシュボード** — 月次収支サマリーとグラフ
- **クイック入力** — 2タップで取引を登録（モバイル最適化）
- **2種類の貯蓄**
  - *現金貯蓄* — 純粋な積立・貯金
  - *保険型積立* — 支出と長期貯蓄の両方に計上
- **レシート写真** — 取引にレシート画像を添付
- **予算管理** — カテゴリーごとの月次予算と色分け進捗バー（緑・黄・赤）
- **支出グラフ** — 6ヶ月の収支トレンド
- **AI 家計分析** — Gemini AI があなたの家計を分析し、具体的なアドバイスを提供

### 定期取引
- 家賃・給料・保険料・サブスクなどのテンプレート作成
- 頻度: 毎日 / 毎週 / 毎月 / 毎年
- すべての期日分をワンクリックで一括記録
- テンプレートの有効/無効を個別に切り替え可能

### メール通知
- 指定日数以上記録がない場合にリマインダーメール送信
- 家族単位で設定
- 複数の通知先メールアドレスに対応

### 将来予測
- 最大60年先の貯蓄推移を予測
- 直近12ヶ月の実績データをもとに計算
- 現金貯蓄と保険積立を分けて表示
- スピナー操作（マウスホイール・スワイプ）で予測期間を変更

### 家族共有
- 複数メンバーが同じ家計簿を共有
- 期限付き招待リンク（有効期限7日間）でメンバーを追加
- 各取引に登録者を表示

### その他
- **支払方法** — 現金、クレジットカード、QR決済、銀行振込、ICカードなど
- **カスタムカテゴリー** — カテゴリーの追加・編集・削除
- **データエクスポート** — CSV形式でダウンロード
- **多通貨対応** — JPY・USD・EUR・GBP・CNY・KRW・SGD・AUD（家族単位で切り替え）
- **多言語対応** — 日本語 / 英語 / イタリア語（Cookie保存、いつでも切り替え可）
- **個人 AI APIキー** — 設定画面から個人の Gemini API キーを登録可能
- **PWA対応** — スマートフォンのホーム画面にインストール可能

---

## クイックスタート

### 動作要件
- Python 3.11+
- pip

### インストール手順

```bash
# 1. リポジトリをクローン
git clone https://github.com/Rikiza89/family-budget-app.git
cd family-budget-app

# 2. 仮想環境を作成・有効化
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate

# 3. 依存パッケージをインストール
pip install -r requirements.txt

# 4. マイグレーションを実行（テーブル作成 + 通貨データの初期投入）
python manage.py migrate

# 5. スーパーユーザーを作成（任意、/admin アクセス用）
python manage.py createsuperuser

# 6. 開発サーバーを起動
python manage.py runserver
```

ブラウザで `http://localhost:8000` を開いてください。

> **既存のデータベースをお使いの場合（マイグレーション履歴がない場合）:**
> ```bash
> python manage.py migrate --fake 0001
> python manage.py migrate
> ```

---

## プロジェクト構成

```
family-budget-app/
├── budget/
│   ├── models.py                  # データモデル
│   ├── views.py                   # ダッシュボード・AI分析・エクスポート
│   ├── setup_views.py             # 設定・カテゴリー・通貨・招待
│   ├── auth_views.py              # ログイン・登録・プロフィール設定
│   ├── forms.py                   # Django フォーム
│   ├── urls.py                    # URL ルーティング
│   ├── admin.py                   # Django 管理画面設定
│   ├── migrations/                # マイグレーションファイル（通貨初期投入含む）
│   ├── management/commands/
│   │   └── send_log_reminders.py  # メール通知 cron コマンド
│   ├── templatetags/
│   │   └── translation_tags.py    # 動的文字列用 |translate フィルター
│   └── templates/budget/          # HTML テンプレート
├── family_budget/
│   ├── settings.py
│   └── urls.py
├── locale/
│   ├── en/LC_MESSAGES/            # 英語翻訳（.po + コンパイル済み .mo）
│   └── it/LC_MESSAGES/            # イタリア語翻訳（.po + コンパイル済み .mo）
├── requirements.txt
└── manage.py
```

---

## 技術スタック

| レイヤー | 技術 |
|---|---|
| バックエンド | Django 5.2+ |
| フロントエンド | HTML5、Tailwind CSS（CDN）、Vanilla JS |
| データベース | SQLite（デフォルト）/ PostgreSQL 対応 |
| グラフ | Chart.js |
| AI | Google Gemini API（`google-generativeai`）|
| 画像処理 | Pillow |
| 日付処理 | python-dateutil |
| 国際化 | Django i18n（JA / EN / IT）|

---

## データモデル

| モデル | 役割 |
|---|---|
| `Family` | 家族グループ（通貨設定を保持）|
| `FamilyMember` | Django `User` と `Family` を紐付け・個人 Gemini API キーを保存 |
| `Transaction` | 収入または支出の記録 |
| `CashSaving` | 現金貯蓄の記録 |
| `Category` | ユーザー定義カテゴリー（`is_insurance_saving=True` で保険型扱い）|
| `PaymentMethod` | 現金、カードなどの支払方法 |
| `Budget` | カテゴリーごとの月次予算上限 |
| `RecurringTemplate` | 定期取引のテンプレート |
| `Currency` | 通貨コード・記号・円換算レート |
| `EmailNotificationSettings` | 家族単位のメールリマインダー設定 |

### 貯蓄の仕組み

**現金貯蓄（`CashSaving`）:** 使えるお金が減る。長期貯蓄として計上。

**保険型積立（`is_insurance_saving=True` の `Transaction`）:** 月次支出にも計上され、かつ長期貯蓄にも加算される。

---

## 設定

### AI（Gemini）

共有 API キーを `.env` または `settings.py` に設定：

```python
GEMINI_API_KEY = 'AIzaSy...'
```

ユーザーは **設定 → AI API キー** から個人の API キーを設定可能です。個人キーが優先されます。

### メール通知

```python
# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'   # Gmail アプリパスワード
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
```

Cron ジョブでリマインダーコマンドを毎日実行：

```bash
# /etc/cron.d/budget-reminders
0 9 * * * youruser /path/to/venv/bin/python /path/to/manage.py send_log_reminders
```

### 本番環境チェックリスト

```python
# settings.py
DEBUG = False
SECRET_KEY = os.environ['SECRET_KEY']
ALLOWED_HOSTS = ['your-domain.com']
CSRF_TRUSTED_ORIGINS = ['https://your-domain.com']
```

---

## 翻訳

翻訳ソースは `locale/<lang>/LC_MESSAGES/django.po` にあります。
`.po` ファイルを編集した後はコンパイルが必要です：

```bash
python manage.py compilemessages
```

コンパイル済みの `.mo` ファイルはリポジトリにコミット済みなので、通常は上記コマンドを実行しなくても動作します。

---

## トラブルシューティング

| 問題 | 解決方法 |
|---|---|
| マイグレーションエラー | `python manage.py migrate --fake 0001 && python manage.py migrate` |
| 通貨ドロップダウンが空 | `python manage.py migrate` — 0003 マイグレーションが通貨データを自動投入します |
| 画像アップロードエラー | `pip install pillow && mkdir -p media/receipts` |
| 翻訳が反映されない | `python manage.py compilemessages` |
| メールが届かない | SMTP 設定を確認。Gmail は 2段階認証 + アプリパスワードが必要です |

---

## ライセンス

MIT ライセンス — 詳細は [LICENSE](LICENSE) をご覧ください。

## バグ報告・機能要望

[GitHub Issues](https://github.com/Rikiza89/family-budget-app/issues) からお気軽にどうぞ。

---

家族で一緒に家計管理を楽しみましょう ❤️

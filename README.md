# 💰 家族向け家計簿アプリ

Djangoで作られたモバイルファースト家計簿管理システム。家族で収支・貯蓄を共有管理できます。

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/django-4.2+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## ✨ 主な機能

### 基本機能
- 📊 **ダッシュボード** - 月次収支サマリーとグラフ表示
- 💸 **クイック入力** - 2タップで記録完了（モバイル最適化）
- 💰 **2種類の貯蓄管理**
  - 現金貯蓄（貯金）- 純粋な積立
  - 保険型積立（保険）- 支出と貯蓄の両方に計上
- 📱 **レシート撮影** - 取引に写真を添付可能
- 🎯 **予算管理** - カテゴリー別に予算設定・追跡・編集
  - 色分け表示（緑=正常、黄=80%超、赤=超過）
- 📈 **グラフ分析** - 過去6ヶ月の収支推移

### 🔄 定期取引（新機能）
- **定期取引テンプレート作成** - 家賃、給料、保険など
- **頻度設定** - 毎日/毎週/毎月/毎年
- **一括記録ボタン** - 全ての定期取引をワンクリックで記録
- **有効/無効切り替え** - 不要な期間は停止可能

### 📧 メール通知（新機能）
- **記録忘れリマインダー** - N日間記録がない場合に自動メール送信
- **通知設定** - 家族ごとにカスタマイズ可能
- **複数メールアドレス対応** - 家族メンバー全員に通知

### 📈 将来予測（新機能）
- **最大60年先の予測** - マウスホイール/スワイプで簡単変更
- **現金貯蓄予測** - 過去実績から自動計算
- **保険積立予測** - 長期資産形成を可視化
- **総貯蓄グラフ** - 将来の資産推移を一目で確認

### 家族共有機能
- 👨‍👩‍👧‍👦 **家族アカウント** - 複数メンバーで1つの家計簿を共有
- 🔗 **招待システム** - 招待リンクで簡単にメンバー追加
- 👤 **メンバー管理** - 誰が何を記録したか表示

### その他
- 💳 **支払方法管理** - 現金・クレカ・QR決済など
- 📂 **カテゴリー管理** - 自由にカテゴリー追加・編集
- 📥 **データエクスポート** - CSVで取引データをダウンロード
- 🌐 **多言語対応** - 日本語/イタリア語（切り替え可能）

## 🚀 クイックスタート

### 必要環境
- Python 3.8以上
- pip

### インストール手順

```bash
# 1. リポジトリをクローン
git clone https://github.com/Rikiza89/family-budget-app.git
cd family-budget-app

# 2. 仮想環境作成
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 依存パッケージインストール
pip install -r requirements.txt

# 4. データベース初期化
python manage.py migrate

# 5. スーパーユーザー作成
python manage.py createsuperuser

# 6. 開発サーバー起動
python manage.py runserver
```

ブラウザで `http://localhost:8000` にアクセス

## 📱 使い方

### 初回セットアップ
1. **新規登録** - ユーザー名・パスワードを入力
2. **プロフィール設定** - 家族名とニックネームを入力
3. **カテゴリー設定** - デフォルトカテゴリーを使用
4. **支払方法設定** - デフォルト支払方法を使用
5. **完了！** - ダッシュボードで使い始められます

### 定期取引の使い方
1. メニュー → 「定期取引」
2. 「追加」をタップ
3. 金額・カテゴリー・頻度を設定
4. 毎月、「すべての定期取引を一括記録」ボタンで簡単登録

### メール通知の設定
1. メニュー → 「メール通知」
2. 通知を有効化
3. 何日間記録がない場合に通知するか設定
4. 通知先メールアドレスを入力

### 将来予測の確認
1. メニュー → 「将来予測」
2. 予測期間をスピナーで調整（1〜60年）
3. 現金貯蓄・保険積立の将来推移を確認

### 家族メンバーを招待
1. メニュー → 設定 → メンバー管理
2. 「新規作成」をタップ
3. 招待リンクをコピー
4. LINEやメールで家族に送信

### 貯蓄の記録方法

**現金貯蓄（給料からの積立など）**
- メニュー → 「貯金を登録」から入力

**保険型積立（生命保険など）**
- 「支出を記録」から入力
- カテゴリーで「保険（積立）」を選択
- → 支出としても貯蓄としても計上されます

## 📁 プロジェクト構成

```
family_budget/
├── budget/
│   ├── models.py              # データモデル（Transaction, CashSaving, RecurringTemplate, etc.）
│   ├── views.py               # ビュー（dashboard, forecast, etc.）
│   ├── forms.py               # フォーム定義
│   ├── auth_views.py          # 認証関連
│   ├── setup_views.py         # 設定・管理画面
│   ├── urls.py                # URLルーティング
│   ├── admin.py               # Django管理画面
│   ├── management/
│   │   └── commands/
│   │       └── send_log_reminders.py  # メール通知コマンド
│   └── templates/             # HTMLテンプレート
├── locale/                    # 翻訳ファイル
│   ├── it/                   # イタリア語
│   └── ja/                   # 日本語
├── media/                    # アップロード画像
├── requirements.txt
└── manage.py
```

## 🎨 技術スタック

- **Backend**: Django 4.2+
- **Frontend**: HTML5, Tailwind CSS (CDN), Vanilla JavaScript
- **Database**: SQLite (デフォルト) / PostgreSQL対応
- **Charts**: Chart.js
- **画像処理**: Pillow
- **日付処理**: python-dateutil
- **国際化**: Django i18n (日本語/イタリア語)

## 📊 データモデル

### 重要な特徴

**貯蓄の2つのタイプ**

1. **CashSaving（現金貯蓄）**
   - 給料からの積立、ボーナス貯金
   - 使えるお金が減る
   - 長期貯蓄に計上

2. **Transaction（保険型積立）**
   - `is_insurance_saving=True` のカテゴリー
   - 月次支出に計上
   - 同時に長期貯蓄にも計上

**定期取引**

3. **RecurringTemplate**
   - 定期的な収支のテンプレート
   - 毎日/毎週/毎月/毎年の頻度設定
   - 一括記録機能で簡単管理

## 🔐 セキュリティ

開発環境用設定です。本番環境では以下を設定してください：

```python
# settings.py
DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY')
ALLOWED_HOSTS = ['your-domain.com']
CSRF_TRUSTED_ORIGINS = ['https://your-domain.com']
```

## 📦 依存パッケージ

```
Django
Pillow
python-dateutil
```

PostgreSQL使用時は追加：
```
psycopg2-binary
```

## 📧 メール通知の設定

### SMTP設定（settings.py）

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'  # Gmailアプリパスワード
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
```

### Cronジョブ設定（サーバー）

```bash
# 毎日朝9時に実行
0 9 * * * cd /path/to/project && python manage.py send_log_reminders
```

または cron.d に追加：
```bash
# /etc/cron.d/budget-reminders
0 9 * * * youruser cd /path/to/project && /path/to/venv/bin/python manage.py send_log_reminders
```

## 📄 デモサイトはこちら

デモサイトを公開しています。 [サイトリンク](https://mydemoapplication.pythonanywhere.com) 
是非一度お試しください。

※ストレージ管理の為定期的にデータを削除しますのでご了承ください。
本番使用にご興味ある方はぜひ連絡ください。サーバー運用に協力します。

## 🐛 トラブルシューティング

**マイグレーションエラー**
```bash
python manage.py makemigrations budget
python manage.py migrate
```

**画像アップロードエラー**
```bash
mkdir -p media/receipts
pip install pillow
```

**メール送信エラー**
- Gmailの場合：アプリパスワードを使用
- 2段階認証を有効化してアプリパスワードを生成

**翻訳が表示されない**
```bash
python manage.py compilemessages
python manage.py runserver
```

## 🤝 コントリビューション

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 ライセンス

MIT License - 詳細は [LICENSE](LICENSE) ファイルを参照

## 📞 サポート

問題が発生した場合は [Issues](https://github.com/Rikiza89/family-budget-app/issues) で報告してください。

## 🎯 今後の予定

- [ ] PWA対応（オフライン利用）
- [ ] LINE通知連携
- [ ] 銀行API連携（自動取込）
- [ ] 複数通貨対応
- [ ] AI支出分析

## 🙏 謝辞

このプロジェクトは以下を使用しています：
- [Django](https://www.djangoproject.com/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Chart.js](https://www.chartjs.org/)

---

Made with ❤️ for families managing their budgets together

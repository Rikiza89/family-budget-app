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
- 🎯 **予算管理** - カテゴリー別に予算設定・追跡
- 📈 **グラフ分析** - 過去6ヶ月の収支推移

### 家族共有機能
- 👨‍👩‍👧‍👦 **家族アカウント** - 複数メンバーで1つの家計簿を共有
- 🔗 **招待システム** - 招待リンクで簡単にメンバー追加
- 👤 **メンバー管理** - 誰が何を記録したか表示

### その他
- 💳 **支払方法管理** - 現金・クレカ・QR決済など
- 📂 **カテゴリー管理** - 自由にカテゴリー追加・編集
- 📥 **データエクスポート** - CSVで取引データをダウンロード
- 📅 **固定費対応** - 家賃・保険など定期支払いをマーク

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

### 支出を記録

1. 右下の「+」ボタンをタップ
2. 金額を入力（クイック金額ボタンも使用可）
3. カテゴリーを選択
4. 「保存」

### 家族メンバーを招待

1. メニュー → 設定 → メンバー管理
2. 「新規作成」をタップ
3. 招待リンクをコピー
4. LINEやメールで家族に送信
5. 相手がリンクからアカウント作成 → 自動参加

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
├── budget/              # メインアプリ
│   ├── models.py        # データモデル
│   ├── views.py         # ビュー（ダッシュボード等）
│   ├── forms.py         # フォーム定義
│   ├── auth_views.py    # 認証関連
│   ├── setup_views.py   # 設定・管理画面
│   ├── urls.py          # URLルーティング
│   ├── admin.py         # Django管理画面
│   └── templates/       # HTMLテンプレート
├── family_budget/       # プロジェクト設定
│   ├── settings.py
│   └── urls.py
├── media/               # アップロード画像
├── requirements.txt     # 依存パッケージ
└── manage.py
```

## 🎨 技術スタック

- **Backend**: Django 4.2+
- **Frontend**: HTML5, Tailwind CSS (CDN), Vanilla JavaScript
- **Database**: SQLite (デフォルト) / PostgreSQL対応
- **Charts**: Chart.js
- **画像処理**: Pillow

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
```

PostgreSQL使用時は追加：
```
psycopg2-binary
```

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

**招待リンクが動かない**
- 招待コードがUUID形式か確認
- 有効期限（7日）を確認
- データベースに `FamilyInvite` モデルがあるか確認

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
- [ ] 月次レポート自動生成
- [ ] LINE通知連携
- [ ] 銀行API連携（自動取込）
- [ ] 複数通貨対応

## 🙏 謝辞

このプロジェクトは以下を使用しています：
- [Django](https://www.djangoproject.com/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Chart.js](https://www.chartjs.org/)

---

Made with ❤️ for families managing their budgets together
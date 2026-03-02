# 【個人開発】家族で使える家計簿Webアプリを無料でDjangoで作った話 〜AI分析・多言語・多通貨対応まで〜

## はじめに — なぜ作ったのか

「今月も赤字だ...」「お金、どこに消えたんだろう...」

そんな経験、ありませんか？私もです。市販の家計簿アプリはたくさんあるけど、**自分が本当に欲しい機能**が揃っているものってなかなかないんですよね。

それなら、**作っちゃえ！** ということで、Djangoで家計簿アプリを自作しました。しかも**完全無料**で動く環境を目指して。

この記事では、**PythonAnywhereの無料プラン**で動かしている家計簿アプリの開発ストーリーと、実装した機能について紹介します。コード職人というより「こんな機能があったらいいな」を形にした話です。

> ⚠️ **デモサイトについての注意**
> デモサイト（https://mydemoapplication.pythonanywhere.com）は古いバージョンです。
> **AI分析の多言語対応・個人APIキー設定・多通貨機能**など最新機能を試したい方は、
> GitHubからクローンしてローカルで動かしてください（手順は記事末尾に記載）。

---

## 🎯 このアプリのコンセプト

### 誰のため？
- 家族で家計を管理したい人
- スマホでサクッと記録したい人
- 貯蓄と支出を分けて管理したい人
- **お金をかけずに**家計管理を始めたい人
- 海外在住で複数通貨を使っている人

### 何ができる？（2025年最新版）

| 機能 | 詳細 |
|---|---|
| ✅ **2タップで記録** | モバイルファースト設計 |
| ✅ **家族で共有** | 招待リンクで簡単参加 |
| ✅ **AI分析** | Gemini APIで支出パターンを分析 |
| ✅ **個人AIキー** | ユーザーごとに独自のGemini APIキーを設定可能 |
| ✅ **将来予測** | 最大60年先の貯蓄推移を表示 |
| ✅ **定期取引** | 家賃・給料を一括登録 |
| ✅ **多言語対応** | 日本語・イタリア語・英語（完全実装済み） |
| ✅ **多通貨対応** | JPY・USD・EUR・GBP・CNY・KRW・SGD・AUD |
| ✅ **PWA対応** | ホーム画面に追加してネイティブアプリ風に |

そして何より、**完全無料で使える**！

> 📸 **[画像: アプリのダッシュボード画面 — 月次収支グラフ・予算状況・クイック入力ボタン]**
> ![ダッシュボード](./docs/images/dashboard.png)

---

## 🌐 なぜWebアプリなのか？ — これが最強の理由

ここで声を大にして言いたいことがあります。

**Webアプリケーション、最高です。**

### 📱 ワンソース、マルチデバイス

ネイティブアプリを作ろうとすると、こうなります：

- iOS用にSwift/Objective-Cで開発 → App Store審査
- Android用にKotlin/Javaで開発 → Google Play審査
- Windows用に...？
- Mac用に...？

**コードが5倍、工数が5倍、メンテナンスも5倍。**

一方、Webアプリなら？

```
ブラウザがあれば、どこでも動く。以上。
```

**たった1つのコードベース**で、iPhone・Android・Windows・Mac・Linux・タブレット、全部カバー。

| 比較項目 | ネイティブアプリ | Webアプリ（本作） |
|---|---|---|
| 開発期間 | 3ヶ月〜 | **3週間** |
| 対応デバイス | iOS or Android | **全OS** |
| 更新反映 | 審査待ち（1週間〜） | **即時** |
| 初期コスト | $100〜 | **$0** |
| ランニングコスト | $99/年〜 | **$0**（無料プラン） |
| メンテナンス工数 | 高（OS別対応） | **低**（ワンソース） |

**コスパ、圧勝。**

### 🚀 開発スピードが違う

Webアプリのバージョンアップ：

```bash
git push → デプロイ → 即反映
```

**5分で終わる。** 緊急のバグ修正も深夜2時にサッと対応できます（やったことある笑）。

### 🎯 ユーザー視点でも便利

「アプリダウンロードしてください」と言われると、正直面倒ですよね？インストール→権限許可→アカウント作成……疲れます。

Webアプリなら：
1. URLをタップ
2. 使える

**2ステップ。** しかもPWA化すればホーム画面に追加してネイティブアプリ風にも使えます。

### 💡 個人開発者にとっての現実

正直な話、個人開発者がネイティブアプリを作るのはハードルが高いです。Webアプリなら：

- **Python/Djangoだけ**でバックエンド・フロントエンド両方OK
- **無料のエディタ**で開発可能
- **審査なし**で即公開
- **PythonAnywhereの無料プラン**で運用可能

**個人開発で「アイデアを形にする」なら、Webアプリ一択でしょう。**

---

## 🚀 技術スタック — シンプルイズベスト

```
Backend:  Django 5.2+
Frontend: Tailwind CSS (CDN) + Vanilla JavaScript
Database: SQLite
Hosting:  PythonAnywhere (Free Tier)
AI:       Google Gemini API (gemini-2.5-flash)
Charts:   Chart.js
i18n:     Django i18n (JA / EN / IT)
```

なぜこの構成？答えは簡単：**無料で動くから**です（笑）

> 📸 **[画像: 技術スタックの構成図 — Django→SQLite、Tailwind、Gemini API、Chart.jsの関係]**
> ![技術スタック](./docs/images/tech-stack.png)

---

## 💡 実装した機能たち

### 1. クイック入力 — スマホで2タップ記録

家計簿アプリの最大の敵は「**記録の面倒くささ**」です。

だから、このアプリは**2タップで完了**を目指しました：

1. 金額をタップ（よく使う金額ボタンあり）
2. カテゴリーをタップ

これだけ。日付も支払方法もデフォルト値で自動入力。レシート写真も撮れるけど**任意**。とにかく手軽さ優先です。

> 📸 **[画像: クイック入力画面 — 金額入力パッド・クイックボタン（+1000, +5000）・カテゴリー選択]**
> ![クイック入力](./docs/images/quick-entry.png)

```python
@login_required
def quick_add_transaction(request):
    if request.method == 'POST':
        form = QuickTransactionForm(request.POST, family=family)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.family = family
            transaction.member = member
            transaction.save()
            return redirect('dashboard')
```

### 2. 家族共有機能 — 招待リンクで簡単参加

「夫婦で家計管理したい」「親の支出も見守りたい」

そんなニーズに応えて、**招待リンク機能**を実装しました。UUIDで生成したリンクをLINEやメールで送るだけ。有効期限は7日間、使い切りです。

> 📸 **[画像: メンバー管理画面 — 招待リンクのコピーボタン・メンバー一覧]**
> ![メンバー管理](./docs/images/member-management.png)

```python
class FamilyInvite(models.Model):
    code = models.UUIDField(default=uuid.uuid4, unique=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
```

最初はシンプルな数字コードにしようとしたけど、セキュリティ的にUUIDの方が安心。「コピー」ボタンは必須でした（笑）

### 3. 貯蓄の2つのタイプ — ここがポイント！

これが個人的に一番こだわった部分。貯蓄には**2種類**あります：

#### 📌 現金貯蓄（純粋な積立）
給料から毎月3万円を別口座へ移すやつ。「使えるお金が減る」かつ「貯蓄が増える」。

#### 📌 保険型積立（保険・学資保険）
生命保険や学資保険は「支出」だけど、実は「貯蓄」でもある。だから**両方に計上**します。

> 📸 **[画像: 貯蓄サマリー画面 — 現金貯蓄・保険積立・総貯蓄額の円グラフ]**
> ![貯蓄サマリー](./docs/images/savings-summary.png)

```python
def is_insurance_saving(self):
    return (self.transaction_type == 'expense' and
            self.category.is_insurance_saving)
```

この機能のおかげで、「今月の支出が多い！」と思っても、保険料の分は将来の資産になっていることが**一目でわかる**んです。

### 4. AI支出分析 — Gemini APIで賢く分析（多言語対応）

ここが**目玉機能**！

過去1〜12ヶ月の支出データをGemini API（gemini-2.5-flash）に投げて、具体的なアドバイスをもらいます。

**分析タイプは5種類：**

| タイプ | 内容 |
|---|---|
| 総合支出分析 | 現状・改善提案・節約ターゲットを総合評価 |
| 貯蓄最適化 | 貯蓄率の評価・改善方法・将来見通し |
| 予算計画アドバイス | 理想的な予算配分と月次提案 |
| カテゴリー深掘り | 特定カテゴリーの詳細分析 |
| カスタム質問 | 家計について何でも聞ける |

> 📸 **[画像: AI分析オプション画面 — 分析期間選択・分析タイプ選択・開始ボタン]**
> ![AI分析オプション](./docs/images/ai-options.png)

**ポイント（2025年最新版）：AIの回答言語がUIに連動します！**

英語に切り替えていれば英語で、イタリア語なら Italian で回答。`get_language()` を使って動的に切り替えています：

```python
from django.utils.translation import get_language

_lang_names = {'ja': 'Japanese', 'en': 'English', 'it': 'Italian'}
_response_lang = _lang_names.get(get_language() or 'ja', 'Japanese')

prompt = f"""
You are an experienced financial planner.
Based on the following data, provide actionable advice in {_response_lang}.
...
"""
```

> 📸 **[画像: AI分析結果画面 — 総収入・総支出・貯蓄率カード + AIのMarkdownアドバイス本文]**
> ![AI分析結果](./docs/images/ai-result.png)

実際のAI回答例：

> 「コンビニ利用が月12回・¥18,000です。週2回に減らすだけで月¥9,000の節約になります。買う前に『本当に必要？』と5秒考える習慣をつけましょう。」

**これが結構的確**で、自分でも「なるほど...」ってなります（笑）

#### 💡 さらに：個人Gemini APIキーの設定

2025年版の新機能として、**ユーザーごとに独自のGemini APIキーを設定**できます。

> 📸 **[画像: 設定画面のAI APIキーセクション — パスワード入力欄・保存ボタン・「個人キー設定済み」表示]**
> ![APIキー設定](./docs/images/api-key-settings.png)

```python
# FamilyMemberモデル
gemini_api_key = models.CharField(max_length=200, blank=True, default='')

# ビュー側 — 個人キー優先、なければ共通キー
api_key = member.gemini_api_key.strip() or settings.GEMINI_API_KEY
genai.configure(api_key=api_key)
```

共有サーバーで動かす場合でも、各ユーザーが自分のAPIキーを使えるので**レート制限の心配なし**。

### 5. 将来予測 — 60年後の資産は？

「このペースで貯金を続けたら、30年後いくらになる？」

気になりますよね？だから**将来予測機能**を実装しました。過去12ヶ月の実績から月平均を計算し、最大**60年先**まで予測します。

> 📸 **[画像: 将来予測画面 — 年数スピナー・Chart.jsの折れ線グラフ（現金貯蓄・保険積立・総貯蓄の3本線）]**
> ![将来予測](./docs/images/forecast.png)

```python
for i in range(1, forecast_years * 12 + 1):
    cumulative_cash += avg_cash_saving
    cumulative_insurance += avg_insurance
    # 月次データとして蓄積
```

マウスホイールでスピナー操作、スマホではスワイプ対応。グラフで見ると「定年までに結構貯まるな...」とか「やばい、全然足りない！」とか**現実が見えてきます**。

### 6. 定期取引 — 一括登録で楽ちん

毎月の固定費（家賃、保険、給料など）を**テンプレート化**。

> 📸 **[画像: 定期取引リスト画面 — 各テンプレートの有効/無効トグル・「⚡一括記録」ボタン]**
> ![定期取引](./docs/images/recurring.png)

毎月1日に「⚡すべての定期取引を一括記録」をポチッ。これだけで全部登録完了。

```python
for template in templates:
    if template.should_generate():  # 今日記録すべき？
        template.generate_transaction()
        generated_count += 1
```

**重複チェックも自動**なので、間違えて2回押しても安心。地味に便利な機能です。

### 7. 多通貨対応 — 海外在住者にも嬉しい（✅完成！）

以前は「現在作業中」だった多通貨対応、**ついに完成しました！**

対応通貨：JPY / USD / EUR / GBP / CNY / KRW / SGD / AUD

マイグレーションで自動的に初期データが投入されます：

> 📸 **[画像: 通貨設定画面 — ドロップダウンに8通貨が並び、現在の通貨が「$ US Dollar」と表示]**
> ![通貨設定](./docs/images/currency-settings.png)

```python
# 0003_seed_currencies.py — migrate実行時に自動投入
currencies = [
    {'code': 'JPY', 'name': 'Japanese Yen',      'symbol': '¥', 'exchange_rate': 1.0},
    {'code': 'USD', 'name': 'US Dollar',          'symbol': '$', 'exchange_rate': 0.0065},
    {'code': 'EUR', 'name': 'Euro',               'symbol': '€', 'exchange_rate': 0.0060},
    {'code': 'GBP', 'name': 'British Pound',      'symbol': '£', 'exchange_rate': 0.0053},
    # + CNY, KRW, SGD, AUD
]
for c in currencies:
    Currency.objects.get_or_create(code=c['code'], defaults=c)
```

`get_or_create` を使っているので、`migrate` を再実行しても重複しません。

### 8. メール通知 — 記録忘れ防止

「あれ、もう1週間記録してない...」を防ぐ**リマインダー機能**。

> 📸 **[画像: メール通知設定画面 — 日数入力・メールアドレス複数行入力欄・通知有効チェック]**
> ![メール通知](./docs/images/email-settings.png)

```python
# python manage.py send_log_reminders
class Command(BaseCommand):
    def handle(self, *args, **options):
        for settings in EmailNotificationSettings.objects.all():
            if days_since >= settings.days_without_log:
                send_mail(...)  # リマインダー送信
```

Cronで毎朝9時実行するだけ。

### 9. 多言語対応 — Django i18n（日本語・英語・イタリア語）

日本語・イタリア語・英語の3言語対応。なぜイタリア語？...作者がイタリア在住だからです（笑）

> 📸 **[画像: 画面左下の言語切替ドロップダウン — 🇯🇵 / 🇬🇧 / 🇮🇹 の3択]**
> ![言語切替](./docs/images/language-switcher.png)

Django i18n の仕組み：

```django
{% load i18n %}
<h1>{% trans "家計簿アプリ" %}</h1>
```

`.po` ファイルで翻訳を管理し、`msgfmt` でコンパイル：

```
msgid "家計簿アプリ"
msgstr "Budget App"         # 英語
# または
msgstr "App Bilancio"       # イタリア語
```

**実装で詰まったポイント**：`.po` ファイルを書くだけでは動きません。必ず `compilemessages` で `.mo`（バイナリ）にコンパイルが必要です。このコンパイル済み `.mo` ファイルをリポジトリにコミットするまで、言語を切り替えても何も変わらない状態が続きます（実際に苦労しました笑）。

言語切り替えボタンは画面左下に固定配置。フラグ絵文字で直感的に操作できます。

---

## 🎨 デザインの工夫 — Tailwindで爆速開発

Tailwind CSS、慣れたら**めちゃくちゃ速い**。

```html
<button class="w-full bg-blue-600 text-white py-4 rounded-lg
               font-bold hover:bg-blue-700 transition">
    保存
</button>
```

これだけでモダンなボタン完成。CSSファイルを一切書かなくて済みます。

**モバイルファースト**を意識して、全てスマホで使いやすいサイズに：
- タップターゲットは最低44px
- フォントサイズは16px以上（iOSの自動ズームを防ぐ）

> 📸 **[画像: スマートフォンでの表示 — iOS Safariのホーム画面追加ダイアログ + アプリアイコン]**
> ![モバイル表示](./docs/images/mobile-pwa.png)

Chart.jsでグラフもサクッと：

```javascript
new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['1月', '2月', '3月', '4月', '5月', '6月'],
        datasets: [
            { label: '収入', data: [...], borderColor: 'rgb(59, 130, 246)' },
            { label: '支出', data: [...], borderColor: 'rgb(239, 68, 68)'  }
        ]
    }
});
```

数字だけより**圧倒的に分かりやすい**。

---

## 🆓 PythonAnywhere無料プランの制約と工夫

| 項目 | 無料プランの制限 | 対応策 |
|---|---|---|
| ストレージ | 512MBまで | 画像を自動圧縮（Pillow） |
| Webアプリ数 | 1つまで | 問題なし |
| 外部APIアクセス | ホワイトリスト方式 | Gemini APIはホワイトリスト内 |
| スリープ | 毎日リロード必要 | 手動またはスクリプトで対応 |

### 画像圧縮

```python
from PIL import Image

def compress_receipt(image_file):
    img = Image.open(image_file)
    img.thumbnail((1200, 1200))         # リサイズ
    img.save(path, optimize=True, quality=85)  # 圧縮
```

元画像5MBでも、保存時は500KB以下に。

### 静的ファイル

Tailwind・Chart.jsは全てCDN経由。ローカルに置かないのでストレージ節約。

```html
<script src="https://cdn.tailwindcss.com"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"></script>
```

---

## 🚧 開発で苦労したこと（と解決法）

### 1. 翻訳が全く反映されない問題

最初、言語を切り替えても何も変わりませんでした。

**原因**：`.po` ファイルは書いたけど、コンパイルした `.mo` ファイルをリポジトリにコミットしていなかった。

```bash
# これを必ず実行してコミット！
python manage.py compilemessages
git add locale/*/LC_MESSAGES/django.mo
```

**解決策**：コンパイル済みの `.mo` ファイルをリポジトリに含めることで、デプロイ後にコンパイル作業不要にしました。

### 2. 通貨未設定でのAttributeError

```python
# NG: family.currency が None のとき AttributeError
return self.currency.symbol

# OK: Noneガード付き
def get_currency_symbol(self):
    return self.currency.symbol if self.currency else '¥'
```

FK が `null=True` になっていても、テンプレートで直接アクセスすると落ちます。モデルにメソッドを用意してテンプレートから直接アクセスしないようにするのが正解でした。

### 3. 通貨テーブルが空でドロップダウンが空白

コードはあるのにデータがなかった問題。管理コマンドで手動投入していたため、新規環境では常に空でした。

**解決策**：データマイグレーションに組み込んで、`migrate` 一発で自動投入：

```python
# 0003_seed_currencies.py
def seed_currencies(apps, schema_editor):
    Currency = apps.get_model('budget', 'Currency')
    for c in currencies:
        Currency.objects.using(...).get_or_create(code=c['code'], defaults=c)
```

### 4. セッション管理

最初、毎回ログインが必要で「めんどくさい！」ってなりました。

```python
SESSION_COOKIE_AGE = 30 * 60         # 30分
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
```

### 5. Chart.jsのレスポンシブ対応

グラフがスマホで見切れる問題。

```javascript
options: {
    responsive: true,
    maintainAspectRatio: false   // これが重要
}
```

### 6. Gemini APIのレート制限

無料プランは1分に15リクエストまで。連打されると止まる。

```javascript
button.disabled = true;
setTimeout(() => button.disabled = false, 60000);  // 1分間ボタン無効
```

### 7. タイムゾーン問題

サーバーがUTC、ユーザーが日本時間で日付がズレる。

```python
TIME_ZONE = 'Asia/Tokyo'
USE_TZ = True
```

---

## 📱 PWA化 — アプリっぽく使える

このアプリ、実は**PWA**（Progressive Web App）化してます。スマホのホーム画面に追加すると、ネイティブアプリみたいに使えます！

```json
// manifest.json
{
  "name": "家計簿アプリ",
  "short_name": "家計簿",
  "display": "standalone",
  "start_url": "/",
  "theme_color": "#2563eb",
  "icons": [
    { "src": "/static/icons/icon-192x192.png", "sizes": "192x192" },
    { "src": "/static/icons/icon-512x512.png", "sizes": "512x512" }
  ]
}
```

> 📸 **[画像: iPhoneのホーム画面 — 家計簿アプリのアイコンがネイティブアプリのように並んでいる]**
> ![PWAホーム画面](./docs/images/pwa-homescreen.png)

---

## 🎯 今後の展開

| 機能 | 状態 |
|---|---|
| PWA対応 | ✅ 完了 |
| AI支出分析（多言語）| ✅ 完了 |
| 多通貨対応 | ✅ 完了 |
| 個人Gemini APIキー | ✅ 完了 |
| 多言語ドキュメント（EN/IT/JA）| ✅ 完了 |
| LINE通知 | 🔲 検討中 |
| 銀行API連携 | 🔲 検討中（審査が大変そう...）|
| OCR機能（レシート自動読み取り）| 🔲 検討中 |
| 予算超過リアルタイムアラート | 🔲 検討中 |

---

## 💭 振り返り — 作ってみて思ったこと

### 良かった点
- **Django便利すぎ**：認証・管理画面・ORM・i18nが最初から揃ってる
- **Tailwind最高**：CSSほぼ書かずにモダンUIが作れる
- **Gemini API面白い**：プロンプト次第で何でもできる
- **PythonAnywhere楽**：デプロイがコマンド一発

### 反省点
- **ストレージ管理が甘かった**：最初から画像圧縮しておけば良かった
- **テスト不足**：手動テストしかしていない（ごめんなさい！）
- **初期データを管理コマンドでやっていた**：データマイグレーションにすべきだった

### 学んだこと
- 「作りたい」から始めると、**技術は後からついてくる**
- 完璧を目指すより、**動くものを作って改善**する方が楽しい
- 無料でもここまで作れる（お金がないは言い訳にならない笑）

---

## 🎁 試してみたい方へ

### ⚠️ デモサイトについて

デモサイト（https://mydemoapplication.pythonanywhere.com）は古いバージョンで動いています。

**以下の最新機能はデモサイトには反映されていません：**
- 多言語対応（言語切替が正常動作する版）
- 個人Gemini APIキー設定
- 多通貨対応（JPY/USD/EUR/GBP/CNY/KRW/SGD/AUD）

**最新機能を試したい方は、GitHubからクローンしてローカルで動かしてください：**

### ローカルで動かす（最新版）

```bash
# 1. クローン
git clone https://github.com/Rikiza89/family-budget-app.git
cd family-budget-app

# 2. 仮想環境
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. 依存パッケージ
pip install -r requirements.txt

# 4. マイグレーション（通貨データも自動投入されます）
python manage.py migrate

# 5. スーパーユーザー作成（任意）
python manage.py createsuperuser

# 6. 起動
python manage.py runserver
```

`http://localhost:8000` にアクセスしてください。

> 💡 **Gemini APIキーについて**
> `settings.py` の `GEMINI_API_KEY` に自分のキーを設定するか、
> ログイン後に **設定 → AI API キー** から個人キーを登録してください。
> 無料キーは [Google AI Studio](https://aistudio.google.com/) で取得できます。

### 既存のDB（マイグレーション履歴なし）をお使いの方

```bash
python manage.py migrate --fake 0001   # 既存テーブルをスキップ
python manage.py migrate               # 新しい変更のみ適用
```

---

## 🙏 最後に

この家計簿アプリは、**「こんな機能があったらいいな」を形にしたプロジェクト**です。

売るためじゃなく、**アイデアを実現する楽しさ**を追求しました。完璧じゃないし、バグもあるかもしれない（見つけたら教えてください笑）。でも、**動くものを作り上げた達成感**は最高です。

「こんな機能追加したら？」「ここ改善できるよ！」といったフィードバックは大歓迎です。GitHubのIssueやPull Requestお待ちしてます！

👉 **GitHub**: https://github.com/Rikiza89/family-budget-app

それでは、**Happy Budgeting! 💰✨**

---

**P.S.** イタリア語対応は完全に趣味です（笑）でも作者がイタリア在住なので、海外在住の日本人にも届けたくて。多通貨対応も含め、引き続き改善していきます！🌍

from django.utils.translation import gettext_lazy as _

_("食費")
_("外食")
_("日用品")
_("交通費")
_("光熱費")
_("通信費")
_("医療費")
_("娯楽")
_("衣服")
_("保険（積立）")
_("その他")
_("給料")
_("賞与")
_("副収入")
_("その他収入")
_("現金")
_("クレジットカード")
_("交通系ICカード")
_("PayPay")
_("銀行振込")

# Translation dictionary for default data
CATEGORY_TRANSLATIONS = {
    'ja': {
        'food': ('食費', '🍚'),
        'dining': ('外食', '🍽️'),
        'daily': ('日用品', '🧴'),
        'transport': ('交通費', '🚃'),
        'utilities': ('光熱費', '💡'),
        'communication': ('通信費', '📱'),
        'medical': ('医療費', '🏥'),
        'entertainment': ('娯楽', '🎮'),
        'clothing': ('衣服', '👕'),
        'insurance': ('保険（積立）', '📋'),
        'other': ('その他', '📦'),
        'salary': ('給料', '💰'),
        'bonus': ('賞与', '🎁'),
        'side_income': ('副収入', '💵'),
        'other_income': ('その他収入', '📈'),
    },
    'it': {
        'food': ('Alimentari', '🍚'),
        'dining': ('Ristoranti', '🍽️'),
        'daily': ('Casa', '🧴'),
        'transport': ('Trasporti', '🚃'),
        'utilities': ('Utenze', '💡'),
        'communication': ('Telefono', '📱'),
        'medical': ('Mediche', '🏥'),
        'entertainment': ('Svago', '🎮'),
        'clothing': ('Abbigliamento', '👕'),
        'insurance': ('Assicurazione', '📋'),
        'other': ('Altro', '📦'),
        'salary': ('Stipendio', '💰'),
        'bonus': ('Bonus', '🎁'),
        'side_income': ('Entrate Extra', '💵'),
        'other_income': ('Altre Entrate', '📈'),
    }
    'en': {
        'food': ('Groceries', '🍚'),
        'dining': ('Eating Out', '🍽️'),
        'daily': ('Household Goods', '🧴'),
        'transport': ('Transportation', '🚃'),
        'utilities': ('Utilities', '💡'),
        'communication': ('Communication', '📱'),
        'medical': ('Medical/Health', '🏥'),
        'entertainment': ('Entertainment', '🎮'),
        'clothing': ('Clothing', '👕'),
        'insurance': ('Insurance (Savings)', '📋'),
        'other': ('Other Expense', '📦'),
        'salary': ('Salary', '💰'),
        'bonus': ('Bonus', '🎁'),
        'side_income': ('Side Income', '💵'),
        'other_income': ('Other Income', '📈'),
    }
}

PAYMENT_METHODS = {
    'ja': {
        'cash': '現金',
        'credit': 'クレジットカード',
        'ic': '交通系ICカード',
        'qr': 'PayPay',
        'bank': '銀行振込',
    },
    'it': {
        'cash': 'Contanti',
        'credit': 'Carta di Credito',
        'ic': 'Carta Prepagata',
        'qr': 'Pagamento Digitale',
        'bank': 'Bonifico',
      }
      'en': {
        'cash': 'Cash',
        'credit': 'Credit Card',
        'ic': 'IC Card/Transit',
        'qr': 'Digital Payment',
        'bank': 'Bank Transfer',
    }
}

def get_category_name(key, language='ja'):
    """Get category name in specified language"""
    return CATEGORY_TRANSLATIONS.get(language, {}).get(key, ('', ''))[0]

def get_category_icon(key):
    """Get category icon (same for all languages)"""
    return CATEGORY_TRANSLATIONS['ja'].get(key , ('', ''))[1] }


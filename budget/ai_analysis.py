# # Add to views.py or create ai_analysis.py

# import google.generativeai as genai
# from django.conf import settings
# from datetime import timedelta

# # Configure Gemini
# genai.configure(api_key=settings.GEMINI_API_KEY)

# @login_required
# def ai_spending_analysis(request):
#     try:
#         member = request.user.familymember
#         family = member.family
#     except FamilyMember.DoesNotExist:
#         return redirect('setup_profile')
    
#     # Get last 3 months data
#     today = timezone.now().date()
#     three_months_ago = today - timedelta(days=90)
    
#     transactions = Transaction.objects.filter(
#         family=family,
#         date__gte=three_months_ago
#     ).select_related('category')
    
#     # Prepare data for AI
#     category_totals = {}
#     for trans in transactions:
#         cat_name = trans.category.name
#         if cat_name not in category_totals:
#             category_totals[cat_name] = {
#                 'total': 0,
#                 'count': 0,
#                 'type': trans.transaction_type
#             }
#         category_totals[cat_name]['total'] += float(trans.amount)
#         category_totals[cat_name]['count'] += 1
    
#     # Calculate totals
#     total_income = sum(v['total'] for k, v in category_totals.items() if v['type'] == 'income')
#     total_expense = sum(v['total'] for k, v in category_totals.items() if v['type'] == 'expense')
    
#     # Build prompt
#     currency_symbol = family.get_currency_symbol()
#     prompt = f"""
# あなたは家計アドバイザーです。以下のデータを分析し、日本語で改善提案をしてください。

# 【期間】過去3ヶ月
# 【通貨】{family.currency.code}
# 【総収入】{currency_symbol}{total_income:,.0f}
# 【総支出】{currency_symbol}{total_expense:,.0f}

# 【カテゴリー別支出】
# """
#     for cat_name, data in category_totals.items():
#         if data['type'] == 'expense':
#             prompt += f"- {cat_name}: {currency_symbol}{data['total']:,.0f} ({data['count']}回)\n"
    
#     prompt += """

# 以下の形式で分析してください：
# 1. 支出の特徴（3つ）
# 2. 改善提案（3つ）
# 3. 節約できそうな項目（具体的な金額目標付き）
# 4. 良い点（1つ）

# 簡潔に、箇条書きで回答してください。
# """
    
#     try:
#         model = genai.GenerativeModel('gemini-2.0-flash-exp')
#         response = model.generate_content(prompt)
#         ai_analysis = response.text
#     except Exception as e:
#         ai_analysis = f"AI分析エラー: {str(e)}"
    
#     context = {
#         'ai_analysis': ai_analysis,
#         'total_income': total_income,
#         'total_expense': total_expense,
#         'category_totals': category_totals,
#         'currency_symbol': currency_symbol
#     }
    
#     return render(request, 'budget/ai_analysis.html', context)
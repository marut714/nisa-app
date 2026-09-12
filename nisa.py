import streamlit as st
import pandas as pd

# ページの設定
st.set_page_config(page_title="NISAシミュレーター", layout="centered")

st.title("💰 友達のための新NISAまるわかりアプリ")

st.markdown("""
## そもそもNISAって何？
通常、投資の利益には約20%の税金がかかりますが、NISAを使えば**利益がすべて非課税（ゼロ）**になる国のお得なボーナス制度です！
""")

st.header("📈 NISAの威力がわかる！積立シミュレーション")
st.write("毎月コツコツ積み立てたらどうなるか、実際にバーを動かして確かめてみよう。")

# 入力スライダー
col1, col2 = st.columns(2)
with col1:
    monthly_invest = st.slider("毎月の積立額（万円）", 1, 30, 3)
with col2:
    return_rate = st.slider("想定利回り（年率％）", 1, 15, 5)

years = st.slider("積立期間（年）", 1, 40, 20)

# 計算処理（毎月複利計算）
monthly_rate = (return_rate / 100) / 12
principal_list = []
total_list = []

for i in range(1, years + 1):
    n_months = i * 12
    # 将来価値（FV）の計算
    P = monthly_invest * 10000
    if return_rate > 0:
        fv = P * (((1 + monthly_rate)**n_months - 1) / monthly_rate)
    else:
        fv = P * n_months
    
    principal_list.append(monthly_invest * 10000 * 12 * i)
    total_list.append(fv)

# グラフ描画用にデータフレームを作成
df = pd.DataFrame({
    "元本（投資したお金）": principal_list,
    "運用結果（元本＋利益）": total_list
}, index=range(1, years + 1))

# エリアチャートで差をわかりやすく表示
st.area_chart(df)

# 結果まとめ
final_principal = principal_list[-1]
final_total = total_list[-1]
profit = final_total - final_principal
tax_saved = profit * 0.20315

# 見やすいように枠をつけて結果を表示
st.success(f"🎉 {years}年後の資産額：約 **{int(final_total):,}** 円")
st.info(f"💡 NISAなら、本来引かれるはずの税金 約 **{int(tax_saved):,}** 円がタダになります！")

st.markdown("""
---
### 📝 NISAの2つの枠
* **つみたて投資枠（年120万円まで）**: 少額からコツコツ。国が選んだ安全性の高い投資信託が中心。
* **成長投資枠（年240万円まで）**: 幅広い株や投資信託に自由に投資できる枠。
""")

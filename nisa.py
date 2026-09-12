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

st.markdown("---")

# リスクについての説明（暴落時の心構えを追加）
st.warning("""
**⚠️ 注意：必ず得をするわけではありません！**  
このシミュレーションは「ずっと同じ利回りで増え続けた場合」の計算ですが、実際の投資では価格が上がったり下がったりします。タイミングによっては投資した金額より減ってしまう（元本割れ）リスクもあります。

**💡 暴落したときの心構え**  
ニュースなどで株価が大きく下がったと聞いても、**絶対に焦って売らない（ガチホする）こと！** 途中でやめず、長期間コツコツ続ける「長期・分散・積立」が投資を成功させる一番のコツです。
""")

# 2つの枠の違い
st.markdown("""
### 📝 NISAの2つの枠の違い
NISAには2つの枠があり、これらは**同時に使う（併用する）**こともできます！

| 項目 | つみたて投資枠 | 成長投資枠 |
| :--- | :--- | :--- |
| **年間上限額** | **120万円**（月10万円まで） | **240万円** |
| **買える商品** | 国の基準をクリアした**投資信託のみ** | **上場株式**、投資信託など幅広い |
| **買い方** | **積立のみ** | **一括購入** ＋ **積立** |
| **生涯の枠** | 1,800万円すべて使い切れる | 1,800万円のうち、最大1,200万円まで |
""")

# 銘柄選びのヒント
st.markdown("""
### 🛒 何を買えばいいの？（代表的な2つ）
初心者のうちは、「つみたて投資枠」で以下のどちらかの投資信託を毎月買う設定にするのが定番です！

* 🌍 **全世界株式（オール・カントリー）**：迷ったらこれ！世界中の会社に分散投資できる一番無難で手堅い選択肢。
***米国株式（S&P500）**：アメリカの主要企業500社に投資。少しリスクを取ってでも、より大きなリターンを狙いたい人向け。
""")

# おすすめ証券会社とアクションプラン
st.markdown("""
### 🏢 どこで始めるのがおすすめ？
NISAの口座を作るなら、以下のネット証券が圧倒的におすすめです。
* **楽天証券** または **SBI証券**
（※銀行の窓口は手数料が高い商品を勧められることがあるので注意！）

---



""")

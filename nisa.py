import React, { useState, useMemo } from 'react';
import { 
  AreaChart, 
  Area, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  Legend
} from 'recharts';
import { 
  Calculator, 
  TrendingUp, 
  ShieldCheck, 
  PiggyBank, 
  Info,
  Gift
} from 'lucide-react';

// 金額を見やすくフォーマットするヘルパー関数
const formatCurrency = (value) => {
  return Math.round(value).toLocaleString() + '円';
};

const formatManYen = (value) => {
  if (value === 0) return '0円';
  const man = value / 10000;
  if (man >= 10000) {
    const oku = Math.floor(man / 10000);
    const remainingMan = Math.floor(man % 10000);
    return remainingMan > 0 ? `${oku}億${remainingMan}万円` : `${oku}億円`;
  }
  return `${Math.floor(man).toLocaleString()}万円`;
};

// グラフ用のツールチップカスタムコンポーネント
const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-white/95 p-4 rounded-xl shadow-lg border border-slate-100">
        <p className="font-bold text-slate-700 mb-2">{`${label}年目`}</p>
        {payload.map((entry, index) => (
          <div key={index} className="flex items-center gap-2 text-sm my-1">
            <div 
              className="w-3 h-3 rounded-full" 
              style={{ backgroundColor: entry.color }}
            />
            <span className="text-slate-600">{entry.name}:</span>
            <span className="font-semibold text-slate-800">
              {formatManYen(entry.value)}
            </span>
          </div>
        ))}
      </div>
    );
  }
  return null;
};

export default function NisaSimulator() {
  // スライダーのステート管理
  const [monthlyInvestment, setMonthlyInvestment] = useState(3); // 万円
  const [returnRate, setReturnRate] = useState(5); // %
  const [years, setYears] = useState(20); // 年

  // シミュレーションデータの計算（依存配列の値が変わった時だけ再計算）
  const simulationData = useMemo(() => {
    const data = [];
    const P = monthlyInvestment * 10000; // 月の積立額（円）
    const r = (returnRate / 100) / 12;   // 月利
    
    let currentPrincipal = 0;
    let currentTotal = 0;

    for (let year = 0; year <= years; year++) {
      if (year === 0) {
        data.push({ year: 0, principal: 0, total: 0 });
        continue;
      }
      
      const months = year * 12;
      currentPrincipal = P * months;
      
      if (returnRate === 0) {
        currentTotal = currentPrincipal;
      } else {
        // 毎月末積立の複利計算公式: FV = P * (((1 + r)^n - 1) / r)
        currentTotal = P * (Math.pow(1 + r, months) - 1) / r;
      }
      
      data.push({
        year,
        principal: currentPrincipal,
        total: currentTotal
      });
    }
    return data;
  }, [monthlyInvestment, returnRate, years]);

  // 最終結果の抽出
  const finalResult = simulationData[simulationData.length - 1];
  const totalProfit = finalResult.total - finalResult.principal;
  const taxSaved = totalProfit * 0.20315; // 利益にかかる約20%の税金が非課税に

  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-800 pb-20">
      {/* ヘッダーセクション */}
      <div className="bg-gradient-to-r from-emerald-600 to-teal-700 text-white py-12 px-4 shadow-md">
        <div className="max-w-4xl mx-auto text-center space-y-4">
          <div className="inline-flex items-center justify-center p-3 bg-white/20 rounded-2xl mb-4 backdrop-blur-sm">
            <PiggyBank size={40} className="text-emerald-100" />
          </div>
          <h1 className="text-3xl md:text-5xl font-extrabold tracking-tight">
            新NISA まるわかりシミュレーター
          </h1>
          <p className="text-emerald-100 text-lg md:text-xl max-w-2xl mx-auto leading-relaxed">
            「投資の利益が非課税になる」最強の資産形成ツール。<br className="hidden md:block"/>
            毎月コツコツ積み立てたらどうなるか、実際に確かめてみましょう！
          </p>
        </div>
      </div>

      <div className="max-w-5xl mx-auto px-4 -mt-8 relative z-10 space-y-8">
        
        {/* NISAとは？（解説カード） */}
        <div className="bg-white rounded-3xl shadow-xl p-6 md:p-8 border border-slate-100">
          <div className="flex items-center gap-3 mb-6">
            <Info className="text-emerald-500" size={28} />
            <h2 className="text-2xl font-bold text-slate-800">新NISAの2つの投資枠</h2>
          </div>
          <div className="grid md:grid-cols-2 gap-6">
            <div className="bg-emerald-50 rounded-2xl p-6 border border-emerald-100 relative overflow-hidden">
              <div className="absolute top-0 right-0 w-24 h-24 bg-emerald-500/10 rounded-bl-full -mr-4 -mt-4" />
              <ShieldCheck className="text-emerald-600 mb-3" size={32} />
              <h3 className="text-xl font-bold text-emerald-900 mb-2">つみたて投資枠</h3>
              <p className="text-emerald-800/80 text-sm mb-4">年間 120万円まで</p>
              <ul className="space-y-2 text-sm text-slate-700">
                <li className="flex items-start gap-2">
                  <span className="text-emerald-500 font-bold">✓</span>
                  金融庁が厳選した安全性の高い投資信託
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-emerald-500 font-bold">✓</span>
                  少額からコツコツ長期投資したい人向け
                </li>
              </ul>
            </div>
            
            <div className="bg-teal-50 rounded-2xl p-6 border border-teal-100 relative overflow-hidden">
              <div className="absolute top-0 right-0 w-24 h-24 bg-teal-500/10 rounded-bl-full -mr-4 -mt-4" />
              <TrendingUp className="text-teal-600 mb-3" size={32} />
              <h3 className="text-xl font-bold text-teal-900 mb-2">成長投資枠</h3>
              <p className="text-teal-800/80 text-sm mb-4">年間 240万円まで</p>
              <ul className="space-y-2 text-sm text-slate-700">
                <li className="flex items-start gap-2">
                  <span className="text-teal-500 font-bold">✓</span>
                  国内外の株式や幅広い投資信託が対象
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-teal-500 font-bold">✓</span>
                  一括投資や、応援したい企業がある人向け
                </li>
              </ul>
            </div>
          </div>
          <p className="mt-4 text-center text-sm text-slate-500 bg-slate-50 p-3 rounded-xl">
            💡 2つの枠は<strong>併用可能</strong>！ 生涯で合計 <strong>1,800万円</strong> まで非課税で投資できます。
          </p>
        </div>

        {}
        {/* シミュレーター本体 */}
        <div className="bg-white rounded-3xl shadow-xl p-6 md:p-8 border border-slate-100">
          <div className="flex items-center gap-3 mb-8 border-b pb-4">
            <Calculator className="text-emerald-500" size={28} />
            <h2 className="text-2xl font-bold text-slate-800">積立シミュレーション</h2>
          </div>

          <div className="grid lg:grid-cols-12 gap-8">
            {/* 左側：入力パネル */}
            <div className="lg:col-span-4 space-y-8">
              
              {/* 毎月の積立額 */}
              <div className="space-y-4 bg-slate-50 p-5 rounded-2xl border border-slate-100">
                <div className="flex justify-between items-end">
                  <label className="font-bold text-slate-700">毎月の積立額</label>
                  <div className="text-2xl font-black text-emerald-600">
                    {monthlyInvestment}<span className="text-base font-medium text-slate-500 ml-1">万円</span>
                  </div>
                </div>
                <input 
                  type="range" 
                  min="1" max="30" step="1"
                  value={monthlyInvestment}
                  onChange={(e) => setMonthlyInvestment(Number(e.target.value))}
                  className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-emerald-500"
                />
                <div className="flex justify-between text-xs text-slate-400 font-medium">
                  <span>1万円</span>
                  <span>30万円</span>
                </div>
              </div>

              {/* 想定利回り */}
              <div className="space-y-4 bg-slate-50 p-5 rounded-2xl border border-slate-100">
                <div className="flex justify-between items-end">
                  <label className="font-bold text-slate-700">想定利回り (年率)</label>
                  <div className="text-2xl font-black text-blue-600">
                    {returnRate}<span className="text-base font-medium text-slate-500 ml-1">%</span>
                  </div>
                </div>
                <input 
                  type="range" 
                  min="1" max="15" step="1"
                  value={returnRate}
                  onChange={(e) => setReturnRate(Number(e.target.value))}
                  className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-blue-500"
                />
                <div className="flex justify-between text-xs text-slate-400 font-medium">
                  <span>1%</span>
                  <span>15%</span>
                </div>
              </div>

              {/* 積立期間 */}
              <div className="space-y-4 bg-slate-50 p-5 rounded-2xl border border-slate-100">
                <div className="flex justify-between items-end">
                  <label className="font-bold text-slate-700">積立期間</label>
                  <div className="text-2xl font-black text-purple-600">
                    {years}<span className="text-base font-medium text-slate-500 ml-1">年</span>
                  </div>
                </div>
                <input 
                  type="range" 
                  min="1" max="40" step="1"
                  value={years}
                  onChange={(e) => setYears(Number(e.target.value))}
                  className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-purple-500"
                />
                <div className="flex justify-between text-xs text-slate-400 font-medium">
                  <span>1年</span>
                  <span>40年</span>
                </div>
              </div>
            </div>

            {}
            {/* 右側：グラフと結果 */}
            <div className="lg:col-span-8 flex flex-col">
              
              {/* グラフ */}
              <div className="h-72 md:h-96 w-full mb-8">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart
                    data={simulationData}
                    margin={{ top: 10, right: 10, left: 0, bottom: 0 }}
                  >
                    <defs>
                      <linearGradient id="colorTotal" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#10b981" stopOpacity={0.8}/>
                        <stop offset="95%" stopColor="#10b981" stopOpacity={0.1}/>
                      </linearGradient>
                      <linearGradient id="colorPrincipal" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#94a3b8" stopOpacity={0.8}/>
                        <stop offset="95%" stopColor="#94a3b8" stopOpacity={0.2}/>
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                    <XAxis 
                      dataKey="year" 
                      tickFormatter={(tick) => `${tick}年`}
                      stroke="#94a3b8"
                      tick={{ fill: '#64748b', fontSize: 12 }}
                      tickMargin={10}
                    />
                    <YAxis 
                      tickFormatter={(tick) => {
                        if (tick === 0) return '0';
                        return `${Math.floor(tick / 10000)}万円`;
                      }}
                      stroke="#94a3b8"
                      tick={{ fill: '#64748b', fontSize: 12 }}
                      width={80}
                    />
                    <Tooltip content={<CustomTooltip />} />
                    <Legend verticalAlign="top" height={36} iconType="circle" />
                    <Area 
                      type="monotone" 
                      dataKey="total" 
                      name="運用結果（元本＋利益）" 
                      stroke="#10b981" 
                      strokeWidth={3}
                      fillOpacity={1} 
                      fill="url(#colorTotal)" 
                      animationDuration={1000}
                    />
                    <Area 
                      type="monotone" 
                      dataKey="principal" 
                      name="投資元本" 
                      stroke="#64748b" 
                      strokeWidth={2}
                      fillOpacity={1} 
                      fill="url(#colorPrincipal)" 
                      animationDuration={1000}
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </div>

              {}
              {/* 結果サマリー */}
              <div className="grid md:grid-cols-2 gap-4 mt-auto">
                <div className="bg-slate-800 text-white p-6 rounded-2xl shadow-lg relative overflow-hidden">
                  <div className="relative z-10">
                    <p className="text-slate-400 text-sm font-bold mb-1">{years}年後の最終積立金額</p>
                    <div className="flex items-baseline gap-2">
                      <span className="text-4xl font-black tracking-tight">{formatManYen(finalResult.total)}</span>
                    </div>
                    <div className="mt-3 text-sm text-slate-300">
                      うち投資元本: <span className="font-semibold text-white">{formatManYen(finalResult.principal)}</span>
                    </div>
                    <div className="mt-1 text-sm text-emerald-400 font-medium">
                      運用利益: +{formatManYen(totalProfit)}
                    </div>
                  </div>
                  {/* 背景装飾 */}
                  <TrendingUp className="absolute -right-6 -bottom-6 text-slate-700/50" size={120} />
                </div>

                <div className="bg-gradient-to-br from-emerald-400 to-teal-500 text-white p-6 rounded-2xl shadow-lg shadow-emerald-500/20 relative overflow-hidden">
                  <div className="relative z-10">
                    <div className="flex items-center gap-2 mb-1">
                      <Gift size={18} className="text-emerald-100" />
                      <p className="text-emerald-100 text-sm font-bold">NISAの非課税パワー</p>
                    </div>
                    <p className="text-xs text-emerald-50 mb-3 opacity-90">通常引かれるはずの税金（約20%）がゼロに！</p>
                    <div className="flex items-baseline gap-2">
                      <span className="text-sm font-bold">約</span>
                      <span className="text-4xl font-black tracking-tight">{formatManYen(taxSaved)}</span>
                      <span className="text-sm font-bold">お得！</span>
                    </div>
                  </div>
                  {/* 背景装飾 */}
                  <ShieldCheck className="absolute -right-6 -bottom-6 text-emerald-900/10" size={120} />
                </div>
              </div>

              <p className="text-xs text-slate-400 mt-6 text-center">
                ※このシミュレーションは、毎月末に積立を行い、指定した年率で複利運用された場合の試算です。将来の運用成果を保証するものではありません。<br/>
                ※税金は簡便的に利益に対して20.315%で計算しています。
              </p>

            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
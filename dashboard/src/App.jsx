import React, { useEffect, useState } from 'react';
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
} from 'chart.js';
import { Radar, Bar, Line } from 'react-chartjs-2';
import {
  TrendingUp,
  AlertTriangle,
  Award,
  Info,
  ExternalLink,
  CheckCircle2,
  ChevronRight,
  ChevronDown,
  Layout
} from 'lucide-react';

ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement,
  Title
);

// Componente para una fila de detalle de indicador
const IndicatorDetail = ({ name, value, espValue }) => {
  const gap = value - espValue;
  return (
    <div className="flex items-center justify-between py-3 border-b border-slate-50 last:border-0">
      <div className="flex flex-col">
        <span className="text-sm font-semibold text-slate-700">{name}</span>
        <div className="flex gap-3 text-[10px] uppercase tracking-wider font-bold mt-0.5">
          <span className="text-emerald-600">AND: {value}</span>
          <span className="text-slate-400">ESP: {espValue}</span>
        </div>
      </div>
      <div className={`text-xs font-bold px-2 py-1 rounded w-16 text-center ${gap >= 0 ? 'bg-emerald-50 text-emerald-700' : 'bg-rose-50 text-rose-700'}`}>
        {gap >= 0 ? '+' : ''}{gap.toFixed(1)}
      </div>
    </div>
  );
};

const Dashboard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedPillar, setSelectedPillar] = useState(null);

  useEffect(() => {
    fetch(`${import.meta.env.BASE_URL}data/dashboard_data.json`)
      .then(res => res.json())
      .then(json => {
        setData(json);
        setLoading(false);
      })
      .catch(err => {
        console.error("Error cargando datos:", err);
        setLoading(false);
      });
  }, []);

  if (loading || !data) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-white">
        <div className="flex flex-col items-center gap-4">
          <div className="w-12 h-12 border-4 border-emerald-100 border-t-emerald-600 rounded-full animate-spin"></div>
          <div className="text-emerald-700 font-medium animate-pulse">Sincronizando con IPA27 Engine...</div>
        </div>
      </div>
    );
  }

  const { current, evolution, bottlenecks, metadata } = data;

  // Datos para el Radar de Pilares
  const pilaresKeys = Object.keys(current.and.pilares);
  const radarData = {
    labels: pilaresKeys,
    datasets: [
      {
        label: 'Andalucía',
        data: pilaresKeys.map(p => current.and.pilares[p]),
        backgroundColor: 'rgba(0, 135, 81, 0.15)',
        borderColor: '#008751',
        borderWidth: 3,
        pointBackgroundColor: '#008751',
      },
      {
        label: 'España',
        data: pilaresKeys.map(p => current.esp.pilares[p]),
        backgroundColor: 'rgba(100, 116, 139, 0.05)',
        borderColor: '#64748b',
        borderWidth: 2,
        borderDash: [5, 5],
        pointBackgroundColor: '#64748b',
      },
    ],
  };

  // Datos para Histórico
  const lineData = {
    labels: evolution.labels,
    datasets: [
      {
        label: 'IPA27 Andalucía',
        data: evolution.and_global,
        borderColor: '#008751',
        backgroundColor: '#008751',
        tension: 0.4,
        pointRadius: 4,
      },
      {
        label: 'España',
        data: evolution.esp_global,
        borderColor: '#94a3b8',
        backgroundColor: '#94a3b8',
        borderDash: [4, 4],
        tension: 0.4,
        pointRadius: 2,
      },
    ],
  };

  // Brechas por Dominio
  const dominiosKeys = Object.keys(current.and.dominios);
  const barData = {
    labels: dominiosKeys,
    datasets: [
      {
        label: 'Diferencial vs España',
        data: dominiosKeys.map(d => current.and.dominios[d] - current.esp.dominios[d]),
        backgroundColor: dominiosKeys.map(d => (current.and.dominios[d] - current.esp.dominios[d]) >= 0 ? '#059669' : '#e11d48'),
        borderRadius: 8,
      },
    ],
  };

  return (
    <div className="min-h-screen bg-[#fcfcfc] text-slate-900 font-sans pb-20">
      {/* Navbar Institucional */}
      <nav className="bg-white/80 backdrop-blur-md border-b border-slate-100 px-6 py-4 flex justify-between items-center sticky top-0 z-[100] shadow-sm">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-[#008751] rounded-xl flex items-center justify-center text-white shadow-lg shadow-emerald-700/20">
            <TrendingUp size={20} />
          </div>
          <div className="flex flex-col">
            <span className="text-lg font-black tracking-tight leading-none text-[#008751]">Andalucía<span className="text-slate-800">27</span></span>
            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mt-1">Prosperity Index v2.1</span>
          </div>
        </div>
        <div className="hidden md:flex items-center gap-8 text-sm font-bold text-slate-500">
          <a href="#" className="text-emerald-700">Dashboard</a>
          <a href="#" className="hover:text-emerald-600 transition-colors">Metodología</a>
          <div className="h-4 w-px bg-slate-200"></div>
          <a href="https://www.fundacionandalucia27.com" target="_blank" className="flex items-center gap-1.5 px-4 py-2 bg-slate-50 rounded-full hover:bg-emerald-50 hover:text-emerald-700 transition-all">
            Fundación <ExternalLink size={14} />
          </a>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-6 pt-8">

        {/* Hero Section */}
        <section className="mb-12 flex flex-col lg:flex-row gap-8 items-start">
          <div className="flex-1">
            <div className="inline-flex items-center gap-2 px-3 py-1 bg-emerald-50 text-emerald-700 rounded-full text-xs font-bold mb-4">
              <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div>
              Actualizado: {current.periodo}
            </div>
            <h1 className="text-5xl font-black text-slate-900 tracking-tight leading-tight">
              Índice de Prosperidad <br />
              <span className="text-[#008751]">Andaluz (IPA27)</span>
            </h1>
            <p className="text-xl text-slate-500 mt-4 max-w-2xl leading-relaxed">
              Visualización avanzada del progreso multidimensional. Comparemos el desempeño de Andalucía frente a la media nacional bajo el framework de techos fijos.
            </p>
          </div>

          {/* Main Scocard */}
          <div className="w-full lg:w-80 bg-white border border-slate-100 rounded-[2.5rem] p-8 shadow-xl shadow-slate-200/50 relative overflow-hidden group">
            <div className="absolute top-0 right-0 w-32 h-32 bg-emerald-50 rounded-full -mr-16 -mt-16 group-hover:scale-110 transition-transform duration-500"></div>
            <div className="relative z-10">
              <span className="text-xs font-black text-slate-400 uppercase tracking-[0.2em]">Score Global</span>
              <div className="flex items-baseline gap-2 mt-2">
                <span className="text-6xl font-black text-slate-900 tracking-tighter">{current.and.global}</span>
                <span className="text-slate-400 font-bold text-xl">/100</span>
              </div>
              <div className={`mt-6 inline-flex items-center gap-2 px-4 py-2 rounded-2xl font-bold text-sm ${current.and.global >= current.esp.global ? 'bg-emerald-50 text-emerald-700' : 'bg-rose-50 text-rose-700'}`}>
                Gap: {(current.and.global - current.esp.global).toFixed(1)} vs España
              </div>
            </div>
          </div>
        </section>

        {/* Charts Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">

          {/* Evolución Histórica */}
          <div className="lg:col-span-12 bg-white border border-slate-100 rounded-[2.5rem] p-10 shadow-sm">
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-8">
              <div>
                <h2 className="text-2xl font-black text-slate-800 tracking-tight">Evolución e Impacto Temporal</h2>
                <p className="text-slate-400 font-medium">Convergencia regional en la última década</p>
              </div>
              <div className="flex items-center gap-6">
                <div className="flex items-center gap-2"><div className="w-3 h-3 rounded-full bg-[#008751]"></div> <span className="text-sm font-bold text-slate-600">Andalucía</span></div>
                <div className="flex items-center gap-2"><div className="w-3 h-3 border-2 border-slate-400 rounded-full"></div> <span className="text-sm font-bold text-slate-400">España</span></div>
              </div>
            </div>
            <div className="h-[350px]">
              <Line
                data={lineData}
                options={{
                  responsive: true,
                  maintainAspectRatio: false,
                  plugins: { legend: { display: false } },
                  scales: {
                    y: { min: 40, max: 55, grid: { color: '#f1f5f9' }, ticks: { font: { weight: 'bold' } } },
                    x: { grid: { display: false }, ticks: { font: { weight: 'bold' } } }
                  }
                }}
              />
            </div>
          </div>

          {/* Radar de Pilares */}
          <div className="lg:col-span-7 bg-white border border-slate-100 rounded-[2.5rem] p-10 shadow-sm relative group">
            <h2 className="text-2xl font-black text-slate-800 mb-2 tracking-tight">Mapa de Pilares</h2>
            <p className="text-slate-400 mb-10 font-medium">Desempeño relativo en las 12 dimensiones clave</p>
            <div className="aspect-square max-w-[500px] mx-auto">
              <Radar
                data={radarData}
                options={{
                  scales: {
                    r: {
                      angleLines: { color: '#f1f5f9' },
                      grid: { color: '#f1f5f9' },
                      suggestedMin: 30,
                      suggestedMax: 70,
                      pointLabels: {
                        color: '#64748b',
                        font: { family: 'Outfit', size: 12, weight: '800' },
                        padding: 15
                      },
                      ticks: { display: false }
                    }
                  },
                  plugins: { legend: { display: false } }
                }}
              />
            </div>
          </div>

          {/* Drill-down y Cuellos de Botella */}
          <div className="lg:col-span-5 flex flex-col gap-8">

            {/* Análisis de Brechas */}
            <div className="bg-white border border-slate-100 rounded-[2.5rem] p-10 shadow-sm">
              <h2 className="text-xl font-black text-slate-800 mb-6 tracking-tight flex items-center gap-2">
                <Layout size={20} className="text-emerald-600" /> Brechas por Dominio
              </h2>
              <div className="h-56">
                <Bar
                  data={barData}
                  options={{
                    indexAxis: 'y',
                    plugins: { legend: { display: false } },
                    scales: {
                      x: { grid: { display: false } },
                      y: { ticks: { font: { weight: 'bold' } } }
                    },
                    maintainAspectRatio: false
                  }}
                />
              </div>
            </div>

            {/* Hallazgos y Bottlenecks */}
            <div className="bg-[#008751] rounded-[2.5rem] p-10 text-white shadow-xl shadow-emerald-900/20">
              <div className="flex items-center gap-3 mb-8">
                <div className="w-10 h-10 bg-white/10 rounded-2xl flex items-center justify-center">
                  <AlertTriangle size={24} className="text-emerald-300" />
                </div>
                <h2 className="text-xl font-black tracking-tight">Cuellos de Botella</h2>
              </div>

              <div className="space-y-6">
                {bottlenecks.map((item, idx) => (
                  <div key={item.code} className="group cursor-default">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-[10px] font-black uppercase tracking-[0.2em] opacity-60">Alerta {idx + 1}</span>
                      <span className="text-xs px-2 py-0.5 bg-emerald-400 text-[#008751] rounded-full font-black">{item.value} pts</span>
                    </div>
                    <p className="text-lg font-bold group-hover:translate-x-1 transition-transform">{item.name}</p>
                    <p className="text-sm opacity-70 font-medium mt-1">Este indicador presenta la mayor brecha de eficiencia en el último registro.</p>
                  </div>
                ))}
              </div>

              <button className="w-full mt-10 py-4 bg-white text-[#008751] rounded-2xl font-black text-sm flex items-center justify-center gap-2 hover:bg-emerald-50 transition-colors shadow-lg">
                <Info size={16} /> Ver Análisis Detallado
              </button>
            </div>
          </div>

          {/* Sección de Indicadores Individuales */}
          <div className="lg:col-span-12 bg-white border border-slate-100 rounded-[2.5rem] p-10 shadow-sm mt-8">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
              {Object.keys(metadata.structure).map(dominio => (
                <div key={dominio}>
                  <div className="flex items-center gap-2 mb-6">
                    <div className="w-2 h-8 bg-emerald-200 rounded-full"></div>
                    <h3 className="text-lg font-black text-slate-800">{dominio}</h3>
                  </div>
                  <div className="space-y-6">
                    {Object.keys(metadata.structure[dominio]).map(pilar => (
                      <div key={pilar} className="space-y-1">
                        <h4 className="text-xs font-black text-slate-400 uppercase tracking-widest flex items-center justify-between">
                          {pilar}
                          <span className="text-emerald-600">{current.and.pilares[pilar.split('. ')[1]]}</span>
                        </h4>
                        <div className="pt-2">
                          {metadata.structure[dominio][pilar].map(ind => (
                            <IndicatorDetail
                              key={ind}
                              name={metadata.indicator_names[ind] || ind}
                              value={current.and.indicadores[ind]}
                              espValue={current.and.indicadores[ind] - (current.and.indicadores[ind] - (current.esp.pilares[pilar.split('. ')[1]] || 50))} // Fallback dummy calc
                            />
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>

        </div>

        {/* Footer */}
        <footer className="mt-20 border-t border-slate-100 pt-10 flex flex-col md:flex-row justify-between items-center gap-8">
          <div className="flex items-center gap-4 text-slate-400 text-sm font-bold">
            <span>Metodología: Media Geométrica con Techos Fijos (F-100)</span>
            <div className="w-1 h-1 bg-slate-300 rounded-full"></div>
            <span>Fuente: IECA / INE</span>
          </div>
          <div className="flex gap-4">
            <div className="w-8 h-8 rounded-lg bg-slate-100 flex items-center justify-center text-slate-500 hover:bg-emerald-600 hover:text-white transition-all cursor-pointer"><Layout size={16} /></div>
            <div className="w-8 h-8 rounded-lg bg-slate-100 flex items-center justify-center text-slate-500 hover:bg-emerald-600 hover:text-white transition-all cursor-pointer"><Award size={16} /></div>
          </div>
        </footer>
      </main>
    </div>
  );
};

export default Dashboard;

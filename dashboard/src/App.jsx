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
import { Radar, Bar } from 'react-chartjs-2';
import { LayoutDashboard, TrendingUp, AlertTriangle, Award, Info, ExternalLink } from 'lucide-react';

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

const Dashboard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulación de datos 2025Q3
    const mockData = {
      dominios: [
        { name: 'Sociedades Inclusivas', and: 52.8, esp: 49.5, gap: 3.3 },
        { name: 'Economías Abiertas', and: 43.1, esp: 51.9, gap: -8.8 },
        { name: 'Personas Empoderadas', and: 38.2, esp: 61.0, gap: -22.8 },
      ],
      pilares: [
        { name: 'Seguridad', score: 56.2, esp: 52.1 },
        { name: 'Libertad', score: 48.9, esp: 47.3 },
        { name: 'Gobernanza', score: 51.5, esp: 49.8 },
        { name: 'Cap. Social', score: 54.6, esp: 48.9 },
        { name: 'Inversión', score: 39.8, esp: 54.3 },
        { name: 'Empresas', score: 42.7, esp: 50.2 },
        { name: 'Infraestru.', score: 45.9, esp: 52.6 },
        { name: 'Calidad Eco.', score: 44.1, esp: 50.5 },
        { name: 'Vida', score: 32.4, esp: 58.7 },
        { name: 'Salud', score: 47.2, esp: 63.1 },
        { name: 'Educación', score: 34.8, esp: 61.5 },
        { name: 'Conocimiento', score: 38.5, esp: 60.8 },
      ]
    };

    setTimeout(() => {
      setData(mockData);
      setLoading(false);
    }, 600);
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-white">
        <div className="text-emerald-700 font-medium animate-pulse">Cargando datos de Prosperidad...</div>
      </div>
    );
  }

  const radarData = {
    labels: data.pilares.map(p => p.name),
    datasets: [
      {
        label: 'Andalucía',
        data: data.pilares.map(p => p.score),
        backgroundColor: 'rgba(0, 135, 81, 0.15)',
        borderColor: '#008751',
        borderWidth: 3,
        pointBackgroundColor: '#008751',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: '#008751'
      },
      {
        label: 'España',
        data: data.pilares.map(p => p.esp),
        backgroundColor: 'rgba(107, 114, 128, 0.1)',
        borderColor: '#6b7280',
        borderWidth: 2,
        borderDash: [5, 5],
        pointBackgroundColor: '#6b7280',
      },
    ],
  };

  const barData = {
    labels: data.dominios.map(d => d.name),
    datasets: [
      {
        label: 'Brecha (Andalucía - España)',
        data: data.dominios.map(d => d.gap),
        backgroundColor: data.dominios.map(d => d.gap >= 0 ? '#008751' : '#dc2626'),
        borderRadius: 4,
      },
    ],
  };

  return (
    <div className="min-h-screen bg-[#fcfcfc] text-slate-900 font-sans">
      {/* Top Navbar */}
      <nav className="bg-white border-b border-slate-100 px-6 py-4 flex justify-between items-center sticky top-0 z-50 shadow-sm">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-[#008751] rounded flex items-center justify-center text-white font-bold text-xl">A</div>
          <span className="text-xl font-bold tracking-tight text-[#008751]">Andalucía<span className="text-slate-800">27</span></span>
        </div>
        <div className="hidden md:flex gap-6 text-sm font-medium text-slate-600">
          <a href="#" className="hover:text-[#008751] transition-colors">Dashboard</a>
          <a href="#" className="hover:text-[#008751] transition-colors">Metodología</a>
          <a href="https://www.fundacionandalucia27.com" target="_blank" className="flex items-center gap-1 hover:text-[#008751] transition-colors">
            Fundación <ExternalLink size={14} />
          </a>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto p-6">
        {/* Header Hero */}
        <header className="mb-10">
          <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-6">
            <div>
              <h1 className="text-4xl font-extrabold text-slate-900 tracking-tight mb-2">
                Índice de Prosperidad Andaluz <span className="text-[#008751]">(IPA27)</span>
              </h1>
              <p className="text-lg text-slate-500 max-w-2xl">
                Monitorización trimestral del bienestar multidimensional. Un enfoque basado en techos fijos y convergencia regional.
              </p>
            </div>
            <div className="bg-[#008751] text-white rounded-2xl p-6 shadow-lg shadow-emerald-900/10 min-w-[240px]">
              <span className="text-xs uppercase tracking-widest opacity-80 font-bold">Score Global Andalucía</span>
              <div className="flex items-baseline gap-2 mt-1">
                <span className="text-4xl font-black">46.3</span>
                <span className="text-emerald-200 text-sm font-medium">/ 100</span>
              </div>
              <div className="mt-2 text-xs bg-white/10 py-1 px-2 rounded-full inline-block border border-white/10">
                Brecha: <span className="font-bold">-4.7 vs España</span>
              </div>
            </div>
          </div>
        </header>

        {/* Main Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">

          {/* Radar Chart Section */}
          <div className="lg:col-span-8 bg-white border border-slate-100 rounded-[2.5rem] p-8 shadow-sm radar-container">
            <div className="flex items-center justify-between mb-8">
              <div>
                <h2 className="text-2xl font-bold text-slate-800 flex items-center gap-2">
                  <TrendingUp className="text-[#008751]" size={24} /> Desempeño por Pilares
                </h2>
                <p className="text-slate-400 text-sm mt-1">Comparativa directa entre Andalucía y la media nacional.</p>
              </div>
              <div className="flex gap-6 text-sm font-bold">
                <span className="flex items-center gap-2"><div className="w-4 h-1 bg-[#008751]"></div> Andalucía</span>
                <span className="flex items-center gap-2"><div className="w-4 h-1 bg-slate-400"></div> España</span>
              </div>
            </div>
            <div className="aspect-square max-h-[550px] mx-auto">
              <Radar
                data={radarData}
                options={{
                  scales: {
                    r: {
                      angleLines: { color: '#f1f5f9' },
                      grid: { color: '#f1f5f9' },
                      pointLabels: {
                        color: '#475569',
                        font: { family: 'Outfit', size: 12, weight: '700' },
                        padding: 20
                      },
                      ticks: { display: false },
                      suggestedMin: 30,
                      suggestedMax: 70
                    }
                  },
                  plugins: { legend: { display: false } }
                }}
              />
            </div>
          </div>

          {/* Side Info */}
          <div className="lg:col-span-4 flex flex-col gap-8">

            {/* Brechas Dominio */}
            <div className="bg-white border border-slate-100 rounded-[2.5rem] p-8 shadow-sm">
              <h2 className="text-xl font-bold text-slate-800 mb-6 flex items-center gap-2">
                <Info className="text-[#008751]" size={20} /> Análisis de Brechas
              </h2>
              <div className="h-64">
                <Bar
                  data={barData}
                  options={{
                    indexAxis: 'y',
                    plugins: { legend: { display: false } },
                    scales: {
                      x: { display: false },
                      y: { grid: { display: false }, ticks: { color: '#475569', font: { weight: '600' } } }
                    },
                    maintainAspectRatio: false
                  }}
                />
              </div>
              <div className="mt-4 p-4 bg-slate-50 rounded-2xl text-xs text-slate-500 leading-relaxed font-medium">
                La brecha más acentuada se localiza en el dominio de <span className="text-slate-800 font-bold">Personas Empoderadas</span>, con un diferencial de -22.8 puntos.
              </div>
            </div>

            {/* Hallazgos */}
            <div className="bg-[#008751] rounded-[2.5rem] p-8 text-white shadow-xl shadow-emerald-900/10">
              <h2 className="text-xl font-bold mb-6 flex items-center gap-2">
                <Award size={20} /> Hallazgos Clave
              </h2>
              <div className="space-y-6">
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs font-black uppercase tracking-widest opacity-70">Dominio Líder</span>
                    <span className="text-xs px-2 py-0.5 bg-white/20 rounded-full">+3.3 gap</span>
                  </div>
                  <p className="text-lg font-bold">Sociedades Inclusivas</p>
                  <p className="text-sm opacity-80 mt-1 italic">Andalucía supera la media nacional en capital social y seguridad ciudadana.</p>
                </div>

                <div className="pt-6 border-t border-white/10">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs font-black uppercase tracking-widest opacity-70 italic text-rose-200">Alerta Estructural</span>
                  </div>
                  <p className="text-lg font-bold">Educación y Conocimiento</p>
                  <p className="text-sm opacity-80 mt-1">El abandono escolar y la baja inversión en I+D actúan como los principales frenos al crecimiento.</p>
                </div>
              </div>
            </div>

          </div>
        </div>

        {/* Footer Meta */}
        <div className="mt-16 flex flex-col md:flex-row justify-between items-center bg-white border border-slate-100 rounded-3xl p-8 gap-6 shadow-sm">
          <div className="flex items-center gap-4">
            <div className="flex -space-x-2">
              <div className="w-10 h-10 rounded-full border-2 border-white bg-slate-100 flex items-center justify-center text-xs font-bold text-slate-400">IE</div>
              <div className="w-10 h-10 rounded-full border-2 border-white bg-[#008751] flex items-center justify-center text-xs font-bold text-white">A27</div>
            </div>
            <div className="text-left">
              <p className="text-xs font-black text-slate-400 uppercase tracking-widest">Fuentes Oficiales</p>
              <p className="text-sm font-bold text-slate-600">IECA • INE • Min. Interior</p>
            </div>
          </div>
          <p className="text-slate-400 text-sm max-w-sm text-center md:text-right">
            Metodología de agregación geométrica basada en el Prosperity Index Framework adaptado para Andalucía.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

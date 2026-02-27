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
import { LayoutDashboard, TrendingUp, AlertTriangle, Award, Info } from 'lucide-react';

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
    // In a real scenario, we would parse the CSVs here. 
    // For this prototype, we'll simulate the data based on your 2025Q3 results.
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
    }, 800);
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-slate-900 text-white">
        <div className="animate-pulse text-xl">Cargando Dashboard IPA27...</div>
      </div>
    );
  }

  const radarData = {
    labels: data.pilares.map(p => p.name),
    datasets: [
      {
        label: 'Andalucía',
        data: data.pilares.map(p => p.score),
        backgroundColor: 'rgba(5, 150, 105, 0.2)',
        borderColor: '#10b981',
        borderWidth: 2,
        pointBackgroundColor: '#10b981',
      },
      {
        label: 'España',
        data: data.pilares.map(p => p.esp),
        backgroundColor: 'rgba(99, 102, 241, 0.2)',
        borderColor: '#6366f1',
        borderWidth: 2,
        pointBackgroundColor: '#6366f1',
      },
    ],
  };

  const barData = {
    labels: data.dominios.map(d => d.name),
    datasets: [
      {
        label: 'Brecha (Andalucía - España)',
        data: data.dominios.map(d => d.gap),
        backgroundColor: data.dominios.map(d => d.gap >= 0 ? '#10b981' : '#ef4444'),
        borderRadius: 8,
      },
    ],
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      {/* Header */}
      <header className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4 border-b border-slate-800 pb-6">
        <div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-emerald-400 to-teal-400 bg-clip-text text-transparent">
            IPA27: Índice de Prosperidad Andaluz
          </h1>
          <p className="text-slate-400 mt-1 flex items-center gap-2">
            <LayoutDashboard size={16} /> Dashboard de Resultados Multidimensionales • 2025Q3
          </p>
        </div>
        <div className="bg-emerald-500/10 border border-emerald-500/20 rounded-xl p-3 px-5">
          <span className="block text-xs uppercase tracking-wider text-emerald-500 font-semibold">IPA27 Global Andalucía</span>
          <span className="text-2xl font-bold text-emerald-400">46.3 <small className="text-sm font-normal text-emerald-500/60 font-mono">(-4.7 vs ESP)</small></span>
        </div>
      </header>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Radar Chart */}
        <div className="lg:col-span-7 bg-slate-900/50 border border-slate-800 rounded-3xl p-6 shadow-xl backdrop-blur-sm">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-semibold flex items-center gap-2">
              <TrendingUp className="text-emerald-400" size={20} /> Comparativa por Pilares
            </h2>
            <div className="flex gap-4 text-xs">
              <span className="flex items-center gap-1.5"><div className="w-3 h-3 bg-emerald-500 rounded-full"></div> Andalucía</span>
              <span className="flex items-center gap-1.5"><div className="w-3 h-3 bg-indigo-500 rounded-full"></div> España</span>
            </div>
          </div>
          <div className="aspect-square max-h-[500px] mx-auto opacity-90">
            <Radar 
              data={radarData}
              options={{
                scales: {
                  r: {
                    angleLines: { color: 'rgba(148, 163, 184, 0.1)' },
                    grid: { color: 'rgba(148, 163, 184, 0.1)' },
                    pointLabels: { color: '#94a3b8', font: { size: 11, weight: '500' } },
                    ticks: { display: false, backdropColor: 'transparent' },
                    suggestedMin: 30,
                    suggestedMax: 70
                  }
                },
                plugins: { legend: { display: false } }
              }}
            />
          </div>
        </div>

        {/* Right Sidebar */}
        <div className="lg:col-span-5 flex flex-col gap-6">
          
          {/* Dominios Brecha Card */}
          <div className="bg-slate-900/50 border border-slate-800 rounded-3xl p-6 shadow-xl">
            <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
              <Info className="text-emerald-400" size={20} /> Brechas por Dominio
            </h2>
            <div className="h-64">
              <Bar 
                data={barData}
                options={{
                  indexAxis: 'y',
                  plugins: { legend: { display: false } },
                  scales: {
                    x: { grid: { display: false }, ticks: { color: '#64748b' } },
                    y: { grid: { display: false }, ticks: { color: '#94a3b8' } }
                  },
                  maintainAspectRatio: false
                }}
              />
            </div>
          </div>

          {/* Critical Insights */}
          <div className="bg-gradient-to-br from-slate-900 to-slate-900/50 border border-slate-800 rounded-3xl p-6">
            <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
              <AlertTriangle className="text-amber-400" size={20} /> Hallazgos Críticos
            </h2>
            <div className="space-y-4">
              <div className="p-4 bg-emerald-500/5 border border-emerald-500/10 rounded-2xl">
                <div className="flex justify-between items-start">
                  <span className="text-sm font-medium text-emerald-400 uppercase tracking-tight">Fortaleza Regional</span>
                  <Award size={18} className="text-emerald-500" />
                </div>
                <p className="text-slate-200 mt-1 font-semibold">Sociedades Inclusivas</p>
                <p className="text-xs text-slate-400 mt-1">Ventaja de +3.3 puntos impulsada por capital social y participación ciudadana.</p>
              </div>

              <div className="p-4 bg-rose-500/5 border border-rose-500/10 rounded-2xl">
                <div className="flex justify-between items-start">
                  <span className="text-sm font-medium text-rose-400 uppercase tracking-tight">Cuello de Botella</span>
                  <AlertTriangle size={18} className="text-rose-500" />
                </div>
                <p className="text-slate-200 mt-1 font-semibold">Personas Empoderadas</p>
                <p className="text-xs text-slate-400 mt-1">Brecha crítica de -22.8 puntos en Educación y Conocimiento (I+D).</p>
              </div>
            </div>
          </div>

        </div>
      </div>

      <footer className="mt-12 text-center text-slate-500 text-sm border-t border-slate-900 pt-8">
        <p>Métodos: Techos Fijos y Agregación Geométrica • Desarrollado por Equipo IPA27</p>
        <p className="mt-2 text-xs">Los datos presentados son proyecciones basadas en modelos econométricos ARIMA y Chow-Lin.</p>
      </footer>
    </div>
  );
};

export default Dashboard;

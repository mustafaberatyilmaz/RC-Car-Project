
import React, { useState } from 'react';
import { Zap, Activity, Gauge } from 'lucide-react';

const TelemetryPanel: React.FC = () => {
  const [throttle, setThrottle] = useState(0);

  // Simplified handler for visualization
  const handleSliderTouch = (e: React.TouchEvent | React.MouseEvent) => {
    // In a real app, logic to calculate Y percentage would go here
  };

  return (
    <div className="flex flex-col w-[26%] min-w-[180px] h-full bg-[#121214] border border-white/5 rounded-2xl p-4 sm:p-5 shadow-2xl overflow-hidden">
      
      {/* Stats Group */}
      <div className="space-y-4 mb-4">
        <div className="p-3 bg-white/5 rounded-xl border border-white/5 space-y-3">
          {/* Health */}
          <div className="space-y-1.5">
            <div className="flex justify-between items-center px-1">
              <div className="flex items-center gap-1.5 opacity-60">
                <Activity className="w-3 h-3 text-green-400" />
                <span className="text-[9px] font-bold uppercase tracking-widest text-gray-300">Car Health</span>
              </div>
              <span className="text-[10px] font-bold text-green-400">98%</span>
            </div>
            <div className="h-1.5 w-full bg-black/40 rounded-full overflow-hidden">
              <div className="h-full bg-gradient-to-r from-green-600 to-green-400 w-[98%] shadow-[0_0_8px_rgba(74,222,128,0.3)]"></div>
            </div>
          </div>

          <div className="h-[1px] w-full bg-white/5"></div>

          {/* Battery */}
          <div className="space-y-1.5">
            <div className="flex justify-between items-center px-1">
              <div className="flex items-center gap-1.5 opacity-60">
                <Zap className="w-3 h-3 text-cyan-400" />
                <span className="text-[9px] font-bold uppercase tracking-widest text-gray-300">Battery</span>
              </div>
              <span className="text-[10px] font-bold text-cyan-400">76%</span>
            </div>
            <div className="flex gap-1 h-1.5 w-full">
              <div className="flex-1 bg-cyan-500 rounded-sm"></div>
              <div className="flex-1 bg-cyan-500 rounded-sm"></div>
              <div className="flex-1 bg-cyan-500 rounded-sm"></div>
              <div className="flex-1 bg-white/10 rounded-sm"></div>
            </div>
          </div>
        </div>
      </div>

      {/* Throttle Controls */}
      <div className="flex-1 flex flex-col items-center">
        {/* Speed Label */}
        <div className="flex items-center gap-1.5 mb-2 opacity-80">
          <Gauge className="w-3.5 h-3.5 text-cyan-400" />
          <span className="text-[10px] font-black uppercase tracking-[0.2em] text-cyan-400">Throttle</span>
        </div>

        {/* Speed Display */}
        <div className="w-full flex justify-center mb-3">
          <div className="bg-black/60 border border-white/5 px-4 py-2 rounded-xl flex items-baseline gap-1.5 min-w-[100px] justify-center shadow-inner">
            <span className="text-[10px] font-bold text-cyan-500/60 font-sans tracking-tight">PWR</span>
            <span className="text-2xl font-black font-mono text-white tabular-nums">00</span>
            <span className="text-[10px] font-bold text-gray-500">%</span>
          </div>
        </div>

        {/* Throttle Slider Container */}
        <div className="relative flex-1 w-full max-w-[80px] flex justify-center group">
          {/* Vertical Track */}
          <div className="relative w-14 h-full bg-[#18181b] border border-white/10 rounded-full overflow-hidden shadow-inner">
            {/* Center Fill (Forward/Neutral/Reverse) */}
            <div className="absolute top-1/2 left-0 right-0 h-0.5 bg-cyan-500/30"></div>
            
            {/* Tick Marks */}
            <div className="absolute inset-0 flex flex-col justify-between py-6 px-1 opacity-20 pointer-events-none">
               {[...Array(9)].map((_, i) => (
                 <div key={i} className={`w-full h-px ${i === 4 ? 'bg-cyan-400' : 'bg-white'}`}></div>
               ))}
            </div>

            {/* Labels */}
            <div className="absolute left-2 top-4 flex flex-col gap-0.5 text-[9px] font-black text-cyan-500/60 rotate-90 origin-left">
              <span>FWD</span>
            </div>
            <div className="absolute left-2 bottom-4 flex flex-col gap-0.5 text-[9px] font-black text-red-500/60 rotate-90 origin-left">
              <span>REV</span>
            </div>
          </div>

          {/* Draggable Handle (Simplified Visual) */}
          <div 
            className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-24 h-14 bg-[#1e1e21] border-2 border-cyan-500 rounded-xl flex items-center justify-center shadow-[0_0_20px_rgba(6,182,212,0.4)] cursor-pointer active:scale-95 transition-transform"
          >
            <div className="flex gap-1.5">
               <div className="w-1 h-6 bg-cyan-500/40 rounded-full"></div>
               <div className="w-1 h-6 bg-cyan-500/40 rounded-full"></div>
               <div className="w-1 h-6 bg-cyan-500/40 rounded-full"></div>
            </div>
            <div className="absolute -right-12 text-[10px] font-mono text-gray-500 hidden sm:flex flex-col items-start gap-1">
               <span>100</span>
               <span className="text-cyan-400">0</span>
               <span>-100</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TelemetryPanel;

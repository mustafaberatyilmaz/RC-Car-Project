
import React from 'react';
import { ArrowLeft, ArrowRight, ShieldAlert } from 'lucide-react';

const SteeringPanel: React.FC = () => {
  return (
    <div className="flex flex-col w-[28%] min-w-[200px] h-full bg-[#121214] border border-white/5 rounded-2xl p-4 sm:p-6 justify-between shadow-2xl">
      {/* Header */}
      <div className="flex flex-col items-center gap-2 opacity-80">
        <div className="flex items-center gap-2">
           <div className="grid grid-cols-2 gap-0.5 w-4">
              <div className="w-1.5 h-1.5 bg-cyan-400"></div>
              <div className="w-1.5 h-1.5 bg-cyan-400 opacity-40"></div>
              <div className="w-1.5 h-1.5 bg-cyan-400 opacity-40"></div>
              <div className="w-1.5 h-1.5 bg-cyan-400"></div>
           </div>
           <span className="text-[10px] sm:text-xs font-black tracking-[0.3em] text-cyan-400 uppercase">Steering</span>
        </div>
      </div>

      {/* Directional Controls - Increased gap and button sizes */}
      <div className="flex flex-1 items-center justify-center gap-8 sm:gap-12 py-4">
        <button className="group relative w-24 h-24 sm:w-36 sm:h-36 rounded-full border-2 border-cyan-500/40 flex items-center justify-center transition-all active:scale-90 active:bg-cyan-500/20 active:border-cyan-400 active:shadow-[0_0_40px_rgba(6,182,212,0.7)]">
          <ArrowLeft className="w-12 h-12 sm:w-20 sm:h-20 text-cyan-400 transition-transform group-active:-translate-x-2" />
          <div className="absolute inset-0 rounded-full border border-cyan-400/10 blur-[2px]"></div>
        </button>

        <button className="group relative w-24 h-24 sm:w-36 sm:h-36 rounded-full border-2 border-cyan-500/40 flex items-center justify-center transition-all active:scale-90 active:bg-cyan-500/20 active:border-cyan-400 active:shadow-[0_0_40px_rgba(6,182,212,0.7)]">
          <ArrowRight className="w-12 h-12 sm:w-20 sm:h-20 text-cyan-400 transition-transform group-active:translate-x-2" />
          <div className="absolute inset-0 rounded-full border border-cyan-400/10 blur-[2px]"></div>
        </button>
      </div>

      {/* Emergency Stop */}
      <button className="w-full h-20 sm:h-24 bg-red-500/10 border-2 border-red-500/80 rounded-xl flex items-center justify-center gap-3 sm:gap-4 transition-all active:bg-red-600 active:scale-[0.98] group relative overflow-hidden">
        <div className="absolute inset-0 bg-red-500/5 group-active:bg-transparent animate-pulse"></div>
        <div className="flex items-center justify-center w-10 h-10 sm:w-12 sm:h-12 bg-red-500 rounded-lg text-white shadow-lg">
          <ShieldAlert className="w-6 h-6 sm:w-8 sm:h-8" />
        </div>
        <div className="flex flex-col items-start uppercase leading-none">
          <span className="text-[10px] font-bold tracking-widest text-red-300 opacity-80">Emergency</span>
          <span className="text-xl sm:text-2xl font-black text-red-500 group-active:text-white tracking-wide">Stop</span>
        </div>
      </button>
    </div>
  );
};

export default SteeringPanel;


import React from 'react';
import { Camera, Signal, Maximize2 } from 'lucide-react';

const MainViewport: React.FC = () => {
  return (
    <div className="flex-1 relative bg-black rounded-2xl border border-white/10 overflow-hidden group">
      {/* Mock Video Feed */}
      <img 
        src="https://picsum.photos/seed/carview/1280/720" 
        alt="Camera Feed" 
        className="w-full h-full object-cover opacity-80 transition-transform duration-700 group-hover:scale-105"
      />
      
      {/* Overlays */}
      <div className="absolute inset-0 flex flex-col pointer-events-none">
        {/* Top Bar */}
        <div className="flex justify-between items-start p-4">
          <div className="bg-black/60 backdrop-blur-md px-3 py-1.5 rounded-lg border border-white/10 flex items-center gap-2 pointer-events-auto">
             <div className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse shadow-[0_0_8px_rgba(6,182,212,0.8)]"></div>
             <span className="text-[10px] font-bold uppercase tracking-wider text-cyan-100">Live • Connected</span>
          </div>
          <div className="bg-black/60 backdrop-blur-md px-3 py-1.5 rounded-lg border border-white/10 flex items-center gap-2 pointer-events-auto">
             <Signal className="w-3.5 h-3.5 text-green-400" />
             <span className="text-[10px] font-mono text-white">-62dBm</span>
          </div>
        </div>

        {/* Center Crosshair */}
        <div className="flex-1 flex items-center justify-center">
          <div className="relative w-20 h-20 opacity-30">
            <div className="absolute top-0 left-1/2 -translate-x-1/2 w-0.5 h-3 bg-cyan-400"></div>
            <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-0.5 h-3 bg-cyan-400"></div>
            <div className="absolute left-0 top-1/2 -translate-y-1/2 h-0.5 w-3 bg-cyan-400"></div>
            <div className="absolute right-0 top-1/2 -translate-y-1/2 h-0.5 w-3 bg-cyan-400"></div>
            <div className="absolute inset-4 border border-cyan-400 rounded-full"></div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="flex justify-between items-end p-4 bg-gradient-to-t from-black/80 to-transparent">
          <div className="flex flex-col">
            <div className="flex items-center gap-2 mb-1">
              <Camera className="w-4 h-4 text-cyan-400" />
              <span className="text-xs font-black uppercase text-white tracking-widest">Main Cam</span>
            </div>
            <span className="text-[10px] font-mono text-gray-400 tracking-tighter">1920x1080 @ 60 FPS</span>
          </div>
          <button className="w-10 h-10 flex items-center justify-center rounded-lg bg-white/10 hover:bg-white/20 text-white transition-colors pointer-events-auto">
            <Maximize2 className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default MainViewport;

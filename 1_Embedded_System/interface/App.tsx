
import React, { useState, useEffect } from 'react';
import SteeringPanel from './components/SteeringPanel';
import MainViewport from './components/MainViewport';
import TelemetryPanel from './components/TelemetryPanel';

const App: React.FC = () => {
  const [orientation, setOrientation] = useState<string>(window.innerWidth > window.innerHeight ? 'landscape' : 'portrait');

  useEffect(() => {
    const handleResize = () => {
      setOrientation(window.innerWidth > window.innerHeight ? 'landscape' : 'portrait');
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <div className="flex h-screen w-screen bg-[#09090b] text-white overflow-hidden p-2 sm:p-4 gap-2 sm:gap-4 select-none">
      {/* Landscape Orientation Warning (Simplified Overlay) */}
      {orientation === 'portrait' && (
        <div className="fixed inset-0 z-50 bg-black flex flex-col items-center justify-center p-8 text-center">
          <div className="w-16 h-16 border-2 border-cyan-500 rounded-lg animate-spin-slow mb-4 flex items-center justify-center">
            <svg className="w-8 h-8 text-cyan-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
          </div>
          <h1 className="text-xl font-bold text-cyan-400">Please Rotate Your Device</h1>
          <p className="text-gray-400 mt-2">This controller is designed for landscape mode.</p>
        </div>
      )}

      {/* Left Panel: Steering & Emergency */}
      <SteeringPanel />

      {/* Middle: Main Camera Viewport */}
      <MainViewport />

      {/* Right Panel: Telemetry & Throttle */}
      <TelemetryPanel />
    </div>
  );
};

export default App;

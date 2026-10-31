import React, { useEffect, useRef, useState } from 'react';
import L from 'leaflet';
import { Map as MapIcon } from 'lucide-react';
import { MOCK_STATIONS } from '../../services/mockData';
import { getAqiColor, getAqiBadgeClasses } from '../../utils/aqiUtils';
import { DemoBadge } from '../../components/common/DemoBadge';
import { Station } from '../../types/aqi';

interface InteractiveMapProps {
  stations?: Station[];
}

export const InteractiveMap: React.FC<InteractiveMapProps> = ({
  stations = MOCK_STATIONS,
}) => {
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<L.Map | null>(null);
  const [selectedStation, setSelectedStation] = useState<Station | null>(stations[0] || null);

  useEffect(() => {
    if (!mapContainerRef.current) return;

    if (mapInstanceRef.current) {
      mapInstanceRef.current.remove();
    }

    const map = L.map(mapContainerRef.current, {
      center: [28.6139, 77.2090],
      zoom: 11,
      zoomControl: true,
      attributionControl: true,
    });

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 18,
      attribution: '&copy; OpenStreetMap contributors | EcoPredict',
    }).addTo(map);

    stations.forEach((station) => {
      const color = getAqiColor(station.category);

      L.circle([station.lat, station.lng], {
        radius: 2200,
        fillColor: color,
        fillOpacity: 0.15,
        stroke: false,
      }).addTo(map);

      const marker = L.circleMarker([station.lat, station.lng], {
        radius: 12,
        fillColor: color,
        color: '#ffffff',
        weight: 2,
        opacity: 0.95,
        fillOpacity: 0.85,
      }).addTo(map);

      marker.bindPopup(`
        <div style="font-family: inherit; font-size: 13px;">
          <div style="font-weight: 700; color: #0f172a; margin-bottom: 4px;">${station.name}</div>
          <div style="margin-bottom: 2px;">AQI: <strong style="color: ${color};">${station.aqi}</strong> (${station.category})</div>
          <div style="color: #64748b; font-size: 11px;">Main: ${station.mainPollutant}</div>
          <div style="color: #64748b; font-size: 11px;">Status: ${station.status}</div>
        </div>
      `);

      marker.on('click', () => {
        setSelectedStation(station);
      });
    });

    mapInstanceRef.current = map;

    return () => {
      map.remove();
      mapInstanceRef.current = null;
    };
  }, [stations]);

  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-xl overflow-hidden shadow-sm flex flex-col h-full">
      {/* Header bar */}
      <div className="p-4 border-b border-slate-800 flex flex-wrap items-center justify-between gap-3">
        <div>
          <div className="flex items-center space-x-2">
            <MapIcon className="w-4 h-4 text-emerald-400" />
            <h2 className="text-base font-bold text-white">Interactive AQI Map</h2>
            <DemoBadge label="Monitoring Stations" />
          </div>
          <p className="text-xs text-slate-400 mt-0.5">
            Live pollution hotspots & monitoring stations across Delhi NCR
          </p>
        </div>

        <div className="flex items-center space-x-2">
          <span className="text-xs text-slate-400 bg-slate-800/80 px-2.5 py-1 rounded border border-slate-700/60 font-mono">
            {stations.length} Stations Active
          </span>
        </div>
      </div>

      {/* Map display */}
      <div className="relative flex-1 min-h-[380px] w-full">
        <div ref={mapContainerRef} className="absolute inset-0 z-0" />

        {/* Legend Overlay */}
        <div className="absolute bottom-3 left-3 z-[1000] bg-slate-950/85 backdrop-blur border border-slate-800 rounded-lg p-2.5 text-xs text-slate-300 shadow-lg">
          <div className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 mb-1.5">
            AQI Severity Legend
          </div>
          <div className="grid grid-cols-2 gap-x-3 gap-y-1 text-[11px]">
            <div className="flex items-center space-x-1.5">
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 inline-block" />
              <span>Good (0-50)</span>
            </div>
            <div className="flex items-center space-x-1.5">
              <span className="w-2.5 h-2.5 rounded-full bg-yellow-500 inline-block" />
              <span>Moderate (51-100)</span>
            </div>
            <div className="flex items-center space-x-1.5">
              <span className="w-2.5 h-2.5 rounded-full bg-orange-500 inline-block" />
              <span>Poor (101-200)</span>
            </div>
            <div className="flex items-center space-x-1.5">
              <span className="w-2.5 h-2.5 rounded-full bg-red-500 inline-block" />
              <span>Very Poor (201-300)</span>
            </div>
            <div className="flex items-center space-x-1.5">
              <span className="w-2.5 h-2.5 rounded-full bg-purple-500 inline-block" />
              <span>Severe (301-400)</span>
            </div>
            <div className="flex items-center space-x-1.5">
              <span className="w-2.5 h-2.5 rounded-full bg-rose-900 inline-block" />
              <span>Hazardous (400+)</span>
            </div>
          </div>
        </div>

        {/* Selected Station Quick Summary Drawer */}
        {selectedStation && (
          <div className="absolute top-3 right-3 z-[1000] bg-slate-950/90 backdrop-blur border border-slate-800 rounded-lg p-3 text-xs text-slate-200 shadow-xl max-w-xs">
            <div className="flex items-center justify-between mb-1.5">
              <span className="text-[11px] uppercase tracking-wider text-slate-400 font-semibold">
                Station Inspect
              </span>
              <span
                className={`text-[10px] px-2 py-0.5 rounded font-semibold border ${getAqiBadgeClasses(
                  selectedStation.category
                )}`}
              >
                {selectedStation.category}
              </span>
            </div>
            <div className="font-bold text-sm text-white">{selectedStation.name}</div>
            <div className="flex items-baseline space-x-2 mt-1">
              <span className="text-2xl font-bold font-mono text-emerald-400">
                {selectedStation.aqi}
              </span>
              <span className="text-slate-400 text-xs">AQI Index</span>
            </div>
            <div className="text-[11px] text-slate-400 mt-1">
              Primary: <span className="text-slate-200">{selectedStation.mainPollutant}</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

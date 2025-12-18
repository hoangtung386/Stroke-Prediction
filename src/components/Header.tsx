import React from 'react';
import { Activity } from 'lucide-react';

export const Header: React.FC = () => {
    return (
        <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between items-center h-16">
                    <div className="flex items-center gap-2">
                        <div className="bg-sky-500 p-2 rounded-lg text-white">
                            <Activity size={24} />
                        </div>
                        <div>
                            <h1 className="text-xl font-bold text-gray-900 leading-tight">StrokeGuard AI</h1>
                            <p className="text-xs text-gray-500">Advanced Risk Assessment System</p>
                        </div>
                    </div>
                    <div className="hidden md:flex items-center gap-6 text-sm font-medium text-gray-500">
                        <span>Powered by ML Models</span>
                        <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-xs">System Active</span>
                    </div>
                </div>
            </div>
        </header>
    );
};

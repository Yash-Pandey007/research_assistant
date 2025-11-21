import React from 'react';

function ResultDisplay({ result }) {
    if (!result) return null;

    return (
        <div className="mt-8 p-6 bg-white rounded-lg shadow-lg border border-gray-200">
            <div className="mb-4 pb-4 border-b border-gray-200">
                <p className="text-sm text-indigo-600 font-semibold">✨ Your Research Assistant has found something for you:</p>
            </div>

            <h2 className="text-2xl font-bold mb-4 text-gray-800">Answer</h2>
            <div className="prose max-w-none text-gray-700 whitespace-pre-wrap">
                {result.answer}
            </div>

            {result.sources && result.sources.length > 0 && (
                <div className="mt-6">
                    <h3 className="text-lg font-semibold mb-3 text-gray-800">Sources</h3>
                    <ul className="space-y-2">
                        {result.sources.map((source, index) => (
                            <li key={index} className="text-sm">
                                <a
                                    href={source.url}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="text-blue-600 hover:text-blue-800 hover:underline flex items-start"
                                >
                                    <span className="mr-2">[{index + 1}]</span>
                                    <span>{source.title}</span>
                                </a>
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
}

export default ResultDisplay;

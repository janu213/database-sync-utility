import React, { useState } from 'react';
import api from '../api';

const QueryEditor = ({ connection, onPreview }) => {
    const [query, setQuery] = useState('SELECT TOP 10 * FROM Users');
    const [loading, setLoading] = useState(false);

    const handleRun = async () => {
        if (!connection) return alert('Please connect to source DB first');
        setLoading(true);
        try {
            const res = await api.post('/api/preview-query', { connection, query });
            onPreview(res.data.data, query);
        } catch (err) {
            alert('Query failed: ' + err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="card">
            <div className="flex justify-between items-center mb-4">
                <h3>Query Editor</h3>
                <button className="btn btn-primary" onClick={handleRun} disabled={loading}>
                    {loading ? 'Running...' : 'Run Query'}
                </button>
            </div>
            <textarea
                rows={5}
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="SELECT * FROM ..."
                style={{ fontFamily: 'monospace' }}
            />
        </div>
    );
};

export default QueryEditor;

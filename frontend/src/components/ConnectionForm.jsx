import React, { useState } from 'react';
import api from '../api';

const ConnectionForm = ({ type, onConnect }) => {
    const [formData, setFormData] = useState({
        type: type,
        host: 'localhost',
        port: type === 'mssql' ? 1433 : 3306,
        user: '',
        password: '',
        database: ''
    });
    const [status, setStatus] = useState(null);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleTest = async () => {
        setStatus('testing');
        try {
            await api.post('/api/test-connection', formData);
            setStatus('success');
            onConnect(formData);
        } catch (err) {
            console.error(err);
            setStatus('error');
        }
    };

    return (
        <div className="card">
            <h3>{type === 'mssql' ? 'Source (MSSQL)' : 'Target (MySQL)'}</h3>
            <div className="grid grid-cols-2">
                <label>
                    Host:
                    <input name="host" value={formData.host} onChange={handleChange} />
                </label>
                <label>
                    Port:
                    <input name="port" type="number" value={formData.port} onChange={handleChange} />
                </label>
                <label>
                    User:
                    <input name="user" value={formData.user} onChange={handleChange} />
                </label>
                <label>
                    Password:
                    <input name="password" type="password" value={formData.password} onChange={handleChange} />
                </label>
                <label>
                    Database:
                    <input name="database" value={formData.database} onChange={handleChange} />
                </label>
            </div>
            <div style={{ marginTop: '1rem', display: 'flex', gap: '1rem', alignItems: 'center' }}>
                <button className="btn btn-secondary" onClick={handleTest}>
                    {status === 'testing' ? 'Testing...' : 'Test Connection'}
                </button>
                {status === 'success' && <span style={{ color: 'var(--accent-success)' }}>✓ Connected</span>}
                {status === 'error' && <span style={{ color: 'var(--accent-danger)' }}>✗ Failed</span>}
            </div>
        </div>
    );
};

export default ConnectionForm;

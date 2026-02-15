import React, { useState } from 'react';

const JobScheduler = ({ onSchedule }) => {
    const [name, setName] = useState('');
    const [interval, setInterval] = useState(60);

    const handleSave = () => {
        if (!name) return alert('Please enter a job name');
        onSchedule({ name, schedule_interval: parseInt(interval) });
    };

    return (
        <div className="card">
            <h3>Job Schedule</h3>
            <div className="grid grid-cols-2">
                <label>
                    Job Name:
                    <input
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        placeholder="e.g. Daily User Sync"
                    />
                </label>
                <label>
                    Run Every (minutes):
                    <input
                        type="number"
                        min="1"
                        value={interval}
                        onChange={(e) => setInterval(e.target.value)}
                    />
                </label>
            </div>
            <div>
                <button className="btn btn-primary" onClick={handleSave} style={{ marginTop: '1rem' }}>
                    Save & Activate Job
                </button>
            </div>
        </div>
    );
};

export default JobScheduler;

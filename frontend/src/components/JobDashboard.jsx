import React, { useEffect, useState } from 'react';
import api from '../api';

const JobDashboard = ({ onEdit }) => {
    const [jobs, setJobs] = useState([]);
    const [loading, setLoading] = useState(true);

    const fetchJobs = async () => {
        try {
            const res = await api.get('/api/jobs');
            setJobs(res.data);
        } catch (err) {
            console.error("Failed to fetch jobs", err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchJobs();
        const interval = setInterval(fetchJobs, 5000); // Poll every 5 seconds
        return () => clearInterval(interval);
    }, []);

    const handleDelete = async (id) => {
        if (!window.confirm("Are you sure you want to delete this job?")) return;
        try {
            await api.delete(`/api/jobs/${id}`);
            fetchJobs();
        } catch (err) {
            alert("Failed to delete job");
        }
    };

    const handleToggle = async (id) => {
        try {
            await api.post(`/api/jobs/${id}/toggle`);
            fetchJobs();
        } catch (err) {
            alert("Failed to toggle job");
        }
    };

    if (loading && jobs.length === 0) return <div>Loading jobs...</div>;

    return (
        <div className="card">
            <h3>Job Dashboard</h3>
            <div className="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Schedule</th>
                            <th>Status</th>
                            <th>Last Run</th>
                            <th>Result</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {jobs.length === 0 ? (
                            <tr><td colSpan="6" style={{ textAlign: 'center' }}>No jobs created yet.</td></tr>
                        ) : (
                            jobs.map(job => (
                                <tr key={job.id}>
                                    <td><strong>{job.name}</strong></td>
                                    <td>Every {job.schedule_interval} min</td>
                                    <td>
                                        <span style={{
                                            color: job.status === 'active' ? 'var(--accent-success)' : 'var(--text-secondary)'
                                        }}>
                                            {job.status.toUpperCase()}
                                        </span>
                                    </td>
                                    <td>{job.last_run_time ? new Date(job.last_run_time).toLocaleString() : 'Never'}</td>
                                    <td>
                                        {job.last_run_status === 'success' && <span style={{ color: 'var(--accent-success)' }}>Success</span>}
                                        {job.last_run_status === 'failed' && <span style={{ color: 'var(--accent-danger)' }} title={job.last_run_message}>Failed</span>}
                                        {!job.last_run_status && '-'}
                                    </td>
                                    <td>
                                        <div className="flex gap-2">
                                            <button className="btn btn-secondary" onClick={() => handleToggle(job.id)} style={{ padding: '0.25rem 0.5rem', fontSize: '0.75rem' }}>
                                                {job.status === 'active' ? 'Pause' : 'Resume'}
                                            </button>
                                            <button className="btn btn-primary" onClick={() => onEdit(job)} style={{ padding: '0.25rem 0.5rem', fontSize: '0.75rem' }}>
                                                Edit
                                            </button>
                                            <button className="btn btn-danger" onClick={() => handleDelete(job.id)} style={{ padding: '0.25rem 0.5rem', fontSize: '0.75rem' }}>
                                                Delete
                                            </button>
                                        </div>
                                    </td>
                                </tr>
                            ))
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default JobDashboard;

import React, { useState } from 'react';
import ConnectionForm from './components/ConnectionForm';
import QueryEditor from './components/QueryEditor';
import PreviewTable from './components/PreviewTable';
import MappingConfig from './components/MappingConfig';
import JobScheduler from './components/JobScheduler';
import JobDashboard from './components/JobDashboard';
import api from './api';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard'); // 'new-job' or 'dashboard'

  const [sourceConn, setSourceConn] = useState(null);
  const [targetConn, setTargetConn] = useState(null);
  const [previewData, setPreviewData] = useState([]);
  const [query, setQuery] = useState('');
  const [targetTable, setTargetTable] = useState('');
  const [mapping, setMapping] = useState({});
  const [step, setStep] = useState(1); // 1: Connect, 2: Query, 3: Map, 4: Schedule

  const [editingJobId, setEditingJobId] = useState(null);

  const handleSourceConnect = (conn) => {
    setSourceConn(conn);
  };

  const handleTargetConnect = (conn) => {
    setTargetConn(conn);
    if (sourceConn) setStep(2);
  };

  const handlePreview = (data, q) => {
    setPreviewData(data);
    setQuery(q);
    setStep(3);
  };

  const handleMap = (table, map) => {
    setTargetTable(table);
    setMapping(map);
  };

  const handleEdit = (job) => {
    setEditingJobId(job.id);
    setSourceConn(job.source_connection);
    setTargetConn(job.target_connection);
    setQuery(job.query);
    setTargetTable(job.target_table);
    setMapping(job.mapping);
    setPreviewData([]); // Reset preview or fetch if needed (optional)
    setStep(4); // Jump to schedule/review step
    setActiveTab('new-job');
  };

  const handleSchedule = async (scheduleData) => {
    if (!sourceConn || !targetConn || !query || !targetTable) {
      return alert("Missing required configuration");
    }

    const jobData = {
      ...scheduleData,
      source_connection: sourceConn,
      target_connection: targetConn,
      query,
      target_table: targetTable,
      mapping
    };

    try {
      if (editingJobId) {
        await api.put(`/api/jobs/${editingJobId}`, jobData);
        alert('Job updated successfully!');
      } else {
        await api.post('/api/jobs', jobData);
        alert('Job created successfully!');
      }

      setActiveTab('dashboard'); // Switch to dashboard
      // Reset form state
      setStep(1);
      setPreviewData([]);
      setEditingJobId(null);
      setSourceConn(null);
      setTargetConn(null);
      setQuery('');
      setTargetTable('');
      setMapping({});
    } catch (err) {
      alert('Failed to save job: ' + err.message);
    }
  };

  return (
    <div className="container">
      <header style={{ marginBottom: '2rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h1>Database Sync Utility</h1>
          <p className="text-secondary">Sync data from MSSQL to MySQL effortlessly.</p>
        </div>
        <div className="flex">
          <button
            className={`btn ${activeTab === 'dashboard' ? 'btn-primary' : 'btn-secondary'}`}
            onClick={() => setActiveTab('dashboard')}
          >
            Dashboard
          </button>
          <button
            className={`btn ${activeTab === 'new-job' ? 'btn-primary' : 'btn-secondary'}`}
            onClick={() => setActiveTab('new-job')}
          >
            + New Job
          </button>
        </div>
      </header>

      {activeTab === 'dashboard' ? (
        <div className="animate-fade-in">
          <JobDashboard onEdit={handleEdit} />
        </div>
      ) : (
        <div className="grid animate-fade-in">
          {/* Step 1: Connections */}
          <div className="grid grid-cols-2 gap-4">
            <ConnectionForm type="mssql" onConnect={handleSourceConnect} />
            <ConnectionForm type="mysql" onConnect={handleTargetConnect} />
          </div>

          {/* Step 2: Query */}
          {step >= 2 && (
            <div className="animate-fade-in">
              <QueryEditor connection={sourceConn} onPreview={handlePreview} />
            </div>
          )}

          {/* Step 3: Preview & Mapping */}
          {step >= 3 && (
            <div className="animate-fade-in grid gap-4">
              <PreviewTable data={previewData} />
              <MappingConfig
                sourceColumns={previewData.length > 0 ? Object.keys(previewData[0]) : []}
                onMap={handleMap}
              />
              {/* Step 4: Schedule */}
              <JobScheduler onSchedule={handleSchedule} />
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;

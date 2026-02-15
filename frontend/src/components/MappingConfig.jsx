import React, { useState, useEffect } from 'react';

const MappingConfig = ({ sourceColumns, onMap }) => {
    const [targetTable, setTargetTable] = useState('');
    const [mapping, setMapping] = useState({});

    useEffect(() => {
        // Auto-map if possible (same name)
        const initialMapping = {};
        sourceColumns.forEach(col => {
            initialMapping[col] = col;
        });
        setMapping(initialMapping);
    }, [sourceColumns]);

    const handleMappingChange = (sourceCol, targetCol) => {
        const newMapping = { ...mapping, [sourceCol]: targetCol };
        setMapping(newMapping);
        onMap(targetTable, newMapping);
    };

    const handleTableChange = (e) => {
        setTargetTable(e.target.value);
        onMap(e.target.value, mapping);
    };

    if (!sourceColumns.length) return null;

    return (
        <div className="card">
            <h3>Column Mapping</h3>
            <div className="form-group">
                <label>Target Table Name (MySQL):</label>
                <input
                    value={targetTable}
                    onChange={handleTableChange}
                    placeholder="e.g. synced_users"
                />
            </div>
            <div className="grid grid-cols-2">
                <div>
                    <h4>Source Column</h4>
                </div>
                <div>
                    <h4>Target Column</h4>
                </div>
                {sourceColumns.map(col => (
                    <React.Fragment key={col}>
                        <div className="flex items-center">
                            <span>{col}</span>
                        </div>
                        <div>
                            <input
                                value={mapping[col] || ''}
                                onChange={(e) => handleMappingChange(col, e.target.value)}
                                placeholder="Target column name"
                            />
                        </div>
                    </React.Fragment>
                ))}
            </div>
        </div>
    );
};

export default MappingConfig;

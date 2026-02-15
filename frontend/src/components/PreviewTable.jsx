import React from 'react';

const PreviewTable = ({ data }) => {
    if (!data || data.length === 0) return <div className="text-secondary">No data to preview</div>;

    const headers = Object.keys(data[0]);

    return (
        <div className="card">
            <h3>Preview Results</h3>
            <div className="table-container">
                <table>
                    <thead>
                        <tr>
                            {headers.map((h) => (
                                <th key={h}>{h}</th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {data.map((row, i) => (
                            <tr key={i}>
                                {headers.map((h) => (
                                    <td key={h}>{row[h]}</td>
                                ))}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default PreviewTable;

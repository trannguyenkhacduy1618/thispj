import React from "react";

const ReportTable = ({ reports }) => {
  if (!reports || reports.length === 0) {
    return <p>No reports available.</p>;
  }

  return (
    <table className="report-table">
      <thead>
        <tr>
          <th>Task</th>
          <th>Assigned To</th>
          <th>Date</th>
          <th>Time Spent (hh:mm:ss)</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        {reports.map((report) => (
          <tr key={report.task_id + report.date}>
            <td>{report.task_title}</td>
            <td>{report.assigned_to_name || "Unassigned"}</td>
            <td>{new Date(report.date).toLocaleDateString()}</td>
            <td>
              {Math.floor(report.seconds / 3600)
                .toString()
                .padStart(2, "0")}
              :
              {Math.floor((report.seconds % 3600) / 60)
                .toString()
                .padStart(2, "0")}
              :
              {(report.seconds % 60).toString().padStart(2, "0")}
            </td>
            <td>{report.status}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default ReportTable;

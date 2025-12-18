import React, { useState, useEffect } from "react";
import Stopwatch from "./Stopwatch";
import TaskCard from "./TaskCard";
import ReportTable from "./ReportTable";
import Statistics from "./Statistics";
import axios from "axios";

const Dashboard = () => {
  const [tasks, setTasks] = useState([]);
  const [reports, setReports] = useState([]);
  const [selectedTaskId, setSelectedTaskId] = useState(null);

  // Lấy danh sách tasks
  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const res = await axios.get("/api/tasks/my/assigned"); // API của backend
        setTasks(res.data);
      } catch (error) {
        console.error("Error fetching tasks:", error);
      }
    };
    fetchTasks();
  }, []);

  // Lấy báo cáo
  useEffect(() => {
    const fetchReports = async () => {
      try {
        const res = await axios.get("/api/reports/daily"); // API backend trả về báo cáo
        setReports(res.data);
      } catch (error) {
        console.error("Error fetching reports:", error);
      }
    };
    fetchReports();
  }, []);

  return (
    <div className="dashboard-container">
      <h1>Dashboard</h1>

      <section className="stopwatch-section">
        <h2>Stopwatch</h2>
        <Stopwatch taskId={selectedTaskId} />
      </section>

      <section className="tasks-section">
        <h2>My Tasks</h2>
        <div className="task-cards">
          {tasks.map((task) => (
            <TaskCard
              key={task.id}
              task={task}
              onSelect={() => setSelectedTaskId(task.id)}
            />
          ))}
        </div>
      </section>

      <section className="reports-section">
        <h2>Daily Reports</h2>
        <ReportTable reports={reports} />
      </section>

      <section className="statistics-section">
        <h2>Statistics</h2>
        <Statistics reports={reports} />
      </section>
    </div>
  );
};

export default Dashboard;

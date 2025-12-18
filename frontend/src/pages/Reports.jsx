import { useEffect, useState } from "react";
import ReportTable from "../components/ReportTable";
import api from "../services/api";
import "../styles/report.css";
const Reports = () => {
  const [date, setDate] = useState(() =>
    new Date().toISOString().split("T")[0]
  );
  const [dailyReport, setDailyReport] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchDailyReport();
    fetchStatistics();
    // eslint-disable-next-line
  }, [date]);

  const fetchDailyReport = async () => {
    try {
      setLoading(true);
      const res = await api.get("/reports/daily", {
        params: { date },
      });
      setDailyReport(res.data);
      setError("");
    } catch (err) {
      setError("Không thể tải daily report");
    } finally {
      setLoading(false);
    }
  };

  const fetchStatistics = async () => {
    try {
      const res = await api.get("/reports/statistics", {
        params: {
          from: date,
          to: date,
        },
      });
      setStats(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">📊 Báo cáo thời gian làm việc</h1>

      {/* Date filter */}
      <div className="mb-4 flex items-center gap-3">
        <label className="font-medium">Chọn ngày:</label>
        <input
          type="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
          className="border rounded px-2 py-1"
        />
      </div>

      {/* Statistics */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="border rounded p-4 bg-gray-50">
            <p className="text-sm text-gray-500">Tổng thời gian</p>
            <p className="text-xl font-bold">
              {stats.total_hours} giờ
            </p>
          </div>

          <div className="border rounded p-4 bg-gray-50">
            <p className="text-sm text-gray-500">Số task</p>
            <p className="text-xl font-bold">
              {stats.tasks_count}
            </p>
          </div>

          <div className="border rounded p-4 bg-gray-50">
            <p className="text-sm text-gray-500">Thời gian trung bình / task</p>
            <p className="text-xl font-bold">
              {stats.avg_hours_per_task} giờ
            </p>
          </div>
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="text-red-500 mb-4">{error}</div>
      )}

      {/* Daily report table */}
      {loading ? (
        <p>Đang tải dữ liệu...</p>
      ) : (
        <ReportTable data={dailyReport} />
      )}
    </div>
  );
};

export default Reports;

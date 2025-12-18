import api from "./api";

/**
 * ============================
 * ⏱️ TIME TRACKING / STOPWATCH
 * ============================
 */

/**
 * Bắt đầu đo thời gian cho task
 */
const startTimer = async (taskId) => {
  const response = await api.post("/time/start", {
    task_id: taskId,
  });
  return response.data;
};

/**
 * Dừng đo thời gian (stopwatch)
 */
const stopTimer = async (entryId) => {
  const response = await api.post("/time/stop", {
    entry_id: entryId,
  });
  return response.data;
};

/**
 * Lấy time entry đang chạy (nếu có)
 */
const getRunningEntry = async () => {
  const response = await api.get("/time/running");
  return response.data;
};

/**
 * Lấy time entries của task
 */
const getTaskTimeEntries = async (taskId) => {
  const response = await api.get(`/time/task/${taskId}`);
  return response.data;
};

/**
 * ============================
 * 📅 DAILY REPORT
 * ============================
 */

/**
 * Báo cáo thời gian theo ngày
 */
const getDailyReport = async (date) => {
  const response = await api.get("/reports/daily", {
    params: { date },
  });
  return response.data;
};

/**
 * ============================
 * 📊 STATISTICS
 * ============================
 */

/**
 * Thống kê theo khoảng thời gian
 */
const getStatistics = async (startDate, endDate) => {
  const response = await api.get("/reports/statistics", {
    params: {
      start_date: startDate,
      end_date: endDate,
    },
  });
  return response.data;
};

export default {
  startTimer,
  stopTimer,
  getRunningEntry,
  getTaskTimeEntries,
  getDailyReport,
  getStatistics,
};

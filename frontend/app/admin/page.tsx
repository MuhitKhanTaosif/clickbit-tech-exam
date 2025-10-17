"use client";
import { useEffect, useState } from "react";
import { adminRequests, adminUpdateRequest } from "@/lib/api";

export default function AdminPage() {
  const [token, setToken] = useState<string | null>(null);
  const [rows, setRows] = useState<any[]>([]);
  const [status, setStatus] = useState<string>("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  async function load() {
    if (!token) return;
    setLoading(true);
    try {
      const data = await adminRequests(token, status || undefined);
      setRows(data);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    const t = localStorage.getItem("token");
    if (!t) {
      window.location.href = "/auth/login";
      return;
    }
    setToken(t);
  }, []);

  useEffect(() => {
    load();
  }, [token, status]);

  async function update(id: string, next: string) {
    if (!token) return;
    await adminUpdateRequest(token, id, next);
    await load();
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-10">
      <h1 className="text-3xl font-bold mb-6">Admin Dashboard</h1>
      <div className="mb-4 flex gap-3 items-center">
        <label className="text-sm">Filter status</label>
        <select
          className="border rounded px-2 py-2"
          value={status}
          onChange={(e) => setStatus(e.target.value)}
        >
          <option value="">All</option>
          <option value="pending">Pending</option>
          <option value="approved">Approved</option>
          <option value="rejected">Rejected</option>
          <option value="completed">Completed</option>
        </select>
      </div>
      {loading && <p>Loading...</p>}
      {error && <p className="text-red-600">{error}</p>}
      <div className="space-y-3">
        {rows.map((r) => (
          <div
            key={r.id}
            className="border rounded p-4 grid grid-cols-5 gap-3 items-center"
          >
            <div className="col-span-2">
              <div className="text-sm text-gray-600">User: {r.user_id}</div>
              <div className="text-sm text-gray-600">
                Service: {r.service_id}
              </div>
            </div>
            <div>
              Status: <span className="font-medium">{r.status}</span>
            </div>
            <div className="text-sm text-gray-500">
              {new Date(r.request_date).toLocaleString()}
            </div>
            <div className="flex gap-2 justify-end">
              <button
                className="px-3 py-1 rounded border"
                onClick={() => update(r.id, "approved")}
              >
                Approve
              </button>
              <button
                className="px-3 py-1 rounded border"
                onClick={() => update(r.id, "rejected")}
              >
                Reject
              </button>
              <button
                className="px-3 py-1 rounded border"
                onClick={() => update(r.id, "completed")}
              >
                Complete
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

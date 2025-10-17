"use client";
import { useEffect, useState } from "react";
import { myRequests, getServices, createRequest, ApiService } from "@/lib/api";

export default function DashboardPage() {
  const [token, setToken] = useState<string | null>(null);
  const [services, setServices] = useState<ApiService[]>([]);
  const [selected, setSelected] = useState<number | "">("");
  const [notes, setNotes] = useState("");
  const [requests, setRequests] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const t = localStorage.getItem("token");
    if (!t) {
      window.location.href = "/auth/login";
      return;
    }
    setToken(t);
    Promise.all([getServices(), myRequests(t)])
      .then(([svcs, reqs]) => {
        setServices(svcs);
        setRequests(reqs);
      })
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  async function submitRequest() {
    if (!token || selected === "") return;
    try {
      await createRequest(token, Number(selected), notes || undefined);
      const updated = await myRequests(token);
      setRequests(updated);
      setSelected("");
      setNotes("");
    } catch (e: any) {
      alert(e.message);
    }
  }

  return (
    <div className="max-w-5xl mx-auto px-4 py-10">
      <h1 className="text-3xl font-bold mb-6">My Dashboard</h1>
      {loading && <p>Loading...</p>}
      {error && <p className="text-red-600">{error}</p>}

      <div className="bg-white border rounded p-4 mb-8">
        <h2 className="font-semibold mb-3">Request a Service</h2>
        <div className="flex gap-3">
          <select
            className="border rounded px-2 py-2"
            value={selected}
            onChange={(e) =>
              setSelected(e.target.value === "" ? "" : Number(e.target.value))
            }
          >
            <option value="">Select service</option>
            {services.map((s) => (
              <option key={s.id} value={s.id}>
                {s.service_name}
              </option>
            ))}
          </select>
          <input
            className="border rounded px-2 py-2 flex-1"
            placeholder="Notes (optional)"
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
          />
          <button
            className="bg-blue-600 text-white px-4 py-2 rounded"
            onClick={submitRequest}
          >
            Submit
          </button>
        </div>
      </div>

      <h2 className="text-xl font-semibold mb-3">My Requests</h2>
      <div className="space-y-3">
        {requests.map((r) => (
          <div
            key={r.id}
            className="border rounded p-4 flex items-center justify-between"
          >
            <div>
              <div className="font-medium">{r.service.service_name}</div>
              <div className="text-sm text-gray-600">Status: {r.status}</div>
            </div>
            <div className="text-sm text-gray-500">
              {new Date(r.request_date).toLocaleString()}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

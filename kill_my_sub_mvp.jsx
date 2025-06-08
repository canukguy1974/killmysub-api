// Project: Kill My Sub - MVP UI
// Stack: React (Vite), Tailwind, FastAPI, MongoDB

import { useEffect, useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

export default function SubscriptionDashboard() {
  const [subs, setSubs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchSubs() {
      const res = await fetch('/api/subscriptions');
      const data = await res.json();
      setSubs(data);
      setLoading(false);
    }
    fetchSubs();
  }, []);

  async function handleCancel(id) {
    await fetch(`/api/subscriptions/${id}/cancel`, { method: 'POST' });
    setSubs(subs.map(s => s._id === id ? { ...s, status: 'cancel_requested' } : s));
  }

  return (
    <div className="min-h-screen bg-zinc-900 text-white p-4">
      <h1 className="text-3xl font-bold mb-6">Kill My Sub</h1>
      {loading ? (
        <p>Loading subscriptions...</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {subs.map(sub => (
            <Card key={sub._id} className="bg-zinc-800 border border-zinc-700">
              <CardContent>
                <h2 className="text-xl font-semibold">{sub.service}</h2>
                <p className="text-sm">{sub.tier} — Next charge: {sub.next_charge || 'N/A'}</p>
                <p className="text-xs text-zinc-400">{sub.payment_method || 'Unknown payment method'}</p>
                <div className="mt-2">
                  {sub.status === 'active' ? (
                    <Button onClick={() => handleCancel(sub._id)}>Cancel</Button>
                  ) : (
                    <span className="text-green-400">Cancel Requested</span>
                  )}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}

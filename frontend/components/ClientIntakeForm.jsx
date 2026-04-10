'use client';
import { useState } from 'react';

export default function ClientIntakeForm({ onProfileCreated }) {
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({ budget: '', location: '', lifestyle: '' });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/client/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ preferences: formData })
      });
      const data = await response.json();
      if (data.client_id) {
        onProfileCreated(data.client_id);
      }
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  return (
    <div className="max-w-2xl mx-auto p-8 border rounded-lg shadow-sm bg-white mt-10">
      <h2 className="text-3xl font-bold mb-6 text-center">Tell us what you're looking for</h2>
      <form className="space-y-6" onSubmit={handleSubmit}>
        <div>
          <label className="block text-gray-700 font-bold mb-2">Budget Range</label>
          <input type="text" placeholder="e.g. $500k - $800k" className="w-full p-2 border rounded"
            value={formData.budget} onChange={e => setFormData({...formData, budget: e.target.value})} required/>
        </div>
        <div>
          <label className="block text-gray-700 font-bold mb-2">Preferred Location</label>
          <input type="text" placeholder="City or Region" className="w-full p-2 border rounded"
            value={formData.location} onChange={e => setFormData({...formData, location: e.target.value})} required/>
        </div>
        <div>
          <label className="block text-gray-700 font-bold mb-2">Describe your ideal lifestyle</label>
          <textarea rows="4" placeholder="I love walkability, coffee shops, and quiet streets..." className="w-full p-2 border rounded"
            value={formData.lifestyle} onChange={e => setFormData({...formData, lifestyle: e.target.value})} required></textarea>
        </div>
        <button type="submit" disabled={loading} className="w-full bg-blue-600 text-white font-bold py-3 rounded hover:bg-blue-700 transition disabled:bg-blue-300">
          {loading ? 'Generating Profile...' : 'Generate My Profile'}
        </button>
      </form>
    </div>
  );
}

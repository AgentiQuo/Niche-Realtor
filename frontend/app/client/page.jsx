'use client';
import { useState, useEffect } from 'react';
import ClientIntakeForm from '../../components/ClientIntakeForm';
import ClientDashboard from '../../components/ClientDashboard';

export default function ClientPage() {
  const [clientId, setClientId] = useState(null);

  // In a real app we'd fetch the client state if client_id exists
  return (
    <div className="min-h-screen bg-gray-50 py-10">
      {!clientId ? (
        <ClientIntakeForm onProfileCreated={setClientId} />
      ) : (
        <ClientDashboard client={{ client_id: clientId }} savedProperties={[]} recommendedProperties={[]} />
      )}
    </div>
  );
}

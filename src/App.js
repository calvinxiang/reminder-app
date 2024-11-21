import React, { useEffect } from 'react';
import './App.css';
import AddReminder from './components/AddReminder';
import ViewReminders from './components/ViewReminders';
import { subscribeUser } from './subscribe';

function App() {
  useEffect(() => {
    subscribeUser();
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-2xl mx-auto bg-white p-6 rounded-lg shadow-lg">
        <h1 className="text-2xl font-bold mb-6 text-center">Reminder App</h1>
        <AddReminder />
        <ViewReminders />
      </div>
    </div>
  );
}

export default App;
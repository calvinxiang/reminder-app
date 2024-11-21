import React, { useEffect, useState } from 'react';
import axios from 'axios';

function ViewReminders() {
  const [reminders, setReminders] = useState([]);

  useEffect(() => {
    const fetchReminders = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/get_reminders/');
        setReminders(response.data);
      } catch (error) {
        console.error('Error fetching reminders:', error);
      }
    };
    fetchReminders();
  }, []);

  return (
    <div>
      <h2 className="text-xl font-bold mb-4">Existing Reminders</h2>
      <ul>
        {reminders.length > 0 ? (
          reminders.map((reminder) => (
            <li key={reminder.id} className="mb-2 p-3 border rounded bg-gray-50">
              <strong>{reminder.title}</strong> - {reminder.time}
            </li>
          ))
        ) : (
          <p>No reminders available</p>
        )}
      </ul>
    </div>
  );
}

export default ViewReminders;

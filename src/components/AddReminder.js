import React, { useState } from 'react';
import axios from 'axios';

function AddReminder() {
  const [title, setTitle] = useState('');
  const [time, setTime] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:8000/add_reminder/', {
        id: Math.floor(Math.random() * 1000), // Generating a random ID
        title,
        time,
      });
      console.log(response.data);
      alert('Reminder added successfully!');
      setTitle('');
      setTime('');
    } catch (error) {
      console.error('Error adding reminder:', error);
      alert('Failed to add reminder');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mb-6">
      <div className="mb-4">
        <label className="block mb-2 text-sm font-medium">Reminder Title</label>
        <input
          type="text"
          className="w-full p-2 border rounded"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
      </div>
      <div className="mb-4">
        <label className="block mb-2 text-sm font-medium">Reminder Time (YYYY-MM-DD HH:MM:SS)</label>
        <input
          type="text"
          className="w-full p-2 border rounded"
          value={time}
          onChange={(e) => setTime(e.target.value)}
          required
        />
      </div>
      <button
        type="submit"
        className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600"
      >
        Add Reminder
      </button>
    </form>
  );
}

export default AddReminder;

import React, { useEffect, useState } from 'react';

const API_URL = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/activities/`;

function Activities() {
  const [activities, setActivities] = useState([]);
  useEffect(() => {
    console.log('Fetching Activities from:', API_URL);
    fetch(API_URL)
      .then(res => res.json())
      .then(data => {
        const results = data.results || data;
        setActivities(results);
        console.log('Fetched Activities:', results);
      })
      .catch(err => console.error('Error fetching activities:', err));
  }, []);

  return (
    <div>
      <h2 className="h4 mb-3">Activities</h2>
      <table className="table table-striped table-bordered">
        <thead className="table-primary">
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Date</th>
            <th>Duration</th>
            <th>Calories</th>
          </tr>
        </thead>
        <tbody>
          {activities.map((a, i) => (
            <tr key={a.id || i}>
              <td>{a.id}</td>
              <td>{a.name}</td>
              <td>{a.date}</td>
              <td>{a.duration}</td>
              <td>{a.calories}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Activities;

import { useState, useEffect } from 'react';
import { userAPI } from '../services/api';

export default function AdminPanel({ onSelectUser }) {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    userAPI.getAll().then(data => {
      setUsers(data);
      setLoading(false);
    });
  }, []);

  if (loading) return <p className="text-center py-20 text-gray-500">Loading users...</p>;

  return (
    <div>
      <h2 className="text-2xl font-bold mb-6">User Management</h2>
      <div className="border-2 border-black overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b-2 border-black bg-gray-50">
              <th className="text-left px-4 py-3 font-semibold">Username</th>
              <th className="text-left px-4 py-3 font-semibold">Role</th>
              <th className="text-left px-4 py-3 font-semibold">Joined</th>
              <th className="px-4 py-3" />
            </tr>
          </thead>
          <tbody>
            {users.map((user, i) => (
              <tr key={user.id} className={i < users.length - 1 ? 'border-b border-black' : ''}>
                <td className="px-4 py-3 font-medium">{user.username}</td>
                <td className="px-4 py-3">
                  <span className={`px-2 py-1 border text-xs font-medium ${
                    user.role === 'admin' ? 'border-black bg-black text-white' : 'border-gray-400 text-gray-600'
                  }`}>
                    {user.role}
                  </span>
                </td>
                <td className="px-4 py-3 text-gray-600 text-sm">
                  {new Date(user.created_at).toLocaleDateString()}
                </td>
                <td className="px-4 py-3 text-right">
                  <button
                    className="px-4 py-1 border-2 border-black text-sm font-medium hover:bg-gray-100 transition-colors"
                    onClick={() => onSelectUser(user.id)}
                  >
                    View Profile
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

import { useState, useEffect } from 'react';
import { ChevronLeft, Trash2 } from 'lucide-react';
import { userAPI } from '../services/api';
import ChangePasswordForm from './ChangePasswordForm';

export default function UserProfile({ userId, currentUser, onBack, onUserDeleted }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);
  const [editForm, setEditForm] = useState({ username: '', password: '', role: '' });
  const [editError, setEditError] = useState('');
  const [editSuccess, setEditSuccess] = useState('');
  const [resetting, setResetting] = useState(false);

  const isSelf = userId === currentUser.id;

  useEffect(() => {
    loadUser();
  }, [userId]);

  const loadUser = () => {
    setLoading(true);
    const fetch = currentUser.isAdmin ? userAPI.getOne(userId) : userAPI.getMe();
    fetch.then(data => {
      setUser(data);
      setEditForm({ username: data.username, password: '', role: data.role });
      setLoading(false);
    });
  };

  const handleEditSubmit = async (e) => {
    e.preventDefault();
    setEditError('');
    setEditSuccess('');
    const payload = {};
    if (editForm.username !== user.username) payload.username = editForm.username;
    if (editForm.password) payload.password = editForm.password;
    if (editForm.role !== user.role) payload.role = editForm.role;
    if (Object.keys(payload).length === 0) {
      setEditing(false);
      return;
    }
    try {
      await userAPI.update(userId, payload);
      setEditSuccess('User updated.');
      setEditing(false);
      loadUser();
    } catch (err) {
      setEditError(err.message || 'Update failed');
    }
  };

  const handleDelete = async () => {
    if (!window.confirm(`Delete user "${user.username}"? This cannot be undone.`)) return;
    try {
      await userAPI.delete(userId);
      onUserDeleted();
    } catch (err) {
      alert(err.message || 'Delete failed');
    }
  };

  const handleResetProgress = async () => {
    if (!window.confirm('Reset all studied progress for this user?')) return;
    setResetting(true);
    try {
      await userAPI.resetProgress(userId);
      loadUser();
    } catch (err) {
      alert(err.message || 'Reset failed');
    } finally {
      setResetting(false);
    }
  };

  if (loading) return <p className="text-center py-20 text-gray-500">Loading profile...</p>;
  if (!user) return <p className="text-center py-20 text-gray-500">User not found.</p>;

  return (
    <div className="max-w-2xl">
      <button
        className="flex items-center gap-2 text-sm font-medium hover:underline mb-6"
        onClick={onBack}
      >
        <ChevronLeft className="w-4 h-4" />
        Back
      </button>

      <div className="flex items-start justify-between mb-6">
        <div>
          <h2 className="text-2xl font-bold">{user.username}</h2>
          <div className="flex items-center gap-3 mt-1">
            <span className={`px-2 py-1 border text-xs font-medium ${
              user.role === 'admin' ? 'border-black bg-black text-white' : 'border-gray-400 text-gray-600'
            }`}>
              {user.role}
            </span>
            <span className="text-sm text-gray-500">
              Joined {new Date(user.created_at).toLocaleDateString()}
            </span>
          </div>
        </div>
        <div className="flex gap-2">
          {(currentUser.isAdmin || isSelf) && (
            <button
              className="px-4 py-2 border-2 border-black text-sm font-medium hover:bg-gray-100 transition-colors disabled:opacity-50"
              onClick={handleResetProgress}
              disabled={resetting}
            >
              {resetting ? 'Resetting...' : 'Reset Progress'}
            </button>
          )}
          {currentUser.isAdmin && !isSelf && (
            <button
              className="px-4 py-2 border-2 border-black text-sm font-medium hover:bg-red-50 text-primary-red transition-colors flex items-center gap-1"
              onClick={handleDelete}
            >
              <Trash2 className="w-4 h-4" />
              Delete User
            </button>
          )}
        </div>
      </div>

      {editSuccess && (
        <p className="text-green-700 font-medium text-sm mb-4">{editSuccess}</p>
      )}

      {/* Admin edit form */}
      {currentUser.isAdmin && (
        <div className="border-2 border-black p-6 mb-6">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-bold">Edit User</h3>
            {!editing && (
              <button
                className="px-4 py-1 border-2 border-black text-sm font-medium hover:bg-gray-100"
                onClick={() => setEditing(true)}
              >
                Edit
              </button>
            )}
          </div>
          {editing ? (
            <form onSubmit={handleEditSubmit} className="flex flex-col gap-3">
              <div>
                <label className="text-sm font-medium block mb-1">Username</label>
                <input
                  type="text"
                  value={editForm.username}
                  onChange={(e) => setEditForm({ ...editForm, username: e.target.value })}
                  required
                  className="w-full px-4 py-2 border-2 border-black text-base focus:outline-none focus:ring-2 focus:ring-primary-red"
                />
              </div>
              <div>
                <label className="text-sm font-medium block mb-1">New Password <span className="text-gray-400">(leave blank to keep current)</span></label>
                <input
                  type="password"
                  value={editForm.password}
                  onChange={(e) => setEditForm({ ...editForm, password: e.target.value })}
                  placeholder="New password"
                  className="w-full px-4 py-2 border-2 border-black text-base focus:outline-none focus:ring-2 focus:ring-primary-red"
                />
              </div>
              <div>
                <label className="text-sm font-medium block mb-1">Role</label>
                <select
                  value={editForm.role}
                  onChange={(e) => setEditForm({ ...editForm, role: e.target.value })}
                  className="w-full px-4 py-2 border-2 border-black text-base focus:outline-none focus:ring-2 focus:ring-primary-red"
                >
                  <option value="user">user</option>
                  <option value="admin">admin</option>
                </select>
              </div>
              {editError && <p className="text-primary-red font-medium text-sm">{editError}</p>}
              <div className="flex gap-2 pt-1">
                <button
                  type="submit"
                  className="px-6 py-2 bg-primary-red text-white border-2 border-black font-medium hover:bg-red-700 transition-colors"
                >
                  Save
                </button>
                <button
                  type="button"
                  className="px-6 py-2 border-2 border-black font-medium hover:bg-gray-100 transition-colors"
                  onClick={() => { setEditing(false); setEditError(''); }}
                >
                  Cancel
                </button>
              </div>
            </form>
          ) : (
            <div className="text-sm text-gray-600 space-y-1">
              <p><span className="font-medium text-black">Username:</span> {user.username}</p>
              <p><span className="font-medium text-black">Role:</span> {user.role}</p>
            </div>
          )}
        </div>
      )}

      {/* Self-service password change */}
      {isSelf && !currentUser.isAdmin && (
        <ChangePasswordForm />
      )}
      {isSelf && currentUser.isAdmin && (
        <ChangePasswordForm />
      )}

      {/* Practice history */}
      <div className="border-2 border-black p-6">
        <h3 className="text-lg font-bold mb-4">
          Practice History
          <span className="text-sm font-normal text-gray-500 ml-2">({user.card_views.length} recent views)</span>
        </h3>
        {user.card_views.length === 0 ? (
          <p className="text-gray-500 text-sm">No practice history yet.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b-2 border-black">
                  <th className="text-left py-2 pr-4 font-semibold">Card</th>
                  <th className="text-left py-2 pr-4 font-semibold">English</th>
                  <th className="text-left py-2 font-semibold">Viewed at</th>
                </tr>
              </thead>
              <tbody>
                {user.card_views.map((view, i) => (
                  <tr key={view.id} className={i < user.card_views.length - 1 ? 'border-b border-gray-200' : ''}>
                    <td className="py-2 pr-4 text-2xl">{view.card_chinese}</td>
                    <td className="py-2 pr-4 text-gray-700">{view.card_english}</td>
                    <td className="py-2 text-gray-500">
                      {new Date(view.viewed_at).toLocaleString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

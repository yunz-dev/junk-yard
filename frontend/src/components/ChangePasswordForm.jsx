import { useState } from 'react';
import { userAPI } from '../services/api';

export default function ChangePasswordForm({ onSuccess }) {
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    if (newPassword !== confirmPassword) {
      setError('New passwords do not match');
      return;
    }
    if (newPassword.length < 1) {
      setError('New password cannot be empty');
      return;
    }
    setLoading(true);
    try {
      await userAPI.changePassword(currentPassword, newPassword);
      setSuccess(true);
      setCurrentPassword('');
      setNewPassword('');
      setConfirmPassword('');
      if (onSuccess) onSuccess();
    } catch (err) {
      setError(err.message || 'Failed to change password');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="border-2 border-black p-6 mt-6">
      <h3 className="text-lg font-bold mb-4">Change Password</h3>
      {success && (
        <p className="text-green-700 font-medium text-sm mb-4">Password updated successfully.</p>
      )}
      <form onSubmit={handleSubmit} className="flex flex-col gap-3 max-w-sm">
        <input
          type="password"
          placeholder="Current password"
          value={currentPassword}
          onChange={(e) => setCurrentPassword(e.target.value)}
          required
          className="px-4 py-3 border-2 border-black text-base focus:outline-none focus:ring-2 focus:ring-primary-red"
        />
        <input
          type="password"
          placeholder="New password"
          value={newPassword}
          onChange={(e) => setNewPassword(e.target.value)}
          required
          className="px-4 py-3 border-2 border-black text-base focus:outline-none focus:ring-2 focus:ring-primary-red"
        />
        <input
          type="password"
          placeholder="Confirm new password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          required
          className="px-4 py-3 border-2 border-black text-base focus:outline-none focus:ring-2 focus:ring-primary-red"
        />
        {error && <p className="text-primary-red font-medium text-sm">{error}</p>}
        <button
          type="submit"
          disabled={loading}
          className="py-3 bg-primary-red text-white border-2 border-black font-medium hover:bg-red-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? 'Updating...' : 'Update Password'}
        </button>
      </form>
    </div>
  );
}

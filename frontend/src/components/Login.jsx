import { useState } from 'react';
import { Dog } from 'lucide-react';
import { authAPI } from '../services/api';

export default function Login({ onLogin }) {
  const [mode, setMode] = useState('login'); // 'login' | 'register'
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleModeSwitch = (newMode) => {
    setMode(newMode);
    setError('');
    setConfirmPassword('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    if (mode === 'register' && password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }
    setLoading(true);
    try {
      const result = mode === 'login'
        ? await authAPI.login(username, password)
        : await authAPI.register(username, password);
      onLogin(result.access_token, result.username, result.role);
    } catch (err) {
      setError(err.message || 'Something went wrong');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-white flex flex-col items-center justify-center p-4">
      <div className="w-full max-w-sm">
        <div className="flex items-center gap-3 justify-center mb-8">
          <Dog className="w-8 h-8" strokeWidth={2} />
          <h1 className="text-3xl font-bold tracking-tight">Ni-Howl</h1>
        </div>

        <div className="border-2 border-black p-8">
          <div className="flex mb-6">
            <button
              type="button"
              className={`flex-1 py-2 font-medium border-2 border-black transition-colors ${
                mode === 'login' ? 'bg-primary-red text-white' : 'bg-white text-black hover:bg-gray-100'
              }`}
              onClick={() => handleModeSwitch('login')}
            >
              Login
            </button>
            <button
              type="button"
              className={`flex-1 py-2 font-medium border-2 border-black border-l-0 transition-colors ${
                mode === 'register' ? 'bg-primary-red text-white' : 'bg-white text-black hover:bg-gray-100'
              }`}
              onClick={() => handleModeSwitch('register')}
            >
              Register
            </button>
          </div>

          <form onSubmit={handleSubmit} className="flex flex-col gap-4">
            <input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              className="px-4 py-3 border-2 border-black text-base focus:outline-none focus:ring-2 focus:ring-primary-red"
            />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="px-4 py-3 border-2 border-black text-base focus:outline-none focus:ring-2 focus:ring-primary-red"
            />
            {mode === 'register' && (
              <input
                type="password"
                placeholder="Confirm Password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
                className="px-4 py-3 border-2 border-black text-base focus:outline-none focus:ring-2 focus:ring-primary-red"
              />
            )}
            {error && (
              <p className="text-primary-red font-medium text-sm">{error}</p>
            )}
            <button
              type="submit"
              disabled={loading}
              className="py-3 bg-primary-red text-white border-2 border-black font-medium hover:bg-red-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Please wait...' : mode === 'login' ? 'Login' : 'Create Account'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

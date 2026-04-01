import { useState } from 'react';

export default function FlashcardForm({ onSubmit, onCancel }) {
  const [formData, setFormData] = useState({
    chinese: '',
    pinyin: '',
    english: '',
    category: 'HSK 1'
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
    setFormData({ chinese: '', pinyin: '', english: '', category: 'HSK 1' });
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" onClick={onCancel}>
      <div className="bg-white border-4 border-black p-8 w-11/12 max-w-md" onClick={(e) => e.stopPropagation()}>
        <h2 className="text-2xl font-bold mb-6">Add New Flashcard</h2>
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <input
            type="text"
            placeholder="Chinese"
            value={formData.chinese}
            onChange={(e) => setFormData({ ...formData, chinese: e.target.value })}
            className="px-4 py-3 border-2 border-black focus:outline-none focus:ring-2 focus:ring-primary-red"
            required
          />
          <input
            type="text"
            placeholder="Pinyin"
            value={formData.pinyin}
            onChange={(e) => setFormData({ ...formData, pinyin: e.target.value })}
            className="px-4 py-3 border-2 border-black focus:outline-none focus:ring-2 focus:ring-primary-red"
            required
          />
          <input
            type="text"
            placeholder="English"
            value={formData.english}
            onChange={(e) => setFormData({ ...formData, english: e.target.value })}
            className="px-4 py-3 border-2 border-black focus:outline-none focus:ring-2 focus:ring-primary-red"
            required
          />
          <select
            value={formData.category}
            onChange={(e) => setFormData({ ...formData, category: e.target.value })}
            className="px-4 py-3 border-2 border-black focus:outline-none focus:ring-2 focus:ring-primary-red"
          >
            <option>HSK 1</option>
            <option>HSK 2</option>
            <option>HSK 3</option>
            <option>HSK 4</option>
            <option>HSK 5</option>
            <option>HSK 6</option>
            <option>Greetings</option>
            <option>Numbers</option>
            <option>Food</option>
            <option>Travel</option>
          </select>
          <div className="flex gap-3 mt-2">
            <button type="submit" className="flex-1 px-6 py-3 bg-primary-red text-white border-2 border-black font-medium hover:bg-red-700 transition-colors">
              Add Card
            </button>
            <button type="button" onClick={onCancel} className="flex-1 px-6 py-3 bg-white border-2 border-black font-medium hover:bg-gray-100 transition-colors">
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

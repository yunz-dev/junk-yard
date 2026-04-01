import { useState, useEffect } from 'react';
import { Dog, ChevronLeft, ChevronRight, Shuffle } from 'lucide-react';
import Flashcard from './components/Flashcard';
import FlashcardForm from './components/FlashcardForm';
import CardList from './components/CardList';
import { flashcardAPI } from './services/api';
import './App.css';

export default function App() {
  const [allCards, setAllCards] = useState([]);
  const [studyCards, setStudyCards] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [showForm, setShowForm] = useState(false);
  const [view, setView] = useState('study');
  const [studyCategory, setStudyCategory] = useState('');
  const [manageCategory, setManageCategory] = useState('');

  useEffect(() => {
    loadCards();
  }, []);

  useEffect(() => {
    filterStudyCards();
  }, [allCards, studyCategory]);

  const loadCards = async () => {
    const cards = await flashcardAPI.getAll();
    setAllCards(cards);
  };

  const filterStudyCards = () => {
    let filtered = allCards;
    if (studyCategory) {
      filtered = allCards.filter(c => c.category === studyCategory);
    }
    setStudyCards(filtered);
    setCurrentIndex(0);
  };

  const handleShuffle = () => {
    const shuffled = [...studyCards].sort(() => Math.random() - 0.5);
    setStudyCards(shuffled);
    setCurrentIndex(0);
  };

  const handlePrev = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
    }
  };

  const handleNext = () => {
    if (currentIndex < studyCards.length - 1) {
      setCurrentIndex(currentIndex + 1);
    }
  };

  const handleCreateCard = async (cardData) => {
    await flashcardAPI.create(cardData);
    setShowForm(false);
    await loadCards();
  };

  const handleDeleteCard = async (id) => {
    await flashcardAPI.delete(id);
    await loadCards();
  };

  const handleReset = async () => {
    const confirmed = window.confirm(
      'Are you sure you want to reset the database? This will delete all custom flashcards and restore only the 50 default cards.'
    );

    if (confirmed) {
      await flashcardAPI.resetStudied();
      await loadCards();
      setStudyCategory('');
      setManageCategory('');
    }
  };

  const getManageCards = () => {
    if (manageCategory) {
      return allCards.filter(c => c.category === manageCategory);
    }
    return allCards;
  };

  const currentCard = studyCards[currentIndex];

  return (
    <div className="min-h-screen bg-white p-4 md:p-8">
      <div className="max-w-6xl mx-auto">
        <header className="flex flex-col md:flex-row justify-between items-center gap-4 mb-8 pb-6 border-b-2 border-black">
          <div className="flex items-center gap-3">
            <Dog className="w-8 h-8" strokeWidth={2} />
            <h1 className="text-3xl font-bold tracking-tight">Ni-Howl</h1>
          </div>
          <nav className="flex gap-2">
            <button
              className={`px-6 py-2 border-2 border-black font-medium transition-colors ${
                view === 'study' ? 'bg-primary-red text-white' : 'bg-white text-black hover:bg-gray-100'
              }`}
              onClick={() => setView('study')}
            >
              Study
            </button>
            <button
              className={`px-6 py-2 border-2 border-black font-medium transition-colors ${
                view === 'manage' ? 'bg-primary-red text-white' : 'bg-white text-black hover:bg-gray-100'
              }`}
              onClick={() => setView('manage')}
            >
              Manage
            </button>
          </nav>
        </header>

        <main className="min-h-[500px]">
          {view === 'study' ? (
            <div className="flex flex-col items-center gap-8">
              <div className="flex flex-col md:flex-row gap-4 w-full max-w-2xl">
                <select
                  value={studyCategory}
                  onChange={(e) => setStudyCategory(e.target.value)}
                  className="flex-1 px-4 py-3 border-2 border-black text-base focus:outline-none focus:ring-2 focus:ring-primary-red"
                >
                  <option value="">All Categories</option>
                  <option value="HSK 1">HSK 1</option>
                  <option value="HSK 2">HSK 2</option>
                  <option value="HSK 3">HSK 3</option>
                  <option value="HSK 4">HSK 4</option>
                  <option value="HSK 5">HSK 5</option>
                  <option value="HSK 6">HSK 6</option>
                  <option value="Greetings">Greetings</option>
                  <option value="Numbers">Numbers</option>
                  <option value="Food">Food</option>
                  <option value="Travel">Travel</option>
                </select>
                <button
                  className="px-6 py-3 bg-white border-2 border-black font-medium hover:bg-gray-100 transition-colors flex items-center gap-2"
                  onClick={handleShuffle}
                  disabled={studyCards.length === 0}
                >
                  <Shuffle className="w-4 h-4" />
                  Shuffle
                </button>
                <button
                  className="px-6 py-3 bg-primary-yellow border-2 border-black font-medium hover:bg-yellow-300 transition-colors"
                  onClick={handleReset}
                >
                  Reset All
                </button>
              </div>

              <div className="text-xl font-medium">
                {studyCards.length > 0 ? `${currentIndex + 1} / ${studyCards.length}` : '0 / 0'}
              </div>

              {currentCard ? (
                <>
                  <Flashcard card={currentCard} />
                  <div className="flex gap-4">
                    <button
                      className="px-6 py-3 bg-white border-2 border-black font-medium hover:bg-gray-100 transition-colors flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                      onClick={handlePrev}
                      disabled={currentIndex === 0}
                    >
                      <ChevronLeft className="w-5 h-5" />
                      Previous
                    </button>
                    <button
                      className="px-6 py-3 bg-white border-2 border-black font-medium hover:bg-gray-100 transition-colors flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                      onClick={handleNext}
                      disabled={currentIndex === studyCards.length - 1}
                    >
                      Next
                      <ChevronRight className="w-5 h-5" />
                    </button>
                  </div>
                </>
              ) : (
                <div className="text-center py-20">
                  <Dog className="w-24 h-24 mx-auto mb-4" strokeWidth={1.5} />
                  <h2 className="text-3xl font-bold mb-2">No cards available</h2>
                  <p className="text-lg text-gray-600">Add some cards or change the filter</p>
                </div>
              )}
            </div>
          ) : (
            <div className="flex flex-col gap-8">
              <div className="flex flex-col md:flex-row gap-4">
                <button
                  className="px-6 py-3 bg-primary-red text-white border-2 border-black font-medium hover:bg-red-700 transition-colors"
                  onClick={() => setShowForm(true)}
                >
                  Add New Card
                </button>
                <select
                  value={manageCategory}
                  onChange={(e) => setManageCategory(e.target.value)}
                  className="flex-1 md:flex-none md:w-64 px-4 py-3 border-2 border-black text-base focus:outline-none focus:ring-2 focus:ring-primary-red"
                >
                  <option value="">All Categories</option>
                  <option value="HSK 1">HSK 1</option>
                  <option value="HSK 2">HSK 2</option>
                  <option value="HSK 3">HSK 3</option>
                  <option value="HSK 4">HSK 4</option>
                  <option value="HSK 5">HSK 5</option>
                  <option value="HSK 6">HSK 6</option>
                  <option value="Greetings">Greetings</option>
                  <option value="Numbers">Numbers</option>
                  <option value="Food">Food</option>
                  <option value="Travel">Travel</option>
                </select>
              </div>
              <CardList cards={getManageCards()} onDelete={handleDeleteCard} />
            </div>
          )}
        </main>

        {showForm && (
          <FlashcardForm
            onSubmit={handleCreateCard}
            onCancel={() => setShowForm(false)}
          />
        )}
      </div>
    </div>
  );
}

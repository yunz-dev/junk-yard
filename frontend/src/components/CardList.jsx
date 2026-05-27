export default function CardList({ cards, onDelete, isAdmin }) {
  return (
    <div>
      <h2 className="text-2xl font-bold mb-6">Manage Flashcards</h2>
      {cards.length === 0 ? (
        <p className="text-center text-gray-500 py-20">No flashcards yet. Create some to get started!</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {cards.map(card => (
            <div key={card.id} className="border-2 border-black p-4 flex flex-col gap-3 hover:shadow-lg transition-shadow">
              <div className="flex-1">
                <div className="text-3xl font-bold mb-2">{card.chinese}</div>
                <div className="text-base italic text-gray-600 mb-2">{card.pinyin}</div>
                <div className="text-lg mb-3">{card.english}</div>
                <div className="inline-block px-3 py-1 border border-black text-sm">
                  {card.category}
                </div>
              </div>
              {isAdmin && (
                <button
                  className="w-full px-4 py-2 bg-primary-red text-white border-2 border-black font-medium hover:bg-red-700 transition-colors"
                  onClick={() => onDelete(card.id)}
                >
                  Delete
                </button>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

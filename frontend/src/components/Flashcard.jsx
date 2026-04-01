import { useState, useEffect } from 'react';

export default function Flashcard({ card }) {
  const [flipped, setFlipped] = useState(false);

  useEffect(() => {
    setFlipped(false);
  }, [card.id]);

  const handleFlip = () => {
    setFlipped(!flipped);
  };

  return (
    <div className={`flashcard w-full max-w-sm md:w-96 h-72 cursor-pointer ${flipped ? 'flipped' : ''}`} onClick={handleFlip}>
      <div className="flashcard-inner relative w-full h-full">
        <div className="flashcard-front absolute w-full h-full flex flex-col items-center justify-center border-4 border-black bg-primary-red p-8">
          <div className="text-7xl font-bold text-white mb-4">{card.chinese}</div>
          <div className="absolute top-4 right-4 px-3 py-1 border-2 border-white text-white text-sm font-medium">
            {card.category}
          </div>
        </div>
        <div className="flashcard-back absolute w-full h-full flex flex-col items-center justify-center border-4 border-black bg-primary-yellow p-8">
          <div className="text-3xl mb-3 italic">{card.pinyin}</div>
          <div className="text-2xl font-medium">{card.english}</div>
        </div>
      </div>
    </div>
  );
}

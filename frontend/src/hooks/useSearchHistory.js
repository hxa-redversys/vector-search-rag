import { useState, useEffect } from 'react';

const MAX_HISTORY_ITEMS = 5;

export function useSearchHistory() {
  // Initialize state from localStorage
  const [searchHistory, setSearchHistory] = useState(() => {
    const saved = localStorage.getItem('searchHistory');
    return saved ? JSON.parse(saved) : [];
  });

  // Save to localStorage whenever history changes
  useEffect(() => {
    localStorage.setItem('searchHistory', JSON.stringify(searchHistory));
  }, [searchHistory]);

  // Add new search to history
  const addToHistory = (query) => {
    setSearchHistory(prev => {
      const newHistory = [
        { query, timestamp: new Date().toISOString() },
        ...prev.filter(item => item.query !== query) // Remove duplicates
      ].slice(0, MAX_HISTORY_ITEMS); // Keep only recent searches
      return newHistory;
    });
  };

  // Clear history
  const clearHistory = () => {
    setSearchHistory([]);
    localStorage.removeItem('searchHistory');
  };

  return {
    searchHistory,
    addToHistory,
    clearHistory
  };
} 
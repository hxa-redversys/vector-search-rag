import { useState, useEffect } from 'react';

const DEFAULT_FILTERS = {
  yearRange: [1900, new Date().getFullYear()],
  genres: [],
  sortBy: 'relevance'
};

export function useFilterPreferences() {
  // Initialize state from localStorage
  const [filters, setFilters] = useState(() => {
    const saved = localStorage.getItem('filterPreferences');
    return saved ? JSON.parse(saved) : DEFAULT_FILTERS;
  });

  // Save to localStorage whenever filters change
  useEffect(() => {
    localStorage.setItem('filterPreferences', JSON.stringify(filters));
  }, [filters]);

  // Reset filters to default
  const resetFilters = () => {
    setFilters(DEFAULT_FILTERS);
    localStorage.removeItem('filterPreferences');
  };

  return {
    filters,
    setFilters,
    resetFilters
  };
} 
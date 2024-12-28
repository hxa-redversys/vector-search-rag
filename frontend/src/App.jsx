import { useState, useEffect } from 'react';
import { 
  Container, 
  Typography, 
  TextField, 
  Button, 
  Box, 
  Paper, 
  Chip,
  CircularProgress,
  Alert,
  Skeleton,
  useMediaQuery,
  IconButton,
  ThemeProvider,
  CssBaseline,
  Pagination,
  Stack
} from '@mui/material';
import Brightness4Icon from '@mui/icons-material/Brightness4';
import Brightness7Icon from '@mui/icons-material/Brightness7';
import { lightTheme, darkTheme } from './theme';
import SearchFilters from './components/SearchFilters';
import ErrorBoundary from './components/ErrorBoundary';
import NetworkStatus from './components/NetworkStatus';
import { useSearchHistory } from './hooks/useSearchHistory';
import { useFilterPreferences } from './hooks/useFilterPreferences';
import { LoadingState, SearchBarLoading } from './components/LoadingState';

function App() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const { searchHistory, addToHistory, clearHistory } = useSearchHistory();
  const [darkMode, setDarkMode] = useState(() => {
    const savedMode = localStorage.getItem('darkMode');
    return savedMode ? JSON.parse(savedMode) : false;
  });
  const { filters, setFilters, resetFilters } = useFilterPreferences();
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const ITEMS_PER_PAGE = 5;
  
  const theme = darkMode ? darkTheme : lightTheme;
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  useEffect(() => {
    localStorage.setItem('darkMode', JSON.stringify(darkMode));
  }, [darkMode]);

  useEffect(() => {
    document.body.style.backgroundColor = darkMode ? '#303030' : '#f5f5f5';
  }, [darkMode]);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    try {
      setIsLoading(true);
      setError(null);
      const response = await fetch(`http://localhost:8000/search?${new URLSearchParams({
        query: query,
        yearStart: filters.yearRange[0],
        yearEnd: filters.yearRange[1],
        genres: filters.genres.join(','),
        sortBy: filters.sortBy
      })}`);
      
      if (!response.ok) {
        if (response.status === 429) {
          throw new Error('Too many requests. Please wait a moment and try again.');
        }
        throw new Error(`Server error (${response.status}). Please try again later.`);
      }
      
      const data = await response.json();
      setResults(data);
      addToHistory(query);
      
    } catch (err) {
      setError(err.message);
      console.error('Search error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handlePageChange = (event, value) => {
    setPage(value);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <ThemeProvider theme={darkMode ? darkTheme : lightTheme}>
      <CssBaseline />
      <ErrorBoundary>
        <Container maxWidth="md" sx={{ py: 4 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
            <Typography 
              variant={isMobile ? "h5" : "h4"} 
              component="h1"
            >
              Movie Recommendations
            </Typography>
            <IconButton 
              onClick={() => setDarkMode(!darkMode)} 
              color="inherit"
              aria-label="toggle dark mode"
            >
              {darkMode ? <Brightness7Icon /> : <Brightness4Icon />}
            </IconButton>
          </Box>
          
          <Box component="form" onSubmit={handleSearch} sx={{ mb: 4 }}>
            {isLoading ? (
              <SearchBarLoading />
            ) : (
              <TextField
                fullWidth
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search for movies..."
                variant="outlined"
                sx={{ mb: 2 }}
                disabled={isLoading}
                error={!!error}
                helperText={error}
              />
            )}
            <Button 
              type="submit"
              variant="contained"
              disabled={isLoading || !query.trim()}
              fullWidth
            >
              {isLoading ? (
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <CircularProgress size={20} color="inherit" />
                  Searching...
                </Box>
              ) : (
                'Search'
              )}
            </Button>
          </Box>

          <SearchFilters 
            filters={filters}
            onFilterChange={setFilters}
            onReset={resetFilters}
            disabled={isLoading}
          />

          {searchHistory.length > 0 && (
            <Box sx={{ mb: 4 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                <Typography variant="subtitle2">
                  Recent Searches
                </Typography>
                <Button 
                  size="small" 
                  onClick={clearHistory}
                  sx={{ minWidth: 'auto' }}
                >
                  Clear
                </Button>
              </Box>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                {searchHistory.map(({ query, timestamp }) => (
                  <Chip
                    key={timestamp}
                    label={query}
                    size="small"
                    onClick={() => {
                      setQuery(query);
                      handleSearch({ preventDefault: () => {} });
                    }}
                    sx={{ mr: 1, mb: 1 }}
                  />
                ))}
              </Box>
            </Box>
          )}

          {error && (
            <Alert 
              severity="error" 
              sx={{ mb: 2 }}
              onClose={() => setError(null)}
            >
              {error}
            </Alert>
          )}

          {isLoading ? (
            <LoadingState />
          ) : results && (
            <Box>
              <Paper 
                sx={{ 
                  p: 2, 
                  mb: 3,
                  transition: 'all 0.3s ease-in-out'
                }}
              >
                <Typography>{results.answer}</Typography>
              </Paper>

              <Box>
                {results.movies
                  ?.slice((page - 1) * ITEMS_PER_PAGE, page * ITEMS_PER_PAGE)
                  .map((movie) => (
                    <Paper 
                      key={movie._id}
                      sx={{ 
                        p: 2, 
                        mb: 2,
                        transition: 'all 0.3s ease-in-out',
                        '&:hover': {
                          transform: 'translateY(-2px)',
                          boxShadow: 3
                        }
                      }}
                      elevation={1}
                    >
                      <Typography variant="h6" gutterBottom>
                        {movie.title} {movie.year && `(${movie.year})`}
                      </Typography>
                      <Typography paragraph>{movie.plot}</Typography>
                      <Box sx={{ mt: 1 }}>
                        {movie.genres?.map((genre) => (
                          <Chip 
                            key={genre}
                            label={genre}
                            size="small"
                            sx={{ mr: 1, mb: 1 }}
                          />
                        ))}
                      </Box>
                    </Paper>
                  ))}

                {results.movies?.length > ITEMS_PER_PAGE && (
                  <Stack spacing={2} alignItems="center" sx={{ mt: 4 }}>
                    <Pagination
                      count={Math.ceil(results.movies.length / ITEMS_PER_PAGE)}
                      page={page}
                      onChange={handlePageChange}
                      color="primary"
                    />
                  </Stack>
                )}
              </Box>
            </Box>
          )}
        </Container>
        <NetworkStatus />
      </ErrorBoundary>
    </ThemeProvider>
  );
}

export default App;

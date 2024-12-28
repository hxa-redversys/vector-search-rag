import {
    Box,
    Accordion,
    AccordionSummary,
    AccordionDetails,
    Typography,
    Slider,
    Chip,
    FormControl,
    Select,
    MenuItem,
    Button
  } from '@mui/material';
  import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
  
  const GENRES = [
    'Action', 'Adventure', 'Animation', 'Comedy', 'Crime',
    'Documentary', 'Drama', 'Family', 'Fantasy', 'Horror',
    'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War'
  ];
  
  const SORT_OPTIONS = [
    { value: 'relevance', label: 'Relevance' },
    { value: 'year_desc', label: 'Year (Newest)' },
    { value: 'year_asc', label: 'Year (Oldest)' },
    { value: 'title_asc', label: 'Title (A-Z)' },
    { value: 'title_desc', label: 'Title (Z-A)' }
  ];
  
  const SearchFilters = ({ filters, onFilterChange, onReset }) => {
    const handleYearChange = (event, newValue) => {
      onFilterChange({ ...filters, yearRange: newValue });
    };
  
    const handleGenreClick = (genre) => {
      const newGenres = filters.genres.includes(genre)
        ? filters.genres.filter(g => g !== genre)
        : [...filters.genres, genre];
      onFilterChange({ ...filters, genres: newGenres });
    };
  
    const handleSortChange = (event) => {
      onFilterChange({ ...filters, sortBy: event.target.value });
    };
  
    return (
      <Accordion>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', width: '100%', pr: 2 }}>
            <Typography>Advanced Filters</Typography>
            <Button 
              size="small" 
              onClick={(e) => {
                e.stopPropagation();
                onReset();
              }}
            >
              Reset Filters
            </Button>
          </Box>
        </AccordionSummary>
        <AccordionDetails>
          <Box sx={{ mb: 3 }}>
            <Typography gutterBottom>Year Range</Typography>
            <Slider
              value={filters.yearRange}
              onChange={handleYearChange}
              valueLabelDisplay="auto"
              min={1900}
              max={new Date().getFullYear()}
            />
          </Box>
  
          <Box sx={{ mb: 3 }}>
            <Typography gutterBottom>Genres</Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
              {GENRES.map((genre) => (
                <Chip
                  key={genre}
                  label={genre}
                  clickable
                  color={filters.genres.includes(genre) ? "primary" : "default"}
                  onClick={() => handleGenreClick(genre)}
                />
              ))}
            </Box>
          </Box>
  
          <Box>
            <Typography gutterBottom>Sort By</Typography>
            <FormControl fullWidth size="small">
              <Select
                value={filters.sortBy}
                onChange={handleSortChange}
              >
                {SORT_OPTIONS.map((option) => (
                  <MenuItem key={option.value} value={option.value}>
                    {option.label}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Box>
        </AccordionDetails>
      </Accordion>
    );
  };
  
  export default SearchFilters;
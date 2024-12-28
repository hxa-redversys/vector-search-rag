import { useState } from 'react';
import {
  Input,
  Box,
  Button
} from '@chakra-ui/react';

const SearchBar = ({ onSearch, isLoading }) => {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query);
    }
  };

  return (
    <Box as="form" onSubmit={handleSubmit} width="100%" maxW="600px" mx="auto">
      <Input
        placeholder="Search for movies... (e.g., sci-fi movies about virtual reality)"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        disabled={isLoading}
        size="lg"
      />
      <Button 
        type="submit" 
        ml={2} 
        isLoading={isLoading}
      >
        Search
      </Button>
    </Box>
  );
};

export default SearchBar;

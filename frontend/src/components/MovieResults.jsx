import {
  Box,
  Text,
  VStack,
  Card,
  CardBody,
  Heading,
  Tag,
  Skeleton
} from '@chakra-ui/react';

const MovieResults = ({ answer, movies, isLoading }) => {
  if (isLoading) {
    return (
      <VStack spacing={4} width="100%" maxW="800px" mx="auto" mt={8}>
        <Skeleton height="100px" width="100%" />
        {[1, 2, 3].map((i) => (
          <Skeleton key={i} height="200px" width="100%" />
        ))}
      </VStack>
    );
  }

  if (!movies?.length) {
    return null;
  }

  return (
    <VStack spacing={4} width="100%" maxW="800px" mx="auto" mt={8}>
      {answer && (
        <Box p={4} bg="gray.50" borderRadius="md" width="100%">
          <Text>{answer}</Text>
        </Box>
      )}

      {movies.map((movie) => (
        <Card key={movie._id} width="100%">
          <CardBody>
            <Heading size="md" mb={2}>
              {movie.title} {movie.year && `(${movie.year})`}
            </Heading>
            <Text mb={3}>{movie.plot}</Text>
            <Box>
              {movie.genres?.map((genre) => (
                <Tag key={genre} mr={2} mb={2}>
                  {genre}
                </Tag>
              ))}
            </Box>
          </CardBody>
        </Card>
      ))}
    </VStack>
  );
};

export default MovieResults; 
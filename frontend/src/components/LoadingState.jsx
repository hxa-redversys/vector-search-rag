import { Box, Skeleton, Paper } from '@mui/material';

export const LoadingState = () => {
  return (
    <Box sx={{ width: '100%' }}>
      {/* Answer skeleton */}
      <Paper sx={{ p: 2, mb: 3 }}>
        <Skeleton variant="text" sx={{ fontSize: '1rem', mb: 1 }} />
        <Skeleton variant="text" sx={{ fontSize: '1rem', width: '80%' }} />
      </Paper>

      {/* Movie results skeletons */}
      {[1, 2, 3].map((i) => (
        <Paper key={i} sx={{ p: 2, mb: 2 }}>
          {/* Title */}
          <Skeleton variant="text" sx={{ fontSize: '1.5rem', mb: 1, width: '60%' }} />
          
          {/* Plot */}
          <Skeleton variant="text" sx={{ fontSize: '1rem', mb: 1 }} />
          <Skeleton variant="text" sx={{ fontSize: '1rem', mb: 1 }} />
          <Skeleton variant="text" sx={{ fontSize: '1rem', width: '80%', mb: 2 }} />
          
          {/* Genres */}
          <Box sx={{ display: 'flex', gap: 1 }}>
            <Skeleton variant="rounded" width={60} height={24} />
            <Skeleton variant="rounded" width={80} height={24} />
            <Skeleton variant="rounded" width={70} height={24} />
          </Box>
        </Paper>
      ))}
    </Box>
  );
};

export const SearchBarLoading = () => (
  <Box sx={{ width: '100%', mb: 2 }}>
    <Skeleton variant="rounded" height={56} />
  </Box>
); 
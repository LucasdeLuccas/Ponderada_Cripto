import React, { useState } from 'react';
import {
  Button,
  Select,
  MenuItem,
  InputLabel,
  FormControl,
  TextField,
  Box,
} from '@mui/material';
import { DatePicker, LocalizationProvider } from '@mui/lab';
import AdapterDateFns from '@mui/lab/AdapterDateFns';
import EventIcon from '@mui/icons-material/Event';

const assets = ['Bitcoin', 'Ethereum', 'BNB', 'Solana', 'Dogecoin'];

function PredictionForm({ onSubmit }) {
  const [asset, setAsset] = useState('Bitcoin');
  const [date, setDate] = useState(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (date) {
      onSubmit({ asset, date: date.toISOString().split('T')[0] });
    }
  };

  return (
    <Box component="form" onSubmit={handleSubmit} noValidate>
      <FormControl fullWidth margin="normal">
        <InputLabel id="asset-label">Criptoativo</InputLabel>
        <Select
          labelId="asset-label"
          value={asset}
          label="Criptoativo"
          onChange={(e) => setAsset(e.target.value)}
        >
          {assets.map((a) => (
            <MenuItem key={a} value={a}>
              {a}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
      <LocalizationProvider dateAdapter={AdapterDateFns}>
        <DatePicker
          label="Data"
          value={date}
          onChange={(newDate) => setDate(newDate)}
          renderInput={(params) => (
            <TextField
              {...params}
              fullWidth
              margin="normal"
              InputProps={{
                endAdornment: <EventIcon />,
              }}
            />
          )}
        />
      </LocalizationProvider>
      <Button
        type="submit"
        variant="contained"
        color="primary"
        fullWidth
        sx={{ mt: 2 }}
      >
        Consultar
      </Button>
    </Box>
  );
}

export default PredictionForm;

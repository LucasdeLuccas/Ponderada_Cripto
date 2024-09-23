import React from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
} from '@mui/material';
import { Line } from 'react-chartjs-2';

function GraphDialog({ open, onClose, data }) {
  if (!data) return null;

  const chartData = {
    labels: data.dates,
    datasets: [
      {
        label: 'Preço de Fechamento',
        data: data.prices,
        borderColor: 'blue',
        fill: false,
      },
    ],
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>Gráfico de Preços para {data.asset}</DialogTitle>
      <DialogContent>
        <Line data={chartData} />
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose} color="primary">
          Fechar
        </Button>
      </DialogActions>
    </Dialog>
  );
}

export default GraphDialog;

import React, { useState } from 'react';
import {
  Container,
  Typography,
  Box,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Paper,
  TextField,
} from '@mui/material';
import axios from 'axios';
import GraphDialog from '../components/GraphDialog';
import { LocalizationProvider, DatePicker } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';

const assets = ['Bitcoin', 'Ethereum', 'BNB', 'Solana', 'Dogecoin'];

function HomePage() {
  const [asset, setAsset] = useState('Bitcoin');
  const [date, setDate] = useState(null); // Inicializado como null
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showGraph, setShowGraph] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async () => {
    if (!asset) {
      setError('Por favor, selecione um criptoativo.');
      return;
    }

    if (!date) {
      setError('Por favor, selecione uma data.');
      return;
    }

    setLoading(true);
    setError('');
    try {
      // Formatar a data para 'YYYY-MM-DD'
      const formattedDate = date.toISOString().split('T')[0];
      const response = await axios.get('http://backend:5000/predict', {
        params: { asset, date: formattedDate },
      });
      setResult(response.data);
    } catch (error) {
      console.error(error);
      if (error.response && error.response.data && error.response.data.error) {
        setError(`Erro: ${error.response.data.error}`);
      } else {
        setError('Erro ao obter os dados. Por favor, tente novamente mais tarde.');
      }
    }
    setLoading(false);
  };

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      {/* Seção de Informação */}
      <Box textAlign="center" mb={4}>
        <Typography variant="h3" gutterBottom>
          Bem-vindo ao DeLuccas Crypto
        </Typography>
        <Typography variant="h6" color="textSecondary">
          Seu sistema de previsão para investimentos em criptoativos.
          Selecione uma data e aguarde...
        </Typography>
      </Box>

      {/* Animação ou Vídeo */}
      <Box display="flex" justifyContent="center" mb={4}>
        <video
          src="./assets/images/crypto_animation.mov"
          controls
          style={{ maxWidth: '100%', height: 'auto' }} // Corrigido 'tyle' para 'style' e ajustado para 100%
        >
          Seu navegador não suporta a tag de vídeo.
        </video>
      </Box>

      {/* Formulário de Consulta */}
      <Paper elevation={3} sx={{ p: 4 }}>
        {/* Container para os Inputs com largura fixa */}
        <Box
          display="flex"
          flexDirection="column"
          alignItems="center"
          sx={{
            width: '100%',
            maxWidth: '400px', // Definindo a largura máxima do container
            margin: '0 auto', // Centralizando o container
          }}
        >
          {/* Seleção de Criptoativo */}
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

          {/* Seleção de Data com DatePicker */}
          <LocalizationProvider dateAdapter={AdapterDateFns}>
            <DatePicker
              label="Data"
              value={date}
              onChange={(newValue) => {
                setDate(newValue);
              }}
              renderInput={(params) => <TextField {...params} fullWidth margin="normal" />}
              maxDate={new Date()} // Data máxima até hoje
            />
          </LocalizationProvider>

          {/* Botão Consultar */}
          <Button
            variant="contained"
            color="primary"
            fullWidth
            sx={{ mt: 2 }}
            onClick={handleSubmit}
            disabled={loading}
          >
            {loading ? 'Consultando...' : 'Consultar'}
          </Button>

          {/* Exibir Mensagem de Erro */}
          {error && (
            <Typography variant="body1" color="error" mt={2}>
              {error}
            </Typography>
          )}
        </Box>
      </Paper>

      {/* Resultado */}
      {result && (
        <Box mt={4}>
          <Paper elevation={3} sx={{ p: 4 }}>
            <Typography variant="h5" gutterBottom>
              Resultado para {result.asset} em {result.date}
            </Typography>
            <Typography
              variant="h6"
              color={result.signal === 'Buy' ? 'green' : 'red'}
              gutterBottom
            >
              Sinal: {result.signal}
            </Typography>
            <Typography variant="body1" gutterBottom>
              <strong>Preço Atual:</strong> ${result.current_price.toFixed(2)}
            </Typography>
            <Typography variant="body1" gutterBottom>
              <strong>Preço Previsto:</strong> ${result.prediction.toFixed(2)}
            </Typography>
            {/* Botão para ver o gráfico */}
            <Button
              variant="outlined"
              color="primary"
              onClick={() => setShowGraph(true)}
              sx={{ mt: 2 }}
            >
              Ver Gráfico
            </Button>
          </Paper>

          {/* Modal para o Gráfico */}
          <GraphDialog
            open={showGraph}
            onClose={() => setShowGraph(false)}
            data={result.graphData}
          />
        </Box>
      )}
    </Container>
  );
}

export default HomePage;
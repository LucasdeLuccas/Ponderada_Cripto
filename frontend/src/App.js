import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import HomePage from './pages/HomePage';
import LogsPage from './pages/LogsPage'; // Importação da nova página
import { AppBar, Toolbar, Typography, Button } from '@mui/material';

function App() {
  return (
    <Router>
      {/* Barra de Navegação */}
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            DeLuccasCrypto!
          </Typography>
          <Button color="inherit" component={Link} to="/">
            Home
          </Button>
          <Button color="inherit" component={Link} to="/logs">
            Logs
          </Button>
        </Toolbar>
      </AppBar>

      {/* Rotas */}
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/logs" element={<LogsPage />} />
      </Routes>
    </Router>
  );
}

export default App;

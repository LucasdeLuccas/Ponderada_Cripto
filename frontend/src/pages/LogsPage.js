import React, { useEffect, useState } from 'react';
import { Table, Container, Alert, Button } from 'react-bootstrap';

/**

 * @returns {Array}
 */
const getLogs = () => {
  return JSON.parse(localStorage.getItem('solana_logs')) || [];
};


const clearLogs = () => {
  localStorage.removeItem('solana_logs');
};

function LogsPage() {

  const [logs, setLogs] = useState([]);

  useEffect(() => {
 
    setLogs(getLogs());
  }, []);


  const handleClearLogs = () => {
    if (window.confirm('Tem certeza que deseja limpar todos os logs?')) {
      clearLogs();
      setLogs([]);
    }
  };

  return (
    <Container className="mt-5">
      <h2>Logs de Previsões</h2>
      <Button variant="danger" className="mb-3" onClick={handleClearLogs}>Limpar Logs</Button>
      {logs.length === 0 ? (
        <Alert variant="info">Nenhum log disponível.</Alert>
      ) : (
        <Table striped bordered hover>
          <thead>
            <tr>
              <th>#</th>
              <th>Data Selecionada</th>
              <th>Ação</th>
              <th>Mensagem</th>
              <th>Timestamp</th>
            </tr>
          </thead>
          <tbody>
            {logs.map((log, index) => (
              <tr key={index}>
                <td>{index + 1}</td>
                <td>{log.date}</td>
                <td>{log.action}</td>
                <td>{log.message}</td>
                <td>{new Date(log.timestamp).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </Table>
      )}
    </Container>
  );
}

export default LogsPage;

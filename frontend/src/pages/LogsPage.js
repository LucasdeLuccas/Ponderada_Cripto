import React, { useEffect, useState, useRef } from 'react';
import { Container, Typography, Box, Paper } from '@mui/material';

function LogsPage() {
  const [logs, setLogs] = useState([]);
  const logEndRef = useRef(null);

  useEffect(() => {
    const eventSource = new EventSource('http://localhost:5001/logs');

    eventSource.onmessage = function(event) {
      setLogs(prevLogs => [...prevLogs, event.data]);
      scrollToBottom();
    };

    eventSource.onerror = function(err) {
      console.error("EventSource failed:", err);
      eventSource.close();
    };

    return () => {
      eventSource.close();
    };
  }, []);

  const scrollToBottom = () => {
    if (logEndRef.current) {
      logEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  };

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom>
        Logs em Tempo Real
      </Typography>
      <Paper elevation={3} sx={{ p: 2, maxHeight: '70vh', overflow: 'auto', backgroundColor: '#1e1e1e', color: '#d4d4d4' }}>
        <Box component="pre" sx={{ whiteSpace: 'pre-wrap', fontFamily: 'monospace' }}>
          {logs.map((log, index) => (
            <div key={index}>{log}</div>
          ))}
          <div ref={logEndRef} />
        </Box>
      </Paper>
    </Container>
  );
}

export default LogsPage;
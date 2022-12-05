import * as React from 'react';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import Box from '@mui/material/Box';
import MuiAppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { BrowserRouter, Routes, Route} from "react-router-dom";
import Copyright from '../tool/Copyright';
import ProjectList from '../project/ProjectList';
import ProjectPage from '../project/ProjectPage';


const mdTheme = createTheme();

function Main() {

  return (
    <ThemeProvider theme={mdTheme}>
      <Box sx={{ display: 'flex' }}>
        <MuiAppBar position="absolute">
          <Toolbar>
            <Typography component="h1" variant="h6">
              Machine Learning Toolkit
            </Typography>
            
          </Toolbar>
        </MuiAppBar>
        <Box
          component="main"
          sx={{
            backgroundColor: (theme) =>
              theme.palette.mode === 'light'
                ? theme.palette.grey[100]
                : theme.palette.grey[900],
            flexGrow: 1,
            height: '100vh',
            overflow: 'auto',
          }}
        >
          <Toolbar />
          
          <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
            

          <BrowserRouter>
            <Routes>
                <Route path="/" element={<ProjectList />}/>
                <Route path="/project/:projectId" element={<ProjectPage />}/>
            </Routes>
          </BrowserRouter>
          
            <Copyright sx={{ pt: 4 }} />
          </Container>
        </Box>
      </Box>
    </ThemeProvider>
  );
}

export default Main;
